import argparse
import pathlib
import os
import binascii
from tqdm import tqdm

__author__ = "Olivo28"
__license__ = 'MIT'
__version__ = '1.1'

def calcular_crc(filename):

    buf = open(filename,'rb')
    total_size = os.path.getsize(filename)

    crc = 0
    with tqdm(total=total_size, unit='MB', unit_scale=True, desc='Calculando el CRC...') as pbar:
        for chunk in iter(lambda: buf.read(1024), b''):
            crc = binascii.crc32(chunk, crc) & 0xFFFFFFFF
            pbar.update(len(chunk))

    crc_c = "%08X" % crc
    print(f'El CRC calculado fue: {crc_c}')
    return crc_c

def colocar_crc(filename):

    crc = calcular_crc(filename)
    os.rename(filename, os.path.splitext(filename)[0] + " [" + crc + "]" + os.path.splitext(filename)[1])

def main():

    if not args.clip:
        print("¡No haz colocado ningún video al cual generar el CRC32!")
        return
    else:
        file = args.clip
        
    if args.colocar_crc == 1:
        colocar_crc(file)
        print(f"CRC colocado a {file}")
    if args.calcular_crc == 1:
        calcular_crc(file)
        print(f"{calcular_crc(file)}")
    if args.colocar_crc == 0 and args.calcular_crc == 0:
        print("No has seleccionado ninguna opción")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('clip', help="el video al que hacer el keyframe.")
    parser.add_argument('--colocar_crc', action='store_true', help="colocar el crc al video")
    parser.add_argument('--calcular_crc', action='store_true', help="calcular el crc del video")
    args = parser.parse_args()
    main()
    