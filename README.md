# Monitoreo de Conexión en WhatsApp Web con Selenium

Este proyecto utiliza **Selenium** para monitorear el estado de conexión de un contacto en **WhatsApp Web** mediante **Google Chrome**. El programa registra el tiempo de conexión y desconexión, proporcionando la duración de cada sesión.

## Requisitos

### Prerrequisitos
1. **Python 3.x**: [Descargar Python](https://www.python.org/downloads/).
2. **Google Chrome**: [Descargar Chrome](https://www.google.com/intl/es/chrome/).
3. **ChromeDriver**: Descarga [ChromeDriver]([https://sites.google.com/chromium.org/driver/](https://googlechromelabs.github.io/chrome-for-testing/)) compatible con tu versión de Chrome e instálalo en `C:\SeleniumDrivers\`.

### Instalación de Dependencias
Instala Selenium ejecutando:

## Configuración Inicial

1. **Configura ChromeDriver**: Asegúrate de que el archivo `chromedriver.exe` esté en la carpeta `C:\SeleniumDrivers\`. Si está en otra ubicación, actualiza la ruta en el script.
2. Para instalar Selenium, abre una terminal y ejecuta el siguiente comando:`pip install selenium`

3. **Actualiza el Nombre del Contacto**: En el script, reemplaza `"Nombre del contacto"` con el nombre del contacto que deseas monitorear.

   ```python
   contact_name = "Nombre del contacto"

