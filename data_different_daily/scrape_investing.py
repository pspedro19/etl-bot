from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd
import os

def configurar_driver(download_dir, chrome_driver_path, user_data_dir, profile_dir):
    """
    Configura el driver de Chrome con los perfiles y opciones especificadas
    """
    chrome_options = webdriver.ChromeOptions()
    
    # Configuración de preferencias
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    
    # Agregar opciones experimentales y argumentos
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_dir}")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Configurar el servicio
    service = Service(executable_path=chrome_driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def scrape_table(driver, url, wait_time=10):
    """
    Extrae datos de la tabla de una URL específica, detectando automáticamente el ID de la tabla
    """
    driver.get(url)
    wait = WebDriverWait(driver, wait_time)

    # Extraer el ID numérico de la URL
    table_id = url.split('-')[-1]  # Obtiene el número del final de la URL

    try:
        # Esperar a que la tabla esté presente usando un XPath más general
        table_xpath = f"//table[contains(@id, 'eventHistoryTable')]"
        wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))

        # Hacer clic en "Show More" hasta que desaparezca
        while True:
            try:
                show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Show more']")))
                driver.execute_script("arguments[0].click();", show_more_button)
                time.sleep(2)  # Esperar que cargue el contenido
            except TimeoutException:
                print("No hay más 'Show more' que hacer clic.")
                break

        # Extraer datos de la tabla usando un XPath más general
        table_rows = driver.find_elements(By.XPATH, f"//table[contains(@id, 'eventHistoryTable')]/tbody/tr")
        
        if not table_rows:
            print(f"No se encontraron datos en la tabla para la URL: {url}")
            return []

        data = []
        for row in table_rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            data.append([col.text for col in cols][:-1])  # Omitimos la última columna

        return data

    except TimeoutException:
        print(f"Tiempo de espera agotado al buscar la tabla en {url}")
        return []
    except Exception as e:
        print(f"Error al extraer datos de la tabla: {str(e)}")
        return []

def save_to_csv(data, url, output_dir):
    """
    Guarda los datos en un archivo CSV
    """
    columns = ["Release Date", "Time", "Actual", "Forecast", "Previous"]
    df = pd.DataFrame(data, columns=columns)
    
    # Crear nombre de archivo y ruta completa
    csv_filename = f"{url.split('/')[-1]}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    # Guardar el archivo
    df.to_csv(csv_path, index=False)
    print(f"Datos guardados en {csv_path}")

def main():
    # Configuración de rutas
    base_dir = os.path.dirname(os.path.abspath(__file__))
    chrome_driver_path = "C:/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    download_dir = os.path.join(base_dir, "output")
    user_data_dir = os.path.join(base_dir, "C:/Users/Nabucodonosor/AppData/Local/Google/Chrome/User Data")
    profile_dir = "Profile 2"
    
    # Crear directorio de descargas si no existe
    os.makedirs(download_dir, exist_ok=True)

    # URLs a procesar
    urls = [
        "https://www.investing.com/economic-calendar/colombian-gdp-1151",
        "https://www.investing.com/economic-calendar/colombian-interest-rate-decision-497",
        "https://www.investing.com/economic-calendar/colombian-cpi-1197",
        "https://www.investing.com/economic-calendar/interest-rate-decision-168"
    ]

    try:
        # Configurar y iniciar el driver
        driver = configurar_driver(download_dir, chrome_driver_path, user_data_dir, profile_dir)

        # Procesar cada URL
        for url in urls:
            try:
                print(f"\nProcesando URL: {url}")
                data = scrape_table(driver, url)
                if data:
                    save_to_csv(data, url, download_dir)
                else:
                    print(f"No se pudieron obtener datos para: {url}")
            except Exception as e:
                print(f"Error procesando {url}: {str(e)}")

    except Exception as e:
        print(f"Error general: {str(e)}")
    
    finally:
        # Cerrar el driver
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()