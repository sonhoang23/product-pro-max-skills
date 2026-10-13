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
    json_pointer: str | None = None


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


# Phase 4 / US2: offline, evidence-bounded consumer impact evaluation.
# The support ledger never becomes an authority for behavior or publication.

@dataclass(frozen=True)
class ConsumerImpact:
    classification: str
    findings: tuple[Diagnostic, ...]
    covered_consumers: tuple[str, ...]
    unassessed_consumers: tuple[str, ...]


def load_consumer_dependencies(path: Path) -> tuple[ConsumerDependency, ...]:
    """Read explicit consumer->provider edges. No network or inferred external readers.

    Expected fixture/consumer declaration: {"consumers": [{consumer_id,
    provider_component_id, range, required_outputs, required_features,
    strict_reader, declared_by, scope}]}. A null range/strict_reader is unknown.
    """
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"),
                         object_pairs_hook=_no_duplicate_keys)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CompatibilityValidationError(f"{path}: cannot read consumers: {exc}") from exc
    root = _expect_mapping(raw, str(path), {"consumers"}, {"consumers"})
    if not isinstance(root["consumers"], list):
        _fail(str(path), "consumers must be a list")
    edges: list[ConsumerDependency] = []
    seen: set[tuple[str, str]] = set()
    keys = {"consumer_id", "provider_component_id", "range", "required_outputs",
            "required_features", "strict_reader", "declared_by", "scope"}
    for i, entry in enumerate(root["consumers"]):
        where = f"{path}:consumers[{i}]"
        d = _expect_mapping(entry, where, keys, keys)
        cid = _string(d["consumer_id"], where + ".consumer_id")
        provider = _string(d["provider_component_id"], where + ".provider_component_id")
        if not COMPONENT_ID_RE.fullmatch(cid) or not COMPONENT_ID_RE.fullmatch(provider):
            _fail(where, "invalid consumer/provider component ID")
        if (cid, provider) in seen:
            _fail(where, f"duplicate edge {cid} -> {provider}")
        seen.add((cid, provider))
        version_range = d["range"]
        if version_range is not None:
            _string(version_range, where + ".range")
            _parse_version_range(version_range)
        strict = d["strict_reader"]
        if strict is not None and type(strict) is not bool:
            _fail(where, "strict_reader must be boolean or null")
        strings = []
        for key in ("required_outputs", "required_features"):
            values = d[key]
            if not isinstance(values, list) or any(
                not isinstance(x, str) or not x for x in values
            ) or len(set(values)) != len(values):
                _fail(where + "." + key, "must contain unique nonempty strings")
            strings.append(tuple(values))
        edges.append(ConsumerDependency(
            consumer_id=cid, provider_component_id=provider,
            version_range=version_range, required_outputs=strings[0],
            required_features=strings[1], strict_reader=strict,
            declared_by=normalized_relative_path(d["declared_by"], source=where + ".declared_by"),
            scope=_string(d["scope"], where + ".scope")))
    return tuple(edges)


def enumerate_known_consumers(root: Path) -> tuple[ConsumerDependency, ...]:
    """Enumerate only real local reader sources; do not invent support versions.

    These reader paths are audited source surfaces, NOT proof that their version
    ranges or external deployed copies are known. Unknowns remain explicit.
    """
    candidates = (
        ("repo:manifest-parser", "schema:skill-manifest",
         "scripts/skill_registry_common.py", True),
        ("repo:registry-builder", "schema:skill-manifest",
         "scripts/generate_skill_registry.py", True),
        ("repo:model-validator", "product-model",
         "scripts/validate_repo.py", True),
    )
    return tuple(ConsumerDependency(
        consumer_id=cid, provider_component_id=provider, version_range=None,
        required_outputs=(), required_features=(), strict_reader=strict,
        declared_by=source, scope="repo-local-reader; version acceptance unassessed")
        for cid, provider, source, strict in candidates
        if (Path(root) / source).is_file())


def _parse_version_range(expr: str) -> tuple[tuple[str, str], ...]:
    """Conservative SemVer subset: exact, comparators, caret and tilde.

    A space-separated intersection is supported. OR, wildcards and partial
    versions are rejected rather than silently expanded.
    """
    if not isinstance(expr, str) or not expr.strip() or "||" in expr:
        raise CompatibilityValidationError(f"invalid version range: {expr!r}")
    tokens = expr.split()
    parts: list[tuple[str, str]] = []
    for token in tokens:
        match = re.fullmatch(r"(>=|<=|>|<|=|\^|~)?(.+)", token)
        if not match:
            raise CompatibilityValidationError(f"invalid version range: {expr!r}")
        operator, version = match.groups()
        parse_semver(version)
        operator = operator or "="
        if operator in ("^", "~"):
            v = parse_semver(version)
            parts.append((">=", version))
            if operator == "~":
                upper = f"{v.major}.{v.minor + 1}.0"
            elif v.major > 0:
                upper = f"{v.major + 1}.0.0"
            elif v.minor > 0:
                upper = f"0.{v.minor + 1}.0"
            else:
                upper = f"0.0.{v.patch + 1}"
            parts.append(("<", upper))
        else:
            parts.append((operator, version))
    return tuple(parts)


def semver_in_range(version: str, expression: str) -> bool:
    parse_semver(version)
    for operator, expected in _parse_version_range(expression):
        cmp = compare_semver(version, expected)
        if not {
            "=": cmp == 0, ">=": cmp >= 0, "<=": cmp <= 0,
            ">": cmp > 0, "<": cmp < 0
        }[operator]:
            return False
    return True


def _ranges_overlap(expressions: list[str]) -> bool:
    """Compare finite interval bounds; detect impossible strict/equal intersections."""
    lower: str | None = None
    upper: str | None = None
    lower_inclusive = upper_inclusive = True
    for expression in expressions:
        for op, ver in _parse_version_range(expression):
            if op == "=":
                bounds = ((">=", ver), ("<=", ver))
            else:
                bounds = ((op, ver),)
            for relation, value in bounds:
                inclusive = relation in (">=", "<=")
                if relation in (">", ">="):
                    if lower is None or compare_semver(value, lower) > 0:
                        lower, lower_inclusive = value, inclusive
                    elif compare_semver(value, lower) == 0:
                        lower_inclusive &= inclusive
                else:
                    if upper is None or compare_semver(value, upper) < 0:
                        upper, upper_inclusive = value, inclusive
                    elif compare_semver(value, upper) == 0:
                        upper_inclusive &= inclusive
    if lower is None or upper is None:
        return True
    cmp = compare_semver(lower, upper)
    return cmp < 0 or (cmp == 0 and lower_inclusive and upper_inclusive)


def check_consumer_dependencies(
    consumers: tuple[ConsumerDependency, ...],
    providers: dict[str, tuple[str | None, str]],
) -> tuple[Diagnostic, ...]:
    """Fail closed on unsupported/unknown/missing providers, constraints, cycles.

    Providers map component_id -> (current version, support_status). Status is
    from explicit ledger/snapshot, never inferred from a source version alone.
    """
    findings: list[Diagnostic] = []
    by_provider: dict[str, list[ConsumerDependency]] = {}
    graph: dict[str, set[str]] = {}
    for edge in consumers:
        by_provider.setdefault(edge.provider_component_id, []).append(edge)
        graph.setdefault(edge.consumer_id, set()).add(edge.provider_component_id)

        def flag(code: str, classification: str, detail: str, action: str) -> None:
            findings.append(Diagnostic(
                code=code, severity="error" if classification == "breaking" else "warning",
                component_id=edge.provider_component_id, authority_path=edge.declared_by,
                classification=classification, message=detail, required_action=action,
                affected_consumer_ids=(edge.consumer_id,)))

        if edge.provider_component_id not in providers:
            flag("MISSING_PROVIDER", "unassessed", "dependency provider not declared",
                 "Declare source component and immutable supported baseline")
            continue
        version, status = providers[edge.provider_component_id]
        if status not in {"active", "deprecated", "unsupported", "removed", "unknown", "unpublished"}:
            raise CompatibilityValidationError(f"{edge.provider_component_id}: invalid support status")
        if status in {"unsupported", "removed"}:
            flag("UNSUPPORTED_PROVIDER", "breaking", f"provider is {status}",
                 "Upgrade or migrate consumer to a supported dependency")
        elif status in {"unknown", "unpublished"}:
            flag("UNKNOWN_PROVIDER_SUPPORT", "unassessed", f"provider support is {status}",
                 "Declare supported scope and provenance; do not assume publication")
        if version is None:
            flag("UNKNOWN_PROVIDER_VERSION", "unassessed", "provider version unknown",
                 "Declare provider version and supported source")
        elif edge.version_range is None:
            flag("UNKNOWN_DEPENDENCY_RANGE", "unassessed", "consumer version range unknown",
                 "Declare consumer version constraint")
        else:
            try:
                satisfied = semver_in_range(version, edge.version_range)
            except CompatibilityValidationError:
                flag("INVALID_VERSION_RANGE", "unassessed",
                     f"invalid version constraint {edge.version_range!r}",
                     "Fix invalid constraint before assessment")
            else:
                if not satisfied:
                    flag("VERSION_RANGE_MISMATCH", "breaking",
                         f"{version} not accepted by {edge.version_range}",
                         "Upgrade provider or adjust consumer after compatibility review")
    for provider, edges in by_provider.items():
        ranges = [e.version_range for e in edges if e.version_range is not None]
        try:
            overlap = _ranges_overlap(ranges)
        except CompatibilityValidationError:
            overlap = True  # separately surfaced invalid-range diagnostic
        if len(ranges) > 1 and not overlap:
            findings.append(Diagnostic(
                code="CONFLICTING_RANGES", severity="error", component_id=provider,
                authority_path=edges[0].declared_by, classification="breaking",
                message=f"no version satisfies all declared constraints: {ranges}",
                required_action="Resolve incompatible consumer constraints",
                affected_consumer_ids=tuple(sorted(e.consumer_id for e in edges))))
    visited: set[str] = set()
    active: list[str] = []
    emitted: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        if node in active:
            cycle = tuple(active[active.index(node):] + [node])
            if cycle not in emitted:
                emitted.add(cycle)
                findings.append(Diagnostic(
                    code="DEPENDENCY_CYCLE", severity="error", component_id=node,
                    authority_path="<dependency-graph>", classification="breaking",
                    message=" -> ".join(cycle),
                    required_action="Break consumer/provider dependency cycle",
                    affected_consumer_ids=tuple(cycle)))
            return
        if node in visited:
            return
        active.append(node)
        for target in sorted(graph.get(node, ())):
            visit(target)
        active.pop()
        visited.add(node)

    for node in sorted(graph):
        visit(node)
    return tuple(findings)


def _pointer(path: str, part: str) -> str:
    escaped = str(part).replace("~", "~0").replace("/", "~1")
    return path + "/" + escaped


def _model_index(model: dict[str, Any]) -> dict[str, Any]:
    """Flatten canonical IDs with ownership, never compare labels as identity."""
    index: dict[str, Any] = {}
    cycles = model.get("lifecycle", {}).get("cycles", [])
    if not isinstance(cycles, list):
        raise CompatibilityValidationError("product-model:/lifecycle/cycles: expected array")
    for cycle in cycles:
        if not isinstance(cycle, dict) or not isinstance(cycle.get("id"), str):
            raise CompatibilityValidationError("product-model:/lifecycle/cycles: invalid ID")
        cid = cycle["id"]
        if f"cycle:{cid}" in index:
            raise CompatibilityValidationError(f"product-model: duplicate cycle {cid}")
        index[f"cycle:{cid}"] = True
        for phase in cycle.get("phases", []):
            if not isinstance(phase, dict) or not isinstance(phase.get("id"), str):
                raise CompatibilityValidationError(f"product-model: invalid phase in {cid}")
            pid = phase["id"]
            if any(k.endswith(":" + pid) and k.startswith("phase:") for k in index):
                raise CompatibilityValidationError(f"product-model: duplicate phase {pid}")
            index[f"phase:{cid}:{pid}"] = True
    for section in ("tracks", "gates", "decisions", "project_statuses"):
        values = model.get(section, [])
        if not isinstance(values, list):
            raise CompatibilityValidationError(f"product-model:/{section}: expected array")
        for obj in values:
            if not isinstance(obj, dict) or not isinstance(obj.get("id"), str):
                raise CompatibilityValidationError(f"product-model:/{section}: invalid ID")
            key = f"{section}:{obj['id']}"
            if key in index:
                raise CompatibilityValidationError(f"product-model: duplicate {key}")
            index[key] = obj.get("meaning", obj.get("description"))
    return index


def assess_consumer_impact(
    baseline: dict[str, Any] | None,
    candidate: dict[str, Any],
    component_id: str,
    authority_path: str,
    consumers: tuple[ConsumerDependency, ...],
    *,
    component_type: str,
    reader_evidence: frozenset[str] = frozenset(),
    unknown_external_consumers: bool = True,
) -> ConsumerImpact:
    """Static, scope-bounded comparison. Never upgrades static findings to runtime PASS.

    Reader evidence is explicitly supplied per known consumer. A declared
    non-strict reader alone is not verification of enum/metadata tolerance.
    """
    path = normalized_relative_path(authority_path)
    if not isinstance(candidate, dict):
        raise CompatibilityValidationError(f"{path}: candidate must be object")
    if baseline is not None and not isinstance(baseline, dict):
        raise CompatibilityValidationError(f"{path}: baseline must be object")
    applicable = tuple(c for c in consumers if c.provider_component_id == component_id)
    affected = tuple(sorted({c.consumer_id for c in applicable}))
    findings: list[Diagnostic] = []

    def report(code: str, classification: str, pointer: str, message: str,
               action: str, targets: tuple[str, ...] = affected) -> None:
        findings.append(Diagnostic(
            code=code, severity="error" if classification == "breaking" else "warning",
            component_id=component_id, authority_path=path, json_pointer=pointer,
            classification=classification, message=message,
            required_action=action, affected_consumer_ids=targets))

    if baseline is None:
        report("UNKNOWN_BASELINE", "unassessed", "",
               "no supported baseline available", "Declare and verify immutable baseline")
    else:
        def additions(pointer: str, names: set[str], code: str) -> None:
            if not names:
                return
            for name in sorted(names):
                for consumer in applicable:
                    if consumer.strict_reader is True:
                        report(code, "breaking", _pointer(pointer, name),
                               "new value rejected by strict/closed reader",
                               "Migrate reader or use breaking version boundary",
                               (consumer.consumer_id,))
                    elif consumer.strict_reader is None or consumer.consumer_id not in reader_evidence:
                        report("READER_TOLERANCE_UNVERIFIED", "unassessed",
                               _pointer(pointer, name),
                               "reader tolerance not proven for additive change",
                               "Supply reader-specific acceptance test proof",
                               (consumer.consumer_id,))
            if not applicable:
                report("NO_DECLARED_CONSUMER", "unassessed", pointer,
                       "no declared reader for additive change",
                       "Declare scoped readers and verification evidence", ())

        if component_type == "product_model":
            old_ids = _model_index(baseline)
            new_ids = _model_index(candidate)
            for key in sorted(old_ids.keys() - new_ids.keys()):
                report("CANONICAL_ID_REMOVED", "breaking", _pointer("/canonical", key),
                       f"removed or changed canonical ID/phase owner {key}",
                       "Migrate impacted consumers and review canonical identity")
            additions("/canonical", new_ids.keys() - old_ids.keys(),
                      "STRICT_READER_NEW_CANONICAL_ID")
            for key in sorted(old_ids.keys() & new_ids.keys()):
                if old_ids[key] != new_ids[key]:
                    report("CANONICAL_MEANING_CHANGED", "review_required",
                           _pointer("/canonical", key),
                           "gate/decision/status meaning changed",
                           "Obtain semantic reviewer and behavior-test evidence")
            if baseline.get("lifecycle", {}).get("ordered") != candidate.get("lifecycle", {}).get("ordered"):
                report("LIFECYCLE_ORDER_CHANGED", "review_required", "/lifecycle/ordered",
                       "canonical lifecycle order semantics changed",
                       "Review downstream lifecycle assumptions")
        else:
            old_outputs = {x["name"] for x in baseline.get("outputs", [])
                           if isinstance(x, dict) and isinstance(x.get("name"), str)}
            new_outputs = {x["name"] for x in candidate.get("outputs", [])
                           if isinstance(x, dict) and isinstance(x.get("name"), str)}
            for consumer in applicable:
                removed = (old_outputs - new_outputs) & set(consumer.required_outputs)
                for name in sorted(removed):
                    report("REQUIRED_OUTPUT_REMOVED", "breaking", _pointer("/outputs", name),
                           "consumer required output removed or renamed",
                           "Restore output or declare breaking migration",
                           (consumer.consumer_id,))
            if old_outputs - new_outputs and not applicable:
                report("OUTPUT_REMOVAL_UNASSESSED", "unassessed", "/outputs",
                       "removed outputs without declared consumers",
                       "Inventory consumers before classifying output changes", ())
            additions("/outputs", new_outputs - old_outputs, "STRICT_READER_NEW_OUTPUT")

        def walk(old: Any, new: Any, pointer: str = "") -> None:
            if type(old) is not type(new):
                report("FIELD_SHAPE_CHANGED", "breaking", pointer,
                       "field type or expected file shape changed",
                       "Version breaking contract and migrate readers")
                return
            if not isinstance(old, dict):
                return
            old_required = old.get("required", [])
            new_required = new.get("required", [])
            if isinstance(old_required, list) and isinstance(new_required, list):
                for key in sorted(set(new_required) - set(old_required)):
                    report("REQUIRED_FIELD_ADDED", "breaking",
                           _pointer(pointer + "/required", key),
                           "required field newly added",
                           "Migrate old writers/fixtures or make field optional")
            if "enum" in old and "enum" in new and isinstance(old["enum"], list) and isinstance(new["enum"], list):
                additions(pointer + "/enum",
                          set(map(str, new["enum"])) - set(map(str, old["enum"])),
                          "STRICT_READER_NEW_ENUM")
                for value in sorted(set(map(str, old["enum"])) - set(map(str, new["enum"]))):
                    report("ENUM_VALUE_REMOVED", "breaking", _pointer(pointer + "/enum", value),
                           "accepted enum value removed", "Migrate stored values/readers")
            for key in sorted(old.keys() - new.keys()):
                if key in ("description", "title", "examples"):
                    continue
                if key in ("properties", "$defs", "definitions"):
                    report("CONTRACT_MAP_REMOVED", "breaking", _pointer(pointer, key),
                           "contract properties/definitions removed",
                           "Restore shape or migrate consumers")
                elif key not in ("required", "enum"):
                    report("CONTRACT_FIELD_REMOVED", "review_required", _pointer(pointer, key),
                           "contract field removed", "Review readers and semantics")
            semantic = {"triggers", "include", "exclude", "evidence_rules",
                        "evidence", "stop_conditions", "stopping_conditions",
                        "quality_gate", "behavior", "side_effects",
                        "meaning", "decision", "gate"}
            for key in sorted(old.keys() & new.keys()):
                old_value, new_value = old[key], new[key]
                position = _pointer(pointer, key)
                if key in semantic and old_value != new_value:
                    report("SEMANTIC_CHANGE_REVIEW", "review_required", position,
                           "semantic trigger/evidence/gate/decision/stop rule changed",
                           "Require behavioral review and scoped test proof")
                elif key in ("properties", "$defs", "definitions") and isinstance(old_value, dict) and isinstance(new_value, dict):
                    for removed in sorted(old_value.keys() - new_value.keys()):
                        report("SCHEMA_PROPERTY_REMOVED", "breaking",
                               _pointer(position, removed), "schema property removed",
                               "Migrate readers and stored contracts")
                    additions(position, new_value.keys() - old_value.keys(),
                              "STRICT_READER_NEW_FIELD")
                    for child in sorted(old_value.keys() & new_value.keys()):
                        walk(old_value[child], new_value[child], _pointer(position, child))
                elif isinstance(old_value, dict) and isinstance(new_value, dict):
                    walk(old_value, new_value, position)
                elif key in ("type", "additionalProperties") and old_value != new_value:
                    report("EXPECTED_SHAPE_CHANGED", "breaking", position,
                           "schema type or additionalProperties policy changed",
                           "Review all readers and version breaking shape")
        walk(baseline, candidate)
    if unknown_external_consumers:
        report("EXTERNAL_READERS_UNASSESSED", "unassessed", "",
               "external readers not inventoried; universal compatibility unproven",
               "Publish limited coverage; obtain external reader inventory", ())
    unassessed = {c.consumer_id for c in applicable
                  if c.strict_reader is None}
    unassessed.update(x for f in findings if f.classification == "unassessed"
                      for x in f.affected_consumer_ids)
    rank = {"compatible": 0, "review_required": 1, "unassessed": 2, "breaking": 3}
    classification = max(("compatible", *(f.classification for f in findings)), key=rank.__getitem__)
    return ConsumerImpact(
        classification=classification, findings=tuple(findings),
        covered_consumers=tuple(sorted(set(affected) - unassessed)),
        unassessed_consumers=tuple(sorted(unassessed |
                              ({"external:unknown"} if unknown_external_consumers else set()))))
