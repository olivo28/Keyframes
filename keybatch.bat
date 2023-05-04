@echo off
for %%a in  (*.mkv) do (
    keyframes "%%a"
)
for %%I in (.) do set CurrDirName=%%~nxI
echo Finalizada creaciÃ³n de keyframes en la carpeta: %CurrDirName%