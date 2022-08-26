@echo off&setlocal
:: mkvenv.bat

if "%app%"=="" (
	echo This script work only by call from start.bat!
:: you can fix it by setting variable app
	exit /B
)

:: ANSI colours.
:: Requires windows 1909 or newer
set _fBlack=[30m
set _bBlack=[40m
set _fRed=[31m
set _bRed=[41m
set _fGreen=[32m
set _bGreen=[42m
set _fYellow=[33m
set _bYellow=[43m
set _fBlue=[34m
set _bBlue=[44m
set _fMag=[35m
set _bMag=[45m
set _fCyan=[36m
set _bCyan=[46m
set _fLGray=[37m
set _bLGray=[47m
set _fDGray=[90m
set _bDGray=[100m
set _fBRed=[91m
set _bBRed=[101m
set _fBGreen=[92m
set _bBGreen=[102m
set _fBYellow=[93m
set _bBYellow=[103m
set _fBBlue=[94m
set _bBBlue=[104m
set _fBMag=[95m
set _bBMag=[105m
set _fBCyan=[96m
set _bBCyan=[106m
set _fBWhite=[97m
set _bBWhite=[107m
set _RESET=[0m

set download_dir=%USERPROFILE%\Downloads\
set /A test = 0
cls

echo %_RESET%%_bRed%%_fBWhite%
echo  PYTHON DETECTOR 
echo %_RESET%

::Testing Windows registry  
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Python" 2>NUL >NUL
if %ERRORLEVEL% EQU 0 (
	set /A test = %test%+1
	echo HKLM WOW6432Node\Python %_fGreen%detected%_RESET%
) else (
	echo HKLM WOW6432Node\Python %_fRed%no exist! %_RESET%
)

reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore" 2>NUL >NUL
if %ERRORLEVEL% EQU 0 (
	set /A test = %test%+1
	echo HKLM PythonCore %_fGreen%detected%_RESET%
) else (
	echo HKLM PythonCore %_fRed%no exist! %_RESET%
)
::reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\.pyw" 2>NUL >NUL
::reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\.py" 2>NUL >NUL
echo:

:: Check - is all test ok
if %test% GTR 0 (
	echo %_bRed%%_fBWhite% Succes! Python is installed! %_RESET%
) else (
	echo %_fRed% Python installer %_RESET%
	echo %_fBlue% https://www.python.org/downloads/ %_RESET%
	timeout 3 >NUL
    bitsadmin /transfer PYTHON /download /priority FOREGROUND %python_url% %download_dir%%python_file%
	echo:
	echo Start Python instalator: %python_file%
	%download_dir%%python_file% /passive InstallAllUsers=1 PrependPath=1 CompileAll=1
)
echo:

:: Create venv and download requirements
echo %_bBlue%%_fBWhite% Create venv... %_RESET%%_fGreen%
python -m venv venv
echo Upgrade PIP and install requirements...
if exist requirements.txt (
	call venv\Scripts\activate.bat
	venv\Scripts\python.exe -m pip install --upgrade pip
	pip install -r requirements.txt
) else (
	echo:
	echo %_fRed%requirements.txt file not exist!%_RESET%
	exit /B
)
echo:

:: Finaly start app
echo %_RESET%%_fBlue%Starting %app%%_RESET%
start venv\Scripts\pythonw.exe %app%
timeout 5 >NUL
