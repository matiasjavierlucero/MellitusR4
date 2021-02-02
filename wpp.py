# ACÁ SON TODOS IMPORT. VER PARA WINDOWS
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import socket
from datetime import date
import datetime
import time



# from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response, jsonify
# from flask_mysqldb import MySQL,MySQLdb
# import bcrypt
# import os 
# import json
# from datetime import datetime
# import webbrowser




# # url = 'http://127.0.0.1:3333/enviarWhatsapps'

# # # Open URL in a new tab, if a browser window is already open.
# # webbrowser.open_new_tab(url)



# app = Flask (__name__)

# # MySQL Connection config
# app.config['MYSQL_HOST'] = '160.153.51.194'
# app.config['MYSQL_USER'] = 'root2'
# app.config['MYSQL_PASSWORD'] = 'mellitus'
# app.config['MYSQL_DB'] = 'Mellitusdb'


# mysql = MySQL(app)

import pymysql

# Open database connection
db = pymysql.connect("160.153.51.194","root2","mellitus","Mellitusdb" )

# prepare a cursor object using cursor() method
cur = db.cursor()

# execute SQL query using execute() method.
cur.execute("""SELECT turnos.IdTur, turnos.FecTur, turnos.HorTur, turnos.HorFtur, turnos.EstTur,
                proesp.IdProEsp, proesp.IdPro, proesp.IdEsp, proesp.MeProEsp,
                profesional.IdPro, profesional.NomPro, profesional.DniPro,
                pacplan.IdPacPlan, pacplan.IdPac, pacplan.IdPlan,
                paciente.IdPac, paciente.NomPac, paciente.DniPac, paciente.TelPac, paciente.IdUs,
                especialidad.IdEsp, especialidad.NomEsp
                FROM (turnos
                INNER JOIN proesp
                ON proesp.IdProEsp = turnos.IdProEsp)
                INNER JOIN profesional
                ON profesional.IdPro = proesp.IdPro
                INNER JOIN pacplan
                ON pacplan.IdPacPlan = turnos.IdPacPlan
                INNER JOIN paciente
                ON paciente.IdPac = pacplan.IdPac
                INNER JOIN especialidad
                ON especialidad.IdEsp = proesp.IdEsp""")

# Fetch a single row using fetchone() method.
turnos = cur.fetchall()

# fechaTurno = str (turnos [18][1])
# horaITurno = str (turnos [18][2])
# horaFTurno = str (turnos [18][3])
# EstadoTurno = str (turnos [18][4])
# nombreProfesional = str (turnos [18][10])
# nombrePaciente = str (turnos [18][16])
# dniPaciente  = str (turnos [18][18])
# telefonoPaciente  = str (turnos [18][18])
# EspecialidadProfesional = str (turnos [18][21])
# msjFechaTurno = 'Fecha turno(Año-mes-dia): ' + fechaTurno
# msjHoraITurno = '.Hora inicio turno: ' + horaITurno + 'hs'
# msjHoraFTurno = '.                                                     Hora  fin turno: ' + horaFTurno + 'hs'
# msjEstadoTurno = ''
# msjNombreProfesional ='.                                                                  Profesional: ' + nombreProfesional
# msjNombrePaciente = '.                                                      nombre Paciente: ' + nombrePaciente
# msjDniPaciente  = '.                                                      DNI Paciente: ' + dniPaciente
# msjEspecialidadProfesional = '.                                                       Especialidad: ' + EspecialidadProfesional


# fechaHoy = str (date.today())
# fechaHoyFalsa = str (datetime.date(2020, 3, 22))
# fechaManana = str (date.today() + datetime.timedelta(days=1))
fechaMananaFalsa = str (datetime.date(2020, 3, 25))

prefijo = str (54)
turnosManana = []
# ACA CONSULTO LA DB Y METO EN UN ARRAY LOS TURNOS DE MANANA.
# OJO Q ESTOY USANDO FECHAS FALSAS, PARA PODER TRABAJR
for turno in turnos:
    if str (turno[1]) == fechaMananaFalsa:
        turnosManana.append (turno)
    else:
        # print ('no hay turnos para manana')
        pass
# print (turnosManana[0][2])

# disconnect from server
db.close()

# ////////////////////////////////////////////////////////////////////////////
no_of_message = 1  # Num de mensajes a enviar
# lista de números de teléfono
# 543584185852, 543584319481, 543584851168
# prefijo + telefonoPaciente

# esto sinceramente no se bien q hace, pero busca los paths al chrome driver y demas giladas
def element_presence(by, xpath, time):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(driver, time).until(element_present)

# acá hace un check de la conexión a internet
def is_connected():
    try:
        # conectarse al host: nos dice si el host es en realidad
        # accesible
        socket.create_connection(("www.google.com", 80))
        return True
    except:
        is_connected()

# para configurar el webdriver, en ooptions pasamos todos los parámetros
options = Options()

#  con add_argument metemos los argumentos. ESTO CAMBIA SUSTANCIALMENTE EN WINDOWS. HAY Q GOOGLEAR QUÉ RUTA USAR
options.add_argument('--user-data-dir=/home/alfonso/.config/chromium/') # En user-data-dir -> vamos a buscar DONDE se encuentran TODOS los perfiles de chromium (hay q crear 1 previamente) 
options.add_argument('--profile-directory=Profile 1') #Acá le indicamos QUÉ perfil usar. AL perfil le pones nombre selenium pero se guarda como profile 1,al ser el primero q creas(o no)
# options.add_argument("--headless") #CON ESTA LINEA HACES Q NO SE ABRA EL CHROMIUM
options.add_argument("--window-size=1,1")
# options.add_argument("--chrome.switches")
# options.add_argument("--disable-extensions")
# options.add_argument("--no-sandbox")
driver = webdriver.Chrome('/usr/bin/chromedriver', options=options) #acá ya corres el driver indicandole DONDE tenes instalado el chromedriver (VER WINDOWS-GOOGLEAR) Y le sumas las OPTIONS
driver.get("http://web.whatsapp.com") #acá la pagina q tiene q abrir
sleep(20)  # esperar tiempo para escanear el código en segundo
# esto para enviar el msj obviamente
salto = '//salto//'
for turnoManana in turnosManana:
    fechaTurno = str(datetime.datetime.strptime(str(turnoManana [1]), "%Y-%m-%d").strftime("%d-%m-%Y"))
    horaITurno = str(datetime.datetime.strptime(str(turnoManana [2]), "%H:%M:%S").strftime("%H:%M"))
    horaFTurno = str (turnoManana [3])
    EstadoTurno = str (turnoManana [4])
    nombreProfesional = str (turnoManana [10])
    nombrePaciente = str (turnoManana [16])
    dniPaciente  = str (turnoManana [17])
    telefonoPaciente  = str (turnoManana [18])
    EspecialidadProfesional = str (turnoManana [21])
    msjMellitus = '.      *<<<<<   Mellitus   >>>>>*      .'
    msjSaludo = 'Buenos días, clínica *Mellitus*  //salto//le recuerda su *Turno* para *mañana*:'
    msjFechaTurno = '*Fecha turno:* ' + fechaTurno + '.'
    msjHoraITurno = '*Hora turno:* ' + horaITurno + 'hs.'
    # msjHoraFTurno = '              .Hora  fin turno: ' + horaFTurno + 'hs' 
    # msjEstadoTurno = ''
    msjNombreProfesional = '*Profesional:* ' + nombreProfesional + '.'
    msjNombrePaciente = '*Paciente:* ' + nombrePaciente + '.'
    msjDniPaciente  = '*DNI Paciente:* ' + dniPaciente + '.'
    msjEspecialidadProfesional = '*Especialidad:* ' + EspecialidadProfesional + '.'
    msjOpcion = '*Responda* este mensaje con:'
    msjConfirmacion =' *SI* para *CONFIRMAR* turno,'
    msjCancelacion = '*NO* para *CANCELAR* turno'
    fechaHoy = str (date.today())
    fechaHoyFalsa = str (datetime.date(2020, 3, 22))
    fechaManana = str (date.today() + datetime.timedelta(days=1))
    fechaPasadoManana = str (date.today() + datetime.timedelta(days=2))
    fechaPasadoMananaFalsa = str (datetime.date(2020, 3, 24))
    message_text = salto + msjMellitus + salto + msjSaludo + salto + msjFechaTurno + salto + msjHoraITurno + salto + msjNombreProfesional + salto + msjEspecialidadProfesional + salto + msjNombrePaciente + salto + msjDniPaciente + salto +msjOpcion + salto + msjConfirmacion +salto +msjCancelacion + salto + msjMellitus    # mensaje que quieres enviar
    # EL primer numero es el de la secretaria, el 2do del paciente. Se conforma -> 
    # prefijo + telefonoPaciente
    #  543584319481 MATI
    mobile_num_list = [543584185852]
    print ('TURNO MAÑANA', turnoManana)
    
    def send_whatsapp_msg(phone_no, text):
        driver.get(
            "https://web.whatsapp.com/send?phone={}&source=&data=#".format(phone_no))
        try:
            driver.switch_to_alert().accept()
        except Exception as e:
            pass

        try:
            element_presence(
                By.XPATH, '//div[@class="_3u328 copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]', 60)
            txt_box = driver.find_element(
                By.XPATH, '//div[@class="_3u328 copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]' )
            global no_of_message
            for msj in message_text.split('//salto//'):
                txt_box.send_keys(msj)
                ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
            txt_box.send_keys("\n")
                
                

        except Exception as e:
            print("invalid phone no :"+str(phone_no))


    for mobile_num in mobile_num_list:
        try:
            send_whatsapp_msg(mobile_num, message_text)

        except Exception as e:
            sleep(60)
            is_connected()
    
    
driver.close()



# if __name__ == '__main__':
#     # webbrowser.open('http://127.0.0.1:3333')
#     app.secret_key = "privatekeyMellitus"
#     app.run(port = 3333, debug = True)
