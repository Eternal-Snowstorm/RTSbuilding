from pathlib import Path

from PIL import Image


SRC = Path("staging") / "gemini-topbar-icons" / "topbar_mode_icon_concepts.png"
OUT_RESOURCE = Path("src") / "main" / "resources" / "assets" / "rtsbuilding" / "textures" / "gui" / "topbar"
OUT_STAGING = Path("staging") / "gemini-topbar-icons" / "chopped"

MODES = ["interact", "link", "funnel", "rotate"]
STATES = ["inactive", "hover", "active", "pressed"]

# Nano Banana produced an evenly spaced 512x512 4x4 sheet with each button
# centered in a roughly 96x96 cell. These bounds keep the full button frame
# while trimming most of the dark gutter between cells.
CROPS = [
    (26, 26, 122, 122),
    (148, 26, 244, 122),
    (270, 26, 366, 122),
    (392, 26, 488, 122),
    (26, 148, 122, 244),
    (148, 148, 244, 244),
    (270, 148, 366, 244),
    (392, 148, 488, 244),
    (26, 270, 122, 366),
    (148, 270, 244, 366),
    (270, 270, 366, 366),
    (392, 270, 488, 366),
    (26, 392, 122, 488),
    (148, 392, 244, 488),
    (270, 392, 366, 488),
    (392, 392, 488, 488),
]


def main() -> int:
    img = Image.open(SRC).convert("RGBA")
    OUT_RESOURCE.mkdir(parents=True, exist_ok=True)
    OUT_STAGING.mkdir(parents=True, exist_ok=True)

    icon_size = 24
    preview = Image.new("RGBA", (4 * icon_size, 4 * icon_size), (0, 0, 0, 0))
    for row, state in enumerate(STATES):
        for col, mode in enumerate(MODES):
            crop = img.crop(CROPS[row * 4 + col])
            icon = crop.resize((icon_size, icon_size), Image.Resampling.NEAREST)
            name = f"mode_{mode}_{state}.png"
            icon.save(OUT_RESOURCE / name)
            icon.save(OUT_STAGING / name)
            preview.alpha_composite(icon, (col * icon_size, row * icon_size))

    preview.save(OUT_STAGING / "sheet_chopped.png")
    print(OUT_RESOURCE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
