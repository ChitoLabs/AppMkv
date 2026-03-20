#!/usr/bin/env python3
"""
GPU detection module - Detect NVIDIA GPU for NVENC
"""

import subprocess
import platform
from typing import Optional


def detect_gpu() -> bool:
    """
    Detect if NVIDIA GPU with NVENC support is available
    
    Returns:
        True if GPU with NVENC is available, False otherwise
    """
    system = platform.system()
    
    if system == "Windows":
        return detect_nvidia_windows()
    elif system == "Linux":
        return detect_nvidia_linux()
    elif system == "Darwin":
        # macOS doesn't have NVENC (it's NVIDIA-only)
        return False
    else:
        return False


def detect_nvidia_windows() -> bool:
    """Detect NVIDIA GPU on Windows"""
    try:
        # Try nvidia-smi
        result = subprocess.run(
            ["nvidia-smi"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Check if NVENC is available by looking at capabilities
            # nvidia-smi shows GPU info, we can parse it
            return True
        
        return False
        
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def detect_nvidia_linux() -> bool:
    """Detect NVIDIA GPU on Linux"""
    try:
        result = subprocess.run(
            ["nvidia-smi"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Also verify ffmpeg supports nvenc
            check = subprocess.run(
                ["ffmpeg", "-hide_banner", "-encoders"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if "h264_nvenc" in check.stdout:
                return True
        
        return False
        
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_gpu_info() -> Optional[dict]:
    """
    Get detailed GPU information
    
    Returns:
        Dict with GPU info or None
    """
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            if lines:
                parts = lines[0].split(",")
                return {
                    "name": parts[0].strip() if len(parts) > 0 else "Unknown",
                    "memory": parts[1].strip() if len(parts) > 1 else "Unknown",
                    "driver": parts[2].strip() if len(parts) > 2 else "Unknown"
                }
        
        return None
        
    except Exception:
        return None
