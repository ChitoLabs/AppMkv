#!/usr/bin/env python3
"""
Converter module - Convert video and audio tracks
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Optional


def get_ffmpeg_path(ffmpeg_path: Optional[str] = None) -> str:
    """Get ffmpeg binary path"""
    if ffmpeg_path:
        return ffmpeg_path
    
    # Check common locations
    possible_paths = [
        "ffmpeg",
        "./ffmpeg",
        "./ffmpeg.exe",
        "C:\\ffmpeg\\bin\\ffmpeg.exe",
        "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
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
    
    return "ffmpeg"


def convert_video(
    input_path: Path,
    use_gpu: bool = False,
    ffmpeg_path: Optional[str] = None,
    temp_dir: Optional[Path] = None
) -> Optional[Path]:
    """
    Convert video track to H.264 High Profile Level 4.1
    
    Args:
        input_path: Input MKV file
        use_gpu: Use NVIDIA NVENC instead of CPU
        ffmpeg_path: Custom path to ffmpeg
        temp_dir: Directory for temp files
        
    Returns:
        Path to converted video file, or None on failure
    """
    ffmpeg = get_ffmpeg_path(ffmpeg_path)
    
    # Create temp directory if not provided
    if temp_dir is None:
        temp_dir = input_path.parent
    
    output_path = temp_dir / f"{input_path.stem}_video_converted.mp4"
    
    # Build command
    # Scale only if resolution > 1920x1080, otherwise keep original
    scale_filter = "scale=min(1920\\,iw):min(1080\\,ih):force_original_aspect_ratio=decrease"
    
    if use_gpu:
        # GPU encoding with NVENC
        cmd = [
            ffmpeg,
            "-y",  # Overwrite output
            "-i", str(input_path),
            "-map", "0:v:0",  # First video stream
            "-c:v", "h264_nvenc",
            "-preset", "p4",  # Balanced speed/quality
            "-cq", "18",      # Quality (lower = better)
            "-profile:v", "high",
            "-level", "4.1",
            "-pix_fmt", "yuv420p",
            "-vf", scale_filter,
            str(output_path)
        ]
    else:
        # CPU encoding with libx264 - optimized for speed
        cmd = [
            ffmpeg,
            "-y",
            "-i", str(input_path),
            "-map", "0:v:0",
            "-c:v", "libx264",
            "-preset", "superfast",  # Faster encoding
            "-crf", "20",           # Slightly lower quality for speed
            "-profile:v", "high",
            "-level", "4.1",
            "-pix_fmt", "yuv420p",
            "-vf", scale_filter,
            "-threads", "0",        # Use all CPU threads
            str(output_path)
        ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour max
        )
        
        if result.returncode != 0:
            print(f"      Error: {result.stderr}")
            return None
        
        if output_path.exists():
            return output_path
        
        return None
        
    except subprocess.TimeoutExpired:
        print("      Error: Conversion timeout")
        return None
    except Exception as e:
        print(f"      Error: {e}")
        return None


def convert_audio(
    input_path: Path,
    audio_index: int,
    ffmpeg_path: Optional[str] = None,
    temp_dir: Optional[Path] = None
) -> Optional[Path]:
    """
    Convert audio track to AAC 192kbps
    
    Args:
        input_path: Input MKV file
        audio_index: Index of audio stream to convert
        ffmpeg_path: Custom path to ffmpeg
        temp_dir: Directory for temp files
        
    Returns:
        Path to converted audio file, or None on failure
    """
    ffmpeg = get_ffmpeg_path(ffmpeg_path)
    
    if temp_dir is None:
        temp_dir = input_path.parent
    
    output_path = temp_dir / f"{input_path.stem}_audio_{audio_index}.aac"
    
    cmd = [
        ffmpeg,
        "-y",
        "-i", str(input_path),
        "-map", f"0:a:{audio_index}",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",  # 48kHz sample rate
        str(output_path)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 min max per audio
        )
        
        if result.returncode != 0:
            print(f"      Error: {result.stderr}")
            return None
        
        if output_path.exists():
            return output_path
        
        return None
        
    except subprocess.TimeoutExpired:
        print("      Error: Audio conversion timeout")
        return None
    except Exception as e:
        print(f"      Error: {e}")
        return None
