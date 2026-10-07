"""Render canonical social/blog assets from one workspace diagram.html.

This is a thin workspace adapter around export_diagram.py. The generic exporter keeps
its descriptive output naming; this script writes directly to canonical, SEO-friendly
paths derived from the Day folder name.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import tempfile
import time
from pathlib import Path
from types import ModuleType


TARGETS = {
    "linkedin": {
        "relative_path": Path("linkedin.png"),
        "full_page": True,
        "preset": "social-portrait",
    },
    "linkedin-cover-mobile": {
        "relative_path": Path("linkedin-cover-mobile.png"),
        "full_page": True,
        "preset": "social-portrait",
        "html_class": "render-linkedin-cover-mobile",
    },
    "linkedin-square-mobile": {
        "relative_path": Path("linkedin-square-mobile.png"),
        "full_page": True,
        "preset": "square",
        "html_class": "render-linkedin-square-mobile",
    },
    "title-card": {
        "relative_path": Path("linkedin-title-card.png"),
        "full_page": True,
        "preset": "square",
        "html_class": "render-title-card",
    },
    "blog-cover": {
        "full_page": True,
        "preset": "video-landscape",
    },
    "blog-body": {
        "full_page": False,
        "preset": None,
    },
}


def _blog_slug(source: Path) -> str:
    """Resolve SEO filename base from a canonical Day or standalone entry."""
    if source.parent.parent.name == "curated-translations":
        return source.parent.name
    if source.parent.parent.name == "entries":
        return source.parent.name
    day_match = re.fullmatch(r"day-(\d+)-(.+)", source.parent.name)
    series_match = re.fullmatch(r"\d+-days-(.+)", source.parent.parent.name)
    if not day_match or not series_match:
        raise ValueError(
            "Could not derive blog slug; expected series/<n>-days-<series>/day-XX-<topic>/diagram.html"
        )
    day_number, topic = day_match.groups()
    series_slug = series_match.group(1)
    return f"{series_slug}-{day_number}-{topic}"


def _load_engine() -> ModuleType:
    """Load the sibling generic exporter without requiring a Python package."""
    engine_path = Path(__file__).with_name("export_diagram.py")
    spec = importlib.util.spec_from_file_location("diagram_export_engine", engine_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load export engine: {engine_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _atomic_export(
    engine: ModuleType,
    source: Path,
    output: Path,
    *,
    scale: float,
    full_page: bool,
    preset: str | None,
    html_class: str | None,
) -> Path:
    """Render to a temporary PNG, then replace the canonical derivative atomically."""
    output.parent.mkdir(parents=True, exist_ok=True)
    viewport = engine.PRESETS[preset] if preset else None

    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{output.stem}-",
        suffix=output.suffix,
        dir=output.parent,
    )
    os.close(fd)
    temporary = Path(temporary_name)

    try:
        temporary.unlink(missing_ok=True)
        engine.export_png(
            source,
            temporary,
            scale=scale,
            full_page=full_page,
            viewport=viewport,
            html_class=html_class,
        )
        for attempt in range(3):
            try:
                temporary.replace(output)
                break
            except PermissionError:
                if attempt == 2:
                    raise
                time.sleep(0.5)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise

    return output


def _render_target(
    engine: ModuleType,
    source: Path,
    target: str,
    *,
    scale: float,
    body_index: int,
) -> Path:
    config = TARGETS[target]
    blog_slug = _blog_slug(source)
    asset_dir = Path("blog") / blog_slug
    if target == "blog-cover":
        relative_path = asset_dir / f"{blog_slug}-cover.png"
    elif target == "blog-body":
        relative_path = asset_dir / f"{blog_slug}-body-{body_index}.png"
    else:
        relative_path = config["relative_path"]

    preset = config["preset"]

    output = source.parent / relative_path
    return _atomic_export(
        engine,
        source,
        output,
        scale=scale,
        full_page=bool(config["full_page"]),
        preset=preset,
        html_class=config.get("html_class"),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Canonical Day diagram.html")
    parser.add_argument(
        "--target",
        choices=("all", *TARGETS.keys()),
        default="all",
        help="Canonical asset target; default: all",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=2,
        help="PNG device scale factor for all requested targets; default: 2",
    )
    parser.add_argument(
        "--body-index",
        type=int,
        default=1,
        help="Index for blog-body target; default: 1",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    if not source.is_file():
        parser.error(f"Source file not found: {source}")
    if source.name != "diagram.html":
        parser.error("Workspace source must be the canonical file named diagram.html")
    if args.scale <= 0 or args.scale > 4:
        parser.error("--scale must be greater than 0 and no more than 4")
    if args.body_index < 1:
        parser.error("--body-index must be at least 1")

    try:
        engine = _load_engine()
        targets = tuple(TARGETS) if args.target == "all" else (args.target,)
        for target in targets:
            output = _render_target(
                engine,
                source,
                target,
                scale=args.scale,
                body_index=args.body_index,
            )
            print(output)
    except (OSError, RuntimeError, ValueError) as error:
        print(str(error))
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
