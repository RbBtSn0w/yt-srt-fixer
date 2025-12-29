import unittest
import sys
import os
import tempfile
import shutil
import subprocess

class TestYtSrtCLI(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'yt_srt_fixer.py'))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_cli_simple_file(self):
        # Create a dummy SRT file
        input_srt = os.path.join(self.test_dir, "video.srt")
        with open(input_srt, "w") as f:
            f.write("1\n00:00:01,000 --> 00:00:02,000\nFoo\n\n")
            
        # Run the script
        msg = subprocess.check_output([sys.executable, self.script_path, input_srt], cwd=self.test_dir)
        
        # Check output file exists
        expected_output = os.path.join(self.test_dir, "video_fcp.srt")
        self.assertTrue(os.path.exists(expected_output))

    def test_cli_directory_recursive(self):
        # Structure:
        # /subdir/subvideo.srt
        subdir = os.path.join(self.test_dir, "subdir")
        os.mkdir(subdir)
        
        input_srt = os.path.join(subdir, "subvideo.srt")
        with open(input_srt, "w") as f:
            f.write("1\n00:00:01,000 --> 00:00:02,000\nBar\n\n")
            
        # Run script on root test_dir
        subprocess.check_call([sys.executable, self.script_path, self.test_dir], cwd=self.test_dir)
        
        # Check if subdir file was processed
        expected_output = os.path.join(subdir, "subvideo_fcp.srt")
        self.assertTrue(os.path.exists(expected_output))

if __name__ == '__main__':
    unittest.main()
