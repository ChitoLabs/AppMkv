<p align="center">
  <pre>
    ___                   __  __    _  __
   /   |  ____ ___  ___  / /_/ /_  | |/ /
  / /| | / __ `__ \/ _ \/ __/ __/  |   / 
 / ___ |/ / / / / /  __/ /_/ /_   /   |  
/_/  |_/_/ /_/ /_/\___/\__/\__/  /_/|_|  
                                          
  Convertidor de compatibilidad Blu-ray para archivos MKV de anime
  </pre>
</p>

---

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6?logo=windows&logoColor=white)]()
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-97D700?logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
[![GitHub Stars](https://img.shields.io/github/stars/ChitoLabs/AppMkv?style=social)](https://github.com/ChitoLabs/AppMkv/stargazers)

---

## Acerca de

**AppMkv** es una herramienta de línea de comandos que convierte archivos MKV de anime para lograr compatibilidad total con reproductores Blu-ray. Analiza cada archivo, detecta qué flujos necesitan conversión (video y audio) y genera un archivo de salida `_Final.mkv` limpio — conservando subtítulos, capítulos, fuentes y metadatos.

Diseñada para coleccionistas de anime que quieren que sus archivos "simplemente funcionen" en cualquier reproductor Blu-ray sin necesidad de comandos FFmpeg manuales.

---

## Características

- 🎬 **Conversión de video inteligente** — H.264 High Profile Level 4.1 (especificación Blu-ray)
- 🔊 **Normalización de audio** — Convierte audio no compatible a AAC 192 kbps / 48 kHz
- ⚡ **Aceleración por GPU** — Detecta automáticamente NVIDIA NVENC para codificación rápida; usa CPU como respaldo (libx264)
- 📝 **Conserva todos los subtítulos** — Se mantienen todas las pistas de subtítulos (ASS, SRT, PGS, etc.)
- 🔖 **Mantiene los capítulos** — Los marcadores de capítulos permanecen intactos
- 🎨 **Conserva fuentes y archivos adjuntos** — Las fuentes personalizadas para subtítulos con estilos se preservan
- 🔍 **Modo de prueba (dry-run)** — Previsualiza qué se convertiría sin modificar ningún archivo
- 📊 **Procesamiento por lotes** — Escanea carpetas recursivamente y procesa todos los archivos MKV
- 🧠 **Análisis inteligente** — Omite archivos que ya son compatibles con Blu-ray

---

## Instalación

### Requisitos previos

| Requisito | Detalles |
|-----------|----------|
| **SO** | Windows 10 / 11 |
| **FFmpeg** | [Descargar desde gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (se recomienda la versión estática) |
| **Python** | 3.8+ (solo si se ejecuta desde el código fuente) |

### Opción A: Ejecutable independiente

1. Descarga la última versión desde [Releases](https://github.com/ChitoLabs/AppMkv/releases)
2. Coloca todos los archivos en la misma carpeta:

```
AppMkv/
├── app_mkv.exe          # Ejecutable principal
├── ffmpeg.exe           # Binario de FFmpeg
└── ffprobe.exe          # Binario de FFprobe (incluido con FFmpeg)
```

3. Ejecuta desde la terminal — listo.

### Opción B: Ejecutar desde el código fuente

```bash
# Clonar el repositorio
git clone https://github.com/ChitoLabs/AppMkv.git
cd AppMkv

# No se requieren dependencias externas de Python (solo stdlib)
# Solo asegúrate de tener FFmpeg instalado y en el PATH

python app_mkv.py "C:\ruta\al\anime"
```

> **Consejo:** Si `ffmpeg.exe` y `ffprobe.exe` están en el PATH del sistema, no necesitan estar en la misma carpeta.

---

## Uso

### Básico — Convertir una carpeta

```bash
app_mkv.exe "D:\Anime\Attack on Titan"
```

Escanea recursivamente todos los archivos MKV, analiza cada uno y convierte solo lo necesario. Los archivos de salida se crean junto a los originales con el sufijo `_Final.mkv`.

### Modo de previsualización (dry-run)

```bash
app_mkv.exe "D:\Anime\Attack on Titan" --dry-run
```

Muestra qué **se convertiría** sin escribir ningún archivo realmente. Úsalo para planificar antes de comprometerte con una conversión por lotes.

### Forzar codificación por GPU

```bash
app_mkv.exe "D:\Anime\Attack on Titan" --gpu=on"
```

Fuerza la codificación por hardware NVIDIA NVENC. Más rápido, pero requiere una GPU NVIDIA compatible.

### Forzar codificación por CPU

```bash
app_mkv.exe "D:\Anime\Attack on Titan" --gpu=off"
```

Fuerza la codificación por software libx264. Más lento, pero funciona en cualquier equipo y produce una calidad ligeramente superior por bitrate.

### Ruta personalizada de FFmpeg

```bash
app_mkv.exe "D:\Anime\Attack on Titan" --ffmpeg-path "C:\Tools\ffmpeg\bin\ffmpeg.exe"
```

### Registro detallado

```bash
app_mkv.exe "D:\Anime\Attack on Titan" --verbose"
```

Activa la salida detallada para depuración. Los registros también se guardan en la carpeta `logs/`.

---

## Referencia de comandos

| Argumento | Tipo | Valor predeterminado | Descripción |
|-----------|------|----------------------|-------------|
| `folder` | posicional | — | Carpeta raíz que contiene archivos MKV (escaneada recursivamente) |
| `--gpu` | opción | `auto` | Modo de codificación por GPU: `auto` (detectar), `on` (forzar NVENC), `off` (solo CPU) |
| `--dry-run` | bandera | off | Analizar archivos sin convertirlos |
| `--verbose` | bandera | off | Habilitar salida detallada de registros |
| `--ffmpeg-path` | cadena | auto | Ruta personalizada al binario de FFmpeg |

---

## Estructura de salida

Los archivos convertidos se colocan junto a los originales con el sufijo `_Final`:

```
Carpeta de Anime/
├── Episode01.mkv                 ← Original
├── Episode01_Final.mkv           ← Convertido (compatible con Blu-ray)
├── Episode02.mkv                 ← Original
├── Episode02_Final.mkv           ← Convertido (compatible con Blu-ray)
└── logs/
    └── app_mkv_20260320.log      ← Registro de conversión
```

> Los archivos que ya son compatibles con Blu-ray se **omiten** — no se crea una copia `_Final`.

---

## Especificaciones técnicas

### Video

| Propiedad | Valor |
|-----------|-------|
| Códec | H.264 (libx264 para CPU, h264_nvenc para GPU) |
| Perfil | High @ Level 4.1 |
| Profundidad de color | 8 bits |
| Resolución | Original (si ≤1920×1080) o reducida a 1080p |
| Calidad (CPU) | CRF 20 |
| Calidad (GPU) | CQ 18 |

### Audio

| Propiedad | Valor |
|-----------|-------|
| Códec | AAC (se convierte solo si el original no es AAC / AC3 / DTS) |
| Bitrate | 192 kbps |
| Frecuencia de muestreo | 48 kHz |
| Pistas | Se conservan todas las pistas de audio originales |

### Elementos preservados

| Elemento | Comportamiento |
|----------|----------------|
| Subtítulos | Se mantienen todas las pistas (ASS, SRT, PGS, etc.) |
| Capítulos | Los marcadores de capítulos se preservan |
| Fuentes / Archivos adjuntos | Las fuentes personalizadas de subtítulos se conservan |
| Metadatos | Título, etiquetas de idioma y otros metadatos se retienen |

---

## Solución de problemas

### "FFmpeg no encontrado"

Coloca `ffmpeg.exe` y `ffprobe.exe` en el mismo directorio que `app_mkv.exe`, o agrégales al `PATH` del sistema.

Descargar FFmpeg: [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/)

### La conversión es muy lenta

Si tienes una GPU NVIDIA, usa `--gpu=on` para habilitar la codificación acelerada por hardware. Esto puede ser de 5 a 10 veces más rápido que la codificación por CPU.

### El archivo de salida no tiene subtítulos

Esto suele ocurrir porque el formato de subtítulos no fue reconocido. Abre un issue con la información multimedia del archivo fuente (salida de `ffprobe`) para que pueda investigarse.

### "Análisis fallido" para un archivo

Revisa el registro detallado en la carpeta `logs/`. Causas comunes:
- Contenedor MKV dañado
- Configuración de códec o flujo inusual
- Archivo bloqueado por otro proceso

### GPU no detectada

- Asegúrate de tener una **GPU NVIDIA** con controladores actualizados
- NVENC requiere una GTX serie 600 o más reciente
- Intenta ejecutar con `--gpu=on` para forzar el modo GPU y ver el error

---

## Estructura del proyecto

```
AppMkv/
├── app_mkv.py            # Punto de entrada de la CLI
├── src/
│   ├── analyzer.py       # Análisis de archivos basado en FFprobe
│   ├── converter.py      # Lógica de conversión de video y audio
│   ├── scanner.py        # Descubrimiento recursivo de archivos MKV
│   ├── merger.py         # Muxing final del MKV
│   ├── gpu_detect.py     # Detección de GPU NVIDIA
│   └── utils.py          # Registros y validación de FFmpeg
├── logs/                 # Registros de conversión (ignorado por git)
├── exe/                  # Salida de compilación (ignorado por git)
├── requirements.txt      # Dependencias de compilación
└── README.md
```

---

## Contribuciones

¡Las contribuciones son bienvenidas! Así puedes comenzar:

1. Haz un fork del repositorio
2. Crea una rama de funcionalidad: `git checkout -b feature/mi-funcionalidad`
3. Realiza tus cambios y prueba con archivos MKV reales
4. Ejecuta con `--dry-run` y `--verbose` para verificar el comportamiento
5. Envía un pull request

Por favor, abre un issue primero para cambios importantes y poder discutir el enfoque.

---

## Licencia

Este proyecto está bajo la **Licencia MIT** — consulta el archivo [LICENSE](LICENSE) para más detalles.

---

<p align="center">
  <sub>Hecho con 🍵 por <a href="https://github.com/ChitoLabs">ChitoLabs</a></sub>
</p>
