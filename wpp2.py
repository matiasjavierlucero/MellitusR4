from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import os
import sys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import socket
# mensaje que quieres enviar
message_text = 'ULTIMO INTENTO DUPLICADO sin QR John Doe! DNI:33254885 TEL: 54-358-1234567 tu turno ha sido reservado para el dia 24/12/19 a las 10hs con el Dr Mengueche'

no_of_message = 1  # no. de tiempo desea que el mensaje sea enviado
# lista de números de teléfono puede ser de cualquier longitud
mobile_num_list = [543584185852, 543584319481]


def element_presence(by, xpath, time):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(driver, time).until(element_present)


def is_connected():
    try:
        # conectarse al host: nos dice si el host es en realidad
        # accesible
        socket.create_connection(("www.google.com", 80))
        return True
    except:
        is_connected()

profile = FirefoxProfile('/home/alfonso/.mozilla/firefox/4sj3b4y2.Selenium')
driver = webdriver.Firefox(profile)
driver.maximize_window()
print ('Opening Browser!!'
''' Using Firefox Browser and Opening web.whatsapp.com ''')
driver.get('https://web.whatsapp.com')

sleep(30)  # esperar tiempo para escanear el código en segundo


def send_whatsapp_msg(phone_no, text):
    driver.get(
        "https://web.whatsapp.com/send?phone={}&source=&data=#".format(phone_no))
    try:
        driver.switch_to_alert().accept()
    except Exception as e:
        pass

    try:
        element_presence(
            By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]', 30)
        txt_box = driver.find_element(
            By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        global no_of_message
        for x in range(no_of_message):
            txt_box.send_keys(text)
            txt_box.send_keys("\n")

    except Exception as e:
        print("invailid phone no :"+str(phone_no))


for mobile_num in mobile_num_list:
    try:
        send_whatsapp_msg(mobile_num, message_text)

    except Exception as e:
        sleep(10)
        is_connected()

# driver.close()