@echo off
REM The script starts the server with default settings

where pipenv >nul 2>nul
if  NOT %errorlevel%==1 (
    pipenv run python manage.py runserver
) else (
    @echo Ooops, looks like pipenv is not installed.
)

REM -- END --
