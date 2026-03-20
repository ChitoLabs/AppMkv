#!/usr/bin/env python3
"""
Utils module - Common utilities
"""

import subprocess
import logging
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple


def get_app_dir() -> Path:
    """Get the directory where the app/exe is located"""
    # If running as PyInstaller exe, get the bundled app directory
    if getattr(sys, 'frozen', False):
        # Running as exe
        app_dir = Path(sys.executable).parent
    else:
        # Running as script
        app_dir = Path(__file__).parent.parent
    
    return app_dir


def find_ffmpeg() -> Tuple[Optional[str], str]:
    """
    Find FFmpeg executable - check app directory first, then PATH
    
    Returns:
        Tuple of (ffmpeg_path, source: "app" or "system" or None)
    """
    app_dir = get_app_dir()
    
    # Check in app directory first
    # Windows: ffmpeg.exe, Linux/Mac: ffmpeg
    exe_suffix = ".exe" if sys.platform == "win32" else ""
    
    local_ffmpeg = app_dir / f"ffmpeg{exe_suffix}"
    local_ffprobe = app_dir / f"ffprobe{exe_suffix}"
    
    if local_ffmpeg.exists() and local_ffprobe.exists():
        return (str(local_ffmpeg), "app")
    
    # Also check just ffmpeg (might work without ffprobe separately)
    if local_ffmpeg.exists():
        return (str(local_ffmpeg), "app")
    
    # Check in PATH
    ffmpeg_cmd = "ffmpeg" + exe_suffix
    
    try:
        result = subprocess.run(
            [ffmpeg_cmd, "-version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return (ffmpeg_cmd, "system")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    return (None, None)


def validate_ffmpeg(ffmpeg_path: Optional[str] = None) -> bool:
    """
    Validate that FFmpeg is available
    
    Args:
        ffmpeg_path: Custom path to ffmpeg
        
    Returns:
        True if FFmpeg is available, False otherwise
    """
    # If custom path provided, use it
    if ffmpeg_path:
        ffmpeg = ffmpeg_path
    else:
        # Auto-detect
        ffmpeg, source = find_ffmpeg()
        if ffmpeg is None:
            print("\n" + "="*50)
            print("❌ FFmpeg no encontrado!")
            print("="*50)
            print("Por favor, coloca ffmpeg.exe y ffprobe.exe")
            print("en la misma carpeta que app_mkv.exe")
            print("")
            print("O agrega FFmpeg a tu PATH del sistema.")
            print("")
            print("Descarga FFmpeg: https://ffmpeg.org/download.html")
            print("="*50 + "\n")
            return False
        
        # Check if we found it in app folder
        if source == "app":
            print(f"✅ FFmpeg encontrado en carpeta de la app")
        else:
            print(f"✅ FFmpeg encontrado en sistema")
    
    try:
        result = subprocess.run(
            [ffmpeg, "-version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split("\n")[0]
            logging.info(f"FFmpeg: {version_line}")
            return True
        
        return False
        
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("\n" + "="*50)
        print("❌ FFmpeg encontrado pero no se puede ejecutar!")
        print("="*50 + "\n")
        return False


def setup_logging(verbose: bool = False) -> str:
    """
    Setup logging configuration
    
    Args:
        verbose: Enable verbose debug logging
        
    Returns:
        Path to log file
    """
    # Create logs directory
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"appmkv_{timestamp}.log"
    
    # Configure logging
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return str(log_file)


def validate_input_path(path: str) -> Path:
    """
    Validate and return input path
    
    Args:
        path: Input path string
        
    Returns:
        Path object
        
    Raises:
        FileNotFoundError: If path doesn't exist
        NotADirectoryError: If path isn't a directory
    """
    p = Path(path)
    
    if not p.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    
    if not p.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")
    
    return p


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human readable string
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "1h 23m 45s")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def format_size(bytes: int) -> str:
    """
    Format file size in bytes to human readable string
    
    Args:
        bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 GB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    
    return f"{bytes:.1f} PB"


def get_file_info(path: Path) -> dict:
    """
    Get basic file information
    
    Args:
        path: File path
        
    Returns:
        Dict with file info
    """
    stat = path.stat()
    
    return {
        "name": path.name,
        "size": stat.st_size,
        "size_formatted": format_size(stat.st_size),
        "modified": datetime.fromtimestamp(stat.st_mtime)
    }
