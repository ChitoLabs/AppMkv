#!/usr/bin/env python3
"""
Analyzer module - Analyze MKV files with ffprobe
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List


def get_ffprobe_path(ffmpeg_path: Optional[str] = None) -> str:
    """Get ffprobe binary path"""
    if ffmpeg_path:
        # If custom ffmpeg path provided, derive ffprobe
        base = Path(ffmpeg_path).parent
        ffprobe = base / "ffprobe"
        if ffprobe.exists():
            return str(ffprobe)
    
    # Check common locations
    possible_paths = [
        "ffprobe",
        "./ffprobe",
        "./ffprobe.exe",
        "C:\\ffmpeg\\bin\\ffprobe.exe",
        "C:\\Program Files\\ffmpeg\\bin\\ffprobe.exe",
    ]
    
    for path in possible_paths:
        try:
            result = subprocess.run(
                [path, "-version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return path
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    # Default to ffprobe in PATH
    return "ffprobe"


def run_ffprobe(file_path: Path, ffmpeg_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Run ffprobe on a file and return JSON output
    """
    ffprobe_path = get_ffprobe_path(ffmpeg_path)
    
    cmd = [
        ffprobe_path,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(file_path)
    ]
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")
    
    return json.loads(result.stdout)


def analyze_file(mkv_path: Path, ffmpeg_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Analyze an MKV file and determine what needs conversion
    
    Returns:
        Dict with analysis results:
        - video: {codec, profile, bit_depth, width, height, needs_conversion}
        - audio: {codecs, channels, needs_audio_conversion}
        - needs_video_conversion: bool
        - needs_audio_conversion: list of indices needing conversion
    """
    try:
        probe_data = run_ffprobe(mkv_path, ffmpeg_path)
    except Exception as e:
        print(f"   ⚠️  ffprobe error: {e}")
        return None
    
    # Find video stream
    video_stream = None
    audio_streams = []
    
    for stream in probe_data.get("streams", []):
        codec_type = stream.get("codec_type")
        
        if codec_type == "video":
            if video_stream is None:  # Take first video stream
                video_stream = stream
        
        elif codec_type == "audio":
            audio_streams.append(stream)
    
    if not video_stream:
        print("   ⚠️  No video stream found!")
        return None
    
    # Analyze video
    video_codec = video_stream.get("codec_name", "").lower()
    profile = video_stream.get("profile", "").lower()
    bit_depth = int(video_stream.get("bits_per_raw_sample", video_stream.get("bits_per_sample", 8)))
    width = video_stream.get("width", 0)
    height = video_stream.get("height", 0)
    
    # Determine if video needs conversion
    # Rules from spec:
    # - Must be h264
    # - Must be High profile
    # - Must be Level 4.1
    # - Must be 8 bit
    # - Must be <= 1080p
    
    level = video_stream.get("level", 0)
    
    needs_video = False
    
    # Check codec
    if video_codec != "h264":
        needs_video = True
    
    # Check profile
    if "high" not in profile:
        needs_video = True
    
    # Check level (4.1 = 41)
    if level != 41:
        needs_video = True
    
    # Check bit depth
    if bit_depth != 8:
        needs_video = True
    
    # Check resolution (must be <= 1080p)
    if height > 1080:
        needs_video = True
    
    # Analyze audio
    # Compatible codecs: aac, ac3, dts
    compatible_audio = {"aac", "ac3", "dts"}
    
    needs_audio_conversion = []
    audio_codecs = []
    
    for i, audio in enumerate(audio_streams):
        codec_name = audio.get("codec_name", "").lower()
        audio_codecs.append(codec_name)
        
        if codec_name not in compatible_audio:
            needs_audio_conversion.append(i)
    
    return {
        "video": {
            "codec": video_codec,
            "profile": profile,
            "bit_depth": bit_depth,
            "width": width,
            "height": height,
            "level": level,
            "needs_conversion": needs_video
        },
        "audio": {
            "codecs": audio_codecs,
            "channels": [a.get("channels", 0) for a in audio_streams],
            "needs_conversion": needs_audio_conversion
        },
        "needs_video_conversion": needs_video,
        "needs_audio_conversion": needs_audio_conversion,
        "format": probe_data.get("format", {})
    }
