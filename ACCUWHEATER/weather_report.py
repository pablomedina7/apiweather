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
BASE_URL = os.getenv('BASE_URL')

# Diccionario para traducir descripciones de clima
traducciones_clima = {
    "clear sky": "Cielo despejado",
    "few clouds": "Pocas nubes",
    "scattered clouds": "Nubes dispersas",
    "broken clouds": "Nubes rotas",
    "overcast clouds": "Nublado",
    "light rain": "Lluvia ligera",
    "moderate rain": "Lluvia moderada",
    "heavy intensity rain": "Lluvia intensa",
    # Puedes añadir más traducciones según sea necesario
}

# Diccionario para almacenar el cache
cache = {}

def traducir_clima(descripcion):
    return traducciones_clima.get(descripcion.lower(), descripcion)

def get_weather(city, format_output):
    # Verificar si la ciudad ya está en el cache
    if city in cache:
        print(f"Usando datos cacheados para {city}.")
        data = cache[city]
    else:
        try:
            url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)

            # Verificación de errores en la respuesta
            if response.status_code == 200:
                data = response.json()
                # Almacenar los resultados en el cache
                cache[city] = data
            else:
                if response.status_code == 404:
                    print(f"Ubicación no encontrada: {city}. Verifica la ortografía y vuelve a intentarlo.")
                else:
                    print(f"Error al obtener los datos de la API. Código de estado: {response.status_code}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Error en la conexión a la API: {e}")
            return

    main = data['main']
    weather = data['weather'][0]

    # Traducir la descripción del clima
    descripcion_clima = traducir_clima(weather['description'])

    if format_output == "json":
        print(json.dumps(data, indent=4))
    elif format_output == "csv":
        with open(f'{city}_weather.csv', 'w', newline='') as csvfile:
            fieldnames = ['Ciudad', 'Clima', 'Temperatura', 'Humedad']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'Ciudad': city,
                'Clima': descripcion_clima,
                'Temperatura': f"{main['temp']}°C",
                'Humedad': f"{main['humidity']}%"
            })
        print(f"Datos guardados en {city}_weather.csv")
    else:
        print(f"Clima en {city}: {descripcion_clima}")
        print(f"Temperatura: {main['temp']}°C")
        print(f"Humedad: {main['humidity']}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consulta el clima de una o más ciudades.")
    parser.add_argument("Ciudades", nargs="+", help="Nombres de las ciudades (Ej. Asuncion, Madrid, Londres)")
    parser.add_argument("--format", choices=["json", "csv", "text"], default="text", help="Formato de salida (json, csv, text)")
    args = parser.parse_args()

    # Iterar sobre todas las ciudades proporcionadas
    for ciudad in args.Ciudades:
        get_weather(ciudad, args.format)
