import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run import process


class GitPathTests(unittest.TestCase):
    def test_actual_git_diff_with_spaces_and_unicode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            names = ["folder with spaces/file name.txt", "folder/\u8d44\u6599.txt"]
            for name in names:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("old\n")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            for name in names:
                (root / name).write_text("new\nextra\n")
            diff = subprocess.run(["git", "-C", str(root), "diff", "--no-ext-diff"], capture_output=True, text=True, check=True).stdout
            result = process({"diff": diff})
            self.assertEqual({row["path"] for row in result["files"]}, set(names))
            self.assertEqual((result["additions"], result["deletions"]), (4, 2))

    def test_truncated_hunk_is_an_input_error(self):
        diff = "diff --git a/a.txt b/a.txt\n--- a/a.txt\n+++ b/a.txt\n@@ -1,2 +1,2 @@\n-one\n+two\n"
        with self.assertRaises(ValueError):
            process({"diff": diff})

    def test_extra_hunk_content_is_an_input_error(self):
        diff = "diff --git a/a.txt b/a.txt\n--- a/a.txt\n+++ b/a.txt\n@@ -1 +1 @@\n-one\n+two\n+extra\n"
        with self.assertRaises(ValueError):
            process({"diff": diff})

    def test_deletion_keeps_an_embedded_git_prefix_in_the_name(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            for name, content in [("folder b/name.txt", b"text\n"), ("folder b/binary.dat", b"\x00fixture")]:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            for target in (root / 'folder b').iterdir():
                target.unlink()
            diff = subprocess.run(["git", "-C", str(root), "diff", "--no-ext-diff"], capture_output=True, text=True, check=True).stdout
            self.assertEqual({row['path'] for row in process({'diff': diff})['files']}, {"folder b/name.txt", "folder b/binary.dat"})

    def test_unicode_line_separator_is_part_of_the_source_line(self):
        diff = "diff --git a/a.txt b/a.txt\n--- a/a.txt\n+++ b/a.txt\n@@ -1 +1 @@\n-one\u2028line\n+two\u2028line\n"
        result = process({'diff': diff})
        self.assertEqual((result['additions'], result['deletions']), (1, 1))


if __name__ == "__main__":
    unittest.main()
