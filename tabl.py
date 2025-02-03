import requests
from bs4 import BeautifulSoup
import csv

# URL de la página
url = 'https://redgol.cl/resultados/futbol/competencias/campeonato-nacional/c8b5e107-50d8-445c-99b0-57c3b5989ec1/clasificacion'

# Realizar la solicitud HTTP a la URL
response = requests.get(url)

# Crear el objeto BeautifulSoup para parsear el contenido HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Buscar las filas de la tabla
rows = soup.select('.jsx-816981968.tournament-ranking-item')

# Nombre del archivo CSV
filename = 'clasificacion.csv'

# Escribir los datos en el archivo CSV
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    for row in rows:
        position = row.find('span', class_='tournament-ranking-item__position').text.strip()
        team = row.find_all('span', class_='jsx-816981968')[1].text.strip().replace('  ', ' ')
        point = row.find('span', class_='tournament-ranking-item__team-pts').text.strip()
        writer.writerow([f"{position} - {team} - {point}"])

print(f'Datos guardados en {filename}')
