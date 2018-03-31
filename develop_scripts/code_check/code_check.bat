@ECHO OFF
set @directory=""
set @extended="s"
set @filename=" "

:init
if "%1"=="-f" goto lfilename
if "%1"=="-e" goto lextended
if "%1"=="-d" goto ldirectory
if "%1"=="" goto lexecute
goto lerror


:lfilename
shift
set @filename=%1
shift
goto init

:lextended
shift
set @extended=%1
shift
goto init

:ldirectory
shift
set @directory=%1
shift
goto init

:lerror
echo %0 usage error

:lexecute
PowerShell.exe -file code_check.ps1 %@directory% %@extended% %@filename%