import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initialize_driver(edge_driver_path):
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    edge_options.add_argument("--headless")
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Edge(service=Service(edge_driver_path), options=edge_options)
    return driver

def load_page(driver, url):
    driver.get(url)

def search_by_rut(driver, rut):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "rut")))
        rut_input = driver.find_element(By.ID, "rut")
        rut_input.send_keys(rut)

        search_button = driver.find_element(By.ID, "rut-btn")
        search_button.click()

        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".row-tabla-deuda")))
        return driver.find_elements(By.CSS_SELECTOR, ".row-tabla-deuda")
    
    except TimeoutException as e:
        raise TimeoutException(f"Tiempo de espera agotado al buscar un elemento: {e}")
    except NoSuchElementException as e:
        raise NoSuchElementException(f"Elemento no encontrado: {e}")

def process_debts(deudas):
    table_rows = []
    for deuda in deudas:
        try:
            concesionaria = deuda.find_element(By.CSS_SELECTOR, ".concesionaria").text.strip()
            rut_deuda = deuda.find_element(By.CSS_SELECTOR, ".rut").text.strip()
            vence = deuda.find_element(By.CSS_SELECTOR, ".vence").text.strip()
            monto = deuda.find_element(By.CSS_SELECTOR, ".monto").text.strip()

            table_row = f"| {concesionaria:<30} | {rut_deuda:<12} | {vence:<8} | {monto:<34} |"
            table_rows.append(table_row)
        
        except NoSuchElementException as e:
            print(f"Error al procesar una deuda: {e}")

    return table_rows

def print_table(table_rows):
    if table_rows:
        print("| Concesionaria                  | RUT         | Vence    | Observaciones                      |")
        print("|--------------------------------|-------------|----------|------------------------------------|")
        for row in table_rows:
            print(row)

def search_tag_total(rut):
    edge_driver_path = r'C:\bots\Talky-Bot\Archivos\edge\msedgedriver.exe'
    url = "https://unired.tagtotal.cl/"

    try:
        with initialize_driver(edge_driver_path) as driver:
            load_page(driver, url)
            deudas = search_by_rut(driver, rut)
            if deudas:
                table_rows = process_debts(deudas)
                print_table(table_rows)

    except Exception as e:
        print(f"Error al ejecutar la búsqueda: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python tag.py <RUT>")
        sys.exit(1)

    rut = sys.argv[1]
    search_tag_total(rut)
