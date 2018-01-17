@echo off
setlocal enableextensions enabledelayedexpansion
set me=%~n0
set parent=%~dp0

pushd %~dp0

set devfolder=%1
set solution=%2
set config=%3
pushd %devfolder%


REM title Pulling from git ...

REM for /f %%a in ('git status --short') do set gitstatus=%%a
REM if not [%gitstatus%]==[] (
	REM echo Repo has unstaged changes, will be stashed !!!
	REM git stash
REM )
REM git gc
REM :startpull
REM git pull --rebase
REM set waitsec=60
REM if not %errorlevel%==0 (
	REM echo Pull fail, wait %waitsec% to retry
	REM timeout %waitsec%
	REM goto :startpull
REM )

call "%VS110COMNTOOLS%..\..\VC\vcvarsall.bat"

set platforms=%4 %5

for %%a in (%platforms%) do (
	title Building %%a ...
	python "%parent%\BuildCmd.py" "Source\vc32\orgmain\%solution%" --configuration=%config% --platform=%%a --all-output --error-exit
	if not !errorlevel!==0 (
		pause
		exit /b
	)
)
popd

if "%solution%"=="OriginAll.sln" (
	for %%a in (%platforms%) do (
		title Copying %%a dlls ...
		python CopyDlls.py %devfolder% --%%a
	)
)

title Done (%date% %time%)

pause
