@echo off
chcp 65001 >nul
title Asistencia QR SENA - Servidor con Enlace Público
echo ==============================================================
echo     SISTEMA DE ASISTENCIA QR · SENA (REGIONAL HUILA)
echo ==============================================================
echo.
echo 1. Iniciando servidor local en http://localhost:5000 ...
start "Servidor Flask" /B python app.py
timeout /t 3 >nul

echo.
echo 2. Generando enlace público HTTPS accesible para todo el mundo...
echo    (Cualquiera con este enlace o escaneando el QR podrá ingresar)
echo.
"C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:5000
pause
