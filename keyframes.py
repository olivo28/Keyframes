import argparse
import os
import subprocess
import pathlib
import glob

from collections import OrderedDict

import vapoursynth as vs

core = vs.core

__author__ = "Olivo28"
__license__ = 'MIT'
__version__ = '1.9'

def borrar_archivos():

    print("Borrando archivos intermedios...")

    lwi = glob.glob('*.lwi')
    for file in lwi:
        try:
            os.remove(file)
        except:
            print("Error al remover: ", file)

    ffindex = glob.glob('*.ffindex')
    for file in ffindex:
        try:
            os.remove(file)
        except:
            print("Error al remover: ", file)
    
    return

def calcular_tiempo(clip):

    fps = clip.fps.numerator / clip.fps.denominator
    segundoframe = 1 / fps
    segundos= clip.num_frames*segundoframe
    d, r1 = divmod(segundos, 86400)
    h, r2 = divmod(r1, 3600)
    m, s = divmod(r2, 60)

    duracion = '%d:%d:%d' % (h, m, s)

    return duracion

def info_video(clip, out_path) -> None:

    name = clip
    if pathlib.Path(clip).suffix == ".mp4":
        clip1 = core.ffms2.Source(clip)
    else:
        clip1 = core.lsmas.LWLibavSource(clip)

    command = f'ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "{clip}"'
    codec = subprocess.check_output(command, stderr=subprocess.STDOUT)
    codec1 = codec.decode('utf-8').rstrip('\r\n')

    print(f"\nInformación del video...\nVideo: {name}", \
        f"\nResolución: {clip1.width}x{clip1.height}p", \
        f"\nCantidad de frames: {clip1.num_frames}", \
        f"- Duración: {calcular_tiempo(clip1)}", \
        f"\nFramerate: {clip1.fps}", \
        f"\nFormato: {clip1.format.name}", \
        f"\nCodec: {codec1}", \
        f"\nArchivo de Keyframes: {out_path}\n")

def frame_total(clip):

    if not isinstance(clip, vs.VideoNode):
        if pathlib.Path(clip).suffix == ".mp4":
            clip = core.ffms2.Source(clip)
        else:
            clip = core.lsmas.LWLibavSource(clip)
        

    frames = clip.num_frames

    return frames

def iframes(clip):

    out_txt1 = ""

    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [clip]).decode()
    f_types = out.replace('pict_type=','').split()
    frame_types = zip(range(len(f_types)), f_types)
    i_frames = [x[0] for x in frame_types if x[1]=='I']
    for i in i_frames:
        out_txt1 += "%d\n" % i

    return out_txt1

def extraer_audio(clip, stream, out_path=None):

    command = f'ffprobe -v error -select_streams a:{stream} -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "{clip}"'
    codec = subprocess.check_output(command, stderr=subprocess.STDOUT)
    codec1 = codec.decode('utf-8').rstrip('\r\n')

    stream1 = stream + 1
    
    if pathlib.Path(clip).suffix == ".m2ts":
        codec = "wav"
        if not out_path:
            out_path = f'{os.path.basename(clip)[:-5]}_audio_0{stream1}.{codec}'
        else:
            out_path = f'{out_path}\{os.path.basename(clip)[:-5]}_audio_0{stream1}.{codec}'
    else:
        if not out_path:
            out_path = f'{os.path.basename(clip)[:-4]}_audio_0{stream1}.{codec1}'
        else:
            out_path = f'{out_path}\{os.path.basename(clip)[:-4]}_audio_0{stream1}.{codec1}'
    
    if pathlib.Path(clip).suffix == ".m2ts":
        command = f'ffmpeg -loglevel quiet -stats -i "{clip}" -map 0:{stream1} -acodec pcm_s24le "{out_path}"'
    else:
        command = f'ffmpeg -loglevel quiet -stats -i "{clip}" -map 0:{stream1} -acodec copy "{out_path}"'

    subprocess.check_output(command)

def autista(clip, autismo):

    if int(autismo) == int(1):
        clip1 = core.resize.Bilinear(clip, 640, 360, format=vs.YUV420P8)
    if int(autismo) == int(2):
        clip1 = core.resize.Bilinear(clip, 720, 480, format=vs.YUV420P8)
    if int(autismo) == int(3): #por defecto
        clip1 = core.resize.Bilinear(clip, 1280, 720, format=vs.YUV420P8)
    if int(autismo) == int(4):
        clip1 = core.resize.Bilinear(clip, 1920, 1080, format=vs.YUV420P8)
    if int(autismo) == int(5): #en serio... puro autismo
        clip1 = core.resize.Bilinear(clip, 3840, 2160, format=vs.YUV420P8)

    return clip1

def key264(clip, out_txt3):
  
    print("Analizando Keyframes generados por x264...")

    out_txt1 = iframes(clip)
    out_txt1 = out_txt1.splitlines()

    print("Comparando, eliminando y uniendo keyframes...")

    out_txt3 = out_txt3.splitlines()
    out_txt2 = out_txt3 + out_txt1
    out_txt2 = list(OrderedDict.fromkeys(out_txt2))
    out_txt2 = sorted(out_txt2, key=int)
    out_txt2 = '\n'.join(out_txt2)

    return out_txt2


def keyframe_simple(clip, out_path, autismo, analize, use_scxvid=None) -> None:

    out_txt = "# keyframe format v1\nfps 0\n"
    out_txt3 = ""
    
    if not isinstance(clip, vs.VideoNode):
        if pathlib.Path(clip).suffix == ".mp4":
            clip1 = core.ffms2.Source(clip)
        else:
            clip1 = core.lsmas.LWLibavSource(clip)
    else:
        clip1 = clip

    clip1 = core.fmtc.resample(clip1, css="420")
    clip1 = autista(clip1, autismo)

    if not use_scxvid:
        clip1 = core.wwxd.WWXD(clip1)
    else:
        clip1 = core.scxvid.Scxvid(clip1)

    for i in range(clip1.num_frames):
        props = clip1.get_frame(i).props
        if not use_scxvid:
            scenechange = props.Scenechange
        else:
            scenechange = props._SceneChangePrev
        if scenechange:
            out_txt3 += "%d\n" % i
        if i % 1 == 0:
            print(f"Generando keyframe: {i}/{frame_total(clip1)} frames", end="\r")

    print("\n")

    if analize == 0:
        out_txt2 = out_txt3
    else:
        out_txt2 = key264(clip, out_txt3)
    out_txt += out_txt2

    text_file = open(out_path, "w")
    text_file.write(out_txt)
    text_file.close()

    return

def doble(clip, out_path, autismo, analize, qp_file=None) -> None:

    if not qp_file:
        out_txt = "# keyframe format v1\nfps 0\n"
    else:
        out_txt = ""

    out_txt3 = ""

    if not isinstance(clip, vs.VideoNode):
        if pathlib.Path(clip).suffix == ".mp4":
            clip1 = core.ffms2.Source(clip)
        else:
            clip1 = core.lsmas.LWLibavSource(clip)
    else:
        clip1 = clip

    clip1 = core.fmtc.resample(clip1, css="420")
    clip1 = autista(clip1, autismo)
    clip1 = core.scxvid.Scxvid(clip1)
    clip1 = core.wwxd.WWXD(clip1)

    for i in range(clip1.num_frames):
        props = clip1.get_frame(i).props
        if props._SceneChangePrev == 1 or props.Scenechange == 1:
            if not qp_file:
                out_txt3 += "%d\n" % i
            else:
                out_txt += "%d I -1\n" % i
        if i % 1 == 0:
            if not qp_file:
                print(f"Generando keyframes: {i}/{frame_total(clip1)} frames", end="\r")
            else:
                print(f"Generando QPFile: {i}/{frame_total(clip1)} frames", end="\r")
                
    print("\n")

    if not qp_file:
        if analize == 0:
            out_txt2 = out_txt3
        else:
            out_txt2 = key264(clip, out_txt3)
        out_txt += out_txt2 

        text_file = open(out_path, "w")
        text_file.write(out_txt)
        text_file.close()
    else:
        text_file = open(out_path, "w")
        text_file.write(out_txt)
        text_file.close()
    
    return



def generate_keyframes_single(clip, out_path=None, autismo=None, reescribir=None, use_scxvid=None, analize=None) -> None:

    if not out_path:
        out_path = os.path.splitext(clip)[0] + "_keyframes.txt"
        info_video(clip, out_path)
    else:
        info_video(clip, out_path)

    if not autismo:
        autismo = int(3)

    if not analize:
        analize = int(0)
    else:
        analize = int(1)

    if os.path.isfile(out_path) == 1:
        if not reescribir:
            print("Generando keyframes...")
            print("Ya existe el archivo...\nSaltando proceso.")            
        else:
            if use_scxvid:
                keyframe_simple(clip, out_path, autismo, analize, use_scxvid, )
            else:
                keyframe_simple(clip, out_path, autismo, analize)    
    else:
        if use_scxvid:
            keyframe_simple(clip, out_path, autismo, analize, use_scxvid)
        else:
            keyframe_simple(clip, out_path, autismo, analize)

    borrar_archivos()

    return

def generate_keyframes_double(clip, out_path=None, autismo=None, reescribir=None, analize=None) -> None: ## aun ando pensandola xD

    if not out_path:
        out_path = os.path.splitext(clip)[0] + "_keyframes.txt"
        info_video(clip, out_path)
    else:
        info_video(clip, out_path)

    if not autismo:
        autismo = int(3)
    
    if not analize:
        analize = int(0)
    else:
        analize = int(1)
    
    if os.path.isfile(out_path) == 1:
        if not reescribir:
            print("Generando keyframes...")
            print("Ya existe el archivo...\nSaltando proceso.")
        else:
            doble(clip, out_path, autismo, analize)
    else:
        doble(clip, out_path, autismo, analize)

    borrar_archivos()
    
    return


def generate_qpfile_double(clip, out_path=None, autismo=None, reescribir=None) -> None:

    if not out_path:
        out_path = os.path.splitext(clip)[0] + "_qpfile.txt"

    if not autismo:
        autismo = int(3)

    analize = int(0)

    if not isinstance(clip, vs.VideoNode):
        raise TypeError("El clip no es una instancia tipo VideoNode.")

    if os.path.isfile(out_path) == 1:
        if not reescribir:
            print("Generando QPFile...")
            print("Ya existe el archivo...\nSaltando proceso.")
        else:
            doble(clip, out_path, autismo, analize, qp_file=1)
    else:
        doble(clip, out_path, autismo, analize, qp_file=1)

    borrar_archivos()
    
    return

def main():

    if not args.clip:
        print("¡No haz colocado ningún video al cual sacarle el keyframe!")
        return

    if not args.autismo:
        args.autismo = int(3)

    if not args.analize:
        args.autismo = int(0)

    clip = args.clip


    if not args.out_file:
        out_path = os.path.splitext(clip)[0] + "_keyframes.txt"
    else:
        out_path = args.out_file    

    if args.use_doble:
        generate_keyframes_double(clip, out_path, args.autismo, args.reescribir, args.analize)
    else:
        if not args.use_scxvid:
            generate_keyframes_single(clip, out_path, args.autismo, args.reescribir, args.analize)
        else:
            generate_keyframes_single(clip, out_path, args.autismo, args.reescribir, args.use_scxvid, args.analize)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--autismo', help="el modo a usar para hacer el keyframe... de 1 hasta 4, a mayor el numero de modo, mayor detección de escenas, pero más tiempo de procesado. Valor por defecto: 3")
    parser.add_argument('--use-scxvid', action='store_true', help="Usar Scxvid en vez de WWXD para detectar cambios de escena (por defecto usa WWXD.")
    parser.add_argument('--use-doble', action='store_true', help="Usar tanto scxvid como WWXD para detectar los cambios de escenas y luego unirlos (aumenta considerablemente el tiempo de procesamiento).")
    parser.add_argument('--out-file', help="el archivo al que escribir el cambio de escenas en el formato de Aegisub; por defecto a '_keyframes.txt' en el mismo directorio que se encuentra el video.")
    parser.add_argument('--reescribir', action='store_true', help="habilita reescribir el archivo en caso de que exista...")
    parser.add_argument('--analize', action='store_true', help="deshabilita el uso de ffprobe para analizar los I-Frames generados por x264/x265.")
    parser.add_argument('clip', help="el video al que generarle el keyframe.")
    args = parser.parse_args()
    main()
    