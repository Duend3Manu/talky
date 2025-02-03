# -*- coding: utf-8 -*-
import os
import sys
import csv
import argparse
import requests
from bs4 import BeautifulSoup

def save_information_to_csv(informacion):
    with open('patente.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in informacion.items():
            writer.writerow([key, value])

def extract_information(html):
    soup = BeautifulSoup(html, 'html.parser')
    informacion_propietario = {}
    informacion_vehicular = {}
    multas_transito = ""
    informacion_revision_tecnica = {}
    permiso_circulacion = {}
    soap_seguro_obligatorio = {}
    informacion_transporte_publico = {}
    restriccion_vehicular = {}
    # Aquí debes agregar el código para encontrar y extraer la información del HTML
    return (informacion_propietario, informacion_vehicular, multas_transito,
            informacion_revision_tecnica, permiso_circulacion, soap_seguro_obligatorio,
            informacion_transporte_publico, restriccion_vehicular)

def print_information(informacion):
    for key, value in informacion.items():
        print(f"{key}: {value}")

def main():
    parser = argparse.ArgumentParser(description='Buscar información de una patente en Chile.')
    parser.add_argument('patente', type=str, help='Patente a buscar')
    args = parser.parse_args()

    url = f"https://www.patentechile.com/buscar-patente/{args.patente}"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        informacion = extract_information(html)
        save_information_to_csv(informacion)
        print_information(informacion)
    else:
        print("Error al acceder a la página web.")

if __name__ == "__main__":
    main()
