#!/bin/bash

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar la aplicación con una ciudad por defecto
echo "Ejecutando la aplicación para la ciudad de New York..."
python weather_report.py "New York" --format text
