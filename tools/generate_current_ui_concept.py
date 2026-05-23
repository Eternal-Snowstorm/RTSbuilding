from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path("E:/RTSbuilding")
OUT = ROOT / "staging" / "ui-concepts"
OUT.mkdir(parents=True, exist_ok=True)

W = 1440
H = 900
TOP_H = 86
BOTTOM_H = 184

BG_TOP = (16, 17, 22, 235)
BG_WORLD = (38, 58, 44, 255)
BG_BOTTOM = (20, 21, 26, 225)
PANEL = (22, 28, 36, 238)
PANEL_INNER = (30, 38, 49, 255)
LIGHT = (108, 131, 154, 255)
TEXT = (242, 247, 255, 255)
TEXT_DIM = (175, 192, 211, 255)
ACTIVE = (45, 107, 71, 255)
BLUE = (78, 158, 255, 72)
BLUE_LINE = (96, 182, 255, 110)

ICON_DIR = ROOT / "src" / "main" / "resources" / "assets" / "rtsbuilding" / "textures" / "gui" / "quickbuild"


def frame(draw, x, y, w, h, fill, light=LIGHT, dark=(13, 17, 23, 255)):
    draw.rectangle([x, y, x + w, y + h], fill=fill)
    draw.line([x, y, x + w, y], fill=light, width=1)
    draw.line([x, y, x, y + h], fill=light, width=1)
    draw.line([x, y + h, x + w, y + h], fill=dark, width=1)
    draw.line([x + w, y, x + w, y + h], fill=dark, width=1)


def text(draw, xy, value, color=TEXT):
    draw.text(xy, value, fill=color, font=ImageFont.load_default())


def icon(name):
    return Image.open(ICON_DIR / name).convert("RGBA")


def paste_shape(img, shape_name, state, x, y):
    tile = icon(f"shape_{shape_name}_{state}.png").resize((28, 28), Image.Resampling.NEAREST)
    img.alpha_composite(tile, (x, y))


def main():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, TOP_H], fill=BG_TOP)
    draw.rectangle([0, TOP_H, W, H - BOTTOM_H], fill=BG_WORLD)
    draw.rectangle([0, H - BOTTOM_H, W, H], fill=BG_BOTTOM)

    # World texture hint.
    for gx in range(0, W, 48):
        draw.line([gx, TOP_H, gx, H - BOTTOM_H], fill=(55, 82, 61, 120), width=1)
    for gy in range(TOP_H, H - BOTTOM_H, 48):
        draw.line([0, gy, W, gy], fill=(55, 82, 61, 120), width=1)

    # Chunk curtain concept.
    curtain_xs = [300, 460, 620, 780, 940, 1100]
    curtain_zs = [TOP_H + 120, TOP_H + 260, TOP_H + 400]
    for x in curtain_xs:
        draw.rectangle([x - 2, TOP_H + 20, x + 2, H - BOTTOM_H - 20], fill=BLUE)
        draw.line([x, TOP_H + 20, x, H - BOTTOM_H - 20], fill=BLUE_LINE, width=1)
    for y in curtain_zs:
        draw.rectangle([180, y - 2, 1180, y + 2], fill=BLUE)
        draw.line([180, y, 1180, y], fill=BLUE_LINE, width=1)

    # Top bar buttons.
    x = 8
    for label in ("I", "L", "F", "R"):
        frame(draw, x, 8, 32, 24, ACTIVE if label == "I" else PANEL_INNER)
        text(draw, (x + 11, 15), label)
        x += 37
    x += 12
    frame(draw, x, 8, 96, 24, ACTIVE)
    text(draw, (x + 16, 15), "Quick Build")
    x += 101
    frame(draw, x, 8, 32, 24, PANEL_INNER)
    text(draw, (x + 12, 15), "V")
    x += 37
    frame(draw, x, 8, 32, 24, ACTIVE)
    text(draw, (x + 10, 15), "[]")
    frame(draw, W - 40, 8, 32, 24, PANEL_INNER)
    text(draw, (W - 28, 15), "*")

    text(draw, (8, 42), "Mode: Interact    Selected Placement Item: Stone Bricks", TEXT)
    text(draw, (8, 58), "Linked Storage: Warehouse East    Shape: Box    Fill: Fill    Rot: 45deg", TEXT_DIM)

    # Quick Build panel.
    panel_x = W - 198
    panel_y = TOP_H + 10
    frame(draw, panel_x, panel_y, 188, 216, PANEL)
    draw.rectangle([panel_x + 1, panel_y + 1, panel_x + 187, panel_y + 21], fill=(35, 51, 69, 255))
    text(draw, (panel_x + 8, panel_y + 7), "Quick Build")
    text(draw, (panel_x + 8, panel_y + 30), "Shape", TEXT_DIM)

    shapes = ["block", "line", "square", "wall", "circle", "box"]
    for i, shape in enumerate(shapes):
        col = i % 2
        row = i // 2
        sx = panel_x + 8 + col * 40
        sy = panel_y + 40 + row * 38
        state = "active" if shape == "box" else "inactive"
        frame(draw, sx, sy, 32, 32, ACTIVE if state == "active" else PANEL_INNER)
        paste_shape(img, shape, state, sx + 2, sy + 2)

    rx = panel_x + 88
    text(draw, (rx, panel_y + 30), "Fill", TEXT_DIM)
    fills = [("Fill", True), ("Hollow", False), ("Skeleton", False)]
    for idx, (label, active) in enumerate(fills):
        fy = panel_y + 42 + idx * 20
        frame(draw, rx, fy, 84, 16, ACTIVE if active else PANEL_INNER)
        draw.rectangle([rx + 4, fy + 4, rx + 12, fy + 12], fill=(18, 24, 32, 255))
        if active:
            draw.rectangle([rx + 6, fy + 6, rx + 10, fy + 10], fill=(120, 178, 140, 255))
        text(draw, (rx + 18, fy + 4), label)

    text(draw, (rx, panel_y + 120), "Rotation", TEXT_DIM)
    frame(draw, rx, panel_y + 130, 20, 18, PANEL_INNER)
    text(draw, (rx + 8, panel_y + 135), "-")
    frame(draw, rx + 24, panel_y + 130, 56, 18, PANEL_INNER)
    text(draw, (rx + 37, panel_y + 135), "45deg")
    frame(draw, rx + 84, panel_y + 130, 20, 18, PANEL_INNER)
    text(draw, (rx + 91, panel_y + 135), "+")
    text(draw, (panel_x + 8, panel_y + 194), "Selection persists automatically", TEXT_DIM)

    # Bottom dock hint.
    frame(draw, 0, H - BOTTOM_H, W, BOTTOM_H, BG_BOTTOM)
    draw.rectangle([1, H - BOTTOM_H + 1, W - 1, H - BOTTOM_H + 18], fill=(28, 36, 47, 255))
    text(draw, (8, H - BOTTOM_H + 5), "RTS Storage")
    text(draw, (70, H - BOTTOM_H + 28), "Current concept: top mode cluster + Quick Build panel + chunk curtain toggle", TEXT_DIM)

    out = OUT / "current_ui_concept.png"
    img.save(out)
    print(out)


if __name__ == "__main__":
    main()
