#!/usr/bin/env python3
"""
Scanner module - Recursively find MKV files
"""

import os
from pathlib import Path
from typing import List


def scan_mkv_files(root_folder: str) -> List[Path]:
    """
    Recursively scan for MKV files, excluding *_Final.mkv
    
    Args:
        root_folder: Root directory to scan
        
    Returns:
        List of Path objects for MKV files
    """
    root_path = Path(root_folder)
    
    if not root_path.exists():
        raise FileNotFoundError(f"Folder not found: {root_folder}")
    
    if not root_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {root_folder}")
    
    mkv_files = []
    
    for item in root_path.rglob("*.mkv"):
        # Skip *_Final.mkv files
        if item.name.endswith("_Final.mkv"):
            continue
        
        # Skip if it's a temporary/conversion file
        if "_temp" in item.name or "_converted" in item.name:
            continue
            
        mkv_files.append(item)
    
    # Sort by name for consistent processing order
    mkv_files.sort(key=lambda x: x.name)
    
    return mkv_files
