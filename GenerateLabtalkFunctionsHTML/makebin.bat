@echo off

rmdir /s /q bin 2>nul
mkdir bin

set srcfile=GenerateHTML
pyinstaller --distpath bin --onefile --noupx %srcfile%.py

rmdir /s /q build 2>nul
del /q %srcfile%.spec 2>nul

move bin\%srcfile%.exe .
rmdir /s /q bin
