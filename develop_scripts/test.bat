@ECHO OFF

set @version=""
set @clean="yes"
set @coverage="no"
:init
if "%1"=="-nc" goto lnoclean
if "%1"=="-cov" goto :lcoverage
if "%1"=="" goto start
goto lerror

:lnoclean
set @clean="no"
shift
goto init

:lcoverage
set @coverage="yes"
shift
goto init

:lerror
echo %0 usage error

:start
PowerShell.exe -file test.ps1 %@clean% %@coverage%