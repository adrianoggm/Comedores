import re
from datetime import datetime

def procesar_menu():
    # Obtener la fecha actual
    fecha_actual = datetime.now()
    dia_actual = fecha_actual.day
    mes_actual = fecha_actual.month
    anio_actual = fecha_actual.year

    # Diccionario para mapear meses en español a números
    meses = {
        'ENERO': '01',
        'FEBRERO': '02',
        'MARZO': '03',
        'ABRIL': '04',
        'MAYO': '05',
        'JUNIO': '06',
        'JULIO': '07',
        'AGOSTO': '08',
        'SEPTIEMBRE': '09',
        'OCTUBRE': '10',
        'NOVIEMBRE': '11',
        'DICIEMBRE': '12'
    }

    # Leer el contenido del archivo
    try:
        with open("contenido_pagina.txt", "r", encoding='utf-8') as f:
            contenido = f.read()
    except FileNotFoundError:
        print("El archivo 'contenido_pagina.txt' no se encontró en el directorio actual.")
        return

    # Normalizar el contenido: reemplazar múltiples espacios por uno solo
    contenido = re.sub(r'\s+', ' ', contenido)

    # Expresión regular para encontrar cada día con sus menús
    patron_dia = re.compile(
        r'(?P<dia_semana>LUNES|MARTES|MIÉRCOLES|JUEVES|VIERNES|SÁBADO|DOMINGO),\s*(?P<dia>\d{1,2})\s*DE\s*(?P<mes>\w+)\s*DE\s*(?P<anio>\d{4})\s*MENÚ\s*1\s*ALÉRGENOS\s*PRIMERO\s*(?P<primer_plato>.*?)\s*SEGUNDO\s*(?P<segundo_plato>.*?)\s*POSTRE\s*(?P<postre>.*?)\s*MENÚ\s*2\s*ALÉRGENOS\s*PRIMERO\s*(?P<primer_plato2>.*?)\s*SEGUNDO\s*(?P<segundo_plato2>.*?)\s*POSTRE\s*(?P<postre2>.*?)\s*CONSULTAR\s*INGREDIENTES\s*SEMANALES',
        re.IGNORECASE
    )

    # Encontrar todas las coincidencias de días con menús
    matches = patron_dia.finditer(contenido)

    encontrado = False  # Bandera para indicar si se encontró la fecha actual

    # Procesar cada coincidencia
    for match in matches:
        dia_semana = match.group('dia_semana').capitalize()
        dia = int(match.group('dia'))
        mes_texto = match.group('mes').upper()
        mes = meses.get(mes_texto, 0)  # 0 si el mes no se encuentra
        anio = int(match.group('anio'))

        # Verificar si la fecha coincide con la fecha actual
        if dia == dia_actual and mes == f"{mes_actual:02}" and anio == anio_actual:
            # Formatear la fecha
            fecha_formateada = f"{dia:02}/{mes}/{anio} - {dia_semana}"

            # Extraer los platos, eliminando posibles caracteres no deseados
            primer_plato = limpiar_texto(match.group('primer_plato'))
            segundo_plato = limpiar_texto(match.group('segundo_plato'))
            postre = limpiar_texto(match.group('postre'))

            primer_plato2 = limpiar_texto(match.group('primer_plato2'))
            segundo_plato2 = limpiar_texto(match.group('segundo_plato2'))
            postre2 = limpiar_texto(match.group('postre2'))

            # Mostrar el menú formateado
            print(fecha_formateada)
            print("Menú 1")
            print(f"1° plato: {primer_plato}")
            print(f"2° plato: {segundo_plato}")
            print(f"Postre: {postre}\n")

            print("Menú 2")
            print(f"1° plato: {primer_plato2}")
            print(f"2° plato: {segundo_plato2}")
            print(f"Postre: {postre2}\n")
            print("-" * 40)  # Separador entre días

            encontrado = True
            break  # Salir del bucle después de encontrar la fecha actual

    if not encontrado:
        print("No se encontraron menús para la fecha de hoy.")

def limpiar_texto(texto):
    """
    Función para limpiar el texto extraído, eliminando caracteres especiales
    y espacios innecesarios.
    """
    # Eliminar caracteres no alfabéticos excepto espacios
    texto = re.sub(r'[^A-ZÁÉÍÓÚÜÑ ]+', '', texto)
    # Reemplazar múltiples espacios por uno solo
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

if __name__ == "__main__":
    procesar_menu()
