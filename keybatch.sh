#!/bin/bash

for file in *.mkv
do
    keyframes "$file"
done

CurrDirName=$(basename "$PWD")
echo "Finalizada creación de keyframes en la carpeta: $CurrDirName"