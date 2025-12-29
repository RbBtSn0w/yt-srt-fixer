# yt-srt-fixer Instructions

This folder contains a Python script `yt_srt_fixer.py` designed to fix YouTube SRT subtitles for Final Cut Pro (FCP) compatibility by ensuring there are no overlapping timestamps. It targets common YouTube SRT quirks where cues overlap or have zero gap.

主要用于修正 YouTube 导出的 SRT 中的时间重叠与间隔不足问题。

For a project overview and contribution details, see `README.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md`. Release notes live in `CHANGELOG.md`.

## Prerequisites
- Python 3 installed on your system.

## How to Use

### Method 1: Process All Files (current folder)
To process all `.srt` files in this current folder, simply run:
```bash
python3 yt_srt_fixer.py
```
This will create new files ending in `_fcp.srt` (e.g., `video_fcp.srt`).

### Method 2: Process a Single File or Specific Directory
To process a specific file:
```bash
python3 yt_srt_fixer.py "Your File Name.srt"
```

To process all files in a specific folder (recursively, including subfolders):
```bash
python3 yt_srt_fixer.py "/path/to/folder"
```

## Customization
By default, the script enforces an 80ms gap between subtitles. You can change this using the `--gap` argument.
Example (100ms gap):
```bash
python3 yt_srt_fixer.py --gap 100
```

Notes:
- When you pass a directory, it is processed recursively (subfolders included).
- Files ending with `_fcp.srt` are skipped automatically.
