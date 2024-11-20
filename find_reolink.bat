@echo off
setlocal enabledelayedexpansion

:: Define the subnet
set SUBNET=192.168.1

echo Scanning the network for Reolink server...
for /L %%i in (1,1,255) do (
    set IP=!SUBNET!.%%i
    echo Pinging !IP!...
    ping -n 1 -w 1000 !IP! >nul
    if !errorlevel! equ 0 (
        echo Host !IP! is alive. Checking for Reolink server...
        curl -s --connect-timeout 2 http://!IP! | findstr /i "Reolink" >nul
        if !errorlevel! equ 0 (
            echo Reolink server found at !IP!
            goto :end
        ) else (
            echo Not a Reolink server.
        )
    ) else (
        echo Host !IP! did not respond.
    )
)

echo Reolink server not found on the local network.
:end
pause
