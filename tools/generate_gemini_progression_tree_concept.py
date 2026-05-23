import os
import subprocess
import sys
from pathlib import Path


PROMPT = """
Create a professional pixel-art UI concept image for a Minecraft mod skill tree screen.

Context:
- Mod: RTS building Build From Above / Built From Above.
- Screen: RTS Progression skill tree.
- The old screen was a plain vertical list and was confusing.
- The new screen should look like a compact skill tree / technology tree.
- It appears over gameplay, so do not use blur-heavy background. Use a strong dark opaque panel.

Required design:
- One centered dark beveled panel.
- Title: RTS PROGRESSION.
- Nodes connected by thin dependency lines.
- Nodes are compact square/rectangular pixel-art cards with states:
  - unlocked: green glow/check
  - unlockable: amber highlight
  - locked: muted dark blue/gray
- Each node has a tiny icon area, a short label, material cost icons, and an unlock button or status badge.
- Material costs should be displayed as item icons with x-counts, not text-only names.
- Use Minecraft-like crisp pixel art, hard edges, minimal gradients.
- No marketing hero, no bokeh, no decorative orbs.

Deliverable:
- One 1:1 concept image.
- No paragraphs of instructions in the image.
"""


def main() -> int:
    script = Path("tools") / "generate_gemini_topbar_icon_concepts.py"
    if not script.exists():
        print("Missing Gemini helper script.", file=sys.stderr)
        return 1
    env = os.environ.copy()
    env["RTS_GEMINI_PROMPT_OVERRIDE"] = PROMPT
    env["RTS_GEMINI_OUT_DIR"] = str(Path("staging") / "gemini-progression-tree")
    env["RTS_GEMINI_OUT_FILE"] = "progression_tree_concept.png"
    return subprocess.call([sys.executable, str(script)], env=env)


if __name__ == "__main__":
    raise SystemExit(main())
