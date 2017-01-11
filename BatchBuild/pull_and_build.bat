@echo off
setlocal enableextensions enabledelayedexpansion

pushd %~dp0

set devfolder=%1
set config=%2
pushd %devfolder%


title Pulling from git ...

for /f %%a in ('git status --short') do set gitstatus=%%a
if not [%gitstatus%]==[] (
	echo Repo has unstaged changes, will be stashed !!!
	git stash
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

set platforms=%3 %4

for %%a in (%platforms%) do (
	title Building %%a ...
	msbuild  "Source\vc32\orgmain\OriginAll.sln" /p:Configuration=%config% /p:Platform=%%a /m
	if not !errorlevel!==0 (
		pause
		exit /b
	)
)
popd

for %%a in (%platforms%) do (
	title Copying %%a dlls ...
	python CopyDlls.py %devfolder% %%a
)

title Done (%date% %time%)

pause
