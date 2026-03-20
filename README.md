# AppMkv - Convertidor MKV para Blu-ray

Convierte archivos MKV (anime) para compatibilidad con reproductores Blu-ray.

## Características

- **Video**: Convierte a H.264 High Profile Level 4.1
- **Audio**: Convierte a AAC 192kbps (si no es compatible)
- **Resolución**: Mantiene original si ≤1920x1080, escala a 1080p si es mayor
- **Preserva**: Subtítulos, capítulos, fuentes (fonts), metadata
- **Soporte**: CPU (libx264) y GPU NVIDIA (NVENC)

## Requisitos

- Windows 10/11
- FFmpeg y FFprobe (incluidos o en PATH)

## Instalación

### 1. Descarga el ejecutable

Coloca en una carpeta:
- `app_mkv.exe` (este ejecutable)
- `ffmpeg.exe` (descarga de https://ffmpeg.org/download.html)
- `ffprobe.exe` (viene con FFmpeg)

### 2. (Opcional) Agregar al PATH

Si no quieres tener ffmpeg en la misma carpeta, agrégalo al PATH de Windows.

## Uso

```bash
# Procesar carpeta completa
app_mkv.exe "C:\ruta\a\anime"

# Modo análisis (solo muestra qué convertiría)
app_mkv.exe "C:\ruta\a\anime" --dry-run

# Forzar GPU (NVENC)
app_mkv.exe "C:\ruta\a\anime" --gpu=on

# Forzar CPU
app_mkv.exe "C:\ruta\a\anime" --gpu=off

# Ruta personalizada a FFmpeg
app_mkv.exe "C:\ruta\a\anime" --ffmpeg-path "C:\ffmpeg\bin\ffmpeg.exe"

# Salida detallada
app_mkv.exe "C:\ruta\a\anime" --verbose
```

## Parámetros

| Parámetro | Descripción |
|-----------|-------------|
| `folder` | Carpeta raíz con archivos MKV |
| `--gpu=auto` | Auto-detectar GPU (default) |
| `--gpu=on` | Forzar NVIDIA NVENC |
| `--gpu=off` | Forzar CPU (libx264) |
| `--dry-run` | Solo analizar, no convertir |
| `--verbose` | Logs detallados |
| `--ffmpeg-path` | Ruta a ffmpeg.exe |

## Formato de Salida

Los archivos convertidos se crean junto al original con sufijo `_Final.mkv`:

```
Anime/
├── NombreEpisodio.mkv        (original)
├── NombreEpisodio_Final.mkv  (convertido)
```

## Especificaciones de Conversión

### Video
- Codec: H.264 (libx264 o h264_nvenc)
- Profile: High @ Level 4.1
- Bit depth: 8-bit
- Resolución: Original si ≤1080p, 1080p si >1080p
- CRF: 20 (CPU) / CQ 18 (GPU)

### Audio
- Codec: AAC 192kbps (si original no es AAC/AC3/DTS)
-/sample rate: 48kHz

### Preservado
- Todos los subtítulos
- Capítulos
- Fuentes (attachments)
- Metadata

## Solución de Problemas

### "FFmpeg no encontrado"
Coloca `ffmpeg.exe` y `ffprobe.exe` en la misma carpeta que `app_mkv.exe`

### "Error al convertir"
Revisa los logs en la carpeta `logs/`

### Conversión lenta
Usa `--gpu=on` si tienes GPU NVIDIA

## Descargar FFmpeg

Windows: https://www.gyan.dev/ffmpeg/builds/

## Licencia

MIT
