#!/usr/bin/env python3
"""
Convert PNG icons to ICO (Windows) and ICNS (macOS) formats.

This script reads PNG icons from the module-specific linux/ folders and
generates ready-to-use binaries for both pain-compiler and pain-lsp.
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: PIL (Pillow) is required. Install it with: pip install Pillow")
    sys.exit(1)

# Icon sizes for ICO (Windows)
ICO_SIZES = [16, 32, 48, 64, 128, 256]

# Icon sizes for ICNS (macOS) - ICNS format requires specific sizes
ICNS_SIZES = [16, 32, 64, 128, 256, 512, 1024]

try:
    RESAMPLE = Image.Resampling.LANCZOS  # Pillow >= 10
except AttributeError:
    RESAMPLE = Image.LANCZOS  # Pillow < 10


def _load_image(path: Path):
    """Load PNG as RGBA/RGB to keep Windows happy."""
    with Image.open(path) as img:
        if img.mode not in ("RGBA", "RGB"):
            img = img.convert("RGBA" if img.mode in ("LA", "P") else "RGB")
        else:
            img = img.copy()
    return img


def _collect_sources(png_dir: Path, base_name: str):
    """Return dict[size] = Image for every available PNG."""
    sources = {}
    for path in png_dir.glob(f"{base_name}_*x*.png"):
        size_tag = path.stem.rsplit("_", 1)[-1]
        if "x" not in size_tag:
            continue
        try:
            width, height = map(int, size_tag.split("x"))
        except ValueError:
            continue
        if width != height:
            continue
        sources[width] = _load_image(path)
    fallback = png_dir / f"{base_name}.png"
    if fallback.exists():
        img = _load_image(fallback)
        sources[max(img.size)] = img
    return sources


def create_ico_from_pngs(png_dir: Path, output_path: Path, base_name: str):
    """Create ICO file from multiple PNG sizes."""
    print(f"  Looking for PNG files in: {png_dir}")
    print(f"  Base name: {base_name}")
    source_images = _collect_sources(png_dir, base_name)
    if not source_images:
        print(f"ERROR: No PNG files found for {base_name} in {png_dir}")
        print(f"  Expected pattern: {base_name}_*x*.png or {base_name}.png")
        if png_dir.exists():
            print(f"  Directory exists. Contents:")
            for item in png_dir.iterdir():
                print(f"    - {item.name}")
        else:
            print(f"  Directory does not exist!")
        return False
    print(f"  Found {len(source_images)} PNG source(s): {sorted(source_images.keys())}")
    entries = []
    sorted_sizes = sorted(source_images)
    largest = sorted_sizes[-1]
    for size in ICO_SIZES:
        if size in source_images:
            img = source_images[size]
        else:
            larger = next((s for s in sorted_sizes if s > size), largest)
            base_img = source_images[larger]
            img = base_img.resize((size, size), RESAMPLE)
            print(f"Info: {base_name} lacks {size}x{size}, resized from {larger}x{larger}")
        if img.width != size or img.height != size:
            img = img.resize((size, size), RESAMPLE)
        entries.append((size, img))
    entries.sort(key=lambda item: item[0], reverse=True)
    ordered_images = [img for _, img in entries]
    try:
        if len(ordered_images) == 1:
            ordered_images[0].save(output_path, format='ICO')
        else:
            ordered_images[0].save(
                output_path,
                format='ICO',
                sizes=[(img.width, img.height) for img in ordered_images],
                append_images=ordered_images[1:]
            )
        print(
            f"[OK] Created {output_path} with {len(ordered_images)} sizes: "
            f"{[f'{img.width}x{img.height}' for img in ordered_images]}"
        )
        return True
    except Exception as e:
        print(f"Error creating ICO: {e}")
        ordered_images[0].save(output_path, format='ICO')
        print(f"[WARN] Created {output_path} with only first size due to error")
        return False


def create_icns_from_pngs(png_dir: Path, output_path: Path, base_name: str):
    """Create ICNS file from multiple PNG sizes."""
    import tempfile
    import shutil

    temp_dir = Path(tempfile.mkdtemp())
    try:
        iconset_dir = temp_dir / f"{base_name}.iconset"
        iconset_dir.mkdir()

        size_map = {
            16: ("icon_16x16.png", "icon_16x16@2x.png"),
            32: ("icon_32x32.png", "icon_32x32@2x.png"),
            64: ("icon_64x64.png", "icon_64x64@2x.png"),
            128: ("icon_128x128.png", "icon_128x128@2x.png"),
            256: ("icon_256x256.png", "icon_256x256@2x.png"),
            512: ("icon_512x512.png", "icon_512x512@2x.png"),
        }

        created_files = []
        for size in ICNS_SIZES:
            png_path = png_dir / f"{base_name}_{size}x{size}.png"
            if png_path.exists():
                img = Image.open(png_path)

                if size in size_map:
                    filenames = size_map[size]
                    target_path = iconset_dir / filenames[0]
                    img.save(target_path)
                    created_files.append(target_path)

                    if size * 2 <= 1024:
                        double_size = size * 2
                        double_png = png_dir / f"{base_name}_{double_size}x{double_size}.png"
                        if double_png.exists():
                            double_img = Image.open(double_png)
                            target_2x = iconset_dir / filenames[1]
                            double_img.save(target_2x)
                            created_files.append(target_2x)

        if not created_files:
            print(f"Error: No PNG files found for {base_name}")
            return False

        if sys.platform == 'darwin':
            import subprocess

            result = subprocess.run(
                ['iconutil', '-c', 'icns', str(iconset_dir), '-o', str(output_path)],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"Error creating ICNS: {result.stderr}")
                return False
        else:
            print(f"Warning: ICNS creation requires macOS iconutil command.")
            print(f"  Created iconset at {iconset_dir}")
            print(f"  Run on macOS: iconutil -c icns {iconset_dir} -o {output_path}")
            return False

        print(f"[OK] Created {output_path}")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    script_dir = Path(__file__).resolve().parent
    workspace_root = script_dir.parent
    project_root = workspace_root / "pain-compiler"

    icon_configs = [
        {
            "label": "pain (compiler)",
            "base": "pain",
            "linux": project_root / "resources" / "icons" / "linux",
            "windows": [project_root / "resources" / "icons" / "windows" / "pain.ico"],
            "macos": [project_root / "resources" / "icons" / "macOS" / "pain.icns"],
        },
        {
            "label": "lsp",
            "base": "lsp",
            "linux": workspace_root / "pain-lsp" / "resources" / "icons" / "linux",
            "windows": [
                workspace_root / "pain-lsp" / "resources" / "icons" / "windows" / "lsp.ico",
                project_root / "resources" / "icons" / "windows" / "lsp.ico",
            ],
            "macos": [
                workspace_root / "pain-lsp" / "resources" / "icons" / "macOS" / "lsp.icns",
            ],
        },
    ]

    for config in icon_configs:
        print(f"\nProcessing {config['label']} icons...")
        linux_dir = config["linux"]
        print(f"  Linux icons directory: {linux_dir}")
        print(f"  Directory exists: {linux_dir.exists()}")
        if not linux_dir.exists():
            print(f"ERROR: Linux icons directory not found: {linux_dir}")
            print(f"  Absolute path: {linux_dir.resolve()}")
            print("ERROR: Skipping this icon set")
            sys.exit(1)

        for target in config.get("windows", []):
            target.parent.mkdir(parents=True, exist_ok=True)
            success = create_ico_from_pngs(linux_dir, target, config["base"])
            if not success:
                print(f"ERROR: Failed to create {target}")
                sys.exit(1)
            if not target.exists():
                print(f"ERROR: Icon file was not created: {target}")
                sys.exit(1)
            print(f"Verified: {target} exists ({target.stat().st_size} bytes)")

        for target in config.get("macos", []):
            target.parent.mkdir(parents=True, exist_ok=True)
            create_icns_from_pngs(linux_dir, target, config["base"])

    print("\n[OK] Icon conversion complete!")


if __name__ == "__main__":
    main()

