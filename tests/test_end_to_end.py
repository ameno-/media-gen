from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIM_PYTHON = REPO_ROOT / ".venv-manim/bin/python"
FFMPEG = shutil.which("ffmpeg")


class EndToEndWorkflowTests(unittest.TestCase):
    def make_pack(self, pack: str = "lesson") -> Path:
        tmp_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(tmp_dir, ignore_errors=True))
        result = subprocess.run(
            [
                "python3",
                "scripts/build_media_pack.py",
                "--pack",
                pack,
                "--title",
                "End To End Atlas",
                "--brief",
                "Exercise the local workflow from builder through render and mux.",
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

    def test_run_pack_dry_run_covers_full_workflow(self) -> None:
        pack_dir = self.make_pack("promo")
        result = subprocess.run(
            ["python3", "scripts/run_pack.py", "--pack-dir", str(pack_dir), "--dry-run"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        stdout = result.stdout
        self.assertIn("[image] hero-image", stdout)
        self.assertIn("[music] soundtrack", stdout)
        self.assertIn("[tts] narration", stdout)
        self.assertIn("[diagram] diagram", stdout)
        self.assertIn("[video] manim-render", stdout)
        self.assertIn("[post] video-mux", stdout)

    @unittest.skipUnless(MANIM_PYTHON.exists() and FFMPEG, "requires local manim env and ffmpeg")
    def test_render_and_mux_with_local_synthetic_audio(self) -> None:
        pack_dir = self.make_pack("lesson")
        outputs_dir = pack_dir / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)

        narration_path = outputs_dir / "narration.mp3"
        soundtrack_path = outputs_dir / "soundtrack.mp3"

        subprocess.run(
            [
                FFMPEG,
                "-y",
                "-f",
                "lavfi",
                "-i",
                "anullsrc=r=32000:cl=mono",
                "-t",
                "2",
                "-q:a",
                "9",
                "-acodec",
                "libmp3lame",
                str(narration_path),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        subprocess.run(
            [
                FFMPEG,
                "-y",
                "-f",
                "lavfi",
                "-i",
                "sine=frequency=440:sample_rate=44100",
                "-t",
                "2",
                "-q:a",
                "9",
                "-acodec",
                "libmp3lame",
                str(soundtrack_path),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

        subprocess.run(
            [
                "python3",
                "scripts/render_manim_pack.py",
                "--pack-dir",
                str(pack_dir),
                "--quality",
                "low",
                "--render-only",
            ],
            cwd=REPO_ROOT,
            check=True,
        )
        subprocess.run(
            [
                "python3",
                "scripts/render_manim_pack.py",
                "--pack-dir",
                str(pack_dir),
                "--mux-only",
            ],
            cwd=REPO_ROOT,
            check=True,
        )

        self.assertTrue((outputs_dir / "video.mp4").exists())
        self.assertTrue((outputs_dir / "video-with-audio.mp4").exists())
        self.assertTrue((pack_dir / "manim" / "renders" / "Scene1Question.mp4").exists())


if __name__ == "__main__":
    unittest.main()
