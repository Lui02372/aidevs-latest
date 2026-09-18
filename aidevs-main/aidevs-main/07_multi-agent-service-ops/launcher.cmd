@echo off
rem The JSON manifest and Compose launcher live in 00_runtime-and-deployment.
call "%~dp000_runtime-and-deployment\launcher.cmd" %*
exit /b %errorlevel%
