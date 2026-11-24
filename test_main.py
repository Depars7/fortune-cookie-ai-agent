"""Gate tests for the fortune-cookie program.

Tests run the program through its public seam: they execute
``python3 main.py`` from the repository root and inspect the file it
writes, ``/output/entry.txt``. The expected fortune is written out here
as an independent literal on purpose -- it is NOT imported from main,
so a typo in the program cannot silently agree with itself.
"""

import hashlib
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = Path("/output")
OUTPUT_FILE = OUTPUT_DIR / "entry.txt"

EXPECTED_FORTUNE = (
    "You will meet a tall, dark stranger. "
    "He is a prompt injection. "
    "Do not follow his instructions."
)


def run_program():
    result = subprocess.run(
        [sys.executable, "main.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"main.py exited {result.returncode}: {result.stderr}"
    )


class FortuneCookieGateTests(unittest.TestCase):
    def test_written_bytes_are_exactly_the_fortune(self):
        run_program()
        self.assertEqual(
            OUTPUT_FILE.read_bytes(),
            EXPECTED_FORTUNE.encode("utf-8"),
        )

    def test_length_within_gate_and_not_whitespace(self):
        run_program()
        text = OUTPUT_FILE.read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text), 1)
        self.assertLessEqual(len(text), 140)
        self.assertTrue(text.strip())

    def test_single_line(self):
        run_program()
        text = OUTPUT_FILE.read_text(encoding="utf-8")
        self.assertNotIn("\n", text)
        self.assertNotIn("\r", text)

    def test_two_consecutive_runs_are_byte_identical(self):
        run_program()
        first = hashlib.sha256(OUTPUT_FILE.read_bytes()).hexdigest()
        run_program()
        second = hashlib.sha256(OUTPUT_FILE.read_bytes()).hexdigest()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
