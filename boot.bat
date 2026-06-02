@echo off
title PyOS v3 Bootloader
color 0f
cls

call python main.py

if errorlevel 1 (
    echo.
    echo PyOS crashed during execution.
    pause
)

exit