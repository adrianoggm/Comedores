import subprocess
import sys
import os

def run_script(script_name):
    try:
        # Ejecuta el script usando el intérprete de Python actual
        result = subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        print(f"Salida de {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script_name}:\n{e.stderr}")

def borrar_archivo(file_name):
    """
    Borra un archivo si existe.
    """
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Archivo '{file_name}' borrado exitosamente.")
        else:
            print(f"El archivo '{file_name}' no existe, no se necesita borrar.")
    except Exception as e:
        print(f"Error al intentar borrar el archivo '{file_name}': {e}")

def main():
    # Ejecutar app.py
    print("Ejecutando app.py...")
    run_script("app.py")
    print("-" * 40)
    
   
    
    # Ejecutar procesar_menu.py
    print("Ejecutando procesar_menu.py...")
    run_script("procesar_menu.py")
    print("-" * 40)
     # Borrar contenido_pagina.txt
    borrar_archivo("contenido_pagina.txt")

if __name__ == "__main__":
    main()
