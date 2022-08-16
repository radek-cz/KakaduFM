@echo off
if exist venv\ (
  call venv\Scripts\activate.bat
  start venv\Scripts\pythonw.exe kakadufm.pyw
) else (
  echo Create venv...
  python -m venv venv
  echo Upgrade PIP and install requirements...
  call venv\Scripts\activate.bat
  venv\Scripts\python.exe -m pip install --upgrade pip
  pip install -r requirements.txt
  timeout 3
  start venv\Scripts\pythonw.exe kakadufm.pyw
)
