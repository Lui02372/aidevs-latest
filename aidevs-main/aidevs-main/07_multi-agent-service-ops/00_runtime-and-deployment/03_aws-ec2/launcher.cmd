@echo off
rem Forward to the shared JSON launcher.
call "%~dp0..\launcher.cmd" %*
exit /b %errorlevel%
