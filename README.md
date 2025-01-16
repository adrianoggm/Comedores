# Comedores

Este proyecto contiene scripts en Python que extraen información del menú del día actual desde la web de comedores de la **Universidad de Granada** utilizando Selenium.

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalados los siguientes requisitos:

### 1. Instalaciones básicas
- Python 3.8 o superior
- Google Chrome (versión actualizada)

### 2. Dependencias de Python

Instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` debe contener:

```plaintext
selenium
webdriver-manager
beautifulsoup4
```

### 3. Configuración de Locale (opcional)

El script intenta configurar el locale a español (`es_ES.UTF-8`) para mostrar correctamente los días de la semana. Si estás en un sistema basado en Unix/Linux, asegúrate de que el locale esté instalado. Puedes verificarlo ejecutando:

```bash
locale -a
```

Si no ves `es_ES.UTF-8`, instala el locale con:

```bash
sudo locale-gen es_ES.UTF-8
sudo update-locale
```

En Windows, la configuración regional depende del idioma del sistema operativo.

---

## Uso

El proyecto incluye dos scripts principales:

1. **`app.py`**: Este script utiliza Selenium para scrappear la web de los comedores de la UGR y guarda el contenido de la página en un archivo llamado `contenido_pagina.txt`.
2. **`procesar_menu.py`**: Procesa el archivo `contenido_pagina.txt` para extraer el menú del día actual.
3. **`launch.py`**: Un script que automatiza la ejecución de `app.py` seguido de `procesar_menu.py`.

### Instrucciones de uso

1. Clona el repositorio en tu máquina local:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd comedores
   ```

2. Ejecuta el script `launch.py` para realizar todo el proceso automáticamente:

   ```bash
   python launch.py
   ```

3. Revisa los archivos generados:
   - `contenido_pagina.txt`: Contiene el texto completo de la página scrapeada.
   - `contenido_dia.txt`: Contiene el contenido específico del menú del día actual.
   - `menus_formateados.txt`: Contiene el menú del día procesado y formateado.

### Configuración del Navegador con Selenium

El proyecto utiliza Selenium para interactuar con la página web. Para configurar Selenium:

1. **Instalación de ChromeDriver**:
   - El script utiliza la librería `webdriver-manager`, que descarga y configura automáticamente la versión correcta de ChromeDriver.

2. **Opciones del Navegador**:
   - El script ejecuta Google Chrome en modo **headless** (sin interfaz gráfica) por defecto.
   - Si deseas ver el navegador en acción, edita el archivo `app.py` y comenta la línea:
     ```python
     chrome_options.add_argument("--headless")
     ```

3. **Ubicación del Driver**:
   - Si prefieres manejar manualmente el ChromeDriver, descárgalo desde [aquí](https://sites.google.com/chromium.org/driver/) y colócalo en la carpeta del proyecto.
   - Luego, ajusta el siguiente fragmento en `app.py`:
     ```python
     driver = webdriver.Chrome(service=Service('./chromedriver'))
     ```

### Archivos Generados

- **`contenido_pagina.txt`**: Texto completo de la página scrapeada.
- **`contenido_dia.txt`**: Menú del día extraído.
- **`menus_formateados.txt`**: Menú del día procesado y formateado para fácil lectura.
- **`app.log`**: Registro de las actividades y errores de `app.py`.
- **`launch.log`**: Registro de las actividades y errores de `launch.py`.

---

## Estructura del Proyecto

```plaintext
.
├── app.py                 # Script para scrappear la web de comedores UGR
├── procesar_menu.py       # Script para procesar el menú extraído
├── launch.py              # Script para ejecutar todo el proceso
├── contenido_pagina.txt   # Salida: contenido scrapeado de la página
├── contenido_dia.txt      # Salida: contenido del menú del día
├── menus_formateados.txt  # Salida: menú procesado y formateado
├── app.log                # Log de app.py
├── launch.log             # Log de launch.py
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Instrucciones del proyecto
```

---

## Problemas Comunes

1. **Error de ChromeDriver**:
   - Asegúrate de que Google Chrome esté instalado y actualizado.
   - Verifica que la versión de ChromeDriver coincida con tu versión de Chrome (esto se maneja automáticamente con `webdriver-manager`).

2. **Locale no configurado**:
   - Si obtienes errores relacionados con el locale, revisa la sección de configuración de locale.

3. **Errores al scrappear**:
   - Asegúrate de que la página `https://scu.ugr.es` esté accesible.
   - Revisa los archivos de log (`app.log` y `launch.log`) para obtener más detalles sobre el error.

---

## Contribuciones

Si deseas contribuir al proyecto:

1. Haz un fork del repositorio.
2. Crea una rama para tu feature/bugfix:
   ```bash
   git checkout -b mi-feature
   ```
3. Envía un pull request describiendo tus cambios.
