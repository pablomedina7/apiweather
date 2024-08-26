###########################
import requests
import argparse
import json
import csv
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener API_KEY del archivo .env
API_KEY = os.getenv('API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather(city, format_output):
    try:
        url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        # Verificación de errores en la respuesta
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            weather = data['weather'][0]

            if format_output == "json":
                print(json.dumps(data, indent=4))
            elif format_output == "csv":
                with open(f'{city}_weather.csv', 'w', newline='') as csvfile:
                    fieldnames = ['Ciudad', 'Clima', 'Temperatura', 'Humedad']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({
                        'Ciudad': city,
                        'Clima': weather['description'].capitalize(),
                        'Temperatura': f"{main['temp']}°C",
                        'Humedad': f"{main['humidity']}%"
                    })
                print(f"Datos guardados en {city}_weather.csv")
            else:
                print(f"Clima en {city}: {weather['description'].capitalize()}")
                print(f"Temperatura: {main['temp']}°C")
                print(f"Humedad: {main['humidity']}%")
        elif response.status_code == 404:
            print(f"Ubicación no encontrada: {city}. Verifica la ortografía y vuelve a intentarlo.")
        else:
            print(f"Error al obtener los datos de la API. Código de estado: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error en la conexión a la API: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consulta el clima de una ciudad.")
    parser.add_argument("city", help="Nombre de la ciudad (Ej. London)")
    parser.add_argument("--format", choices=["json", "csv", "text"], default="text", help="Formato de salida (json, csv, text)")
    args = parser.parse_args()

    get_weather(args.city, args.format)
#########################
