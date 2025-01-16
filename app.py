import re
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import locale

def configurar_logging():
    """
    Configura el sistema de logging para registrar información y errores en 'app.log'.
    """
    logging.basicConfig(
        filename='app.log',
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def configurar_locale():
    """
    Configura el locale a español.
    """
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        logging.info("Locale configurado a 'es_ES.UTF-8'.")
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES')
            logging.info("Locale configurado a 'es_ES'.")
        except locale.Error as e:
            logging.error("No se pudo configurar el locale a español. Asegúrate de que 'es_ES.UTF-8' esté instalado en tu sistema.")
            raise e

def obtener_menu_del_dia_selenium():
    configurar_logging()
    configurar_locale()

    # Obtener la fecha actual
    hoy = datetime.now()
    dia_semana_en_es = hoy.strftime('%A').upper()
    logging.info(f"Fecha actual: {hoy.strftime('%d/%m/%Y')} - {dia_semana_en_es.capitalize()}")

    # Formatear la fecha para la salida
    fecha_menu_formateada = hoy.strftime('%d/%m/%Y') + f' - {dia_semana_en_es.capitalize()}'

    # Configurar Selenium WebDriver con opciones
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Inicializar WebDriver usando webdriver_manager
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        logging.info("Chrome WebDriver inicializado correctamente.")
    except Exception as e:
        logging.error(f"Error al inicializar ChromeDriver: {e}")
        return

    try:
        driver.get('https://scu.ugr.es')
        logging.info("Página 'https://scu.ugr.es' cargada.")

        # Esperar hasta que un elemento específico esté presente
        # Por ejemplo, esperar hasta que el menú esté presente
        # Debes reemplazar 'elemento_identificador' con un identificador real de la página
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            logging.info("Contenido de la página cargado completamente.")
        except Exception as e:
            logging.warning(f"Tiempo de espera excedido al cargar la página: {e}")

        # Obtener el HTML renderizado
        html = driver.page_source
    except Exception as e:
        logging.error(f"Error al cargar la página con Selenium: {e}")
        return
    finally:
        driver.quit()
        logging.info("Chrome WebDriver cerrado.")

    # Parsear el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Obtener todo el texto de la página en mayúsculas para facilitar la búsqueda
    texto_pagina = soup.get_text(separator='\n', strip=True).upper()

    # Guardar el contenido completo de la página
    try:
        with open("contenido_pagina.txt", "w", encoding='utf-8') as f:
            f.write(texto_pagina)
        logging.info("El contenido de la página se ha guardado en 'contenido_pagina.txt'.")
    except Exception as e:
        logging.error(f"Error al escribir en 'contenido_pagina.txt': {e}")
        return

    # Buscar el encabezado del día actual usando una expresión regular
    patron_dia = rf'{dia_semana_en_es}, \d{{1,2}} DE \w+ DE \d{{4}}'
    match_dia = re.search(patron_dia, texto_pagina)
    if not match_dia:
        logging.error("No se encontró el encabezado del día actual en el texto de la página.")
        return

    # Extraer el texto desde el encabezado del día hasta el siguiente encabezado de día
    indice_inicio = match_dia.end()
    siguiente_dia = None
    # Lista de días en español en mayúsculas
    dias_semana = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO']

    # Encontrar el siguiente día para determinar el final del contenido del día actual
    for dia in dias_semana:
        if dia != dia_semana_en_es:
            patron_siguiente = rf'\n{dia}, \d{{1,2}} DE \w+ DE \d{{4}}'
            match_siguiente = re.search(patron_siguiente, texto_pagina[indice_inicio:])
            if match_siguiente:
                indice_fin = indice_inicio + match_siguiente.start()
                siguiente_dia = match_siguiente.group()
                break

    if siguiente_dia:
        contenido_dia = texto_pagina[indice_inicio:indice_fin]
        logging.info(f"Contenido del día actual extraído hasta el siguiente día: {siguiente_dia}")
    else:
        contenido_dia = texto_pagina[indice_inicio:]
        logging.info("Contenido del día actual extraído hasta el final de la página.")

    # Guardar el contenido del día para inspección
    try:
        with open("contenido_dia.txt", "w", encoding='utf-8') as f:
            f.write(contenido_dia)
        logging.info("El contenido del día actual se ha guardado en 'contenido_dia.txt'.")
    except Exception as e:
        logging.error(f"Error al escribir en 'contenido_dia.txt': {e}")
        return

    # Extraer Menú 1 y Menú 2 usando expresiones regulares
    menu_1 = re.search(r'MENÚ 1\s+ALÉRGENOS\s+(.*?)\s+MENÚ 2', contenido_dia, re.DOTALL)
    menu_2 = re.search(r'MENÚ 2\s+ALÉRGENOS\s+(.*?)\s+CONSULTAR INGREDIENTES SEMANALES', contenido_dia, re.DOTALL)

    def procesar_menu(menu_texto):
        platos = {}
        # Buscar cada tipo de plato usando expresiones regulares
        primero = re.search(r'PRIMERO\s+([^\n]+)', menu_texto)
        segundo = re.search(r'SEGUNDO\s+([^\n]+)', menu_texto)
        acompañamiento = re.search(r'ACOMPAÑAMIENTO\s+([^\n]+)', menu_texto)
        postre = re.search(r'POSTRE\s+([^\n]+)', menu_texto)

        if primero:
            platos['1° plato'] = primero.group(1).strip()
        if segundo:
            platos['2° plato'] = segundo.group(1).strip()
        if acompañamiento:
            platos['Acompañamiento'] = acompañamiento.group(1).strip()
        if postre:
            platos['Postre'] = postre.group(1).strip()
        return platos

    # Procesar Menú 1
    if menu_1:
        menu1 = procesar_menu(menu_1.group(1))
        logging.info("Menú 1 procesado correctamente.")
    else:
        logging.warning("No se encontró Menú 1 para el día actual.")
        menu1 = {}

    # Procesar Menú 2
    if menu_2:
        menu2 = procesar_menu(menu_2.group(1))
        logging.info("Menú 2 procesado correctamente.")
    else:
        logging.warning("No se encontró Menú 2 para el día actual.")
        menu2 = {}

    # Construir la salida
    try:
        with open("menus_formateados.txt", "w", encoding='utf-8') as f:
            f.write(fecha_menu_formateada + "\n")
            f.write("\nMenú 1\n")
            for tipo, plato in menu1.items():
                f.write(f"{tipo}: {plato}\n")
            f.write("\nMenú 2\n")
            for tipo, plato in menu2.items():
                f.write(f"{tipo}: {plato}\n")
            logging.info("Menús formateados guardados en 'menus_formateados.txt'.")
    except Exception as e:
        logging.error(f"Error al escribir en 'menus_formateados.txt': {e}")
        return

    # También imprimir los menús en la consola
    print(fecha_menu_formateada)
    print("\nMenú 1")
    for tipo, plato in menu1.items():
        print(f"{tipo}: {plato}")
    print("\nMenú 2")
    for tipo, plato in menu2.items():
        print(f"{tipo}: {plato}")

if __name__ == "__main__":
    try:
        obtener_menu_del_dia_selenium()
    except Exception as e:
        logging.critical(f"Error crítico en el script: {e}")
