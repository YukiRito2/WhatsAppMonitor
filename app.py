import json
from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import threading
import time
from datetime import date
import os

app = Flask(__name__)
CORS(app, resources={r"/activity_log": {"origins": "*"}})

# Archivo donde se almacenarán los registros
activity_log_file = "activity_log.json"
monitoring_started = False  # Variable de control para evitar múltiples hilos


# Función para cargar registros de activity_log desde el archivo JSON
def load_activity_log():
    if os.path.exists(activity_log_file):
        with open(activity_log_file, "r") as file:
            return json.load(file)
    return []


# Función para guardar activity_log en el archivo JSON
def save_activity_log():
    with open(activity_log_file, "w") as file:
        json.dump(activity_log, file, indent=4)


# Cargar los registros al iniciar la aplicación
activity_log = load_activity_log()


# Función de monitoreo de WhatsApp
def monitor_whatsapp(contact_name):
    service = Service("C:\\SeleniumDrivers\\chromedriver-win64\\chromedriver.exe")
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=C:\\SeleniumDrivers\\chrome-data")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    driver.get("https://web.whatsapp.com")
    input("Escanea el código QR y presiona Enter para continuar...")

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        )
    )

    search_box = driver.find_element(
        By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'
    )
    search_box.clear()
    search_box.send_keys(contact_name)
    time.sleep(2)

    try:
        contact = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f'//span[@title="{contact_name}"]')
            )
        )
        contact.click()
    except Exception as e:
        print(f"No se pudo encontrar el contacto {contact_name}. Error: {e}")
        return

    last_status = None
    connect_time = None

    try:
        while True:
            try:
                online_status = driver.find_element(
                    By.XPATH, '//span[@title="en línea"]'
                )
                if last_status != "Online":
                    # Restar 3 segundos para reflejar el retraso de conexión
                    connect_time = datetime.now() - timedelta(seconds=3)
                    last_status = "Online"
                    print(
                        f"{contact_name} se conectó en (ajustado): {connect_time.strftime('%H:%M:%S')}"
                    )
            except:
                if last_status == "Online":
                    # Restar 5 segundos para reflejar el retraso de desconexión
                    disconnect_time = datetime.now() - timedelta(seconds=6)
                    duration = str(disconnect_time - connect_time).split(".")[0]
                    new_record = {
                        "contact": contact_name,
                        "online": connect_time.strftime("%I:%M:%S %p"),
                        "offline": disconnect_time.strftime("%I:%M:%S %p"),
                        "duration": str(duration),
                        "date": (
                            "Today"
                            if connect_time.date() == date.today()
                            else connect_time.strftime("%b %d")
                        ),
                    }
                    activity_log.append(new_record)
                    save_activity_log()  # Guarda el registro actualizado en el archivo
                    print(
                        f"{contact_name} se desconectó en (ajustado): {disconnect_time.strftime('%H:%M:%S')}"
                    )
                    print(f"Duración de la conexión (ajustada): {duration}")
                    last_status = "Offline"

            time.sleep(5)

    except KeyboardInterrupt:
        print("Monitoreo terminado.")
    finally:
        driver.quit()


@app.route("/activity_log", methods=["GET"])
def get_activity_log():
    if os.path.exists(activity_log_file):
        with open(activity_log_file, "r") as file:
            data = json.load(file)
    else:
        data = []
    return jsonify(data)


def start_monitoring():
    global monitoring_started
    if not monitoring_started:
        monitoring_started = True
        threading.Thread(target=monitor_whatsapp, args=("Andrés Tc",)).start()


if __name__ == "__main__":
    start_monitoring()
    app.run()
