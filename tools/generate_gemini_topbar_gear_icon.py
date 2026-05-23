import os
import subprocess
import sys
from pathlib import Path


PROMPT = """
Create a professional pixel-art UI concept sheet for one tiny settings gear button.

Context:
- Game: Minecraft mod RTSBuilding.
- UI placement: the far-right settings button in the top bar of the RTS Builder screen.
- In-game size: 24x24 button, the gear symbol must remain readable at 18x18.
- Existing topbar visual language: dark beveled Minecraft-like square buttons, hard pixel edges, pale off-white icon, green active state, muted blue hover state, pressed state slightly darker.
- The current gear is crude hand-drawn blocks; replace it with a clean, crisp gear/cog settings icon.

Deliverable:
- One square 1:1 image sheet.
- 2 columns x 2 rows.
- Cells, left to right and top to bottom:
  1. inactive
  2. hover
  3. active/open
  4. pressed
- Each cell is a complete square button mockup with bevel frame and centered gear icon.
- No labels, no words, no watermark, no decorative background.
- Use crisp pixel art, orthographic UI icon design, transparent or very dark background outside cells.
- Prefer a readable cog silhouette with a small center hole, not a photorealistic metal gear.
"""


def main() -> int:
    script = Path("tools") / "generate_gemini_topbar_icon_concepts.py"
    if not script.exists():
        print("Missing Gemini helper script.", file=sys.stderr)
        return 1
    env = os.environ.copy()
    env["RTS_GEMINI_PROMPT_OVERRIDE"] = PROMPT
    env["RTS_GEMINI_OUT_DIR"] = str(Path("staging") / "gemini-topbar-gear")
    env["RTS_GEMINI_OUT_FILE"] = "settings_gear_concepts.png"
    return subprocess.call([sys.executable, str(script)], env=env)


if __name__ == "__main__":
    raise SystemExit(main())
