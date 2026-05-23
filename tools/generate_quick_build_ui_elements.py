from pathlib import Path
from PIL import Image, ImageDraw


OUT_DIR = Path("staging") / "ui-overhaul-elements" / "v1"
TOPBAR_DIR = OUT_DIR / "topbar"
PANEL_DIR = OUT_DIR / "quick-build-panel"
SHEET_DIR = OUT_DIR / "sheets"

SCALE = 4

BG = (0x14, 0x19, 0x22, 255)
PANEL_BG = (0x17, 0x1D, 0x26, 245)
PANEL_INNER = (0x1F, 0x28, 0x34, 255)
EDGE_LIGHT = (0x63, 0x79, 0x93, 255)
EDGE_DARK = (0x0D, 0x12, 0x18, 255)
TEXT = (0xEA, 0xF2, 0xFF, 255)
TEXT_DIM = (0xB8, 0xC7, 0xD8, 255)
NEUTRAL = (0xC9, 0xD5, 0xE2, 255)
ACCENT_GREEN = (0x78, 0xB2, 0x8C, 255)
ACCENT_GREEN_DARK = (0x2D, 0x6B, 0x47, 255)
ACCENT_BLUE = (0x88, 0xBE, 0xF4, 255)
ACCENT_AMBER = (0xFF, 0xC4, 0x72, 255)
ACCENT_RED = (0xD1, 0x74, 0x74, 255)
HOVER_BG = (0x1D, 0x25, 0x30, 255)
CELL_BG = (0x1B, 0x23, 0x2D, 255)
CELL_ACTIVE = (0x2D, 0x6B, 0x47, 255)
CELL_HOVER = (0x273443, 255)
SOFT_GRID = (0x2F, 0x3A, 0x48, 255)


def ensure_dirs():
    for path in (TOPBAR_DIR, PANEL_DIR, SHEET_DIR):
        path.mkdir(parents=True, exist_ok=True)


def px(n):
    return n * SCALE


def new_canvas(w, h, fill=(0, 0, 0, 0)):
    return Image.new("RGBA", (px(w), px(h)), fill)


def rect(draw, x0, y0, x1, y1, fill):
    draw.rectangle([px(x0), px(y0), px(x1) - 1, px(y1) - 1], fill=fill)


def line(draw, x0, y0, x1, y1, fill, width=1):
    draw.line([px(x0), px(y0), px(x1), px(y1)], fill=fill, width=max(1, px(width)))


def frame(draw, x, y, w, h, fill, light=EDGE_LIGHT, dark=EDGE_DARK):
    rect(draw, x, y, x + w, y + h, fill)
    line(draw, x, y, x + w - 1, y, light)
    line(draw, x, y, x, y + h - 1, light)
    line(draw, x, y + h - 1, x + w - 1, y + h - 1, dark)
    line(draw, x + w - 1, y, x + w - 1, y + h - 1, dark)


def save(img, path):
    img.resize((img.width // SCALE, img.height // SCALE), Image.Resampling.NEAREST).save(path)


def draw_interact_icon(draw, ox, oy, color):
    pts = [(0, 0), (0, 14), (7, 11), (12, 22), (17, 20), (12, 8), (22, 8)]
    scaled = [(px(ox + x), px(oy + y)) for x, y in pts]
    draw.polygon(scaled, fill=color)


def draw_gear_icon(draw, ox, oy, color):
    rect(draw, ox + 7, oy + 0, ox + 13, oy + 4, color)
    rect(draw, ox + 7, oy + 16, ox + 13, oy + 20, color)
    rect(draw, ox + 0, oy + 7, ox + 4, oy + 13, color)
    rect(draw, ox + 16, oy + 7, ox + 20, oy + 13, color)
    rect(draw, ox + 2, oy + 2, ox + 6, oy + 6, color)
    rect(draw, ox + 14, oy + 2, ox + 18, oy + 6, color)
    rect(draw, ox + 2, oy + 14, ox + 6, oy + 18, color)
    rect(draw, ox + 14, oy + 14, ox + 18, oy + 18, color)
    rect(draw, ox + 5, oy + 5, ox + 15, oy + 15, color)
    rect(draw, ox + 8, oy + 8, ox + 12, oy + 12, BG)


def draw_check_icon(draw, ox, oy, color):
    rect(draw, ox + 2, oy + 10, ox + 6, oy + 14, color)
    rect(draw, ox + 5, oy + 13, ox + 9, oy + 17, color)
    rect(draw, ox + 8, oy + 10, ox + 12, oy + 14, color)
    rect(draw, ox + 11, oy + 7, ox + 15, oy + 11, color)
    rect(draw, ox + 14, oy + 4, ox + 18, oy + 8, color)


def draw_quick_build_icon(draw, ox, oy, color):
    rect(draw, ox + 1, oy + 2, ox + 9, oy + 10, color)
    rect(draw, ox + 13, oy + 2, ox + 21, oy + 10, color)
    rect(draw, ox + 7, oy + 12, ox + 15, oy + 20, color)
    rect(draw, ox + 9, oy + 4, ox + 13, oy + 6, color)
    rect(draw, ox + 9, oy + 14, ox + 13, oy + 16, color)


def draw_shape_icon(draw, name, ox, oy, color, active=False):
    alt_a = ACCENT_BLUE if active else color
    alt_b = ACCENT_GREEN if active else color
    alt_c = ACCENT_AMBER if active else color
    shade = TEXT_DIM if not active else TEXT
    if name == "block":
        rect(draw, ox + 5, oy + 5, ox + 17, oy + 17, alt_b)
        rect(draw, ox + 7, oy + 7, ox + 15, oy + 15, color)
    elif name == "line":
        rect(draw, ox + 3, oy + 10, ox + 19, oy + 12, alt_a)
        rect(draw, ox + 2, oy + 8, ox + 6, oy + 14, alt_b)
        rect(draw, ox + 16, oy + 8, ox + 20, oy + 14, alt_b)
    elif name == "square":
        rect(draw, ox + 4, oy + 4, ox + 20, oy + 6, alt_a)
        rect(draw, ox + 4, oy + 18, ox + 20, oy + 20, alt_a)
        rect(draw, ox + 4, oy + 4, ox + 6, oy + 20, alt_a)
        rect(draw, ox + 18, oy + 4, ox + 20, oy + 20, alt_a)
    elif name == "wall":
        rect(draw, ox + 4, oy + 8, ox + 17, oy + 18, alt_b)
        rect(draw, ox + 9, oy + 5, ox + 22, oy + 8, alt_a)
        rect(draw, ox + 17, oy + 8, ox + 22, oy + 18, alt_c)
        rect(draw, ox + 6, oy + 10, ox + 8, oy + 16, shade)
        rect(draw, ox + 10, oy + 10, ox + 12, oy + 16, shade)
        rect(draw, ox + 14, oy + 10, ox + 16, oy + 16, shade)
        rect(draw, ox + 18, oy + 10, ox + 20, oy + 16, EDGE_DARK)
        rect(draw, ox + 9, oy + 6, ox + 17, oy + 7, TEXT)
    elif name == "circle":
        rect(draw, ox + 8, oy + 3, ox + 16, oy + 5, alt_a)
        rect(draw, ox + 5, oy + 5, ox + 8, oy + 8, alt_a)
        rect(draw, ox + 16, oy + 5, ox + 19, oy + 8, alt_a)
        rect(draw, ox + 3, oy + 8, ox + 5, oy + 16, alt_a)
        rect(draw, ox + 19, oy + 8, ox + 21, oy + 16, alt_a)
        rect(draw, ox + 5, oy + 16, ox + 8, oy + 19, alt_a)
        rect(draw, ox + 16, oy + 16, ox + 19, oy + 19, alt_a)
        rect(draw, ox + 8, oy + 19, ox + 16, oy + 21, alt_a)
    elif name == "box":
        rect(draw, ox + 5, oy + 9, ox + 15, oy + 19, alt_b)
        rect(draw, ox + 10, oy + 5, ox + 20, oy + 9, alt_a)
        rect(draw, ox + 15, oy + 9, ox + 20, oy + 19, alt_c)
        rect(draw, ox + 10, oy + 5, ox + 15, oy + 9, TEXT)
        rect(draw, ox + 7, oy + 11, ox + 9, oy + 17, shade)
        rect(draw, ox + 11, oy + 11, ox + 13, oy + 17, shade)
        rect(draw, ox + 16, oy + 11, ox + 18, oy + 17, EDGE_DARK)
        rect(draw, ox + 8, oy + 18, ox + 15, oy + 19, EDGE_DARK)


def draw_radio(draw, x, y, selected):
    rect(draw, x, y, x + 10, y + 10, PANEL_INNER)
    line(draw, x, y, x + 9, y, EDGE_LIGHT)
    line(draw, x, y, x, y + 9, EDGE_LIGHT)
    line(draw, x, y + 9, x + 9, y + 9, EDGE_DARK)
    line(draw, x + 9, y, x + 9, y + 9, EDGE_DARK)
    if selected:
        rect(draw, x + 2, y + 2, x + 8, y + 8, ACCENT_GREEN)


def draw_rotation_readout(draw, x, y, active=False):
    bg = CELL_ACTIVE if active else PANEL_INNER
    light = (0x9A, 0xD2, 0xAE, 255) if active else EDGE_LIGHT
    frame(draw, x, y, 64, 22, bg, light, EDGE_DARK)
    rect(draw, x + 6, y + 9, x + 16, y + 11, NEUTRAL)
    rect(draw, x + 6, y + 7, x + 8, y + 13, NEUTRAL)
    rect(draw, x + 44, y + 9, x + 54, y + 11, NEUTRAL)
    rect(draw, x + 52, y + 7, x + 54, y + 13, NEUTRAL)


def topbar_button(name, icon_drawer):
    img = new_canvas(32, 24)
    draw = ImageDraw.Draw(img)
    frame(draw, 0, 0, 32, 24, CELL_BG)
    icon_drawer(draw, 5, 1, NEUTRAL)
    save(img, TOPBAR_DIR / f"{name}.png")
    return img


def topbar_button_active(name, icon_drawer):
    img = new_canvas(32, 24)
    draw = ImageDraw.Draw(img)
    frame(draw, 0, 0, 32, 24, CELL_ACTIVE, (0x9A, 0xD2, 0xAE, 255), EDGE_DARK)
    icon_drawer(draw, 5, 1, TEXT)
    save(img, TOPBAR_DIR / f"{name}_active.png")
    return img


def shape_cell(shape_name, state):
    bg = CELL_BG
    light = EDGE_LIGHT
    active = False
    if state == "hover":
        bg = HOVER_BG
    elif state == "active":
        bg = CELL_ACTIVE
        light = (0x9A, 0xD2, 0xAE, 255)
        active = True
    img = new_canvas(28, 28)
    draw = ImageDraw.Draw(img)
    frame(draw, 0, 0, 28, 28, bg, light, EDGE_DARK)
    draw_shape_icon(draw, shape_name, 2, 2, NEUTRAL if not active else TEXT, active)
    save(img, PANEL_DIR / f"shape_{shape_name}_{state}.png")
    return img


def fill_mode_row(mode, state):
    bg = PANEL_INNER
    light = EDGE_LIGHT
    if state == "hover":
        bg = HOVER_BG
    elif state == "active":
        bg = CELL_ACTIVE
        light = (0x9A, 0xD2, 0xAE, 255)
    img = new_canvas(76, 16)
    draw = ImageDraw.Draw(img)
    frame(draw, 0, 0, 76, 16, bg, light, EDGE_DARK)
    draw_radio(draw, 3, 3, state == "active")
    save(img, PANEL_DIR / f"fill_{mode}_{state}.png")
    return img


def rotation_readout(state):
    img = new_canvas(64, 22)
    draw = ImageDraw.Draw(img)
    draw_rotation_readout(draw, 0, 0, state == "active")
    save(img, PANEL_DIR / f"rotation_readout_{state}.png")
    return img


def quick_build_panel_mock():
    img = new_canvas(176, 220, BG)
    draw = ImageDraw.Draw(img)
    frame(draw, 0, 0, 176, 220, PANEL_BG)
    rect(draw, 1, 1, 175, 20, (0x21, 0x2C, 0x39, 255))
    rect(draw, 0, 24, 176, 25, SOFT_GRID)
    rect(draw, 0, 114, 176, 115, SOFT_GRID)
    rect(draw, 0, 168, 176, 169, SOFT_GRID)

    shapes = ["block", "line", "square", "wall", "circle", "box"]
    for idx, shape in enumerate(shapes):
        col = idx % 2
        row = idx // 2
        x = 12 + col * 40
        y = 36 + row * 32
        bg = CELL_ACTIVE if shape == "box" else CELL_BG
        light = (0x9A, 0xD2, 0xAE, 255) if shape == "box" else EDGE_LIGHT
        frame(draw, x, y, 28, 28, bg, light, EDGE_DARK)
        draw_shape_icon(draw, shape, x + 2, y + 2, TEXT if shape == "box" else NEUTRAL, shape == "box")

    fill_modes = [("fill", False), ("hollow", False), ("skeleton", True)]
    for idx, (mode, active) in enumerate(fill_modes):
        x = 100
        y = 36 + idx * 22
        bg = CELL_ACTIVE if active else PANEL_INNER
        light = (0x9A, 0xD2, 0xAE, 255) if active else EDGE_LIGHT
        frame(draw, x, y, 64, 16, bg, light, EDGE_DARK)
        draw_radio(draw, x + 3, y + 3, active)

    draw_rotation_readout(draw, 100, 118, True)

    rect(draw, 100, 150, 164, 151, SOFT_GRID)
    save(img, SHEET_DIR / "quick_build_panel_mock.png")
    return img


def topbar_layout_mock():
    img = new_canvas(360, 62, BG)
    draw = ImageDraw.Draw(img)
    rect(draw, 0, 0, 360, 52, (0x10, 0x11, 0x16, 235))

    x = 8
    buttons = [
        ("mode_interact", draw_interact_icon, False),
        ("mode_link", lambda d, ox, oy, c: draw_shape_icon(d, "line", ox, oy + 1, c, False), False),
        ("quick_build", draw_quick_build_icon, False),
        ("quest_check", draw_check_icon, False),
    ]
    for name, drawer, active in buttons:
        frame(draw, x, 4, 32, 24, CELL_ACTIVE if active else CELL_BG, (0x9A, 0xD2, 0xAE, 255) if active else EDGE_LIGHT, EDGE_DARK)
        drawer(draw, x + 5, 5, TEXT if active else NEUTRAL)
        x += 37

    x = 360 - 32 - 8
    frame(draw, x, 4, 32, 24, CELL_BG)
    draw_gear_icon(draw, x + 5, 5, NEUTRAL)

    save(img, SHEET_DIR / "topbar_layout_mock.png")
    return img


def gear_menu_mock():
    img = new_canvas(120, 92, BG)
    draw = ImageDraw.Draw(img)
    frame(draw, 0, 0, 120, 92, PANEL_BG)
    row_y = 8
    for width in (86, 94, 64):
        frame(draw, 8, row_y, width, 18, PANEL_INNER)
        row_y += 24
    save(img, SHEET_DIR / "gear_menu_mock.png")
    return img


def sheet_overview(topbar, panel, gear):
    img = new_canvas(380, 400, BG)
    draw = ImageDraw.Draw(img)
    rect(draw, 0, 0, 380, 400, BG)
    img.paste(topbar, (px(10), px(10)), topbar)
    img.paste(panel, (px(10), px(86)), panel)
    img.paste(gear, (px(240), px(86)), gear)
    save(img, SHEET_DIR / "overview_sheet.png")


def main():
    ensure_dirs()
    topbar_button("quick_build", draw_quick_build_icon)
    topbar_button_active("quick_build", draw_quick_build_icon)
    topbar_button("gear", draw_gear_icon)
    topbar_button_active("gear", draw_gear_icon)
    topbar_button("quest_check", draw_check_icon)
    topbar_button_active("quest_check", draw_check_icon)

    for shape in ("block", "line", "square", "wall", "circle", "box"):
        for state in ("inactive", "hover", "active"):
            shape_cell(shape, state)

    for mode in ("fill", "hollow", "skeleton"):
        for state in ("inactive", "hover", "active"):
            fill_mode_row(mode, state)

    for state in ("inactive", "hover", "active"):
        rotation_readout(state)

    topbar = topbar_layout_mock()
    panel = quick_build_panel_mock()
    gear = gear_menu_mock()
    sheet_overview(topbar, panel, gear)


if __name__ == "__main__":
    main()
