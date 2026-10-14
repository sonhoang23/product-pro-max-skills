#!/usr/bin/env python3
"""Opt-in, single-file project-state contract migration (Spec 004 US3).

Default: dry-run, no source/target/receipt mutation. Explicit apply never
bulk-rewrites user directories. Source is authoritative; this only adds
contract_version to legacy source while preserving all existing fields.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any

from compatibility_common import CompatibilityValidationError, parse_semver

CURRENT_VERSION = "1.0.0"
MIGRATION_ID = "project-state-legacy-to-1.0.0"
COMPONENT_ID = "project-data:project-state"
HISTORY_FIELDS = ("critical_assumptions", "evidence", "provenance",
                  "decisions", "decision_history", "gate", "decision")
PROTECTED_KEYS = ("project", "cycle", "phase", "status", "updated_at")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_path(raw: str, *, must_exist: bool = False) -> Path:
    """Reject symlinks in the path chain to avoid backup/output redirection."""
    path = Path(raw).absolute()
    for part in (path, *path.parents):
        if part.is_symlink():
            raise CompatibilityValidationError(f"{path}: symlink path not permitted ({part})")
    if must_exist:
        try:
            info = path.stat()
        except OSError as exc:
            raise CompatibilityValidationError(f"{path}: missing migration input: {exc}") from exc
        if not stat.S_ISREG(info.st_mode):
            raise CompatibilityValidationError(f"{path}: expected regular input file")
    elif not path.parent.is_dir():
        raise CompatibilityValidationError(f"{path}: destination parent directory missing")
    return path


def _load_source(path: Path) -> tuple[dict[str, Any], bytes, str]:
    try:
        payload = path.read_bytes()
        if path.suffix.lower() == ".json":
            from compatibility_common import _no_duplicate_keys
            document = json.loads(payload.decode("utf-8"), object_pairs_hook=_no_duplicate_keys)
        elif path.suffix.lower() in {".yaml", ".yml"}:
            from skill_registry_common import parse_yaml
            document = parse_yaml(path)
        else:
            raise CompatibilityValidationError(f"{path}: expected .json, .yaml or .yml")
    except (OSError, UnicodeError, ValueError) as exc:
        raise CompatibilityValidationError(f"{path}: invalid project-state source: {exc}") from exc
    if not isinstance(document, dict):
        raise CompatibilityValidationError(f"{path}: project-state must be a mapping")
    for key in PROTECTED_KEYS:
        if key not in document or not isinstance(document[key], str) or not document[key]:
            raise CompatibilityValidationError(f"{path}: missing/invalid {key}")
    model = json.loads((Path(__file__).resolve().parents[1] / "model/product-model.json").read_text(encoding="utf-8"))
    owners = {cycle["id"]: {phase["id"] for phase in cycle["phases"]}
              for cycle in model["lifecycle"]["cycles"]}
    if document["cycle"] not in owners or document["phase"] not in owners[document["cycle"]]:
        raise CompatibilityValidationError(f"{path}: noncanonical cycle/phase pair")
    if document["status"] not in {status["id"] for status in model["project_statuses"]}:
        raise CompatibilityValidationError(f"{path}: noncanonical status")
    if "stage" in document:
        raise CompatibilityValidationError(f"{path}: legacy stage is not canonical; requires reviewed migration")
    if "contract_version" not in document:
        return document, payload, "legacy-unversioned"
    version = document["contract_version"]
    if not isinstance(version, str):
        raise CompatibilityValidationError(f"{path}: invalid contract_version (must be SemVer string)")
    parse_semver(version)
    if version != CURRENT_VERSION:
        raise CompatibilityValidationError(
            f"{path}: unsupported source contract_version {version}; "
            "no verified migration path to 1.0.0")
    return document, payload, CURRENT_VERSION


def _serialize(document: dict[str, Any], path: Path) -> bytes:
    """Encode exactly one new key; preserve original fields and collection order."""
    if path.suffix.lower() == ".json":
        return (json.dumps(document, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    import yaml
    return yaml.safe_dump(document, allow_unicode=True, sort_keys=False).encode("utf-8")


def _transform(document: dict[str, Any], original: str) -> dict[str, Any]:
    if original != "legacy-unversioned":
        raise CompatibilityValidationError("source already versioned; migration not needed")
    result = copy.deepcopy(document)
    result["contract_version"] = CURRENT_VERSION
    for key in document:
        if key == "contract_version" or result.get(key) != document[key]:
            raise CompatibilityValidationError(f"history/field preservation failure: {key}")
    for field in HISTORY_FIELDS:
        if field in document and result[field] != document[field]:
            raise CompatibilityValidationError(f"history invariant violation: {field}")
    if set(result) - set(document) != {"contract_version"}:
        raise CompatibilityValidationError("migration adds unexpected fields")
    return result


def _atomic_new(path: Path, payload: bytes, *, replace: bool = False) -> None:
    """Stage + fsync + same-directory replace; never follow destination symlinks."""
    _safe_path(str(path))
    if path.exists() and not replace:
        raise CompatibilityValidationError(f"{path}: output already exists; refusing overwrite")
    staged: Path | None = None
    try:
        fd, name = tempfile.mkstemp(prefix=".compat-", dir=path.parent)
        staged = Path(name)
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        _safe_path(str(path))
        if path.exists() and not replace:
            raise CompatibilityValidationError(f"{path}: destination appeared during write")
        os.replace(staged, path)
        staged = None
    finally:
        if staged is not None:
            staged.unlink(missing_ok=True)


def _receipt_bytes(receipt: dict[str, Any]) -> bytes:
    return (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _load_receipt(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CompatibilityValidationError(f"{path}: invalid existing receipt: {exc}") from exc
    if not isinstance(value, dict) or value.get("migration_id") != MIGRATION_ID:
        raise CompatibilityValidationError(f"{path}: unrelated/invalid migration receipt")
    return value


def preflight(input_path: Path, output_path: Path, *,
              action: str, backup_path: Path | None, receipt_path: Path | None,
              accept_legacy: bool, in_place: bool) -> dict[str, Any]:
    src = _safe_path(str(input_path), must_exist=True)
    dst = _safe_path(str(output_path))
    same = src == dst
    if same and action == "apply" and not in_place:
        raise CompatibilityValidationError(f"{src}: in-place apply requires --in-place")
    if action == "apply" and (backup_path is None or receipt_path is None):
        raise CompatibilityValidationError("apply requires explicit --backup and --receipt")
    paths = [src, dst]
    for p in (backup_path, receipt_path):
        if p is not None:
            paths.append(_safe_path(str(p)))
    if len(set(paths)) != len(paths) - (1 if same else 0):
        raise CompatibilityValidationError("input/output/backup/receipt paths collide")
    document, raw, status = _load_source(src)
    output = _serialize(_transform(document, status), dst) if status == "legacy-unversioned" else raw
    sha = digest(raw)
    key = digest(f"{MIGRATION_ID}\0{sha}\0{CURRENT_VERSION}".encode("utf-8"))
    return {
        "source": src, "target": dst, "raw": raw, "output": output, "document": document,
        "source_version": None if status == "legacy-unversioned" else status,
        "classification": status, "input_digest": sha,
        "output_digest": digest(output), "idempotency_key": key,
        "receipt": receipt_path, "backup": backup_path,
        "accept_legacy": accept_legacy,
    }


def _new_receipt(details: dict[str, Any], status: str, checkpoint: str,
                 errors: list[str] | None = None) -> dict[str, Any]:
    return {
        "migration_id": MIGRATION_ID, "component_id": COMPONENT_ID,
        "source_version": details["source_version"], "target_version": CURRENT_VERSION,
        "input_path": str(details["source"]), "output_path": str(details["target"]),
        "input_digest": details["input_digest"],
        "output_digest": details["output_digest"] if checkpoint in
                         {"output_replaced", "receipt_saved"} else None,
        "idempotency_key": details["idempotency_key"],
        "status": status, "backup_path": str(details["backup"]) if details["backup"] else None,
        "checkpoint": checkpoint, "errors": errors or [],
        "recovery_action": None if status in {"applied", "already_applied"}
                           else "Inspect backup and output; use explicit restore with expected output digest",
        "exception": None, "history_invariants": list(HISTORY_FIELDS),
    }


def _retry_existing(details: dict[str, Any]) -> dict[str, Any] | None:
    receipt_path = details["receipt"]
    if receipt_path is None or not receipt_path.exists():
        return None
    saved = _load_receipt(receipt_path)
    recorded_key = digest(f"{MIGRATION_ID}\0{saved.get('input_digest')}\0{CURRENT_VERSION}".encode("utf-8"))
    if (saved.get("component_id") != COMPONENT_ID or
            saved.get("target_version") != CURRENT_VERSION or
            saved.get("idempotency_key") != recorded_key):
        raise CompatibilityValidationError(f"{receipt_path}: invalid migration provenance/idempotency key")
    same_paths = (saved.get("input_path") == str(details["source"]) and
                  saved.get("output_path") == str(details["target"]) and
                  saved.get("backup_path") == str(details["backup"]))
    if not same_paths or saved.get("status") not in {"applied", "already_applied"}:
        raise CompatibilityValidationError(
            f"{receipt_path}: existing non-success/unrelated receipt; recover manually before retry")
    try:
        actual = digest(details["target"].read_bytes())
        backup = digest(details["backup"].read_bytes())
    except OSError as exc:
        raise CompatibilityValidationError(f"{receipt_path}: missing output/backup: {exc}") from exc
    if actual != saved.get("output_digest") or backup != saved.get("input_digest"):
        raise CompatibilityValidationError(f"{receipt_path}: output/backup changed since apply")
    if details["source"] == details["target"]:
        if details["input_digest"] != saved.get("output_digest"):
            raise CompatibilityValidationError(f"{receipt_path}: in-place source changed")
    elif details["input_digest"] != saved.get("input_digest"):
        raise CompatibilityValidationError(f"{receipt_path}: source digest changed since apply")
    report = dict(saved)
    report["status"] = "already_applied"
    return report  # read only: don't rewrite success receipt


def apply(details: dict[str, Any]) -> dict[str, Any]:
    prior = _retry_existing(details)
    if prior is not None:
        return prior
    if details["classification"] != "legacy-unversioned":
        raise CompatibilityValidationError(
            "already-versioned source without matching receipt: no verified migration needed")
    if not details["accept_legacy"]:
        raise CompatibilityValidationError(
            "legacy-unversioned source requires explicit --accept-legacy; never infer support")
    src, dst = details["source"], details["target"]
    backup, receipt_path = details["backup"], details["receipt"]
    assert backup is not None and receipt_path is not None
    if backup.exists() or receipt_path.exists():
        raise CompatibilityValidationError("backup/receipt already exists; refusing collision")
    if dst != src and dst.exists():
        raise CompatibilityValidationError(f"{dst}: target already exists; refusing overwrite")
    # Recheck source after parsing; prevents preflight evidence drift.
    if digest(src.read_bytes()) != details["input_digest"]:
        raise CompatibilityValidationError(f"{src}: input changed after preflight")
    checkpoint = "preflight"
    try:
        _atomic_new(backup, details["raw"])
        checkpoint = "backup_saved"
        if digest(backup.read_bytes()) != details["input_digest"]:
            raise CompatibilityValidationError(f"{backup}: backup integrity failure")
        if digest(src.read_bytes()) != details["input_digest"]:
            raise CompatibilityValidationError(f"{src}: source changed before commit")
        _atomic_new(dst, details["output"], replace=(src == dst))
        checkpoint = "output_replaced"
        if digest(dst.read_bytes()) != details["output_digest"]:
            raise CompatibilityValidationError(f"{dst}: migrated output mismatch")
        checked, _, version = _load_source(dst)
        if version != CURRENT_VERSION:
            raise CompatibilityValidationError(f"{dst}: invalid migrated contract")
        orig = details["document"]
        for key, value in orig.items():
            if checked.get(key) != value:
                raise CompatibilityValidationError(f"{dst}: original field changed: {key}")
        receipt = _new_receipt(details, "applied", "receipt_saved")
        _atomic_new(receipt_path, _receipt_bytes(receipt))
        return receipt
    except Exception as exc:
        if checkpoint != "preflight":
            state = "partially_applied" if checkpoint == "output_replaced" else "failed"
            failure = _new_receipt(details, state, checkpoint, [str(exc)])
            try:
                if not receipt_path.exists():
                    _atomic_new(receipt_path, _receipt_bytes(failure))
            except Exception as report_error:
                raise CompatibilityValidationError(
                    f"migration {state}, receipt write failed: {report_error}; "
                    f"backup at {backup}") from exc
        raise CompatibilityValidationError(
            f"migration {checkpoint} failed: {exc}; backup={backup}") from exc


def restore(input_path: Path, receipt_path: Path, backup_path: Path,
            expected_current_sha256: str) -> dict[str, Any]:
    dst = _safe_path(str(input_path), must_exist=True)
    receipt = _safe_path(str(receipt_path), must_exist=True)
    backup = _safe_path(str(backup_path), must_exist=True)
    saved = _load_receipt(receipt)
    if saved.get("status") not in {"partially_applied", "failed"}:
        raise CompatibilityValidationError("restore requires failed/partially_applied receipt")
    if saved.get("output_path") != str(dst) or saved.get("backup_path") != str(backup):
        raise CompatibilityValidationError("restore input and backup must match receipt")
    original = backup.read_bytes()
    if digest(original) != saved.get("input_digest"):
        raise CompatibilityValidationError("restore backup digest mismatch")
    if digest(dst.read_bytes()) != expected_current_sha256:
        raise CompatibilityValidationError("restore target changed; refuse destructive replacement")
    _atomic_new(dst, original, replace=True)
    if digest(dst.read_bytes()) != saved["input_digest"]:
        raise CompatibilityValidationError("restored bytes mismatch backup")
    saved["status"], saved["checkpoint"] = "recovered", "recovered"
    saved["recovery_action"] = "Restored original bytes; start new reviewed migration with new receipt"
    _atomic_new(receipt, _receipt_bytes(saved), replace=True)
    return saved


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", nargs="?", choices=("dry-run", "assess", "apply", "restore"),
                        default="dry-run")
    parser.add_argument("--input", required=True, help="Single project YAML/JSON file; no directory recursion")
    parser.add_argument("--output", help="Explicit target for dry-run/apply (default input for preview)")
    parser.add_argument("--receipt", help="Explicit receipt JSON path")
    parser.add_argument("--backup", help="Explicit backup file path")
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--accept-legacy", action="store_true",
                        help="Acknowledge legacy-unversioned is not a published compatibility promise")
    parser.add_argument("--expected-current-sha256", help="Required for explicit restore")
    args = parser.parse_args(argv)
    try:
        src = _safe_path(args.input, must_exist=True)
        if args.action == "restore":
            if not args.backup or not args.receipt or not args.expected_current_sha256:
                raise CompatibilityValidationError(
                    "restore requires --backup, --receipt and --expected-current-sha256")
            if not args.output or _safe_path(args.output) != src:
                raise CompatibilityValidationError("restore requires --output equal --input")
            result = restore(src, Path(args.receipt), Path(args.backup),
                             args.expected_current_sha256)
        else:
            if args.action == "apply" and not args.output:
                raise CompatibilityValidationError("apply requires explicit --output")
            details = preflight(src, Path(args.output or args.input),
                                action=args.action,
                                backup_path=Path(args.backup) if args.backup else None,
                                receipt_path=Path(args.receipt) if args.receipt else None,
                                accept_legacy=args.accept_legacy, in_place=args.in_place)
            if args.action == "apply":
                result = apply(details)
            else:
                result = {
                    "action": args.action, "classification": details["classification"],
                    "source_version": details["source_version"],
                    "target_version": CURRENT_VERSION, "input_digest": details["input_digest"],
                    "proposed_digest": details["output_digest"], "write_performed": False,
                    "status": "review_required" if details["classification"] ==
                              "legacy-unversioned" else "no_change",
                    "reason": "Unversioned legacy support is not inferred; apply requires explicit opt-in"
                              if details["classification"] == "legacy-unversioned"
                              else "Source already versioned at target contract",
                }
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (CompatibilityValidationError, OSError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
