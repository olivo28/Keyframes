import argparse
import os
import ntpath
import subprocess
from collections import OrderedDict

import vapoursynth as vs

core = vs.core

__author__ = "Olivo28"
__license__ = 'MIT'
__version__ = '1.6'


def calcular_tiempo(clip):

    segundoframe = 1 / 23.976
    segundos= clip.num_frames*segundoframe
    d, r1 = divmod(segundos, 86400)
    h, r2 = divmod(r1, 3600)
    m, s = divmod(r2, 60)

    duracion = '%d:%d:%d' % (h, m, s)

    return duracion

def info_video(clip, out_path) -> None:

    name = clip
    clip = core.lsmas.LWLibavSource(clip)

    print(f"\nInformación del video...\nVideo: {name}", \
        f"\nResolución: {clip.width}x{clip.height}p", \
        f"\nCantidad de frames: {clip.num_frames}", \
        f"- Duración: {calcular_tiempo(clip)}", \
        f"\nFramerate: {clip.fps}", \
        f"\nFormato: {clip.format.name}", \
        f"\nArchivo de Keyframes: {out_path}\n")

def frame_total(clip):

    if not type(clip) is vs.VideoNode:
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

def extraer_audio(clip, codec):
    
    command = f'ffmpeg -loglevel quiet -stats -i "{clip}" -vn -acodec copy "{ntpath.basename(clip)[:-4]}.{codec}"'
    subprocess.check_output(command)

def keyframe_simple(clip, out_path, use_scxvid=None) -> None:

    out_txt = "# keyframe format v1\nfps 0\n"
    out_txt3 = ""

    if not type(clip) is vs.VideoNode:
        clip1 = core.lsmas.LWLibavSource(clip)
    else:
        clip1 = clip

    clip1 = core.fmtc.resample(clip1, css="420")
    clip1 = core.resize.Bilinear(clip1, 1280, 720, format=vs.YUV420P8)

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

    print("Analizando Keyframes generados por x264...")

    out_txt1 = iframes(clip)
    out_txt1 = out_txt1.splitlines()

    print("Comparando, eliminando y uniendo keyframes...")

    out_txt3 = out_txt3.splitlines()
    out_txt2 = out_txt3 + out_txt1
    out_txt2 = list(OrderedDict.fromkeys(out_txt2))
    out_txt2 = sorted(out_txt2, key=int)
    out_txt2 = '\n'.join(out_txt2)
    out_txt += out_txt2

    text_file = open(out_path, "w")
    text_file.write(out_txt)
    text_file.close()

def doble(clip, out_path, qp_file=None) -> None:

    if not qp_file:
        out_txt = "# keyframe format v1\nfps 0\n"
    else:
        out_txt = ""

    out_txt3 = ""

    if not type(clip) is vs.VideoNode:
        clip1 = core.lsmas.LWLibavSource(clip)
    else:
        clip1 = clip

    clip1 = core.fmtc.resample(clip1, css="420")
    clip1 = core.resize.Bilinear(clip1, 1280, 720, format=vs.YUV420P8)
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

        print("Analizando Keyframes generados por x264...")

        out_txt1 = iframes(clip)
        out_txt1 = out_txt1.splitlines()

        print("Comparando, eliminando y uniendo keyframes...")

        out_txt3 = out_txt3.splitlines()
        out_txt2 = out_txt3 + out_txt1
        out_txt2 = list(OrderedDict.fromkeys(out_txt2))
        out_txt2 = sorted(out_txt2, key=int)
        out_txt2 = '\n'.join(out_txt2)
        out_txt += out_txt2 

        text_file = open(out_path, "w")
        text_file.write(out_txt)
        text_file.close()
    else:
        text_file = open(out_path, "w")
        text_file.write(out_txt)
        text_file.close()



def generate_keyframes_single(clip, out_path=None, reescribir=None, use_scxvid=None) -> None:

    if not out_path:
        out_path = os.path.splitext(clip)[0] + "_keyframes.txt"
        info_video(clip, out_path)
    else:
        info_video(clip, out_path)

    if os.path.isfile(out_path) == 1:
        if not reescribir:
            print("Generando keyframes...")
            print("Ya existe el archivo...\nSaltando proceso.")            
        else:
            if use_scxvid:
                keyframe_simple(clip, out_path, use_scxvid)
            else:
                keyframe_simple(clip, out_path)    
    else:
        if use_scxvid:
            keyframe_simple(clip, out_path, use_scxvid)
        else:
            keyframe_simple(clip, out_path)


def generate_keyframes_double(clip, out_path=None, reescribir=None) -> None: ## aun ando pensandola xD

    if not out_path:
        out_path = os.path.splitext(clip)[0] + "_keyframes.txt"
        info_video(clip, out_path)
    else:
        info_video(clip, out_path)

    if os.path.isfile(out_path) == 1:
        if not reescribir:
            print("Generando keyframes...")
            print("Ya existe el archivo...\nSaltando proceso.")
        else:
            doble(clip, out_path)
    else:
        doble(clip, out_path)


def generate_qpfile_double(clip, out_path=None, reescribir=None) -> None:

    if not out_path:
        out_path = os.path.splitext(clip)[0] + "_qpfile.txt"

    if os.path.isfile(out_path) == 1:
        if not reescribir:
            print("Generando QPFile...")
            print("Ya existe el archivo...\nSaltando proceso.")
        else:
            doble(clip, out_path, qp_file=1)
    else:
        doble(clip, out_path, qp_file=1)

def main():

    if not args.clip:
        print("¡No haz colocado ningún video al cual sacarle el keyframe!")
        return

    clip = args.clip

    if not args.out_file:
        out_path = os.path.splitext(clip)[0] + "_keyframes.txt"
    else:
        out_path = args.out_file

    if args.use_doble:
        generate_keyframes_double(clip, out_path, args.reescribir)
    else:
        if not args.use_scxvid:
            generate_keyframes_single(clip, out_path, args.reescribir)
        else:
            generate_keyframes_single(clip, out_path, args.reescribir, args.use_scxvid)

    try:
        os.remove(f"{args.clip}.lwi")
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument('--autismo', action='store_true', help="el modo a usar para hacer el keyframe... por defecto 1, hasta 4, a mayor el numero de modo, mayor detección de escenas, pero más tiempo de procesado.")
    parser.add_argument('--use-scxvid', action='store_true', help="usar Scxvid en vez de WWXD para detectar cambios de escena (por defecto usa WWXD.")
    parser.add_argument('--use-doble', action='store_true', help="Usar tanto scxvid como WWXD para detectar los cambios de escenas y luego unirlos (aumenta considerablemente el tiempo de procesamiento). ")
    parser.add_argument('--out-file', help="el archivo al que escribir el cambio de escenas en el formato de Aegisub; por defecto a '_keyframes.txt' en el mismo directorio que se encuentra el video.")
    parser.add_argument('--reescribir', action='store_true', help="habilita reescribir el archivo en caso de que exista...")
    parser.add_argument('clip', help="el video al que hacer el keyframe.")
    args = parser.parse_args()
    main()
    