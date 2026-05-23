from pathlib import Path

from PIL import Image


SRC = Path("staging") / "gemini-topbar-gear" / "settings_gear_concepts.png"
OUT_RESOURCE = Path("src") / "main" / "resources" / "assets" / "rtsbuilding" / "textures" / "gui" / "topbar"
OUT_STAGING = Path("staging") / "gemini-topbar-gear" / "chopped"
STATES = ["inactive", "hover", "active", "pressed"]


def main() -> int:
    img = Image.open(SRC).convert("RGBA")
    width, height = img.size
    cell_w = width // 2
    cell_h = height // 2

    OUT_RESOURCE.mkdir(parents=True, exist_ok=True)
    OUT_STAGING.mkdir(parents=True, exist_ok=True)

    preview = Image.new("RGBA", (24 * 4, 24), (0, 0, 0, 0))
    for index, state in enumerate(STATES):
        col = index % 2
        row = index // 2
        crop = img.crop((col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h))
        # Trim a little gutter but keep the full beveled button.
        inset_x = max(0, cell_w // 10)
        inset_y = max(0, cell_h // 10)
        crop = crop.crop((inset_x, inset_y, cell_w - inset_x, cell_h - inset_y))
        icon = crop.resize((24, 24), Image.Resampling.NEAREST)
        name = f"settings_gear_{state}.png"
        icon.save(OUT_RESOURCE / name)
        icon.save(OUT_STAGING / name)
        preview.alpha_composite(icon, (index * 24, 0))

    preview.save(OUT_STAGING / "settings_gear_chopped_preview.png")
    print(OUT_RESOURCE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
