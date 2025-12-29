# Copilot instructions — yt-srt-fixer

Purpose and scope
- This repo provides a single-file, zero-dependency Python CLI that fixes YouTube SRT subtitle overlaps for strict NLEs (e.g., Final Cut Pro). Keep changes simple, portable, and dependency-free.

Big picture architecture
- Entry point: `yt_srt_fixer.py` with a small pipeline:
  1) `parse_srt(path)` → read UTF-8 SRT, split into blocks, parse cue index + time line + text.
  2) `fix_overlaps(subtitles, min_gap_ms)` → sort by start and trim each cue’s end so the next cue’s start has at least `min_gap_ms` gap. It does NOT shift later cues.
  3) `write_srt(subtitles, output_path)` → reindex and write SRT with enforced gap.
- Data model: list of dicts `{ index, start, end, content }` where `start`/`end` are `datetime.timedelta`.
- Time helpers: `parse_time('HH:MM:SS,mmm')` and `format_time(timedelta)`.

Developer workflows (local usage)
- Process current dir: `python3 yt_srt_fixer.py`
- Process a file: `python3 yt_srt_fixer.py "path/to/file.srt"`
- Process a directory (recursive): `python3 yt_srt_fixer.py "/path/to/dir"`
- Override gap (default 80ms): `python3 yt_srt_fixer.py --gap 100`
- Output naming: writes alongside input as `<name>_fcp.srt`. Inputs already ending with `_fcp.srt` are auto-skipped.
- Sample fixtures for quick checks live at repo root (e.g., `*_fcp.srt` vs original `*.srt`).

Project conventions and patterns
- Pure Python standard library only; avoid adding external packages.
- Encoding is UTF-8 for both read and write.
- CLI is implemented with `argparse`; errors are printed per-file and processing continues for the rest.
- Recursive discovery uses `os.walk`; filtering is by extension `.srt` and suffix exclusion `_fcp.srt`.
- Keep the existing algorithmic contract: resolve conflicts by trimming the current cue’s end only; do not shift the next cue.

Edge cases to respect (intentional behavior)
- Minimal gap is enforced by shortening the current cue. If enforcing the gap would make duration non-positive, the code currently leaves it as-is (comment notes but does not alter next cues). Preserve this unless requirements change.
- `format_time` builds the SRT time string from a `timedelta`; ensure any new arithmetic maintains millisecond precision.

Extension guidance (when adding features)
- Follow the existing pipeline structure (parse → adjust → write) and data model.
- Prefer small, testable helpers co-located in `yt_srt_fixer.py` rather than new modules, unless the file becomes unwieldy.
- Keep I/O predictable: same-directory output, `_fcp.srt` suffix, skip already-fixed files.

Key files
- `yt_srt_fixer.py` — main CLI and all logic.
- `README.md` and `INSTRUCTIONS.md` — usage and context.
- Example SRTs in repo root for manual verification.

Helpful pointers for agents
- When modifying overlap logic, include concrete examples using the repo’s sample SRTs in PR descriptions.
- If you introduce configuration, prefer command-line flags over config files to keep the tool portable.
