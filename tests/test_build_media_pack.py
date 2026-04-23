from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


class BuildMediaPackTests(unittest.TestCase):
    def build_pack(self, pack: str) -> Path:
        tmp_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(tmp_dir, ignore_errors=True))
        result = subprocess.run(
            [
                "python3",
                "scripts/build_media_pack.py",
                "--pack",
                pack,
                "--title",
                "Signal Atlas",
                "--brief",
                "Create a pack for technical storytelling.",
                "--subject",
                "a luminous routing map",
                "--out-dir",
                tmp_dir,
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())

    def test_promo_pack_outputs_manim_and_audio_assets(self) -> None:
        pack_dir = self.build_pack("promo")
        commands = json.loads((pack_dir / "commands.json").read_text(encoding="utf-8"))
        self.assertEqual(len(commands), 8)
        self.assertTrue((pack_dir / "manim" / "plan.md").exists())
        self.assertTrue((pack_dir / "manim" / "script.py").exists())
        self.assertTrue((pack_dir / "prompts" / "narration.txt").exists())
        self.assertTrue((pack_dir / "modules" / "cover-image-brief.md").exists())
        self.assertTrue((pack_dir / "modules" / "diagram-brief.md").exists())
        kinds = {cmd["name"]: cmd["kind"] for cmd in commands}
        self.assertEqual(kinds["diagram"], "diagram")
        self.assertTrue((pack_dir / "diagrams" / "diagram.dot").exists())

    def test_lesson_pack_uses_manim_backend(self) -> None:
        pack_dir = self.build_pack("lesson")
        brief = json.loads((pack_dir / "brief.json").read_text(encoding="utf-8"))
        metadata = json.loads((pack_dir / "pack-metadata.json").read_text(encoding="utf-8"))
        self.assertEqual(brief["style"], "B2")
        self.assertEqual(brief["video_backend"], "manim")
        self.assertTrue((pack_dir / "manim" / "concat.txt").exists())
        self.assertTrue((pack_dir / "prompts" / "storyboard.txt").exists())
        self.assertIn("module_paths", metadata)
        self.assertIn("dot_path", metadata)
        self.assertTrue((pack_dir / "modules" / "publishing-brief.md").exists())
        self.assertTrue((pack_dir / "diagrams" / "diagram.dot").exists())


if __name__ == "__main__":
    unittest.main()
