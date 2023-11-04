# Depedencias

   * Python 3.7 o mayor
   * FTMC (https://github.com/EleonoreMizo/fmtconv)
   * VapourSynth
   * wwxd (https://github.com/dubhater/vapoursynth-wwxd)
   * vapoursynth-scxvid (https://github.com/dubhater/vapoursynth-scxvid)
   * ffmpeg y ffprobe: (https://ffmpeg.org)
   * L-SMASH-Works (https://github.com/VFR-maniac/L-SMASH-Works)
   * FFMS2 (https://github.com/FFMS/ffms2)
   * tqdm (https://github.com/tqdm/tqdm)
   * alive_progress (https://github.com/rsalmei/alive-progress)

   PD: ffmpeg y ffprobe deberia estar en el PATH del usuario

# Comprobar dependecias

Se agrego una opción para comprobar si todas las dependencias se encuentra, para esto, escribir en tu consola:

    py "ubicacion/del/keyframes.py" --check

ejemplo:

    py keyframes.py --check

Lo que hará es saltarse todo el proceso y comprbara sí se encuentran todas las dependencias en el sistema

# Keyframe GUI

Graciasa nuestro amigo de [CiferrC](https://github.com/RcUchiha), ahora hay una GUI para aplicar keyframes, sirve tanto para Windows como Linux.

[Keyframes-GUI](https://github.com/RcUchiha/Keyframes-GUI)

# Archivos extras

Se agregaron 5 archivos nuevos, 3 unicamente para Windows y 2 para Linux

[Windows]

keybatch.bat sirve para crear keyframes en batch de toda una carpeta

keysendto.bat es para usarlo seleccionando los diferentes archivos en usar la opción de "Enviar a" de Windows

keyframes.bat es el archivo normal que se coloca en tu variable de entorno y usar por cmd

PD: para que las opciones de sendto y batch funcionen, keyframes debe estár sí o sí en tu variable de entorno

[Linux]

keyframes.sh es el archivo base normal para usar en tu terminal, este debe ir en  /home/usuario/.local/bin y agregar la carpeta al .bashrc

keybatch.sh lo mismo que la version de windows, pero para Linux

PD: keybatch requiere sí o sí que keyframes funcione sin problemas desde cualquier ubicacion

# Keyframes

Script para generar Keyframes [Standalone] y QPFiles [Vapoursynth] escritos en Python

    V2 - Agregado un comprobador para ver si se encuentran todas las dependencias, ahora es necesario agregar --clip para especificar el clip

Script mejorado para gener keyframes de un video basado en el keyframes.py (https://pastebin.com/cUwStpfw)

Script original editado fuertemente para mostrar más datos, eliminada la funcion de slices, que producia peor resultado a cambio de una mayor velocidad de procesado

# ¿Cómo usar?

El script sirve en 2 formas, usando Python o desde Vapoursynth
    
   Python:
   
```py
    py keyframes.py [--use-scxvid] [--use-doble] [--out-file OUT_FILE] [--autismo (0,1,2,3,4,5,6,7)] [--reescribir] [--analize] [--clip] [--check]
```

Todas los argumentos son opcionales, menos el clip...

        --autismo = el nivel de "autismo" del script.
        --check = analiza si tienes todas las dependencias instaladas
        --linux = para especificar si se crea en linux el keyframe [Linux por alguna razón no reconoce le keyframe creado normalmente, tuve que hacer unos cambios]
        --use-scxvid = le dice al script que use scxvid en vez de WWXD.
        --use-doble = le dice al script que use tanto scxvid como WWXD para generar el keyframe. [Recomendado]
        --out-file OUT_FILE = el archivo al que escribir los keyframes [Opcional, en caso de no especificar uno, se creara con el mismo nombre del video agregando: _keyframes.log]
        --reescribir = Por defecto, el script comprueba si existe o no el archivo, en caso de existir, el proceso se salta... con la opcion, dicho archivo es reescrito.
        --analize = deshabilita el uso de ffprobe para analizar los I-Frames generados por x264/x265. 
        --clip = el video al que generarle el keyframe

--analize está por defecto desactivado, en caso de querer analizar los I-Frames generados por un encode actual, colocarlo.

Usandolo como modulo de Vapoursynth:
```py
    import keyframes as kf

    kf.generate_keyframes_single(clip=clip, out_path="archivodesalida", autismo=3, reescribir=1)
    kf.generate_keyframes_double(clip=clip, out_path="archivodesalida", autimos=3, reescribir=1)
```

el reescribir es opcional, en caso no querer que sea reescrito, simplemente no colocarlo:

```py
    kf.generate_keyframes_single(clip=clip, out_path="archivodesalida", autismo=3)
    kf.generate_keyframes_double(clip=clip, out_path="archivodesalida", autismo=3)
```
        
# QPFile

El script tambien puede generar QPFiles para x264/x265

Para usarlo, se requiere vapoursynth en su totalidad...

```py
    import keyframes as kf

    kf.generate_qpfile_double(clip=clip, out_path="archivodesalida", autismo=3, reescribir=1)
```

Recomendado para cuando se vaya a encodear un video, pasarle el archivo qpfile al x264/x265 para que "escriba" en el video, la información de los keyframes

# Parametro de Autismo

   El parametro de autismo es opcional la verdad, no es necesario colocarlo, ya que por defecto toma que el autismo es de 3...
   Pero ¿qué significa este parametro?
   Facil, con este parametro le decimos al script en que resolución hará el analisis...

Niveles de autismo:
```py
    0 = El analisis se hace a la resolucion actual del video. (Usado mas que todo para resoluciones amorfas, fuera del estandar)
    1 = Analisis a 640x360p
    2 = Analisis a 720x480p
    3 = Analisis a 1280x720p
    4 = Analisis a 1440x810p
    5 = Analisis a 1600x900p
    6 = Analisis a 1920x1080p
    7 = Analisis a 3840x2160p
```

   Ojo: este parametro sirve tanto en el generar keyframes como en el generar qpfile

   PD: el autismo de nivel 7 está por puro meme xD

# Audio

También es posible extrear el audio de un video...

```py
    import keyframes as kf

    kf.extraer_audio(clip, stream, out_path)
```

Un ejemplo:
```py
    kf.extraer_audio("[SubsPlease] Tropical-Rouge! Precure - 04 (1080p) [2AE07A72].mkv", stream=0, out_path=r"F:/Raws/Encode/Audios/")
```

El script analiza el codec correspondiente del stream para extraerlo en su codec...

El stream 0 corresponde al primer audio, el stream 1 al segundo audio y asi sucesivamente...

El out_path es en qué carpeta quieres que se extraiga, sino se coloca, lo hara en donde está ubicado el .vpy

# ¿Cómo generar QPfiles o Keyframes desde un .bat [Windows] o .sh [Linux]?

[Windows]

Crea un archivo llamado keyframe.bat que contenga lo siguiente:

    py "ubicacion/del/keyframes.py" --clip %1 --use-doble --out-file "%~n1_keyframe.log" --autismo 3

Guardalo en cualquiera parte de tu computadora y colocalo en tus Variables de entorno...

Solo te toca abrir tu CMD/PowerShell, navegar hasta la carpeta donde tienes tu video y escribir:

    keyframe "elvideoencuestion.mkv"

Se empezará a crear los keyframes de dicho video.

También es posible a través de la opción de "Enviar a" de Windows... para eso, se creaciaria un .bat nuevo que estaría en: shell:sendto

    @echo off

    for %%I in (%*) do (
    py "ubicacion/del/keyframes.py" --clip "%%I" --use-doble --out-file "%%~nI_keyframe.log" --autismo 3
    )


[Linux]

Crea un archivo llamado keyframe.sh que contenga lo siguiente:

    #!/usr/bin/env python
    py "ubicacion/del/keyframes.py" --clip %1 --use-doble --out-file "%~n1_keyframe.log" --autismo 3

Guardalo en /home/usuario/.local/bin, agregar la carpeta a el .bashrc

Solo te toca abrir tu terminal favorita, navegar hasta la carpeta y escribir

    keyframe "elvideoencuestion.mkv"

Se empezará a crear los keyframes de dicho video.

Puedes completar los argumentos del keyframe.bat/keyframe.sh con los que necesites, asi es generar los keyframes simples de algun webrip con todo por defecto.

# CRC32

Agregado un script para calcular y colocar CRC32 a tus videos...

Argumentos que toma:

    clip =  el video al que se le colocará/calculará el CRC32
    --calcular_crc = Calcula el CRC32 y devuelve el CRC32 que debería tener...
    --colocar_crc = Calcular el CRC32 y se lo coloca al archivo en cuestion...

Modo de uso:

Para calcular:
```py
    py crc.py "video" --calcular_crc
```

Para colocar:
```py
    py crc.py "video" --colocar_crc
```
Util para automatizar procesos como el de colocar CRC32 a un encode y subirlo a un servidor, tipo:

Ejemplo en Windows [Archivo .bat]

```bat
    set name=Mi video encodeado
    set mux=[Raws] Mi video encodeado - 01.mkv
    for /f "tokens=* usebackq" %%f in (`py crc.py "%mux%" --calcular_crc`) do (
    set crcmux=.*%name%*.*.[%%f].*.mkv
    )
    py crc.py "%mux%" --colocar_crc
    for /f "usebackq delims=" %%b in (`dir /b ^| findstr /r /c:"%crcmux%"`) do set _crcmux=%%b
    pscp -pw contraseña -P puerto "%_crcmux%" usuario@host:"/dirección/a/la/que/subir/"
```

