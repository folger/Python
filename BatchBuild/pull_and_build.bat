@echo off

pushd %1

git pull

call "%VS110COMNTOOLS%..\..\VC\vcvarsall.bat"
msbuild  "Source\vc32\orgmain\OriginAll.sln" /p:Configuration=Release /p:Platform=x64 /m
REM msbuild  "Source\vc32\orgmain\OriginAll.sln" /p:Configuration=Release /p:Platform=Win32 /m

popd

python CopyDlls.py %1 %2 x64
REM python CopyDlls.py %1 %2 Win32

pause
