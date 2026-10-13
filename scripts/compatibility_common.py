#!/usr/bin/env python3
"""Spec 004 offline foundation: typed support-ledger parsing and immutable source proof.

This module never writes source files, contacts a remote, invents support baselines
or grants behavioral/runtime compatibility. User-facing assessment is a later phase.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$", re.ASCII
)
COMPONENT_ID_RE = re.compile(r"^[a-z][a-z0-9-]*(?::[a-z0-9-]+)*$")
BASELINE_ID_RE = re.compile(r"^[a-z0-9]+(?:[-.][a-z0-9]+)*$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REF_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_./-]*$")


class CompatibilityValidationError(ValueError):
    """Invalid source, unsupported format or unverified baseline."""


@dataclass(frozen=True)
class VersionedComponent:
    component_id: str
    component_type: str
    authority_path: str
    version_owner: str
    version: str | None
    digest: str
    publication_status: str = "unknown"
    format_version: str | int | None = None


@dataclass(frozen=True)
class ImmutableSource:
    ref: str
    commit_sha: str
    authority_path: str
    sha256: str


@dataclass(frozen=True)
class SupportedBaseline:
    baseline_id: str
    component_id: str
    version: str
    source: ImmutableSource
    support_status: str
    support_scope: tuple[str, ...]
    support_policy_ref: str
    effective_from: str | None = None
    effective_until: str | None = None
    release_evidence: dict[str, Any] | None = None
    record_revision: str | None = None


@dataclass(frozen=True)
class ConsumerDependency:
    consumer_id: str
    provider_component_id: str
    version_range: str | None
    required_outputs: tuple[str, ...]
    required_features: tuple[str, ...]
    strict_reader: bool | None
    declared_by: str
    scope: str


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: str
    component_id: str
    authority_path: str
    classification: str
    message: str
    required_action: str
    baseline_version: str | None = None
    candidate_version: str | None = None
    affected_consumer_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class SupportLedger:
    ledger_version: int
    policy_ref: str
    baselines: tuple[SupportedBaseline, ...]


def _fail(path: str, message: str) -> None:
    raise CompatibilityValidationError(f"{path}: {message}")


def normalized_relative_path(value: str, *, source: str = "path") -> str:
    """Normalize paths for reports; never allow absolute or parent traversal."""
    if not isinstance(value, str) or not value or "\x00" in value:
        _fail(source, "expected nonempty relative path")
    if any(ord(ch) > 127 for ch in value):
        _fail(source, "machine path must use ASCII")
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        _fail(source, "absolute/drive path forbidden")
    parts = normalized.split("/")
    if any(x in ("", ".", "..") for x in parts):
        _fail(source, "empty/current/parent path segment forbidden")
    if any(":" in x for x in parts):
        _fail(source, "colon in path forbidden")
    return str(PurePosixPath(*parts))


def _expect_mapping(value: Any, place: str, required: set[str], allowed: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(place, "must be a JSON object")
    missing = required - value.keys()
    extra = value.keys() - allowed
    if missing or extra:
        _fail(place, f"missing keys {sorted(missing)}; unknown keys {sorted(extra)}")
    return value


def _string(value: Any, place: str) -> str:
    if not isinstance(value, str) or not value:
        _fail(place, "must be a nonempty string")
    return value


def _parse_source(value: Any, place: str) -> ImmutableSource:
    data = _expect_mapping(
        value, place, {"ref", "commit_sha", "authority_path", "sha256"},
        {"ref", "commit_sha", "authority_path", "sha256"}
    )
    ref = _string(data["ref"], place + ".ref")
    if not REF_RE.fullmatch(ref) or ".." in ref or ref.endswith(".lock"):
        _fail(place + ".ref", "invalid local git ref")
    commit = _string(data["commit_sha"], place + ".commit_sha")
    sha = _string(data["sha256"], place + ".sha256")
    if not COMMIT_RE.fullmatch(commit):
        _fail(place + ".commit_sha", "expected full lowercase 40-hex Git commit")
    if not SHA256_RE.fullmatch(sha):
        _fail(place + ".sha256", "expected lowercase 64-hex SHA-256 digest")
    path = normalized_relative_path(data["authority_path"], source=place + ".authority_path")
    return ImmutableSource(ref=ref, commit_sha=commit, authority_path=path, sha256=sha)


def _parse_baseline(value: Any, index: int) -> SupportedBaseline:
    place = f"baselines[{index}]"
    required = {"baseline_id", "component_id", "version", "source",
                "support_status", "support_scope", "support_policy_ref"}
    allowed = required | {"effective_from", "effective_until", "release_evidence", "record_revision"}
    data = _expect_mapping(value, place, required, allowed)
    baseline_id = _string(data["baseline_id"], place + ".baseline_id")
    component_id = _string(data["component_id"], place + ".component_id")
    version = _string(data["version"], place + ".version")
    if not BASELINE_ID_RE.fullmatch(baseline_id):
        _fail(place + ".baseline_id", "invalid stable ID")
    if not COMPONENT_ID_RE.fullmatch(component_id):
        _fail(place + ".component_id", "invalid component ID")
    if not SEMVER_RE.fullmatch(version):
        _fail(place + ".version", "invalid SemVer")
    status = _string(data["support_status"], place + ".support_status")
    if status not in {"active", "deprecated", "unsupported", "removed"}:
        _fail(place + ".support_status", "invalid support state")
    scope = data["support_scope"]
    if (not isinstance(scope, list) or
            any(not isinstance(x, str) or not x for x in scope) or
            len(scope) != len(set(scope))):
        _fail(place + ".support_scope", "must be unique nonempty consumer identities")
    policy = normalized_relative_path(
        _string(data["support_policy_ref"], place + ".support_policy_ref"),
        source=place + ".support_policy_ref")
    for optional in ("effective_from", "effective_until"):
        if data.get(optional) is not None and not isinstance(data[optional], str):
            _fail(place + "." + optional, "must be string or null")
    release = data.get("release_evidence")
    if release is not None and not isinstance(release, dict):
        _fail(place + ".release_evidence", "must be object or null")
    rev = data.get("record_revision")
    if rev is not None:
        _string(rev, place + ".record_revision")
    return SupportedBaseline(
        baseline_id=baseline_id, component_id=component_id, version=version,
        source=_parse_source(data["source"], place + ".source"),
        support_status=status, support_scope=tuple(scope),
        support_policy_ref=policy, effective_from=data.get("effective_from"),
        effective_until=data.get("effective_until"), release_evidence=release,
        record_revision=rev)


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CompatibilityValidationError(f"JSON duplicate key {key!r}")
        result[key] = value
    return result


def load_supported_baselines(path: Path) -> SupportLedger:
    """Fail closed on malformed ledger. Empty list is honest, never 'supported'."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"),
                             object_pairs_hook=_no_duplicate_keys)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CompatibilityValidationError(f"{path}: cannot read ledger: {exc}") from exc
    obj = _expect_mapping(payload, str(path),
                          {"ledger_version", "policy_ref", "baselines"},
                          {"ledger_version", "policy_ref", "baselines"})
    if type(obj["ledger_version"]) is not int or obj["ledger_version"] != 1:
        _fail(str(path) + ".ledger_version", "unsupported ledger version (expected 1)")
    policy_ref = normalized_relative_path(
        _string(obj["policy_ref"], str(path) + ".policy_ref"),
        source=str(path) + ".policy_ref")
    entries = obj["baselines"]
    if not isinstance(entries, list):
        _fail(str(path) + ".baselines", "must be an array")
    baselines = tuple(_parse_baseline(value, i) for i, value in enumerate(entries))
    seen: set[str] = set()
    for baseline in baselines:
        if baseline.baseline_id in seen:
            _fail(str(path) + ".baselines", f"duplicate baseline_id {baseline.baseline_id}")
        seen.add(baseline.baseline_id)
    return SupportLedger(ledger_version=1, policy_ref=policy_ref, baselines=baselines)


def _git(root: Path, *args: str) -> bytes:
    """Local git only; no shell, no remote fetch."""
    command = ["git", "-C", str(root), *args]
    try:
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              check=False)
    except OSError as exc:
        raise CompatibilityValidationError(f"git unavailable: {exc}") from exc
    if proc.returncode != 0:
        details = proc.stderr.decode("utf-8", errors="replace").strip()
        raise CompatibilityValidationError(
            f"git local source lookup failed (exit {proc.returncode}): {details}")
    return proc.stdout


def verify_local_baseline_source(baseline: SupportedBaseline, checkout: Path) -> str:
    """Check ref→commit, git tracked regular blob and declared SHA256 without mutation.

    Returns the validated source SHA256. Does not prove release, reader behavior or
    support status; those require independent scope/review evidence.
    """
    root = Path(checkout)
    source = baseline.source
    ref = source.ref
    commit = _git(root, "rev-parse", "--verify", "--end-of-options",
                  ref + "^{commit}").decode("ascii").strip()
    if commit != source.commit_sha:
        _fail(source.authority_path,
              f"ref {ref!r} resolves to {commit}, expected {source.commit_sha} (stale ref)")
    info = _git(root, "ls-tree", commit, "--", source.authority_path)
    lines = info.decode("utf-8", errors="replace").splitlines()
    if len(lines) != 1 or "\t" not in lines[0]:
        _fail(source.authority_path, "historical blob missing")
    meta, path = lines[0].split("\t", 1)
    mode, typ, _ = meta.split()
    if path != source.authority_path or typ != "blob" or mode not in {"100644", "100755"}:
        _fail(source.authority_path, "not a regular tracked file (symlink or tree denied)")
    data = _git(root, "show", commit + ":" + source.authority_path)
    digest = hashlib.sha256(data).hexdigest()
    if digest != source.sha256:
        _fail(source.authority_path,
              f"SHA-256 mismatch: expected {source.sha256}, actual {digest}")
    return digest


@dataclass(frozen=True)
class ParsedVersion:
    """SemVer 2.0.0 identity; build metadata does not change precedence."""
    major: int
    minor: int
    patch: int
    prerelease: tuple[str, ...] = ()
    build: tuple[str, ...] = ()


def parse_semver(value: str) -> ParsedVersion:
    """Strict ASCII SemVer; reject leading zero in numeric prerelease fields."""
    if not isinstance(value, str) or not SEMVER_RE.fullmatch(value):
        raise CompatibilityValidationError(f"invalid SemVer: {value!r}")
    core_and_pre, _, build = value.partition("+")
    core, sep, pre = core_and_pre.partition("-")
    major, minor, patch = (int(part) for part in core.split("."))
    return ParsedVersion(
        major, minor, patch,
        tuple(pre.split(".")) if sep else (),
        tuple(build.split(".")) if build else ()
    )


def compare_semver(left: str, right: str) -> int:
    """Compare precedence without treating build metadata as a release bump."""
    a, b = parse_semver(left), parse_semver(right)
    for av, bv in zip((a.major, a.minor, a.patch), (b.major, b.minor, b.patch)):
        if av != bv:
            return (av > bv) - (av < bv)
    if not a.prerelease or not b.prerelease:
        return (bool(b.prerelease) > bool(a.prerelease)) - (
            bool(b.prerelease) < bool(a.prerelease))
    for av, bv in zip(a.prerelease, b.prerelease):
        if av == bv:
            continue
        anum, bnum = av.isascii() and av.isdecimal(), bv.isascii() and bv.isdecimal()
        if anum and bnum:
            return (int(av) > int(bv)) - (int(av) < int(bv))
        if anum != bnum:
            return -1 if anum else 1
        return (av > bv) - (av < bv)
    return (len(a.prerelease) > len(b.prerelease)) - (
        len(a.prerelease) < len(b.prerelease))


def minimum_version_increment(change: str, baseline: str | None) -> str | None:
    """Recommend a floor for an independently reviewed change.

    Input is a declared/reviewed impact, never inferred from a source diff.
    No historical supported baseline => no compatibility/bump conclusion.
    """
    if baseline is None:
        return None
    v = parse_semver(baseline)
    if change == "breaking":
        return "minor" if v.major == 0 else "major"
    if change == "feature":
        return "minor"
    if change == "fix":
        return "patch"
    if change == "none":
        return "none"
    raise CompatibilityValidationError(f"unsupported change impact: {change!r}")


def sufficient_version_increment(
    baseline: str | None, candidate: str, change: str
) -> bool | None:
    """Only checks a declared bump against a reviewed impact.

    None means unassessed (no supported baseline), not PASS. An unchanged
    major/minor/patch with only a new build/prerelease cannot satisfy a stable
    public change. This function does not prove semantic compatibility.
    """
    proposed = parse_semver(candidate)
    floor = minimum_version_increment(change, baseline)
    if floor is None:
        return None
    prior = parse_semver(baseline)
    if floor == "none":
        return compare_semver(candidate, baseline) >= 0
    if compare_semver(candidate, baseline) <= 0:
        return False
    if proposed.major > prior.major:
        return True
    if proposed.major < prior.major:
        return False
    if floor == "major":
        return False
    if proposed.minor > prior.minor:
        return True
    if proposed.minor < prior.minor:
        return False
    if floor == "minor":
        return False
    return proposed.patch > prior.patch


def inspect_version_owner(
    root: Path, component_type: str, relative_path: str,
    *, declared_schema_version: str | None = None
) -> VersionedComponent:
    """Read the owning source, not its registry/lock projection.

    No source version is invented for legacy manifests/project state or schemas.
    Machine schema versions exist only when independently declared by policy
    against the source $id/digest; the declaration is not publication evidence.
    """
    root = Path(root).resolve()
    relative = normalized_relative_path(relative_path)
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise CompatibilityValidationError(f"{relative}: source path escapes root") from exc
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise CompatibilityValidationError(f"{relative}: source missing or unreadable: {exc}") from exc
    digest = hashlib.sha256(raw).hexdigest()
    from_json = component_type in {"product_model", "machine_schema"}
    if from_json:
        try:
            data = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicate_keys)
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise CompatibilityValidationError(f"{relative}: invalid source JSON: {exc}") from exc
        if not isinstance(data, dict):
            raise CompatibilityValidationError(f"{relative}: source must be object")
    else:
        try:
            from skill_registry_common import parse_yaml
            data = parse_yaml(path)
        except ImportError as exc:
            raise CompatibilityValidationError("pinned PyYAML parser not installed") from exc
    version: str | None
    if component_type == "product_model":
        version = _string(data.get("model_version"), relative + ".model_version")
        component_id, owner, authority = "product-model", "model_version", relative
    elif component_type == "skill":
        from skill_registry_common import validate_optional_manifest_version
        version = validate_optional_manifest_version(data, path)
        sid = _string(data.get("id"), relative + ".id")
        if not COMPONENT_ID_RE.fullmatch("skill:" + sid):
            _fail(relative, "invalid skill component identity")
        sibling = path.with_name("SKILL.md")
        if not sibling.is_file():
            _fail(relative, "missing behavioral authority SKILL.md")
        component_id, owner = "skill:" + sid, "manifest.version"
        authority = sibling.relative_to(root).as_posix()
    elif component_type == "workflow":
        version = _string(data.get("version"), relative + ".version")
        component_id = "workflow:" + _string(data.get("name"), relative + ".name")
        owner, authority = "workflow.version", relative
    elif component_type == "machine_schema":
        if not isinstance(data.get("$id"), str) or not data["$id"]:
            _fail(relative, "schema missing $id authority")
        version = declared_schema_version
        component_id, owner, authority = "schema:" + path.name.removesuffix(".schema.json"), "support-ledger.version", relative
    elif component_type == "project_data":
        version = data.get("contract_version")
        if version is not None:
            version = _string(version, relative + ".contract_version")
        component_id, owner, authority = "project-data:project-state", "contract_version", relative
    else:
        raise CompatibilityValidationError(f"unsupported component type: {component_type!r}")
    if version is not None:
        parse_semver(version)
    return VersionedComponent(
        component_id=component_id, component_type=component_type,
        authority_path=authority, version_owner=owner, version=version,
        digest=digest, publication_status="unknown"
    )
