<p align="center">
  <pre>
    ___                   __  __    _  __
   /   |  ____ ___  ___  / /_/ /_  | |/ /
  / /| | / __ `__ \/ _ \/ __/ __/  |   / 
 / ___ |/ / / / / /  __/ /_/ /_   /   |  
/_/  |_/_/ /_/ /_/\___/\__/\__/  /_/|_|  
                                          
  Blu-ray Compatibility Converter for MKV Anime Files
  </pre>
</p>

---

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6?logo=windows&logoColor=white)]()
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-97D700?logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
[![GitHub Stars](https://img.shields.io/github/stars/ChitoLabs/AppMkv?style=social)](https://github.com/ChitoLabs/AppMkv/stargazers)

---

## About

**AppMkv** is a command-line tool that converts MKV anime files for full compatibility with Blu-ray players. It analyzes each file, detects which streams need conversion (video and audio), and produces a clean `_Final.mkv` output — preserving subtitles, chapters, fonts, and metadata.

Built for anime collectors who want their files to "just work" on any Blu-ray player without manual FFmpeg commands.

---

## Features

- 🎬 **Smart Video Conversion** — H.264 High Profile Level 4.1 (Blu-ray spec)
- 🔊 **Audio Normalization** — Converts non-compatible audio to AAC 192kbps / 48kHz
- ⚡ **GPU Acceleration** — Auto-detects NVIDIA NVENC for fast encoding; falls back to CPU (libx264)
- 📝 **Preserves All Subtitles** — Every subtitle track (ASS, SRT, PGS, etc.) is carried over
- 🔖 **Keeps Chapters** — Chapter markers remain intact
- 🎨 **Retains Fonts & Attachments** — Custom fonts for styled subs are preserved
- 🔍 **Dry-Run Mode** — Preview what would be converted without touching any files
- 📊 **Batch Processing** — Recursively scans folders and processes all MKV files
- 🧠 **Smart Analysis** — Skips files that are already Blu-ray compatible

---

## Installation

### Prerequisites

| Requirement | Details |
|-------------|---------|
| **OS** | Windows 10 / 11 |
| **FFmpeg** | [Download from gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (static build recommended) |
| **Python** | 3.8+ (only if running from source) |

### Option A: Standalone Executable

1. Download the latest release from [Releases](https://github.com/ChitoLabs/AppMkv/releases)
2. Place all files in the same folder:

```
AppMkv/
├── app_mkv.exe          # Main executable
├── ffmpeg.exe           # FFmpeg binary
└── ffprobe.exe          # FFprobe binary (included with FFmpeg)
```

3. Run from terminal — done.

### Option B: Run from Source

```bash
# Clone the repository
git clone https://github.com/ChitoLabs/AppMkv.git
cd AppMkv

# No external Python dependencies required (stdlib only)
# Just make sure FFmpeg is installed and in PATH

python app_mkv.py "C:\path\to\anime"
```

> **Tip:** If `ffmpeg.exe` and `ffprobe.exe` are in your system PATH, they don't need to be in the same folder.

---

## Usage

### Basic — Convert a Folder

```bash
app_mkv.exe "D:\Anime\Attack on Titan"
```

Recursively scans all MKV files, analyzes each one, and converts only what needs conversion. Output files are created alongside the originals with a `_Final.mkv` suffix.

### Preview Mode (Dry Run)

```bash
app_mkv.exe "D:\Anime\Attack on Titan" --dry-run
```

Shows what **would** be converted without actually writing any files. Use this to plan before committing to a batch conversion.

### Force GPU Encoding

```bash
app_mkv.exe "D:\Anime\Attack on Titan" --gpu=on
```

Forces NVIDIA NVENC hardware encoding. Faster, but requires a compatible NVIDIA GPU.

### Force CPU Encoding

```bash
app_mkv.exe "D:\Anime\Attack on Titan" --gpu=off
```

Forces libx264 software encoding. Slower but works on any machine and produces slightly better quality per bitrate.

### Custom FFmpeg Path

```bash
app_mkv.exe "D:\Anime\Attack on Titan" --ffmpeg-path "C:\Tools\ffmpeg\bin\ffmpeg.exe"
```

### Verbose Logging

```bash
app_mkv.exe "D:\Anime\Attack on Titan" --verbose
```

Enables detailed output for debugging. Logs are also saved to the `logs/` folder.

---

## Command Reference

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `folder` | positional | — | Root folder containing MKV files (scanned recursively) |
| `--gpu` | choice | `auto` | GPU encoding mode: `auto` (detect), `on` (force NVENC), `off` (CPU only) |
| `--dry-run` | flag | off | Analyze files but do not convert |
| `--verbose` | flag | off | Enable detailed logging output |
| `--ffmpeg-path` | string | auto | Custom path to the FFmpeg binary |

---

## Output Structure

Converted files are placed next to the originals with a `_Final` suffix:

```
Anime Folder/
├── Episode01.mkv                 ← Original
├── Episode01_Final.mkv           ← Converted (Blu-ray compatible)
├── Episode02.mkv                 ← Original
├── Episode02_Final.mkv           ← Converted (Blu-ray compatible)
└── logs/
    └── app_mkv_20260320.log      ← Conversion log
```

> Files that are already Blu-ray compatible are **skipped** — no `_Final` copy is created.

---

## Technical Specifications

### Video

| Property | Value |
|----------|-------|
| Codec | H.264 (libx264 for CPU, h264_nvenc for GPU) |
| Profile | High @ Level 4.1 |
| Bit Depth | 8-bit |
| Resolution | Original (if ≤1920×1080) or downscaled to 1080p |
| Quality (CPU) | CRF 20 |
| Quality (GPU) | CQ 18 |

### Audio

| Property | Value |
|----------|-------|
| Codec | AAC (converted only if original is not AAC / AC3 / DTS) |
| Bitrate | 192 kbps |
| Sample Rate | 48 kHz |
| Tracks | All original audio tracks are preserved |

### Preserved Elements

| Element | Behavior |
|---------|----------|
| Subtitles | All tracks kept (ASS, SRT, PGS, etc.) |
| Chapters | Chapter markers preserved |
| Fonts / Attachments | Custom subtitle fonts carried over |
| Metadata | Title, language tags, and other metadata retained |

---

## Troubleshooting

### "FFmpeg not found"

Place `ffmpeg.exe` and `ffprobe.exe` in the same directory as `app_mkv.exe`, or add them to your system `PATH`.

Download FFmpeg: [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/)

### Conversion is very slow

If you have an NVIDIA GPU, use `--gpu=on` to enable hardware-accelerated encoding. This can be 5–10× faster than CPU encoding.

### Output file has no subtitles

This is usually because the subtitle format was not recognized. Open an issue with the source file's media info (`ffprobe` output) so it can be investigated.

### "Analysis failed" for a file

Check the detailed log in the `logs/` folder. Common causes:
- Corrupted MKV container
- Unusual codec or stream configuration
- File locked by another process

### GPU not detected

- Ensure you have an **NVIDIA GPU** with updated drivers
- NVENC requires a GTX 600 series or newer
- Try running with `--gpu=on` to force GPU mode and see the error

---

## Project Structure

```
AppMkv/
├── app_mkv.py            # CLI entry point
├── src/
│   ├── analyzer.py       # FFprobe-based file analysis
│   ├── converter.py      # Video & audio conversion logic
│   ├── scanner.py        # Recursive MKV file discovery
│   ├── merger.py         # Final MKV muxing
│   ├── gpu_detect.py     # NVIDIA GPU detection
│   └── utils.py          # Logging & FFmpeg validation
├── logs/                 # Conversion logs (gitignored)
├── exe/                  # Build output (gitignored)
├── requirements.txt      # Build dependencies
└── README.md
```

---

## Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and test with real MKV files
4. Run with `--dry-run` and `--verbose` to verify behavior
5. Submit a pull request

Please open an issue first for major changes to discuss the approach.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <sub>Built with 🍵 by <a href="https://github.com/ChitoLabs">ChitoLabs</a></sub>
</p>
