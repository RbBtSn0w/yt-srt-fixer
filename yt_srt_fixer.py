
import re
import sys
import os
import argparse
from datetime import timedelta

def parse_time(time_str):
    """
    Parses an SRT timestamp string (HH:MM:SS,mmm) into a timedelta and total milliseconds.
    """
    hours, minutes, seconds = time_str.replace(',', '.').split(':')
    seconds, milliseconds = seconds.split('.')
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))

def format_time(td):
    """
    Formats a timedelta back to SRT timestamp string (HH:MM:SS,mmm).
    """
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def parse_srt(file_path):
    """
    Parses an SRT file into a list of subtitle items.
    Each item is a dict: {'index': int, 'start': timedelta, 'end': timedelta, 'content': str}
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by double newlines to get blocks, but be careful with potential empty blocks
    blocks = re.split(r'\n\s*\n', content.strip())
    subtitles = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            try:
                index = int(lines[0])
                time_line = lines[1]
                match = re.search(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', time_line)
                if match:
                    start_str, end_str = match.groups()
                    start = parse_time(start_str)
                    end = parse_time(end_str)
                    text = '\n'.join(lines[2:])
                    subtitles.append({
                        'index': index,
                        'start': start,
                        'end': end,
                        'content': text
                    })
            except ValueError:
                continue # Skip malformed blocks
    
    return subtitles

def fix_overlaps(subtitles, min_gap_ms=10):
    """
    Adjusts timestamps to ensure a minimum gap between subtitles.
    """
    min_gap = timedelta(milliseconds=min_gap_ms)
    
    # Sort just in case, though SRTs should be sorted
    subtitles.sort(key=lambda x: x['start'])

    for i in range(len(subtitles) - 1):
        current_sub = subtitles[i]
        next_sub = subtitles[i+1]
        
        # Check if current end overlaps or touches next start
        # limit: current.end must be <= next.start - min_gap
        max_allowed_end = next_sub['start'] - min_gap
        
        if current_sub['end'] > max_allowed_end:
            # We have an overlap or insufficient gap
            # Fix current end time
            # But also ensure we don't make the subtitle disappear or backward duration
            # If max_allowed_end < current_sub.start, we have a bigger problem (next sub starts before current ends?) 
            # Usually YouTube just has slight overlaps.
            
            if max_allowed_end > current_sub['start']:
                 current_sub['end'] = max_allowed_end
            else:
                 # If the gap constraint would make the duration <= 0, 
                 # we may need to push the next subtitle forward or shorten the current drastically.
                 # For simplicity, let's keep a minimal duration of 100ms if possible.
                 pass

    return subtitles

def write_srt(subtitles, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, sub in enumerate(subtitles):
            f.write(f"{i+1}\n")
            f.write(f"{format_time(sub['start'])} --> {format_time(sub['end'])}\n")
            f.write(f"{sub['content']}\n\n")

def main():
    parser = argparse.ArgumentParser(description="Fix overlapping timestamps in SRT files for Final Cut Pro.")
    parser.add_argument("input_file", nargs='?', help="Path to the input SRT file. If omitted, processes all .srt files in current folder.")
    parser.add_argument("--gap", type=int, default=80, help="Minimum gap between subtitles in milliseconds (default: 80ms for ~2 frames).")
    
    args = parser.parse_args()
    
    files_to_process = []
    if args.input_file:
        if os.path.isdir(args.input_file):
             # Process all .srt files in the specified directory and subdirectories
             base_dir = args.input_file
             for root, dirs, files in os.walk(base_dir):
                for f in files:
                    if f.endswith('.srt') and not f.endswith('_fcp.srt'):
                        files_to_process.append(os.path.join(root, f))
        else:
             files_to_process.append(args.input_file)
    else:
        # Process all .srt files in current directory that don't end with _fcp.srt
        for f in os.listdir('.'):
            if f.endswith('.srt') and not f.endswith('_fcp.srt'):
                files_to_process.append(f)

    if not files_to_process:
        print("No files found to process.")
        return

    for file_path in files_to_process:
        print(f"Processing {file_path}...")
        try:
            subs = parse_srt(file_path)
            if not subs:
                print(f"  Warning: No subtitles found or could not parse {file_path}")
                continue
                
            fixed_subs = fix_overlaps(subs, min_gap_ms=args.gap)
            
            output_path = os.path.splitext(file_path)[0] + "_fcp.srt"
            write_srt(fixed_subs, output_path)
            print(f"  Saved fixed file to {output_path}")
            
        except Exception as e:
            print(f"  Error processing {file_path}: {e}")

if __name__ == "__main__":
    main()
