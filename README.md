# Requisitos y Dependencias

### Requisitos básicos

- **Python 3.7 o superior**  
- **VapourSynth**

---

### Filtros que requieren instalación manual

Descarga e instala los siguientes filtros:

- [fmtconv](https://gitlab.com/EleonoreMizo/fmtconv/-/releases)  
- [wwxd](https://github.com/dubhater/vapoursynth-wwxd)  
- [scxvid](https://github.com/dubhater/vapoursynth-scxvid)  
- [L-SMASH-Works](https://github.com/HomeOfAviSynthPlusEvolution/L-SMASH-Works)  
- [FFMS2](https://github.com/FFMS/ffms2)  

> **Nota:** En Windows, los filtros se copian en la carpeta:  
> `C:\Users\TuUsuario\AppData\Roaming\VapourSynth\plugins64`

También necesitas tener instalados:

- [**ffmpeg**](https://ffmpeg.org)  
- [**ffprobe**](https://ffmpeg.org)  
> **Nota:** Asegúrate de que `ffmpeg` y `ffprobe` estén en el **PATH** del sistema.

---

### Librerías instalables con pip

Usa `pip` para instalarlas desde la terminal:

```sh
pip install tqdm
pip install alive-progress
```

---

# Comprobar dependencias

Se añadió una opción para verificar si todas las dependencias están correctamente instaladas. Para usarla, ejecuta en la consola:

```sh
py "ubicacion/del/keyframes.py" --check
```

Ejemplo:

```sh
py keyframes.py --check
```

Esto omitirá el proceso normal y simplemente comprobará si el sistema tiene todo lo necesario.

---

# Keyframes GUI

Gracias a nuestro amigo [CiferrC](https://github.com/RcUchiha), ahora hay una interfaz gráfica (GUI) para generar keyframes, también compatible con procesamiento por lotes. Funciona tanto en **Windows** como en **Linux**:

👉 [Keyframes-GUI](https://github.com/RcUchiha/Keyframes-GUI)

---

# Archivos extra

Se añadieron cinco scripts adicionales: tres para **Windows** y dos para **Linux**.

## Windows

- `keybatch.bat`: genera keyframes por lotes desde una carpeta completa.  
- `keysendto.bat`: permite usar el script desde el menú "Enviar a" del Explorador de Windows.  
- `keyframes.bat`: script principal, se recomienda agregarlo a las variables de entorno del sistema.

> **Nota:** Para que las opciones de *batch* y *sendto* funcionen, `keyframes.bat` debe estar en las variables de entorno.

## Linux

- `keyframes.sh`: script principal para usar desde la terminal. Guárdalo en `/home/usuario/.local/bin` y asegúrate de que esa ruta esté en tu `.bashrc`.  
- `keybatch.sh`: equivalente a la versión batch de Windows.

> **Nota:** `keybatch.sh` requiere que `keyframes.sh` funcione correctamente desde cualquier ubicación.

---

# Keyframes

Script en Python para generar keyframes (*standalone*) o QPFiles desde VapourSynth.

### Cambios en la V2:

- Se añadió un verificador de dependencias.
- Ahora es obligatorio usar `--clip` para indicar el video de entrada.

Este script es una versión mejorada de [`keyframes.py`](https://pastebin.com/cUwStpfw), eliminando la función de *slices* (que sacrificaba calidad por velocidad) y mostrando más información útil en la salida.

---

# ¿Cómo usar?

## Desde Python

```py
py keyframes.py [opciones]
```

### Opciones disponibles:

- `--clip`: Ruta del video (obligatorio).
- `--use-scxvid`: Usa `scxvid` en lugar de `wwxd`.
- `--use-doble`: Usa **ambos** filtros (`scxvid` y `wwxd`) para mayor precisión. **(Recomendado)**
- `--autismo`: Nivel de análisis (resolución). Por defecto: 3.
- `--out-file`: Archivo de salida. Si no se especifica, se usará el nombre del video con `_keyframes.log`.
- `--reescribir`: Sobrescribe el archivo de salida si ya existe.
- `--analize`: Desactiva el uso de `ffprobe` (por defecto está desactivado).
- `--linux`: Ajusta el formato del keyframe para mayor compatibilidad en Linux.
- `--check`: Verifica las dependencias.

---

## Como módulo de VapourSynth

```py
import keyframes as kf

kf.generate_keyframes_single(clip=clip, out_path="archivo_de_salida", autismo=3, reescribir=1)
kf.generate_keyframes_double(clip=clip, out_path="archivo_de_salida", autismo=3)
```

- `reescribir` es opcional.

---

# Generar QPFiles

El script también puede generar QPFiles compatibles con `x264`/`x265`.

Requiere tener VapourSynth correctamente instalado.

```py
import keyframes as kf

kf.generate_qpfile_double(clip=clip, out_path="archivo_de_salida", autismo=3, reescribir=1)
```

> Útil para pasarle el QPFile al compresor y mantener los keyframes del análisis.

---

# Parámetro `--autismo`

Define la resolución a la que se realiza el análisis (por rendimiento o compatibilidad):

```py
0 = resolución original
1 = 640x360
2 = 720x480
3 = 1280x720 (por defecto)
4 = 1440x810
5 = 1600x900
6 = 1920x1080
7 = 3840x2160 (modo "por puro meme" xD)
```

Este parámetro funciona tanto para `keyframes` como para `qpfile`.

---

# Extraer Audio

También se puede extraer el audio de un video:

```py
import keyframes as kf

kf.extraer_audio("video.mkv", stream=0, out_path="carpeta/destino/")
```

- `stream=0` es el primer audio, `1` el segundo, y así sucesivamente.
- Si no se indica `out_path`, el archivo se guardará junto al `.vpy`.

---

# ¿Cómo generar Keyframes/QPFiles desde .bat o .sh?

## Windows

Crear un archivo llamado `keyframe.bat`:

```bat
py "ruta/keyframes.py" --clip %1 --use-doble --out-file "%~n1_keyframe.log" --autismo 3
```

Agregalo a tus variables de entorno. Luego en CMD/PowerShell:

```sh
keyframe "video.mkv"
```

### Opción "Enviar a":

Crear un archivo `.bat` y guardarlo en `shell:sendto`:

```bat
@echo off
for %%I in (%*) do (
    py "ruta/keyframes.py" --clip "%%I" --use-doble --out-file "%%~nI_keyframe.log" --autismo 3
)
```

## Linux

Crear un archivo `keyframe.sh`:

```bash
#!/usr/bin/env bash
py "ruta/keyframes.py" --clip "$1" --use-doble --out-file "${1%.*}_keyframe.log" --autismo 3
```

Guardalo en `~/.local/bin` y asegurate de que esté en el PATH.

Luego en la terminal:

```sh
keyframe "video.mkv"
```

Puedes añadirle más argumentos si los necesitas.

---

# CRC32

Script para calcular y/o colocar CRC32 en tus archivos de video.

## Argumentos:

- `--calcular_crc`: calcula el CRC32 y lo imprime.
- `--colocar_crc`: calcula el CRC32 y renombra el archivo agregándolo al nombre.

## Uso

### Calcular:

```bat
py crc.py "video.mkv" --calcular_crc
```

### Colocar:

```bat
py crc.py "video.mkv" --colocar_crc
```

### Ejemplo práctico (Windows, `.bat`):

```bat
set name=Mi video encodeado
set mux=[Raws] Mi video encodeado - 01.mkv
for /f "tokens=* usebackq" %%f in (`py crc.py "%mux%" --calcular_crc`) do (
    set crcmux=.*%name%*.*.[%%f].*.mkv
)
py crc.py "%mux%" --colocar_crc
for /f "usebackq delims=" %%b in (`dir /b ^| findstr /r /c:"%crcmux%"`) do set _crcmux=%%b
pscp -pw contraseña -P puerto "%_crcmux%" usuario@host:"/ruta/de/destino/"
```
