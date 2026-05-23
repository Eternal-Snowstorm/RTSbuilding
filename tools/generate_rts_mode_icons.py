from PIL import Image, ImageDraw
from pathlib import Path


OUT_DIR = Path("staging") / "ui-icon-concepts"
FINAL_DIR = Path("staging") / "ui-icon-final"
STATE_DIR = Path("staging") / "ui-icon-states"
SIZE = 64
UPSCALE = 4
CANVAS = SIZE * UPSCALE

BG = (0x14, 0x19, 0x22, 255)
BG_ALT = (0x1B, 0x22, 0x2C, 255)
BORDER_LIGHT = (0x63, 0x79, 0x93, 255)
BORDER_DARK = (0x0D, 0x12, 0x18, 255)
INK = (0xEA, 0xF2, 0xFF, 255)
GREEN = (0x78, 0xB2, 0x8C, 255)
GREEN_DARK = (0x2D, 0x6B, 0x47, 255)
AMBER = (0xFF, 0xC4, 0x72, 255)
RED = (0xD1, 0x74, 0x74, 255)
BLUE = (0x88, 0xBE, 0xF4, 255)
HOVER_BG = (0x1D, 0x25, 0x30, 255)
ACTIVE_BG = (0x2D, 0x6B, 0x47, 255)
ACTIVE_BG_INNER = (0x38, 0x7F, 0x53, 255)
PRESSED_BG = (0x1F, 0x50, 0x37, 255)
ICON_ACTIVE = (0xF4, 0xFB, 0xF5, 255)
ICON_HOVER = (0xF2, 0xF7, 0xFF, 255)
ICON_PRESSED = (0xE2, 0xF1, 0xE6, 255)
HOVER_BORDER_LIGHT = (0x7A, 0x90, 0xAA, 255)
ACTIVE_BORDER_LIGHT = (0x9A, 0xD2, 0xAE, 255)
PRESSED_BORDER_LIGHT = (0x6A, 0xA7, 0x84, 255)
NEUTRAL_ICON = (0xD9, 0xE3, 0xEF, 255)
NEUTRAL_ICON_DIM = (0xBD, 0xC9, 0xD6, 255)


def rect(draw, x0, y0, x1, y1, fill):
    draw.rectangle([x0 * UPSCALE, y0 * UPSCALE, x1 * UPSCALE - 1, y1 * UPSCALE - 1], fill=fill)


def line(draw, x0, y0, x1, y1, fill, width=1):
    draw.line(
        [x0 * UPSCALE + UPSCALE // 2, y0 * UPSCALE + UPSCALE // 2, x1 * UPSCALE + UPSCALE // 2, y1 * UPSCALE + UPSCALE // 2],
        fill=fill,
        width=width * UPSCALE,
    )


def circle(draw, cx, cy, r, outline=None, fill=None, width=1):
    draw.ellipse(
        [
            (cx - r) * UPSCALE,
            (cy - r) * UPSCALE,
            (cx + r) * UPSCALE - 1,
            (cy + r) * UPSCALE - 1,
        ],
        outline=outline,
        fill=fill,
        width=width * UPSCALE,
    )


def chain_loop(draw, cx, cy, fill, hole=BG_ALT):
    rect(draw, cx - 10, cy - 8, cx + 10, cy - 4, fill)
    rect(draw, cx - 10, cy + 4, cx + 10, cy + 8, fill)
    rect(draw, cx - 10, cy - 6, cx - 6, cy + 6, fill)
    rect(draw, cx + 6, cy - 6, cx + 10, cy + 6, fill)
    rect(draw, cx - 2, cy - 4, cx + 4, cy + 4, hole)


def draw_new_interact(draw, color):
    rect(draw, 18, 12, 26, 44, color)
    rect(draw, 26, 16, 34, 40, color)
    rect(draw, 34, 20, 42, 36, color)
    rect(draw, 42, 24, 50, 32, color)
    rect(draw, 48, 28, 56, 36, color)
    rect(draw, 34, 36, 42, 54, color)
    rect(draw, 42, 48, 52, 54, color)
    rect(draw, 48, 12, 58, 22, BLUE if color == ICON_ACTIVE else (0x45, 0x68, 0x82, 180))
    rect(draw, 52, 16, 56, 20, color)


def draw_new_link(draw, color):
    left = BLUE if color == ICON_ACTIVE else color
    right = GREEN if color == ICON_ACTIVE else color
    chain_loop(draw, 22, 34, left)
    chain_loop(draw, 42, 30, right)
    rect(draw, 26, 30, 46, 34, color)
    rect(draw, 30, 34, 42, 38, color)


def draw_new_funnel(draw, color):
    top = AMBER if color == ICON_ACTIVE else color
    mid = GREEN if color == ICON_ACTIVE else color
    tip = BLUE if color == ICON_ACTIVE else color
    rect(draw, 12, 12, 52, 20, top)
    rect(draw, 16, 20, 48, 28, top)
    rect(draw, 22, 28, 42, 36, mid)
    rect(draw, 26, 36, 38, 42, mid)
    rect(draw, 30, 42, 34, 56, tip)
    rect(draw, 34, 50, 44, 56, tip)


def draw_new_rotate(draw, color):
    rect(draw, 22, 10, 42, 16, color)
    rect(draw, 40, 14, 50, 24, color)
    rect(draw, 46, 24, 52, 32, color)
    rect(draw, 38, 8, 52, 16, color)
    rect(draw, 44, 16, 52, 26, color)
    rect(draw, 12, 30, 18, 40, color)
    rect(draw, 14, 40, 24, 50, color)
    rect(draw, 22, 48, 42, 54, color)
    rect(draw, 12, 44, 26, 52, color)
    rect(draw, 12, 36, 20, 46, color)
    rect(draw, 24, 24, 40, 40, BG_ALT)
    line(draw, 24, 24, 40, 24, color, 1)
    line(draw, 24, 40, 40, 40, color, 1)
    line(draw, 24, 24, 24, 40, color, 1)
    line(draw, 40, 24, 40, 40, color, 1)


def make_base(fill=BG):
    img = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rect(draw, 0, 0, SIZE, SIZE, fill)
    rect(draw, 1, 1, SIZE - 1, SIZE - 1, fill)
    line(draw, 0, 0, SIZE - 1, 0, BORDER_LIGHT)
    line(draw, 0, 0, 0, SIZE - 1, BORDER_LIGHT)
    line(draw, 0, SIZE - 1, SIZE - 1, SIZE - 1, BORDER_DARK)
    line(draw, SIZE - 1, 0, SIZE - 1, SIZE - 1, BORDER_DARK)
    return img, draw


def make_state_base(state):
    fill = BG
    light = BORDER_LIGHT
    dark = BORDER_DARK
    inner = None
    if state == "hover":
        fill = HOVER_BG
        light = HOVER_BORDER_LIGHT
    elif state == "active":
        fill = ACTIVE_BG
        light = ACTIVE_BORDER_LIGHT
        inner = ACTIVE_BG_INNER
    elif state == "pressed":
        fill = PRESSED_BG
        light = PRESSED_BORDER_LIGHT
    img, draw = make_base(fill)
    if inner is not None:
        rect(draw, 4, 4, SIZE - 4, SIZE - 4, inner)
    line(draw, 0, 0, SIZE - 1, 0, light)
    line(draw, 0, 0, 0, SIZE - 1, light)
    line(draw, 0, SIZE - 1, SIZE - 1, SIZE - 1, dark)
    line(draw, SIZE - 1, 0, SIZE - 1, SIZE - 1, dark)
    if state == "pressed":
        line(draw, 1, 1, SIZE - 2, 1, BORDER_DARK)
        line(draw, 1, 1, 1, SIZE - 2, BORDER_DARK)
    return img, draw


def save(img, path):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img.save(OUT_DIR / path)


def save_to(directory, img, path):
    directory.mkdir(parents=True, exist_ok=True)
    img.save(directory / path)


def interact_a():
    img, draw = make_base()
    draw_new_interact(draw, INK)
    return img


def link_a():
    img, draw = make_base()
    draw_new_link(draw, ICON_ACTIVE)
    return img


def funnel_a():
    img, draw = make_base()
    draw_new_funnel(draw, ICON_ACTIVE)
    return img


def rotate_a():
    img, draw = make_base()
    draw_new_rotate(draw, INK)
    return img


def interact_b():
    img, draw = make_base(BG_ALT)
    rect(draw, 18, 14, 46, 44, (0x24, 0x30, 0x3A, 255))
    line(draw, 22, 18, 40, 18, BORDER_LIGHT, 1)
    line(draw, 22, 18, 22, 36, BORDER_LIGHT, 1)
    line(draw, 24, 40, 36, 52, INK, 1)
    rect(draw, 34, 40, 44, 46, GREEN)
    rect(draw, 30, 46, 40, 52, GREEN)
    rect(draw, 26, 10, 32, 16, AMBER)
    return img


def interact_a2():
    img, draw = make_base()
    rect(draw, 14, 14, 50, 50, BG_ALT)
    line(draw, 18, 18, 18, 46, BORDER_LIGHT)
    line(draw, 18, 18, 46, 18, BORDER_LIGHT)
    line(draw, 18, 46, 46, 46, BORDER_DARK)
    line(draw, 46, 18, 46, 46, BORDER_DARK)

    points = [
        (22, 16),
        (22, 44),
        (29, 38),
        (34, 50),
        (39, 48),
        (34, 35),
        (44, 35),
    ]
    draw.polygon([(x * UPSCALE, y * UPSCALE) for x, y in points], fill=INK)
    line(draw, 22, 16, 22, 44, BORDER_LIGHT, 1)
    line(draw, 22, 16, 44, 35, BORDER_LIGHT, 1)
    line(draw, 29, 38, 34, 50, BORDER_DARK, 1)
    line(draw, 34, 35, 44, 35, BORDER_DARK, 1)
    return img


def draw_interact_symbol(draw, color):
    draw_new_interact(draw, color)


def draw_link_symbol(draw, color):
    draw_new_link(draw, color)


def draw_funnel_symbol(draw, color):
    draw_new_funnel(draw, color)


def draw_rotate_symbol(draw, color):
    draw_new_rotate(draw, color)


def build_state_icon(symbol_drawer, state):
    img, draw = make_state_base(state)
    icon_color = NEUTRAL_ICON_DIM
    if state == "hover":
        icon_color = NEUTRAL_ICON
    elif state == "active":
        icon_color = ICON_ACTIVE
    elif state == "pressed":
        icon_color = NEUTRAL_ICON
    symbol_drawer(draw, icon_color)
    return img.resize((SIZE, SIZE), Image.Resampling.NEAREST)


def link_b():
    img, draw = make_base(BG_ALT)
    circle(draw, 22, 22, 9, outline=INK, width=2)
    circle(draw, 42, 42, 9, outline=INK, width=2)
    line(draw, 28, 28, 36, 36, GREEN, 2)
    line(draw, 36, 28, 28, 36, BLUE, 2)
    rect(draw, 39, 15, 49, 25, AMBER)
    rect(draw, 15, 39, 25, 49, RED)
    return img


def funnel_b():
    img, draw = make_base(BG_ALT)
    line(draw, 14, 16, 50, 16, INK, 2)
    line(draw, 18, 24, 46, 24, INK, 2)
    line(draw, 22, 32, 42, 32, INK, 2)
    line(draw, 26, 40, 38, 40, INK, 2)
    line(draw, 30, 40, 30, 50, GREEN, 2)
    line(draw, 34, 40, 34, 50, GREEN, 2)
    rect(draw, 26, 50, 38, 56, BLUE)
    return img


def rotate_b():
    img, draw = make_base(BG_ALT)
    line(draw, 18, 30, 18, 18, BLUE, 2)
    line(draw, 18, 18, 30, 18, BLUE, 2)
    rect(draw, 28, 14, 36, 22, BLUE)
    line(draw, 46, 34, 46, 46, GREEN, 2)
    line(draw, 46, 46, 34, 46, GREEN, 2)
    rect(draw, 28, 42, 36, 50, GREEN)
    circle(draw, 32, 32, 10, outline=INK, width=2)
    return img


def sheet(images):
    cols = 4
    rows = (len(images) + cols - 1) // cols
    gap = 8
    sheet_img = Image.new("RGBA", (cols * SIZE + (cols + 1) * gap, rows * SIZE + (rows + 1) * gap), (12, 15, 20, 255))
    for i, img in enumerate(images):
        x = gap + (i % cols) * (SIZE + gap)
        y = gap + (i // cols) * (SIZE + gap)
        sheet_img.paste(img.resize((SIZE, SIZE), Image.Resampling.NEAREST), (x, y))
    return sheet_img


def main():
    variants = {
        "mode_interact_a.png": interact_a(),
        "mode_interact_a2.png": interact_a2(),
        "mode_link_a.png": link_a(),
        "mode_funnel_a.png": funnel_a(),
        "mode_rotate_a.png": rotate_a(),
        "mode_interact_b.png": interact_b(),
        "mode_link_b.png": link_b(),
        "mode_funnel_b.png": funnel_b(),
        "mode_rotate_b.png": rotate_b(),
    }
    for name, img in variants.items():
        save(img.resize((SIZE, SIZE), Image.Resampling.NEAREST), name)

    save(sheet([variants["mode_interact_a.png"], variants["mode_link_a.png"], variants["mode_funnel_a.png"], variants["mode_rotate_a.png"]]).resize((304, 80), Image.Resampling.NEAREST), "sheet_variant_a.png")
    save(sheet([variants["mode_interact_b.png"], variants["mode_link_b.png"], variants["mode_funnel_b.png"], variants["mode_rotate_b.png"]]).resize((304, 80), Image.Resampling.NEAREST), "sheet_variant_b.png")

    final_icons = {
        "interact": variants["mode_interact_a.png"].resize((SIZE, SIZE), Image.Resampling.NEAREST),
        "link": variants["mode_link_a.png"].resize((SIZE, SIZE), Image.Resampling.NEAREST),
        "funnel": variants["mode_funnel_a.png"].resize((SIZE, SIZE), Image.Resampling.NEAREST),
        "rotate": variants["mode_rotate_a.png"].resize((SIZE, SIZE), Image.Resampling.NEAREST),
    }
    for name, img in final_icons.items():
        save_to(FINAL_DIR, img, f"mode_{name}.png")

    state_builders = {
        "interact": draw_interact_symbol,
        "link": draw_link_symbol,
        "funnel": draw_funnel_symbol,
        "rotate": draw_rotate_symbol,
    }
    state_order = ["inactive", "hover", "active", "pressed"]
    state_preview_rows = []
    for mode_name, builder in state_builders.items():
        row = []
        for state in state_order:
            img = build_state_icon(builder, state)
            save_to(STATE_DIR, img, f"mode_{mode_name}_{state}.png")
            row.append(img)
        state_preview_rows.append(row)

    gap = 8
    cols = len(state_order)
    rows = len(state_preview_rows)
    preview = Image.new(
        "RGBA",
        (cols * SIZE + (cols + 1) * gap, rows * SIZE + (rows + 1) * gap),
        (12, 15, 20, 255),
    )
    for row_index, row in enumerate(state_preview_rows):
        for col_index, img in enumerate(row):
            x = gap + col_index * (SIZE + gap)
            y = gap + row_index * (SIZE + gap)
            preview.paste(img, (x, y))
    save_to(STATE_DIR, preview, "sheet_states.png")


if __name__ == "__main__":
    main()
