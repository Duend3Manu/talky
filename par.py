import requests
from bs4 import BeautifulSoup
import sys

# Configura la salida a UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# URL de la página que deseas extraer
url = 'https://redgol.cl/resultados/futbol/competencias/campeonato-nacional/c8b5e107-50d8-445c-99b0-57c3b5989ec1/calendario?stage_id=a4e891ac-2d38-4aed-bac6-89b084a2bbce&week=30'

# Realizamos la solicitud GET a la página
response = requests.get(url)

# Verificamos que la solicitud fue exitosa
if response.status_code == 200:
    # Decodificamos el contenido con 'latin1'
    soup = BeautifulSoup(response.content.decode('latin1'), 'html.parser')

    # Encontramos todas las secciones del calendario
    calendar_dates = soup.find_all('p', class_='jsx-1253012879 calendar__content__date calendar__content__date--center')
    
    results = []
    for date in calendar_dates:
        match_date = date.find('span', class_='jsx-1253012879').text.strip()
        match_date = match_date.encode('latin1').decode('utf-8')
        results.append(f"**Fecha: {match_date}**\n")
        
        # Extraemos la información de los partidos de cada fecha
        match_section = date.find_next_sibling('ul', class_='jsx-1253012879 calendar-list')
        if match_section:
            matches = match_section.find_all('li', class_='jsx-1253012879 calendar-list__container')
            
            for match in matches:
                home_team_element = match.find('span', title=True)
                away_team_element = match.find('div', class_='jsx-2473550862 match-team reverse').find('span', title=True)
                time_element = match.find('span', class_='jsx-894737674')
                score_element = match.find('div', class_='match-item-list__item__score')
                
                home_team = home_team_element.text.strip() if home_team_element else "N/A"
                away_team = away_team_element.text.strip() if away_team_element else "N/A"
                time = time_element.text.strip() if time_element else "N/A"
                
                if score_element:
                    home_score = score_element.find('span', class_='match-item-list__score match-item-list__score--left').text.strip()
                    away_score = score_element.find('span', class_='match-item-list__score match-item-list__score--right').text.strip()
                    result = f"{home_score} - {away_score}"
                else:
                    result = "Pendiente"
                
                home_team = home_team.encode('latin1').decode('utf-8')
                away_team = away_team.encode('latin1').decode('utf-8')
                
                results.append(f"* {home_team} vs {away_team} a las {time}, Resultado: {result}\n")

    print("\n".join(results))
else:
    print(f"Error: {response.status_code}")
