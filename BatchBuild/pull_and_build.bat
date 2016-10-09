@echo off

pushd %~dp0

pushd %1

title Pulling from git ...

for /f %%a in ('git status --short') do set gitstatus=%%a
if not [%gitstatus%]==[] (
	echo Repo has unstaged changes, will be reseted !!!
	git reset --hard
)
git gc
:startpull
git pull --rebase
set waitsec=60
if not %errorlevel%==0 (
	echo Pull fail, wait %waitsec% to retry
	timeout %waitsec%
	goto :startpull
)

call "%VS110COMNTOOLS%..\..\VC\vcvarsall.bat"
title Building Win32 ...
msbuild  "Source\vc32\orgmain\OriginAll.sln" /p:Configuration=Release /p:Platform=Win32 /m
if not %errorlevel%==0 (
	pause
	exit /b
)
title Building x64 ...
msbuild  "Source\vc32\orgmain\OriginAll.sln" /p:Configuration=Release /p:Platform=x64 /m
if not %errorlevel%==0 (
	pause
	exit /b
)

popd

title Copying Win32 dlls ...
python CopyDlls.py %1 %2 Win32
title Copying x64 dlls ...
python CopyDlls.py %1 %2 x64

pause
