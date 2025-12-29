import unittest
from datetime import timedelta
import sys
import os

# Ensure we can import the script from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from yt_srt_fixer import parse_time, format_time, fix_overlaps

class TestYtSrtFixer(unittest.TestCase):

    def test_parse_time(self):
        self.assertEqual(parse_time("00:00:01,500"), timedelta(seconds=1, milliseconds=500))
        self.assertEqual(parse_time("01:00:00,000"), timedelta(hours=1))

    def test_format_time(self):
        td = timedelta(hours=1, seconds=30, milliseconds=5)
        self.assertEqual(format_time(td), "01:00:30,005")

    def test_fix_overlaps(self):
        # Case 1: Overlap
        # Sub1: 0s -> 2s
        # Sub2: 1.5s -> 3s
        # Gap: 0.1s
        # Result Sub1 end should be 1.5 - 0.1 = 1.4s
        
        subs = [
            {'index': 1, 'start': timedelta(seconds=0), 'end': timedelta(seconds=2), 'content': '1'},
            {'index': 2, 'start': timedelta(seconds=1.5), 'end': timedelta(seconds=3), 'content': '2'}
        ]
        
        fixed = fix_overlaps(subs, min_gap_ms=100)
        
        expected_end_1 = timedelta(seconds=1.4)
        self.assertEqual(fixed[0]['end'], expected_end_1)
        self.assertEqual(fixed[1]['start'], timedelta(seconds=1.5)) # Unchanged

    def test_fix_touching(self):
        # Case 2: Touching (Zero gap)
        # Sub1: 0s -> 2s
        # Sub2: 2s -> 4s
        # Gap: 0.1s
        # Result Sub1 end should be 1.9s
        
        subs = [
            {'index': 1, 'start': timedelta(seconds=0), 'end': timedelta(seconds=2), 'content': '1'},
            {'index': 2, 'start': timedelta(seconds=2), 'end': timedelta(seconds=4), 'content': '2'}
        ]
        
        fixed = fix_overlaps(subs, min_gap_ms=100)
        
        expected_end_1 = timedelta(seconds=1.9)
        self.assertEqual(fixed[0]['end'], expected_end_1)

    def test_fix_sufficient_gap(self):
        # Case 3: Already sufficient gap
        # Sub1: 0s -> 1.8s
        # Sub2: 2s -> 4s
        # Gap: 0.1s
        # 2.0 - 1.8 = 0.2s > 0.1s. No change.
        
        subs = [
            {'index': 1, 'start': timedelta(seconds=0), 'end': timedelta(seconds=1.8), 'content': '1'},
            {'index': 2, 'start': timedelta(seconds=2), 'end': timedelta(seconds=4), 'content': '2'}
        ]
        
        fixed = fix_overlaps(subs, min_gap_ms=100)
        
        self.assertEqual(fixed[0]['end'], timedelta(seconds=1.8))

if __name__ == '__main__':
    unittest.main()
