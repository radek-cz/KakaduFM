@echo off&setlocal
if exist venv\ (
	echo Delete venv directory...
	rd /S /Q venv
) else (
	echo venv directory not exist
)
