#!/usr/bin/env python3
"""
AppMkv - MKV Blu-ray Compatibility Converter
Converts anime MKV files for Blu-ray player compatibility
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from scanner import scan_mkv_files
from analyzer import analyze_file
from converter import convert_video, convert_audio
from merger import merge_final
from gpu_detect import detect_gpu
from utils import setup_logging, validate_ffmpeg


def parse_args():
    parser = argparse.ArgumentParser(
        description="AppMkv - Convert MKV for Blu-ray compatibility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app_mkv.py "C:/Anime"        # Scan folder recursively
  python app_mkv.py "C:/Anime" --gpu=on   # Force GPU encoding
  python app_mkv.py "C:/Anime" --gpu=off  # Force CPU encoding
  python app_mkv.py "C:/Anime" --dry-run   # Show what would be converted
        """
    )
    parser.add_argument(
        "folder",
        help="Root folder containing MKV files to process"
    )
    parser.add_argument(
        "--gpu",
        choices=["auto", "on", "off"],
        default="auto",
        help="GPU encoding mode: auto (detect), on (force NVIDIA), off (CPU only)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze files but don't convert"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--ffmpeg-path",
        help="Custom path to FFmpeg binary"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    
    # Setup logging
    log_file = setup_logging(verbose=args.verbose)
    print(f"📁 AppMkv - MKV Blu-ray Converter")
    print(f"📂 Target: {args.folder}")
    print(f"📝 Log: {log_file}")
    print("-" * 50)
    
    # Validate FFmpeg
    ffmpeg_path = args.ffmpeg_path
    if not validate_ffmpeg(ffmpeg_path):
        print("❌ FFmpeg not found!")
        print("   Please ensure FFmpeg is in PATH or use --ffmpeg-path")
        sys.exit(1)
    
    print("✅ FFmpeg detected")
    
    # Detect GPU
    gpu_available = detect_gpu() if args.gpu in ["auto", "on"] else False
    use_gpu = gpu_available if args.gpu == "auto" else (args.gpu == "on")
    
    if use_gpu:
        print("🟢 GPU encoding enabled (NVIDIA NVENC)")
    else:
        print("🔵 CPU encoding enabled (libx264)")
    
    print("-" * 50)
    
    # Scan for MKV files
    print("🔍 Scanning for MKV files...")
    mkv_files = scan_mkv_files(args.folder)
    
    if not mkv_files:
        print("❌ No MKV files found!")
        sys.exit(0)
    
    print(f"📦 Found {len(mkv_files)} MKV file(s)")
    print("-" * 50)
    
    # Process each file
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for mkv_path in mkv_files:
        print(f"\n📄 Processing: {mkv_path.name}")
        
        try:
            # Analyze file
            analysis = analyze_file(mkv_path, ffmpeg_path)
            
            if analysis is None:
                print(f"   ⚠️  Skipping - analysis failed")
                skip_count += 1
                continue
            
            # Decide what to convert
            needs_video = analysis["needs_video_conversion"]
            needs_audio = analysis["needs_audio_conversion"]
            
            print(f"   🔍 Video: {'CONVERT' if needs_video else 'OK'} ({analysis['video']['codec']})")
            print(f"   🔍 Audio: {'CONVERT' if needs_audio else 'OK'} ({analysis['audio']['codecs']})")
            
            if args.dry_run:
                print(f"   📝 DRY RUN - no conversion performed")
                continue
            
            # Convert if needed
            converted_video = None
            converted_audios = {}
            
            if needs_video:
                print(f"   ⚙️  Converting video...")
                converted_video = convert_video(
                    mkv_path,
                    use_gpu=use_gpu,
                    ffmpeg_path=ffmpeg_path
                )
                if converted_video:
                    print(f"   ✅ Video converted: {converted_video.name}")
            
            for audio_idx in needs_audio:
                print(f"   ⚙️  Converting audio track {audio_idx}...")
                converted_audios[audio_idx] = convert_audio(
                    mkv_path,
                    audio_idx,
                    ffmpeg_path=ffmpeg_path
                )
                if converted_audios[audio_idx]:
                    print(f"   ✅ Audio {audio_idx} converted")
            
            # Merge final file
            if needs_video or needs_audio:
                print(f"   🔀 Merging final file...")
                final_path = merge_final(
                    mkv_path,
                    converted_video,
                    converted_audios,
                    ffmpeg_path=ffmpeg_path
                )
                
                if final_path and final_path.exists():
                    print(f"   ✅ Final: {final_path.name}")
                    success_count += 1
                else:
                    print(f"   ❌ Merge failed")
                    error_count += 1
            else:
                print(f"   ✅ No conversion needed - already compatible")
                skip_count += 1
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            error_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print(f"   ✅ Success: {success_count}")
    print(f"   ⏭️  Skipped: {skip_count}")
    print(f"   ❌ Errors:  {error_count}")
    print("=" * 50)
    
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
