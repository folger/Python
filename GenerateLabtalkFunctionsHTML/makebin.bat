@echo off

set folder=bin

rmdir /s /q %folder% 2>nul
mkdir %folder%

set srcfile=GenerateHTML
pyinstaller --distpath %folder% --onefile --noupx %srcfile%.py

rmdir /s /q build 2>nul
del /q %srcfile%.spec 2>nul

move bin\%srcfile%.exe .
rmdir /s /q bin
