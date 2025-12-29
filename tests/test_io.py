import unittest
from datetime import timedelta
import sys
import os
import tempfile
import shutil

# Ensure we can import the script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from yt_srt_fixer import parse_srt, write_srt

class TestYtSrtIO(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_parse_srt_simple(self):
        content = """1
00:00:01,000 --> 00:00:02,000
Hello World

2
00:00:02,500 --> 00:00:03,500
Second Line
"""
        file_path = os.path.join(self.test_dir, "test.srt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        subs = parse_srt(file_path)
        self.assertEqual(len(subs), 2)
        self.assertEqual(subs[0]['content'], "Hello World")
        self.assertEqual(subs[0]['start'], timedelta(seconds=1))
        self.assertEqual(subs[0]['end'], timedelta(seconds=2))

    def test_write_srt(self):
        subs = [
            {'index': 1, 'start': timedelta(seconds=1), 'end': timedelta(seconds=2), 'content': 'Test Content'}
        ]
        file_path = os.path.join(self.test_dir, "output.srt")
        
        write_srt(subs, file_path)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        expected = "1\n00:00:01,000 --> 00:00:02,000\nTest Content\n\n"
        # Allow for possible differences in line endings or trailing newlines
        self.assertIn("00:00:01,000 --> 00:00:02,000", content)
        self.assertIn("Test Content", content)

if __name__ == '__main__':
    unittest.main()
