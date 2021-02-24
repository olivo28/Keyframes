# Keyframes
 Script para generar Keyframes [Standalone] y QPFiles [Desde Vapoursynth] escritos en Python

    V1.1 - Refactorizado de todo el codigo, agregadas algunas funciones

    V1.2 - Funcion para usar tanto scxvid como WWXD para generar el keyframe
    
    V1.3 - Funcion para crear qpfile, mejorada la escritura de keyframes, tambien funciona sin problemas como un filtro extra de Vapoursynth

    V1.4 - Vuelto a refactorizar el codigo para que sea mas entendible y menos repetitivo...

    V1.5 - Agregada funcion que revisa los keyframes generados por x264, para luego compararlos y agregar las diferencias al keyframe generado con scxvid, wwxd o ambos...
    
    Script mejorado para gener keyframes de un video basado en el keyframes.py (https://pastebin.com/cUwStpfw)

    Script original editado fuertemente para mostrar más datos, eliminada la funcion de slices, que producia peor resultado a cambio de una mayor velocidad de procesado

    Dependencias:
    * Python 3.7 o mayor
    * FTMC (https://github.com/EleonoreMizo/fmtconv)
    * VapourSynth
    * wwxd (https://github.com/dubhater/vapoursynth-wwxd)
    * vapoursynth-scxvid (Opcional: solo si se usa el parametro de --use-scxvid) (https://github.com/dubhater/vapoursynth-scxvid)
    * ffmpeg/ffprobe: (https://ffmpeg.org)
    
    todo: mejorar el calculo de duracion del video... acomodar el scxvid en generate_keyframe_single... terminar el argumento --autismo