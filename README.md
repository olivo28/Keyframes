# Keyframes
 Script para generar Keyframes [Standalone] y QPFiles [Vapoursynth] escritos en Python

   V1.1 - Refactorizado de todo el codigo, agregadas algunas funciones

   V1.2 - Funcion para usar tanto scxvid como WWXD para generar el keyframe
    
   V1.3 - Funcion para crear qpfile, mejorada la escritura de keyframes, tambien funciona sin problemas como un filtro extra de Vapoursynth

   V1.4 - Vuelto a refactorizar el codigo para que sea mas entendible y menos repetitivo...

   V1.5 - Agregada funcion que revisa los keyframes generados por x264, para luego compararlos y agregar las diferencias al keyframe generado con scxvid, wwxd o ambos...

   V1.6 - Agregada función para extrear audios de los videos... [Tip: extraerlo en el codec que es...]

   V1.7 - Función de "autismo" agregada, mejorado el calculo de la duración del video, mostrará el tiempo correcto dependiendo de a que framerate este...
    
   Script mejorado para gener keyframes de un video basado en el keyframes.py (https://pastebin.com/cUwStpfw)

   Script original editado fuertemente para mostrar más datos, eliminada la funcion de slices, que producia peor resultado a cambio de una mayor velocidad de procesado

   Dependencias:
   * Python 3.7 o mayor
   * FTMC (https://github.com/EleonoreMizo/fmtconv)
   * VapourSynth
   * wwxd (https://github.com/dubhater/vapoursynth-wwxd)
   * vapoursynth-scxvid (https://github.com/dubhater/vapoursynth-scxvid)
   * ffmpeg y ffprobe: (https://ffmpeg.org)
   * L-SMASH-Works (https://github.com/VFR-maniac/L-SMASH-Works)

   PD: ffmpeg y ffprobe deberia estar en el PATH del usuario

# ¿Cómo usar?

El script sirve en 2 formas, usando Python o desde Vapoursynth
    
   Python:
   
    py keyframes.py [--use-scxvid] [--use-doble] [--out-file OUT_FILE] [--autismo (1,2,3,4,5)] [--reescribir] clip

    Todas los argumentos son opcionales, menos el clip...
        --autismo = el nivel de "autismo" del script.
        --use-scxvid = le dice al script que use scxvid en vez de WWXD.
        --use-doble = le dice al script que use tanto scxvid como WWXD para generar el keyframe. [Recomendado]
        --out-file OUT_FILE = el archivo al que escribir los keyframes [Opcional, en caso de no especificar uno, se creara con el mismo nombre del video agregando: _keyframes.txt]
        --reescribir = Por defecto, el script comprueba si existe o no el archivo, en caso de existir, el proceso se salta... con la opcion, dicho archivo es reescrito.

   Usandolo como modulo de Vapoursynth:
     
     import keyframes as kf

        kf.generate_keyframes_single(clip=clip, out_path="archivodesalida", autismo=3 reescribir=1)
        kf.generate_keyframes_double(clip=clip, out_path="archivodesalida", autimos=3, reescribir=1)

  el reescribir es opcional, en caso no querer que sea reescrito, simplemente no colocarlo:

        kf.generate_keyframes_single(clip=clip, out_path="archivodesalida", autismo=3)
        kf.generate_keyframes_double(clip=clip, out_path="archivodesalida", autismo=3)
        
# QPFile

El script tambien puede generar QPFiles para x264/x265

Para usarlo, se requiere vapoursynth en su totalidad...

    import keyframes as kf
    
    kf.generate_qpfile_double(clip=clip, out_path="archivodesalida", autismo=3 reescribir=1)

Recomendado para cuando se vaya a encodear un video, pasarle el archivo qpfile al x264/x265 para que "escriba" en el video, la información de los keyframes

# Parametro de Autismo

    El parametro de autismo es opcional la verdad, no es necesario colocarlo, ya que por defecto toma que el autismo es de 3...
    Pero ¿qué significa este parametro?
    Facil, con este parametro le decimos al script en que resolución hará el analisis...

        Niveles de autismo:
        1 = Analisis a 640x360p
        2 = Analisis a 720x480p
        3 = Analisis a 1280x720p
        4 = Analisis a 1920x1080p
        5 = Analisis a 3840x2160p

    Ojo: este parametro sirve tanto en el generar keyframes como en el generar qpfile

    PD: el autismo de nivel 5 está por puro meme xD

# Audio

También es posible extrear el audio de un video...

    import keyframes as kf

    kf.extraer_audio(clip, codec, out_path)

Un ejemplo:

    kf.extraer_audio("[SubsPlease] Tropical-Rouge! Precure - 04 (1080p) [2AE07A72].mkv", codec="aac", out_path=r"F:/Raws/Encode/Audios/Tropical4.aac")

Siempre hay que extrearlo en su codec correspondiente, si el mediainfo muestra que es A_AAC, es mejor extraerlo como aac, si muestra que es A_FLAC, es mejor extraerlo como flac y así...

En su mayoria, los webrip (tanto de Funimation como CR) son A_AAC [aac] en su mayoria, en cambio, Amazon y Netflix, normalmente es A_EAC3 [eac3]

En caso de no especificar un out_path, extraera el audio en la misma ubicación del video :3

Ojo: también sirve para extraer los audios de los bdmv [m2ts] en pcm o wav...

# ¿Cómo generar QPfiles o Keyframes desde un .bat [Windows] o .sh [Linux]?

    Escribiendolo...