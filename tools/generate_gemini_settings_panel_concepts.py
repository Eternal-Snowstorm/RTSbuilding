import os
import subprocess
import sys
from pathlib import Path


PROMPT = """
Create a professional pixel-art UI concept sheet for a Minecraft mod settings panel.

Context:
- Mod: RTSBuilding, a top-down builder/operator interface for Minecraft.
- Existing UI language: dark beveled Minecraft-like panels, compact RTS tool UI, hard pixel edges, pale text, green active states, sparse blue/amber accents.
- Current settings panel is too rough and should become a centered modal.

Design target:
- Centered settings/config modal, not a tiny corner dropdown.
- Sections:
  1. Controls: sensitivity selector, auto-store toggle.
  2. Survival Balance: large on/off toggle.
  3. Skill Cost Editor: list of skill nodes, selected node, editable material requirements.
  4. Buttons: Save, Reset, Close.
- Pixel-art UI, crisp 1:1 concept image.
- Do not use a marketing hero, no gradients, no bokeh, no decorative orbs.
- Keep it practical, readable, and game-ready.
- No large paragraphs of instructional text. Use compact labels only if needed.
"""


def main() -> int:
    script = Path("tools") / "generate_gemini_topbar_icon_concepts.py"
    if not script.exists():
        print("Missing Gemini helper script.", file=sys.stderr)
        return 1
    env = os.environ.copy()
    env["RTS_GEMINI_PROMPT_OVERRIDE"] = PROMPT
    env["RTS_GEMINI_OUT_DIR"] = str(Path("staging") / "gemini-settings-panel")
    env["RTS_GEMINI_OUT_FILE"] = "settings_panel_concepts.png"
    return subprocess.call([sys.executable, str(script)], env=env)


if __name__ == "__main__":
    raise SystemExit(main())
