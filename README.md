# yt-srt-fixer

**yt-srt-fixer** is a lightweight tool designed to fix YouTube auto-generated SRT subtitles for compatibility with video editors like Final Cut Pro (FCP).

YouTube's auto-generated subtitles often contain overlapping timestamps or zero-gap transitions. While players handle this fine, strict NLEs like Final Cut Pro reject these files or produce errors. This tool adjusts the timestamps to ensure a clean, non-overlapping gap between subtitles.

## Features
- **Fix Overlaps**: Automatically adjusts end-times to prevent overlap with the next subtitle.
- **Enforce Gaps**: Ensures a configurable minimum gap (default 80ms) between subtitles.
- **Batch Processing**: Supports processing single files, current directory, or recursive directory scanning.
- **Zero Dependencies**: Pure Python 3, no external libraries required.

## Installation
Just download `yt_srt_fixer.py` to your computer.
Prerequisite: [Python 3](https://www.python.org/downloads/) installed.

## Usage

### 1. Process Current Directory
Run without arguments to process all `.srt` files in the current folder:
```bash
python3 yt_srt_fixer.py
```

### 2. Process a Specific File
```bash
python3 yt_srt_fixer.py "path/to/your/video.srt"
```

### 3. Process a Directory (Recursively)
To process a folder and all its subfolders:
```bash
python3 yt_srt_fixer.py "/path/to/collection"
```

### 4. Customizing the Gap
By default, the script enforces an 80ms gap. To change this (e.g., to 100ms):
```bash
python3 yt_srt_fixer.py --gap 100
```

## Testing
The project uses Python's built-in `unittest` with zero runtime dependencies. From the repo root:
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```
This runs the tests in `tests/` and validates core behaviors like timestamp parsing/formatting and overlap fixing.

### Optional: coverage in VS Code
If your editor sets `COVERAGE_ENABLED=1` (e.g., VS Code Test Explorer), install dev-only tooling first:
```bash
python3 -m pip install -r requirements-dev.txt
```
Then re-run the tests; the `coverage` module will be available for the adapter.

### CI coverage
GitHub Actions runs the suite under `coverage` across Python 3.8/3.10/3.12 and produces `coverage.xml` (not uploaded as an artifact by default).

## Running Tests
To run the included unit tests:
```bash
python3 -m unittest discover tests
```

## Contributing
Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License
MIT — see [LICENSE](LICENSE).
