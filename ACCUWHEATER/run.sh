#!/bin/bash

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar la aplicación con una ciudad por defecto
echo "Ejecutando la aplicación para la ciudad de Asuncion..."
python weather_report.py "Asuncion" --format text
