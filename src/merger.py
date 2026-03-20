#!/usr/bin/env python3
"""
Merger module - Merge converted tracks with original file
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Optional, List


def get_ffmpeg_path(ffmpeg_path: Optional[str] = None) -> str:
    """Get ffmpeg binary path"""
    if ffmpeg_path:
        return ffmpeg_path
    
    for path in ["ffmpeg", "./ffmpeg", "./ffmpeg.exe"]:
        try:
            result = subprocess.run([path, "-version"], capture_output=True, timeout=5)
            if result.returncode == 0:
                return path
        except:
            continue
    
    return "ffmpeg"


def get_ffprobe_path(ffmpeg_path: Optional[str] = None) -> str:
    """Get ffprobe binary path"""
    if ffmpeg_path:
        base = Path(ffmpeg_path).parent
        ffprobe = base / "ffprobe"
        if ffprobe.exists():
            return str(ffprobe)
    
    for path in ["ffprobe", "./ffprobe", "./ffprobe.exe"]:
        try:
            result = subprocess.run([path, "-version"], capture_output=True, timeout=5)
            if result.returncode == 0:
                return path
        except:
            continue
    
    return "ffprobe"


def get_audio_streams(file_path: Path, ffprobe_path: str = "ffprobe") -> List[dict]:
    """Get list of audio streams with their indices"""
    try:
        result = subprocess.run(
            [ffprobe_path, "-v", "quiet", "-print_format", "json", "-show_streams", str(file_path)],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
    except:
        pass
    return []


def merge_final(
    original_path: Path,
    converted_video: Optional[Path],
    converted_audios: Dict[int, Path],
    ffmpeg_path: Optional[str] = None
) -> Optional[Path]:
    """
    Merge converted tracks with original file to create Final.mkv
    """
    ffmpeg = get_ffmpeg_path(ffmpeg_path)
    output_path = original_path.parent / f"{original_path.stem}_Final.mkv"
    
    # Get original audio streams info
    ffprobe = get_ffprobe_path(ffmpeg_path)
    original_audios = get_audio_streams(original_path, ffprobe)
    total_audio = len(original_audios)
    
    # Build ffmpeg command
    cmd = [ffmpeg, "-y"]
    
    # Input 0: original file
    cmd.extend(["-i", str(original_path)])
    
    # Track input indices
    next_input = 1
    
    # Add converted video
    if converted_video:
        cmd.extend(["-i", str(converted_video)])
        next_input += 1
    
    # Add converted audios (sorted by index)
    sorted_audio_indices = sorted(converted_audios.keys())
    audio_input_map = {}  # {original_idx: input_num}
    for orig_idx in sorted_audio_indices:
        cmd.extend(["-i", str(converted_audios[orig_idx])])
        audio_input_map[orig_idx] = next_input
        next_input += 1
    
    # Video: use converted if exists
    if converted_video:
        cmd.extend(["-map", "1:v", "-c:v", "copy"])
    else:
        cmd.extend(["-map", "0:v:0", "-c:v", "copy"])
    
    # Audio mapping
    if total_audio > 0:
        for i in range(total_audio):
            if i in audio_input_map:
                # Use converted audio
                cmd.extend(["-map", f"{audio_input_map[i]}:a:0", "-c:a", "copy"])
            else:
                # Copy original audio
                cmd.extend(["-map", f"0:a:{i}", "-c:a", "copy"])
    else:
        cmd.extend(["-an"])
    
    # Subtitles: copy all
    cmd.extend(["-map", "0:s?", "-c:s", "copy"])
    
    # Chapters and metadata
    cmd.extend(["-map_chapters", "0", "-map_metadata", "0"])
    
    # Attachments
    cmd.extend(["-copy_unknown"])
    
    # Output
    cmd.append(str(output_path))
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode != 0:
            print(f"      Merge error: {result.stderr[-800:]}")
            return None
        
        if output_path.exists():
            # Cleanup
            if converted_video and converted_video.exists():
                converted_video.unlink()
            for audio in converted_audios.values():
                if audio and audio.exists():
                    audio.unlink()
            return output_path
        
        return None
        
    except Exception as e:
        print(f"      Merge error: {e}")
        return None
