import base64
import json
import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_OUT_DIR = Path("staging") / "gemini-topbar-icons"
DEFAULT_OUT_FILE_NAME = "topbar_mode_icon_concepts.png"

MODELS = [
    "gemini-3.1-flash-image-preview",
    "gemini-3-pro-image-preview",
    "gemini-2.5-flash-image-preview",
]

DEFAULT_PROMPT = """
Create a single square concept sheet for four tiny pixel-art game UI icons.

Context:
- Game: Minecraft mod RTSBuilding.
- UI placement: top bar mode buttons, only about 18 pixels tall in-game.
- Button style: dark beveled Minecraft-like UI, hard pixel edges, no gradients, no text.
- Existing active color language: green active button, pale off-white icon, sparse amber/green/blue accents only when active.
- Required icons, left to right:
  1. Interact: clear click/use action, readable as a hand cursor or pointer touching a block.
  2. Link / Bind: clear binding between two containers, prefer chain-link or connector motif.
  3. Funnel: clear hopper/funnel / routing-down motif, not just stacked bars.
  4. Rotate: clear rotate-block motif, circular arrow around a small cube/block.

Deliverable:
- One 1:1 image sheet.
- 4 columns x 4 rows.
- Columns are the four icons: Interact, Link, Funnel, Rotate.
- Rows are UI states: inactive, hover, active, pressed.
- Each cell should look like a 64x64 pixel button mockup, but the symbol must remain readable when reduced to 18x18.
- Use crisp pixel art, orthographic UI icon design, transparent or very dark background outside cells.
- No labels, no words, no watermark, no decorative background, no photorealism.
- Prefer iconic silhouettes over complicated detail.
"""
PROMPT = DEFAULT_PROMPT


def request_image(api_key: str, model: str) -> bytes:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    parts = [{"text": PROMPT}]
    reference_image = os.environ.get("RTS_GEMINI_REFERENCE_IMAGE")
    if reference_image:
        mime_type = os.environ.get("RTS_GEMINI_REFERENCE_MIME", "image/png")
        image_bytes = Path(reference_image).read_bytes()
        parts.append({
            "inlineData": {
                "mimeType": mime_type,
                "data": base64.b64encode(image_bytes).decode("ascii"),
            }
        })
    payload = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
            "imageConfig": {
                "aspectRatio": "1:1",
                "imageSize": os.environ.get("RTS_GEMINI_IMAGE_SIZE", "512"),
            },
        },
    }
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=180) as res:
        body = json.loads(res.read().decode("utf-8"))
    for candidate in body.get("candidates", []):
        content = candidate.get("content") or {}
        for part in content.get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                return base64.b64decode(inline["data"])
    raise RuntimeError(json.dumps(body, ensure_ascii=False)[:2000])


def main() -> int:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Missing GEMINI_API_KEY environment variable.", file=sys.stderr)
        return 2

    global PROMPT
    PROMPT = os.environ.get("RTS_GEMINI_PROMPT_OVERRIDE", DEFAULT_PROMPT)
    out_dir = Path(os.environ.get("RTS_GEMINI_OUT_DIR", str(DEFAULT_OUT_DIR)))
    out_file = out_dir / os.environ.get("RTS_GEMINI_OUT_FILE", DEFAULT_OUT_FILE_NAME)
    model_override = os.environ.get("RTS_GEMINI_MODELS_OVERRIDE")
    models = [m.strip() for m in model_override.split(",") if m.strip()] if model_override else MODELS
    errors = []
    for model in models:
        for attempt in range(3):
            try:
                png = request_image(api_key, model)
                out_dir.mkdir(parents=True, exist_ok=True)
                out_file.write_bytes(png)
                (out_dir / "model.txt").write_text(model + "\n", encoding="utf-8")
                print(str(out_file))
                return 0
            except HTTPError as exc:
                detail = exc.read().decode("utf-8", "replace")
                errors.append(f"{model} attempt {attempt + 1}: HTTP {exc.code} {detail[:800]}")
                if exc.code in (400, 403, 404):
                    break
            except (URLError, TimeoutError, RuntimeError) as exc:
                errors.append(f"{model} attempt {attempt + 1}: {exc}")
            time.sleep(2 + attempt * 3)

    print("\n".join(errors), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
