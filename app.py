from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response, jsonify, g, jsonify, Response
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
import os 
import sys
import json
from datetime import datetime
from flask_restful import Resource, Api
from flask_celery import make_celery
import random
from os import remove
import time
import smtplib
import getpass
from time import gmtime, strftime
from datetime import date, time, timezone, timedelta, datetime
import datetime
from pytz import timezone
from flask_celery import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib,getpass

sys.path.append(os.getcwd())


app = Flask (__name__)


app.config.update(
    CELERY_BROKER_URL='amqp://localhost',
    CELERY_RESULT_BACKEND='amqp://localhost'
)
celery = make_celery(app)

# MySQL Connection config
app.config['MYSQL_HOST'] = environ.get['MYSQL_HOST']
app.config['MYSQL_USER'] =environ.get['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = environ.get['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = environ.get['MYSQL_DB']


mysql = MySQL(app)


@app.route ('/')
def index ():

  return render_template('index.html')

@app.route ('/enviaremail',methods=["POST"])
def enviaremail ():
  if request.method == 'POST':
    nombreEmail = str(request.form['nombre'])
    correoEmail = str(request.form['email'])
    reclamoEmail = str(request.form['reclamo'])

    me = "environ.get['ME_EMAIL']
    my_password = environ.get['MY_PASSWORD']
    you = environ.get['EMAIL']

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Consulta/Reclamo"
    msg['From'] = me
    msg['To'] = you

    html = '<html><body><p><b>Nuevo Mensaje de</b> '+ nombreEmail +' </p><br><p><b>Email :</b> '+ correoEmail +'</p><br><p><b>Consulta/Reclamo : </b>'+ reclamoEmail +'</p</body></html>'
    part2 = MIMEText(html, 'html')

    msg.attach(part2)

    # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    # uncomment if interested in the actual smtp conversation
    # s.set_debuglevel(1)
    # do the smtp auth; sends ehlo if it hasn't been sent already
    s.login(me, my_password)

    s.sendmail(me, you, msg.as_string())
    s.quit()

    flash ('Se envio correctamente su mensaje. Muchas Gracias','success')
    return redirect(url_for('index'))




@app.route ('/inicio')
def inicio ():
  print('Elimina esto')
  #Las declaro globales porq los voy a necesitar en los otros templates
  global listaEspecialidades,listaTiposDoc,listaPaises,listaDias,listaGSanguineos,listaReligiones

  cur = mysql.connection.cursor()

  cur.execute ("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()

  cur.execute ("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()

  cur.execute ('SELECT * FROM paises')
  listaPaises = cur.fetchall ()

  cur.execute ('SELECT * FROM relig')
  listaReligiones =cur.fetchall ()

  listaDias = [[1,'Lunes'],[2,'Martes'],[3,'Miércoles'],[4,'Jueves'],[5,'Viernes'],[6,'Sábado']]
  listaGSanguineos = ['N/S', 'A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-']

  return render_template ('inicio.html', tiposDocProfesional = listaTiposDoc, nacionalidadProfesional = listaPaises, especialidadProfesional = listaEspecialidades,
       listaDias = listaDias ,tiposGSPaciente=listaGSanguineos,listaReligiones=listaReligiones)

@app.route('/panelControl')
def panelControl():
  return render_template('panelControl.html')


@app.route('/perfil')
def perfil():
  cur = mysql.connection.cursor()
  tipoUsuario = int (session['idTusu'])
  idUsuario = session ['idUs']
  if not session.get ('usuario'):
      return redirect(url_for('login'))
  else:
    if session ['idTusu'] == 1 :
      cur.execute("SELECT * FROM usuario WHERE usuario.IdUs =%s",(idUsuario,))
      datosAdmin = cur.fetchall ()
      mysql.connection.commit ()
      return render_template('perfil.html', datosAdmin = datosAdmin)
      cur.close()
    if session ['idTusu'] == 2 :
      cur.execute("SELECT * FROM (profesional INNER JOIN usuario ON usuario.IdUs = profesional.IdUsPro) WHERE profesional.IdUsPro =%s",(idUsuario,))
      datosProf = cur.fetchall ()
      mysql.connection.commit ()
      return render_template('perfil.html', datosProf = datosProf)
      cur.close ()
    if tipoUsuario == 3 :      
      cur.execute("SELECT * FROM (secretaria INNER JOIN usuario ON usuario.IdUs = secretaria.IdUsSec) WHERE secretaria.IdUsSec =%s",(idUsuario,))
      datosSecre = cur.fetchall ()
      mysql.connection.commit ()
      print ("->", datosSecre)
      return render_template('perfil.html', datosSecre = datosSecre)
      cur.close()

#desde el perfil del propio usuario
@app.route('/cambiarPassword',methods=["POST"])
def cambiarPassword():
  if request.method == 'POST':
    if not session.get ('usuario'):
      return redirect(url_for('login'))
    else:
      idUsuario = session['idUs']
      cur = mysql.connection.cursor()
      passwordNueva = request.form ['passNueva'].encode('utf-8')
      passwordNueva2 = request.form ['passNueva2'].encode('utf-8')
      
      if passwordNueva == passwordNueva2:
        passwordNuevaVerificada = bcrypt.hashpw(passwordNueva, bcrypt.gensalt())
      else:
        flash ('ERROR: Las passwords no coinciden', 'danger')
        return redirect(url_for('perfil'))

      cur.execute('''UPDATE usuario SET PassUs =%s  WHERE IdUs = %s''',(passwordNuevaVerificada,idUsuario,))
      mysql.connection.commit ()
      flash ('ÉXITO: tu password ha sido actualizada correctamente', 'success')
      return redirect(url_for('perfil'))

# LOGIN 
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario'] # Almacenamos el usuario del form de login en una variable
        password = request.form['password'].encode('utf-8') # Almacenamos la password del form de login en una variable+encode para q reconozca simbolos

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuario WHERE NomUs =%s",(usuario,)) #buscamos el mail o nombre de usuario? en la DB

        try:
            user = cur.fetchone() #traemos toda la info de USUARIO aca
            if bcrypt.hashpw(password, user[3].encode('utf-8')) == user[3].encode('utf-8'):
                session['idUs'] = user [0],
                session['usuario'] = user[1],
                session['idTusu'] = user [2]
                flash ("Te has logueado exitosamente!", 'success')
                
                return redirect(url_for('inicio'))
            else:
                flash (' ERROR: usuario o password incorrecto!', 'danger')

                return redirect(url_for('login'))
        except:
            flash (' ERROR: usuario o password incorrecto!', 'danger')
            return redirect(url_for('login'))   
        
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash ("Has cerrado sesión. Hasta luego", 'danger')
    return render_template("index.html")

@app.route ('/agregarProfesional', methods=["GET","POST"])
def agregarProfesional ():  
  dateTimeObj = datetime.datetime.now ()
  # SQL CONNECTIONS + INFO UTIL DB
  cur = mysql.connection.cursor()
  
  cur.execute ("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()

  cur.execute ("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()

  cur.execute('SELECT * FROM relig')
  listaReligiones = cur.fetchall()

  cur.execute ('SELECT * FROM paises')
  listaPaises = cur.fetchall ()
  listaDias = [[1,'Lunes'],[2,'Martes'],[3,'Miércoles'],[4,'Jueves'],[5,'Viernes'],[6,'Sábado']]
  
  #CREAR JSON PARA OBSOCIAL Y PLAN
  mysql.connection.commit()
  if request.method == 'POST':
    # RECUPERO INFO DEL FORMULARIO DE CARGA
    nombreProfesional = request.form ['nombreProfesional'].title()
    apellidoProfesional = request.form ['apellidoProfesional'].upper()
    nombreComplProfesional = apellidoProfesional + ', ' + nombreProfesional
    sexoProfesional = request.form ['sexoProfesional']
    tipoDocProfesional = request.form ['tipoDocProfesional']
    numeroDocProfesional = request.form ['numeroDocProfesional']
    fechaNacProfesional = request.form ['fechaNacProfesional']
    if fechaNacProfesional == '' :
      fechaNacProfesional = dateTimeObj
    paisProfesional = request.form ['paisProfesional']
    provinciaProfesional = request.form ['provinciaProfesional']
    localidadProfesional = request.form ['localidadProfesional']
    domicilioProfesional = request.form ['domicilioProfesional']
    nacionalidadProfesional = request.form ['nacionalidadProfesional']
    telefonoProfesional = request.form ['telefonoProfesional']
    emailProfesional = request.form ['emailProfesional']
    especialidadProfesional = request.form.getlist ('especialidadProfesional')
    if len(especialidadProfesional) == 0:
      especialidadProfesional = [53]
    usuarioProfesional = request.form ['usuarioProfesional']
    tipoUsuario = 2
    passwordProfesional = request.form ['passwordProfesional'].encode('utf-8')
    password2Profesional = request.form ['password2Profesional'].encode('utf-8')
    observacionProfesional = request.form ['observacionProfesional']
    numeroMNProfesional = request.form ['numeroMNProfesional']
    numeroMPProfesional = request.form ['numeroMPProfesional']
    if passwordProfesional == password2Profesional:
      passwordVerifUsuario = bcrypt.hashpw(passwordProfesional, bcrypt.gensalt())
    else:
      flash ('ERROR: Las passwords no coinciden', 'danger')
      return redirect(url_for('gestionarProfesional'))
    usuCargaProfesional = session['idUs']
    # ACA CHECKEO Q NO SE REPITA EL DNI
    cur.execute('SELECT * FROM profesional WHERE DniPro = %s', (numeroDocProfesional,))
    checkDni = cur.fetchall()
    if len (checkDni) > 0:
      flash ('ERROR: DNI ya en uso', 'danger')
      return render_template ('inicio.html', tiposDocProfesional = listaTiposDoc, nacionalidadProfesional = listaPaises, especialidadProfesional = listaEspecialidades,
       listaDias = listaDias,listaReligiones=listaReligiones )

    cur.execute ('INSERT INTO usuario (NomUs, IdTusu, PassUs) VALUES (%s, %s, %s)', (usuarioProfesional,tipoUsuario, passwordVerifUsuario))
    mysql.connection.commit ()
    idUsuPro = cur.lastrowid

    cur.execute ('INSERT INTO profesional (NomPro, SexPro, FnaPro, IdTdni, DniPro, DomPro, IdLoc, TelPro, EmaPro,IdUs, IdPais, IdUsPro, ObsPro, MnPro, MpPro ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
    (nombreComplProfesional, sexoProfesional, fechaNacProfesional, tipoDocProfesional, numeroDocProfesional, domicilioProfesional, localidadProfesional, telefonoProfesional, emailProfesional,
    usuCargaProfesional, nacionalidadProfesional, idUsuPro, observacionProfesional, numeroMNProfesional, numeroMPProfesional))
    mysql.connection.commit()
    idProfesional = cur.lastrowid
    cur.execute ('INSERT INTO proplan (IdPro) VALUES (%s)', (idProfesional,))

    for especialidad in especialidadProfesional:
      # TRABAJAR ACA INSERT DE MATRICULA ASJDJAHSD
      cur.execute ('INSERT INTO proesp (IdPro, IdEsp, MeProEsp) VALUES (%s, %s, %s)', (idProfesional, especialidad, numeroMPProfesional))
      mysql.connection.commit()
      idProEsp = cur.lastrowid
      cur.execute ('INSERT INTO proesppres (IdProEsp) VALUES (%s)', (idProEsp,))
      
    mysql.connection.commit()
    flash ('PROFESIONAL CARGADO CORRECTAMENTE', 'success')
    return redirect(url_for('gestionarProfesional'))
  
  
@app.route ('/gestionarProfesional', methods=["GET","POST"])
def gestionarProfesional ():
  especialidades = []
  prestaciones = []
  profesionales = []
  profEspec = []
  listaDias = [[1,'Lunes'],[2,'Martes'],[3,'Miércoles'],[4,'Jueves'],[5,'Viernes'],[6,'Sábado']]
  dateTimeObj = datetime.datetime.now ()
  # SQL CONNECTIONS + INFO UTIL DB
  cur = mysql.connection.cursor()
  cur.execute ('SELECT * FROM paises')
  pa_pr_lo_headers=['id', 'name', 'parent_id']
  listaPaises = cur.fetchall ()
  json_data_pa_pr_lo=[]
  for result in listaPaises:
      json_data_pa_pr_lo.append(dict(zip(pa_pr_lo_headers,result)))
  cur.execute ('SELECT * FROM provincias')
  listaProvincias = cur.fetchall ()
  for result2 in listaProvincias:
      json_data_pa_pr_lo.append(dict(zip(pa_pr_lo_headers,result2)))
  cur.execute ('SELECT * FROM localidades')
  listaLocalidades = cur.fetchall ()
  for result3 in listaLocalidades:
      json_data_pa_pr_lo.append(dict(zip(pa_pr_lo_headers,result3)))
  jsonUbicacion = json.dumps(json_data_pa_pr_lo,ensure_ascii = False, indent=4) #esto esta al pedo creo
  with open('/home/alfonso/myproject/static/data/country_state_city.json', 'w', encoding='utf-8') as ubics:
    json.dump(json_data_pa_pr_lo, ubics, ensure_ascii=False, indent=4)
  listaEstadoProfesional = [[0,'Activo'], [1,'Eliminado']]
  # SQL CONNECTIONS + INFO UTIL DB
  cur = mysql.connection.cursor()
  cur.execute ("SELECT * FROM listadoProfesional")
  listaProfesionales = cur.fetchall ()
  cur.execute ("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()
  cur.execute ("SELECT * FROM usuario")
  listaUsuarios = cur.fetchall ()
  cur.execute ("SELECT * FROM  prestacion")
  listaPrestaciones = cur.fetchall()
  cur.execute ('SELECT *  FROM (especialidad INNER JOIN proesp ON especialidad.IdEsp = proesp.IdEsp)')
  listaProEsp = cur.fetchall ()
  cur.execute ('SELECT * FROM paises')
  listaPaises = cur.fetchall ()
  cur.execute ('SELECT * FROM provincias')
  listaProvincias = cur.fetchall ()
  cur.execute ('SELECT * FROM localidades')
  listaLocalidades = cur.fetchall ()
  cur.execute ('''SELECT *  FROM (proesppres
              INNER JOIN proesp
              ON proesp.IdProEsp = proesppres.IdProEsp)
              INNER JOIN especialidad
              ON especialidad.IdEsp = proesp.IdEsp
              INNER JOIN prestacion
              ON prestacion.IdPrest = proesppres.IdPrest''')
  listaProEspPres = cur.fetchall()
  cur.execute ('''SELECT *  FROM (paises
              INNER JOIN provincias
              ON paises.IdPais = provincias.IdPais)
              INNER JOIN localidades
              ON localidades.IdProv = provincias.IdProv;''')
  listaPaisProvLoc = cur.fetchall()
  cur.execute ("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()
  cur.execute ('''SELECT *  FROM (proesppres
                            INNER JOIN proesp
                            ON proesp.IdProEsp = proesppres.IdProEsp)
                            INNER JOIN especialidad
                            ON especialidad.IdEsp = proesp.IdEsp
                            INNER JOIN prestacion
                            ON prestacion.IdPrest = proesppres.IdPrest
                            INNER JOIN profesional
                            ON profesional.IdPro = proesp.IdPro''')
  listaPrestacionesEspPro = cur.fetchall ()
  cur.execute ('SELECT * FROM dha ORDER BY DiaDha ASC')
  listaDiaHoraTurno = cur.fetchall ()
  cur.execute ('SELECT * FROM listaProPlan')
  listaPlanObSoPro = cur.fetchall()
  cur.execute('SELECT * FROM relig')
  listaReligiones = cur.fetchall()
  
  return render_template ('gestionarProfesional.html', tiposDocProfesional = listaTiposDoc, nacionalidadProfesional = listaPaises, listaPaisProvLoc = listaPaisProvLoc,
   especialidadProfesional = listaEspecialidades, listaProfesionales = listaProfesionales, especialidades = especialidades, profesionales = profesionales,
    listaPrestaciones = listaPrestaciones, listaLocalidades = listaLocalidades, listaUsuarios = listaUsuarios, listaDias = listaDias, listaDiaHoraTurno = listaDiaHoraTurno,
    prestaciones = prestaciones, listaProEsp = listaProEsp, listaProEspPres = listaProEspPres, profEspec = profEspec, 
    listaPrestacionesEspPro = listaPrestacionesEspPro, listaPlanObSoPro = listaPlanObSoPro,listaReligiones=listaReligiones) 
  
  

@app.route ('/modificarProfesional/<string:id>', methods=["GET","POST"])
def modificarProfesional(id): 
  dateTimeObj = datetime.datetime.now ()
  # SQL CONNECTIONS + INFO UTIL DB
  cur = mysql.connection.cursor()
  cur.execute ("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()
  cur.execute ("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()
  cur.execute ('SELECT * FROM paises')
  listaPaises = cur.fetchall ()
  if request.method == 'POST':
    nombreCompProfesional = request.form['nombreCompProfesional']
    sexoProfesional = request.form ['sexoProfesional']
    tipoDocProfesional = request.form ['tipoDocProfesional']
    numeroDocProfesional = request.form ['numeroDocProfesional']
    fechaNacProfesional = request.form ['fechaNacProfesional']
    if fechaNacProfesional == '' :
      fechaNacProfesional = dateTimeObj
    paisProfesional = request.form ['paisProfesional']
    provinciaProfesional = request.form ['provinciaProfesional']
    localidadProfesional = request.form ['localidadProfesional']
    domicilioProfesional = request.form ['domicilioProfesional']
    nacionalidadProfesional = request.form ['nacionalidadProfesional']
    telefonoProfesional = request.form ['telefonoProfesional']
    emailProfesional = request.form ['emailProfesional']
    especialidadProfesional = request.form.getlist ('especialidadProfesional')
    usuarioProfesional = request.form ['usuarioProfesional']
    actividadProfesional = request.form['actividadProfesional']
    tipoUsuario = 2
    # passwordProfesional = request.form ['passwordProfesional']
    # password2Profesional = request.form ['password2Profesional']
    observacionProfesional = request.form ['observacionProfesional']
    numeroMNProfesional = request.form ['numeroMNProfesional']
    # numeroMPProfesional = request.form ['numeroMPProfesional']
    cur=mysql.connection.cursor()
    cur.execute ('SELECT * FROM profesional WHERE IdPro = %s', (id,))
    profesional = cur.fetchall()
    mysql.connection.commit()
    if profesional :
      actualizarProfesional = '''UPDATE profesional SET NomPro = %s, IdTdni = %s, DniPro = %s, FnaPro = %s, DomPro = %s, IdLoc = %s, SexPro = %s, TelPro = %s,
       EmaPro = %s, IdPais = %s, ObsPro = %s, ActPro = %s, MnPro = %s  WHERE IdPro = %s'''
      values = (nombreCompProfesional, tipoDocProfesional, numeroDocProfesional, fechaNacProfesional, domicilioProfesional, localidadProfesional, sexoProfesional, 
      telefonoProfesional, emailProfesional,
      paisProfesional, observacionProfesional, actividadProfesional, numeroMNProfesional, id,)
      cur.execute (actualizarProfesional,values)
      cur = mysql.connection.commit()
      flash ('PROFESIONAL MODIFICADO EXITOSAMENTE', 'success')
    return redirect(url_for('gestionarProfesional'))

@app.route ('/modificarXEspecialidad/<string:idProf>/<string:idEsp>', methods=["GET","POST"])
def modificarXEspecialidad(idProf, idEsp):
  if request.method == 'POST':
    cur = mysql.connection.cursor()
    idProfesional = idProf
    idEspecialidad = idEsp
    nuevaMatricProv = request.form ['numeroMPProfesional']
    cur.execute('SELECT IdProEsp FROM proesp WHERE IdPro = %s AND IdEsp = %s ', (idProfesional,idEspecialidad,)) 
    idProEsp = cur.fetchone()
    if idProEsp:
      cur.execute('UPDATE proesp SET MeProEsp = %s WHERE IdProEsp = %s', (nuevaMatricProv,idProEsp,))
      mysql.connection.commit()
      flash ('MATRICULA ACTUALIZADA CORRECTAMENTE', 'success')
      cur.close()
    else: 
      flash ('UPS. Algo salio mal', 'error')
    return redirect(url_for('gestionarProfesional'))

@app.route ('/agregarEspecialidadPro/<string:idProf>', methods = ['GET', 'POST'])
def agregarEspecialidadPro(idProf):
  if request.method == 'POST':
    
    cur = mysql.connection.cursor()
    idProfesional = idProf
    idEspecialidad = request.form['especialidadProfesionalNueva']
    numMatricula = request.form ['numeroMPProfesional']
    cur.execute('SELECT * FROM proesp WHERE IdPro = %s AND IdEsp = %s', (idProfesional, idEspecialidad,))
    checkEspPro = cur.fetchall()
    if len (checkEspPro) > 0:
      flash ('ERROR: Este profesional ya tiene esta especialidad cargada', 'danger')
      return redirect(url_for('gestionarProfesional'))
    else:
      cur.execute ('INSERT INTO proesp (IdPro, IdEsp, MeProEsp) VALUES (%s, %s, %s)', ( idProfesional, idEspecialidad, numMatricula))
      mysql.connection.commit()
      idProEsp = cur.lastrowid
      cur.execute ('INSERT INTO proesppres (IdProEsp) VALUES (%s)', (idProEsp,))
      mysql.connection.commit()
      cur.close()
      flash ('ESPECIALIDAD AGREGADA CORRECTAMENTE', 'success')
      return redirect(url_for('gestionarProfesional'))
    cur.close()

@app.route ('/agregarPrestacionEspPro/<string:idProf>/<string:idEsp>', methods = ['GET', 'POST'])
def agregarPrestacionEspPro(idProf, idEsp):
  if request.method == 'POST':

    prestsPro = []
    cur = mysql.connection.cursor()
    idProfesional = idProf
    idEspecialidad = idEsp
    idPrestacion = int(request.form ['prestacionProfesionalNueva'])
    cur.execute('SELECT IdProEsp FROM proesp WHERE IdPro = %s AND IdEsp = %s ', (idProfesional,idEspecialidad,)) 
    idProEsp = cur.fetchone()
    mysql.connection.commit()
    if len (idProEsp) > 0: #ACA CHECKEO SI EL PROF YA TIENE ALGUNA PRESTACION CARGADA PARA DICHA ESPECIALIDAD, QUE SIEMPRE DEBERIA TENER 1 YA Q SIEMPRE SE CARGA CONSULTA MEDICA
      cur.execute('SELECT IdPrest FROM proesppres WHERE IdProEsp = %s', (idProEsp,))
      checkEspPrePro = cur.fetchall()
      mysql.connection.commit()
      for prest in checkEspPrePro: 
        prestsPro.append(prest[0])  
      if idPrestacion in prestsPro : #ACA COMPARO Q NO SE REPITA LA PRESTACION
        flash ('ERROR: Este profesional ya tiene esta prestacion cargada para esta especialidad', 'danger')
        return redirect(url_for('gestionarProfesional'))
      else:
        cur.execute ('INSERT INTO proesppres (IdProEsp,IdPrest) VALUES (%s, %s)', ( idProEsp, idPrestacion ))
        mysql.connection.commit()
        flash ('PRESTACION AGREGADA CORRECTAMENTE', 'success')
        return redirect(url_for('gestionarProfesional'))
        cur.close()
    else:
        cur.execute ('INSERT INTO proesppres (IdProEsp,IdPrest) VALUES (%s, %s)', ( idProEsp, idPrestacion ))
        mysql.connection.commit()
        flash ('PRESTACION AGREGADA CORRECTAMENTE', 'success')
        return redirect(url_for('gestionarProfesional'))
       
@app.route('/cargaDiasAtenc/<string:idProf>')
def cargaDiasAtenc(idProf):
  idProf = int(idProf)
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM profesional")
  listaProf=cur.fetchall()
  cur.execute ('SELECT * FROM dha ORDER BY DiaDha ASC')
  listaDiaHoraTurno = cur.fetchall ()
  cur.execute("SELECT * FROM osocial")
  osocial=cur.fetchall()
  listaDias = [[1,'Lunes'],[2,'Martes'],[3,'Miércoles'],[4,'Jueves'],[5,'Viernes'],[6,'Sábado']]
  return render_template("cargaDiasAtenc.html" , listaProf=listaProf,osocial=osocial, listaDiaHoraTurno = listaDiaHoraTurno, listaDias=listaDias, idProf=idProf)
  
@app.route ('/agregarDiaHoraAtenPro/<string:idProf>', methods = ['GET', 'POST'])
def agregarDiaHoraAtenPro(idProf):
  if request.method == 'POST':    
    cur = mysql.connection.cursor()
    idProfesional = idProf
    idUsuCarga = session['idUs']
    idDia = request.form ['diaAtencProfesional']
    horaInicio = request.form ['horaInicioAtencProfesional']
    horaFin = request.form ['horaFinAtencProfesional']
    cur.execute ('INSERT INTO dha (IdPro, DiaDha, HiDha, HfDha, IdUs) VALUES (%s, %s, %s, %s, %s)', ( idProfesional, idDia, horaInicio, horaFin, idUsuCarga ))
    mysql.connection.commit()
    cur.close()
    flash ('MOMENTO DE ATENCION AGREGADA CORRECTAMENTE', 'success')
    return redirect(url_for('gestionarProfesional'))

@app.route ('/agregarDiaHoraAtenProMasiva/<string:idProf>', methods = ['GET', 'POST'])
def agregarDiaHoraAtenProMasiva(idProf):
  if request.method == 'POST':    
    cur = mysql.connection.cursor()
    idProfesional = idProf
    idUsuCarga = session['idUs']
    idDia = request.form ['diaAtencProfesional']
    idDia1 = request.form ['diaAtencProfesional1']
    idDia2 = request.form ['diaAtencProfesional2']
    idDia3 = request.form ['diaAtencProfesional3']
    idDia4 = request.form ['diaAtencProfesional4']
    idDia5 = request.form ['diaAtencProfesional5']
    idDia6 = request.form ['diaAtencProfesional6']
    idDia7 = request.form ['diaAtencProfesional7']
    idDia8 = request.form ['diaAtencProfesional8']
    idDia9 = request.form ['diaAtencProfesional9']
    horaInicio = request.form ['horaInicioAtencProfesional']
    horaInicio1 = request.form ['horaInicioAtencProfesional1']
    horaInicio2 = request.form ['horaInicioAtencProfesional2']
    horaInicio3 = request.form ['horaInicioAtencProfesional3']
    horaInicio4 = request.form ['horaInicioAtencProfesional4']
    horaInicio5 = request.form ['horaInicioAtencProfesional5']
    horaInicio6 = request.form ['horaInicioAtencProfesional6']
    horaInicio7 = request.form ['horaInicioAtencProfesional7']
    horaInicio8 = request.form ['horaInicioAtencProfesional8']
    horaInicio9 = request.form ['horaInicioAtencProfesional9']
    horaFin = request.form ['horaFinAtencProfesional']
    horaFin1 = request.form ['horaFinAtencProfesional1']
    horaFin2 = request.form ['horaFinAtencProfesional2']
    horaFin3 = request.form ['horaFinAtencProfesional3']
    horaFin4 = request.form ['horaFinAtencProfesional4']
    horaFin5 = request.form ['horaFinAtencProfesional5']
    horaFin6 = request.form ['horaFinAtencProfesional6']
    horaFin7 = request.form ['horaFinAtencProfesional7']
    horaFin8 = request.form ['horaFinAtencProfesional8']
    horaFin9 = request.form ['horaFinAtencProfesional9']
    diasNuevos=[[idDia,horaInicio,horaFin],[idDia1,horaInicio1,horaFin1],[idDia2,horaInicio2,horaFin2],[idDia3,horaInicio3,horaFin3],[idDia4,horaInicio4,horaFin4],[idDia5,horaInicio5,horaFin5],[idDia6,horaInicio6,horaFin6],[idDia7,horaInicio7,horaFin7],[idDia8,horaInicio8,horaFin8],[idDia9,horaInicio9,horaFin9]]
    for diaHoraNuevo in diasNuevos:
      if diaHoraNuevo[0] != '0':
        cur.execute ('INSERT INTO dha (IdPro, DiaDha, HiDha, HfDha, IdUs) VALUES (%s, %s, %s, %s, %s)', ( idProfesional, diaHoraNuevo[0], diaHoraNuevo[1], diaHoraNuevo[2], idUsuCarga ))
        mysql.connection.commit()
      else:
        pass
    cur.close()
    flash ('MOMENTO DE ATENCION AGREGADA CORRECTAMENTE', 'success')
    return redirect(url_for('cargaDiasAtenc', idProf = idProfesional))

@app.route ('/quitarDiaHoraAtenPro/<string:idProf>', methods = ['GET', 'POST'])
def quitarDiaHoraAtenPro(idProf):
  if request.method == 'POST':
    idProfesional = idProf
    cur = mysql.connection.cursor()
    idDha = request.form ['idDha']
    borrarDiaHoraAtenc = '''UPDATE dha SET ActDha = %s WHERE IdDha = %s '''
    values = (1, idDha,)
    cur.execute (borrarDiaHoraAtenc,values)
    cur.connection.commit()
    cur.close()
    flash ('¡HORARIO DE ATENCIÓN BORRADO CON ÉXITO!', 'success')
    return redirect(url_for('cargaDiasAtenc', idProf = idProfesional))


@app.route ('/agregarObraSoPlanPro/<string:idProf>', methods = ['GET', 'POST'])
def agregarObraSoPlanPro(idProf):
  cur = mysql.connection.cursor()
  mysql.connection.commit()
  if request.method == 'POST':
    if not session.get ('usuario'):
      return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    idProfesional = idProf
    obraSocialProfesional = request.form ['obraSocialProfesional']
    planObSoProfesional = request.form ['planObSoProfesional']
    cur.execute ('INSERT INTO proplan (IdPlan, IdPro) VALUES (%s, %s)', ( planObSoProfesional, idProfesional,))
    mysql.connection.commit()
    cur.close()
    flash ('PLAN/OS AGREGADA CORRECTAMENTE', 'success')
    return redirect(url_for('gestionarProfesional'))

@app.route ('/agregarPaciente', methods=['GET' , 'POST'])
def agregarPaciente ():
  dateTimeObj = datetime.datetime.now ()
  # SQL CONNECTIONS + INFO UTIL DB
  cur = mysql.connection.cursor()
  cur.execute ("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()
  cur.execute ('SELECT * FROM relig')
  listaReligiones = cur.fetchall ()
  cur.execute ('SELECT * FROM paises')
  pa_pr_lo_headers=['id', 'name', 'parent_id']
  listaPaises = cur.fetchall ()
  json_data_pa_pr_lo=[]
  for result in listaPaises:
      json_data_pa_pr_lo.append(dict(zip(pa_pr_lo_headers,result)))
  cur.execute ('SELECT * FROM provincias')
  listaProvincias = cur.fetchall ()
  for result2 in listaProvincias:
      json_data_pa_pr_lo.append(dict(zip(pa_pr_lo_headers,result2)))
  cur.execute ('SELECT * FROM localidades')
  listaLocalidades = cur.fetchall ()
  for result3 in listaLocalidades:
      json_data_pa_pr_lo.append(dict(zip(pa_pr_lo_headers,result3)))
  jsonUbicacion = json.dumps(json_data_pa_pr_lo,ensure_ascii = False, indent=4) #esto esta al pedo creo
  with open('/home/alfonso/myproject/static/data/country_state_city.json', 'w', encoding='utf-8') as ubics:
    json.dump(json_data_pa_pr_lo, ubics, ensure_ascii=False, indent=4)
  #CREAR JSON PARA OBSOCIAL Y PLAN
  os_pl_headers=['idOS', 'nameOS', 'parent_idOS']
  json_data_os_pl = []
  cur.execute ('SELECT IdOs, NomOs, ParentId FROM osocial')
  listaObrasSociales = cur.fetchall ()
  for result4 in listaObrasSociales:
      json_data_os_pl.append(dict(zip(os_pl_headers,result4)))
  cur.execute ('SELECT IdPlan, NomPlan, IdOs FROM plan')
  listaPlanes = cur.fetchall ()
  for result5 in listaPlanes:
    json_data_os_pl.append(dict(zip(os_pl_headers,result5)))
  with open('static/data/mutual_plan.json', 'w', encoding='utf-8') as obs:
    json.dump(json_data_os_pl, obs, ensure_ascii=False, indent=4)
  listaGSanguineos = ['N/S', 'A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-']
  mysql.connection.commit()
  if request.method == 'POST':
    # RECUPERO INFO DEL FORMULARIO DE CARGA
    nombrePaciente = request.form ['nombrePaciente'].title()
    apellidoPaciente = request.form ['apellidoPaciente'].upper()
    nombreComplPaciente = apellidoPaciente + ', ' + nombrePaciente
    sexoPaciente = request.form ['sexoPaciente']
    tipoDocPaciente = request.form ['tipoDocPaciente']
    numeroDocPaciente = request.form ['numeroDocPaciente']
    cur.execute('SELECT * FROM paciente WHERE DniPac = %s', (numeroDocPaciente,))
    checkDni = cur.fetchall()
    if len (checkDni) > 0:
      flash ('ERROR: DNI ya en uso', 'danger')
      return redirect(url_for('gestionarPaciente'))
    fechaNacPaciente = request.form ['fechaNacPaciente']
    if fechaNacPaciente == '' :
      fechaNacPaciente = dateTimeObj
    paisPaciente = request.form ['paisPaciente']
    provinciaPaciente = request.form ['provinciaPaciente']
    localidadPaciente = request.form ['localidadPaciente']
    if localidadPaciente == '':
      localidadPaciente = 2687
    domicilioPaciente = request.form ['domicilioPaciente']
    nacionalidadPaciente = request.form ['nacionalidadPaciente']
    telefonoPaciente = request.form ['telefonoPaciente']
    grupoSangPaciente = request.form ['grupoSangPaciente']
    obraSocialPaciente = request.form ['obraSocialPaciente']
    planObSoPaciente = request.form ['planObSoPaciente']
    numAfiliadoPaciente = request.form ['numAfiliadoPaciente']
    fechaObSoPaciente = request.form ['fechaObSoPaciente']
    religionPaciente = request.form ['religionPaciente']
    observacionPaciente = request.form ['observacionPaciente']
    if fechaObSoPaciente == '':
      fechaObSoPaciente = dateTimeObj
    usuCargaPaciente = session['idUs']
    cur.execute ('INSERT INTO paciente (NomPac, SexPac, FnacPac, IdTdni, DniPac, DomPac, IdLoc, GsaPac, TelPac, IdUs, IdPais,ObsPac ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
    (nombreComplPaciente, sexoPaciente, fechaNacPaciente, tipoDocPaciente, numeroDocPaciente, domicilioPaciente, localidadPaciente, grupoSangPaciente,telefonoPaciente,
    usuCargaPaciente,nacionalidadPaciente, observacionPaciente))
    mysql.connection.commit()
    idPaciente = cur.lastrowid
    cur.execute ('INSERT INTO pacplan (IdPac, IdPlan, NafilPacPlan, FinPacPlan) VALUES (%s,%s,%s,%s)', (idPaciente, planObSoPaciente, numAfiliadoPaciente, fechaObSoPaciente))
    mysql.connection.commit()
    flash ('PACIENTE CARGADO CORRECTAMENTE', 'success')
    return redirect(url_for('gestionarPaciente'))

@app.route ('/agregarPacienteCalendario', methods=['GET' , 'POST'])
def agregarPacienteCalendario ():
  if request.method == 'POST':
    dateTimeObj = datetime.datetime.now()
    data = request.get_json()
    data = data[0]
    # RECUPERO INFO DEL FORMULARIO DE CARGA
    nombrePaciente = str(data ['nombrePaciente'].title())
    apellidoPaciente = str(data ['apellidoPaciente'].upper())
    nombreComplPaciente = apellidoPaciente + ', ' + nombrePaciente
    sexoPaciente = str(data ['sexoPaciente'])
    tipoDocPaciente = str(data ['tipoDocPaciente'])
    numeroDocPaciente = str(data ['numeroDocPaciente'])
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM paciente WHERE DniPac = %s', (numeroDocPaciente,))
    checkDni = cur.fetchall()
    if len (checkDni) > 0:
      flash ('ERROR: DNI ya en uso', 'danger')
      return redirect(url_for('gestionarPaciente'))
    fechaNacPaciente = str(data ['fechaNacPaciente'])
    if fechaNacPaciente == '' :
      fechaNacPaciente = dateTimeObj
    paisPaciente = str(data ['paisPaciente'])
    provinciaPaciente = str(data ['provinciaPaciente'])
    localidadPaciente = str(data ['localidadPaciente'])
    if localidadPaciente == '':
      localidadPaciente = 2687
    domicilioPaciente = str(data ['domicilioPaciente'])
    nacionalidadPaciente = str(data ['nacionalidadPaciente'])
    telefonoPaciente = str(data ['telefonoPaciente'])
    grupoSangPaciente = str(data ['grupoSangPaciente'])
    obraSocialPaciente = str(data ['obraSocialPaciente'])
    planObSoPaciente = str(data ['planObSoPaciente'])
    numAfiliadoPaciente = str(data ['numAfiliadoPaciente'])
    fechaObSoPaciente = str(data ['fechaObSoPaciente'])
    religionPaciente = str(data ['religionPaciente'])
    observacionPaciente = str(data ['observacionPaciente'])
    if fechaObSoPaciente == '':
      fechaObSoPaciente = dateTimeObj
    usuCargaPaciente = session['idUs']
    cur = mysql.connection.cursor()
    cur.execute ('INSERT INTO paciente (NomPac, SexPac, FnacPac, IdTdni, DniPac, DomPac, IdLoc, GsaPac, TelPac, IdUs, IdPais,ObsPac ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
    (nombreComplPaciente, sexoPaciente, fechaNacPaciente, tipoDocPaciente, numeroDocPaciente, domicilioPaciente, localidadPaciente, grupoSangPaciente,telefonoPaciente,
    usuCargaPaciente,nacionalidadPaciente, observacionPaciente))
    mysql.connection.commit()
    idPaciente = cur.lastrowid
    cur = mysql.connection.cursor()
    cur.execute ('INSERT INTO pacplan (IdPac, IdPlan, NafilPacPlan, FinPacPlan) VALUES (%s,%s,%s,%s)', (idPaciente, planObSoPaciente, numAfiliadoPaciente, fechaObSoPaciente))
    mysql.connection.commit()
    
    #CREACION DEL JSON DATOS DEL PACIENTE DE CADA TURNO PARA LA SECRETARIA

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM listadoPacientesjson')
    respuesta=cur.fetchall()
    global res_query
    res_query = respuesta
    json_dat = {}

    for row in res_query:
      id_paciente = row[0]
      obra_social = {
          "IdPlan": row[9],
          "Plan": row[10],
          "IdOSoc": row[11],
          "NomOSoc": row[12],
          "IdPacPlan": row[13],
          "ActPlan": row[17]
      }
      pac = json_dat.get(id_paciente)

      if pac is not None:
        pac["ObraSocial"].append(obra_social)
      else:
        json_dat[id_paciente] = {
            "IdPaciente": id_paciente,
            "Nombre": row[1],
            "FNac": row[2].strftime("%Y-%m-%d"),
            "Dni": row[3],
            "Domicilio": row[4],
            "Telefono": row[14],
            "Sexo": row[15],
            "Religion": row[16],
            "IdLoc": row[5],
            "NomLoc": row[6],
            "IdPais": row[7],
            "NomPais": row[8],
            "ObraSocial": [obra_social]
        }

    with open('static/paciente.json', 'w') as fp:
        json.dump(list(json_dat.values()), fp, indent=4)

    with open('static/paciente.json') as pacient:
        PacientesC = json.load(pacient)
    return jsonify({'Mensaje':'Correcto','Data':PacientesC})



@app.route ('/gestionarPaciente', methods=["GET","POST"])
def gestionarPaciente ():
  dateTimeObj = datetime.datetime.now ()
  # SQL CONNECTIONS + INFO UTIL DB
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM especialidad INNER JOIN proesp ON especialidad.IdEsp=proesp.IdEsp INNER JOIN profesional ON profesional.IdPro=proesp.IdPro')
  especialidad = cur.fetchall()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM prestacion')
  pres = cur.fetchall()
  cur = mysql.connection.cursor()

  cur.execute("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()
  cur.close()

  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()
  cur.close()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM paises')
  listaPaises = cur.fetchall()
  cur.close()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM relig')
  listaReligiones = cur.fetchall()

  cur.execute ('SELECT * FROM paises')
  listaPaises = cur.fetchall ()

  listaDias = [[1, 'Lunes'], [2, 'Martes'], [3, 'Miércoles'],
               [4, 'Jueves'], [5, 'Viernes'], [6, 'Sábado']]
  listaGSanguineos = ['N/S', 'A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-']
  pa_pr_lo_headers=['id', 'name', 'parent_id']
  
  json_data_pa_pr_lo=[]
  for result in listaPaises:
      json_data_pa_pr_lo.append(dict(zip(pa_pr_lo_headers,result)))
  cur.execute ('SELECT * FROM provincias')
  listaProvincias = cur.fetchall ()
  for result2 in listaProvincias:
      json_data_pa_pr_lo.append(dict(zip(pa_pr_lo_headers,result2)))
  cur.execute ('SELECT * FROM localidades')
  listaLocalidades = cur.fetchall ()
  for result3 in listaLocalidades:
      json_data_pa_pr_lo.append(dict(zip(pa_pr_lo_headers,result3)))
  jsonUbicacion = json.dumps(json_data_pa_pr_lo,ensure_ascii = False, indent=4) #esto esta al pedo creo
  with open('/home/alfonso/myproject/static/data/country_state_city.json', 'w', encoding='utf-8') as ubics:
    json.dump(json_data_pa_pr_lo, ubics, ensure_ascii=False, indent=4)
  #CREAR JSON PARA OBSOCIAL Y PLAN
  os_pl_headers=['idOS', 'nameOS', 'parent_idOS']
  json_data_os_pl = []
  cur.execute ('SELECT IdOs, NomOs, ParentId FROM osocial')
  listaObrasSociales = cur.fetchall ()
  for result4 in listaObrasSociales:
      json_data_os_pl.append(dict(zip(os_pl_headers,result4)))
  cur.execute ('SELECT IdPlan, NomPlan, IdOs FROM plan')
  listaPlanes = cur.fetchall ()
  for result5 in listaPlanes:
    json_data_os_pl.append(dict(zip(os_pl_headers,result5)))
  with open('static/data/mutual_plan.json', 'w', encoding='utf-8') as obs:
    json.dump(json_data_os_pl, obs, ensure_ascii=False, indent=4)
  listaGSanguineos = ['N/S', 'A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-']
  cur.execute ('''SELECT paciente.IdPac AS 'IDPac', paciente.NomPac AS 'NombrePac', paciente.SexPac AS 'SexoPac', paciente.FnacPac AS 'FechaNacPac', 
                  paciente.IdTdni AS 'TipodniPac', paciente.DniPac AS 'DniPac', paciente.DomPac AS 'DomicilioPac', paciente.IdLoc AS 'IDLocalidadPac', 
                  paciente.GsaPac AS 'GrupoSangPac', paciente.TelPac AS 'TelefonoPac', paciente.IdRel AS 'IDReligionPac', paciente.AcPac AS 'EstadoPac', 
                  paciente.IdUs AS 'IDusuCargaPac', paciente.FcPac AS 'FechaCargaPac', paciente.IdPais AS 'NacionalidadPac', paciente.ObsPac AS 'ObservPac' FROM paciente''')
  listaPacientes = cur.fetchall()
  mysql.connection.commit()
  return render_template ('gestionarPaciente.html', listaGSanguineos = listaGSanguineos, listaTiposDoc = listaTiposDoc,nacionalidadProfesional=listaPaises,listaPaises = listaPaises, listaPacientes = listaPacientes, tiposDocProfesional=listaTiposDoc, especialidadProfesional=listaEspecialidades,listaDias=listaDias, tiposGSPaciente=listaGSanguineos, listaReligiones=listaReligiones,listaLocalidades=listaLocalidades)

@app.route ('/agregarSecretaria', methods=["GET","POST"])
def agregarSecretaria ():
  cur = mysql.connection.cursor()
  cur.execute('SELECT secretaria.IdSec, secretaria.NomSec,secretaria.DniSec,secretaria.TelSec,secretaria.DomSec,secretaria.ActSec FROM secretaria')
  listaSecretaria=cur.fetchall()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM especialidad INNER JOIN proesp ON especialidad.IdEsp=proesp.IdEsp INNER JOIN profesional ON profesional.IdPro=proesp.IdPro')
  especialidad = cur.fetchall()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM prestacion')
  pres = cur.fetchall()
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()
  cur.close()

  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()
  cur.close()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM paises')
  listaPaises = cur.fetchall()
  cur.close()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM relig')
  listaReligiones = cur.fetchall()
  cur.close()

  listaDias = [[1, 'Lunes'], [2, 'Martes'], [3, 'Miércoles'],
               [4, 'Jueves'], [5, 'Viernes'], [6, 'Sábado']]
  listaGSanguineos = ['N/S', 'A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-']

  dateTimeObj = datetime.datetime.now ()
  # SQL CONNECTIONS + INFO UTIL DB
  cur = mysql.connection.cursor()
  cur.execute ("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()
  cur.execute ('SELECT * FROM paises')
  pa_pr_lo_headers=['id', 'name', 'parent_id']
  listaPaises = cur.fetchall ()
  json_data_pa_pr_lo=[]
  for result in listaPaises:
      json_data_pa_pr_lo.append(dict(zip(pa_pr_lo_headers,result)))
  cur.execute ('SELECT * FROM provincias')
  listaProvincias = cur.fetchall ()
  for result2 in listaProvincias:
      json_data_pa_pr_lo.append(dict(zip(pa_pr_lo_headers,result2)))
  cur.execute ('SELECT * FROM localidades')
  listaLocalidades = cur.fetchall ()
  for result3 in listaLocalidades:
      json_data_pa_pr_lo.append(dict(zip(pa_pr_lo_headers,result3)))
  jsonUbicacion = json.dumps(json_data_pa_pr_lo,ensure_ascii = False, indent=4) #esto esta al pedo creo
  with open('/home/alfonso/myproject/static/data/country_state_city.json', 'w', encoding='utf-8') as ubics:
    json.dump(json_data_pa_pr_lo, ubics, ensure_ascii=False, indent=4)
  #CREAR JSON PARA OBSOCIAL Y PLAN
  mysql.connection.commit()
  if request.method == 'POST':
    # RECUPERO INFO DEL FORMULARIO DE CARGA
    nombreSecretaria = request.form ['nombreSecretaria'].title()
    apellidoSecretaria = request.form ['apellidoSecretaria'].upper()
    nombreComplSecretaria = apellidoSecretaria + ', ' + nombreSecretaria
    sexoSecretaria = request.form ['sexoSecretaria']
    tipoDocSecretaria = request.form ['tipoDocSecretaria']
    numeroDocSecretaria = request.form ['numeroDocSecretaria']
    cur.execute('SELECT * FROM secretaria WHERE DniSec = %s', (numeroDocSecretaria,))
    checkDni = cur.fetchall()
    if len (checkDni) > 0:
      flash ('ERROR: DNI ya en uso', 'danger')
      return render_template ('inicio.html', tiposDocSecretaria = listaTiposDoc, nacionalidadSecretaria = listaPaises,listaReligiones=listaReligiones)  
    fechaNacSecretaria = request.form ['fechaNacSecretaria']
    if fechaNacSecretaria == '' :
      fechaNacSecretaria = dateTimeObj
    paisSecretaria = request.form ['paisSecretaria']
    provinciaSecretaria = request.form ['provinciaSecretaria']
    localidadSecretaria = request.form ['localidadSecretaria']
    domicilioSecretaria = request.form ['domicilioSecretaria']
    nacionalidadSecretaria = request.form ['nacionalidadSecretaria']
    telefonoSecretaria = request.form ['telefonoSecretaria']
    usuarioSecretaria = request.form ['usuarioSecretaria']
    tipoUsuario = 3
    passwordSecretaria = request.form ['passwordSecretaria'].encode('utf-8')
    password2Secretaria = request.form ['password2Secretaria'].encode('utf-8')
    observacionSecretaria=request.form ['observacionSecretaria']
    if passwordSecretaria == password2Secretaria:
      passwordVerifUsuario = bcrypt.hashpw(passwordSecretaria, bcrypt.gensalt())
    else:
      flash ('ERROR: Las passwords no coinciden', 'danger')
      return render_template ('gestionarSecretaria.html',listaSecretaria=listaSecretaria,tiposDocSecretaria = listaTiposDoc, nacionalidadSecretaria = listaPaises,tiposDocProfesional = listaTiposDoc, nacionalidadProfesional = listaPaises, especialidadProfesional = listaEspecialidades,
       listaDias = listaDias ,tiposGSPaciente=listaGSanguineos) 
    usuCargaSecretaria = session['idUs']
    cur.execute ('INSERT INTO usuario (NomUs, IdTusu, PassUs) VALUES (%s, %s, %s)', (usuarioSecretaria,tipoUsuario, passwordVerifUsuario))
    mysql.connection.commit ()
    idUsuSec = cur.lastrowid
    cur.execute ('INSERT INTO secretaria (NomSec, SexSec, FnaSec, IdTdni, DniSec, DomSec, IdLoc, TelSec, IdUs, IdPais, IdUsSec, ObsSec ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
    (nombreComplSecretaria, sexoSecretaria, fechaNacSecretaria, tipoDocSecretaria, numeroDocSecretaria, domicilioSecretaria, localidadSecretaria, telefonoSecretaria,
     usuCargaSecretaria, nacionalidadSecretaria, idUsuSec,observacionSecretaria))
    mysql.connection.commit()
    flash ('SECRETARIA/O CARGADO CORRECTAMENTE', 'success')
    #return render_template ('gestionarSecretaria.html',listaSecretaria=listaSecretaria,tiposDocSecretaria = listaTiposDoc, nacionalidadSecretaria = listaPaises,tiposDocProfesional = listaTiposDoc, nacionalidadProfesional = listaPaises, especialidadProfesional = listaEspecialidades,
    #   listaDias = listaDias ,tiposGSPaciente=listaGSanguineos) 
    return redirect(url_for('gestionarSecretaria'))
  else:
    return render_template ('gestionarSecretaria.html',listaSecretaria=listaSecretaria,tiposDocSecretaria = listaTiposDoc, nacionalidadSecretaria = listaPaises,tiposDocProfesional = listaTiposDoc, nacionalidadProfesional = listaPaises, especialidadProfesional = listaEspecialidades,
       listaDias = listaDias ,tiposGSPaciente=listaGSanguineos) 



@app.route ('/gestionarSecretaria', methods=["GET","POST"])
def gestionarSecretaria ():
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM especialidad INNER JOIN proesp ON especialidad.IdEsp=proesp.IdEsp INNER JOIN profesional ON profesional.IdPro=proesp.IdPro')
  especialidad = cur.fetchall()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM prestacion')
  pres = cur.fetchall()
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()
  cur.close()

  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()
  cur.close()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM paises')
  listaPaises = cur.fetchall()
  cur.close()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM relig')
  listaReligiones = cur.fetchall()
  cur.close()

  listaDias = [[1, 'Lunes'], [2, 'Martes'], [3, 'Miércoles'],
               [4, 'Jueves'], [5, 'Viernes'], [6, 'Sábado']]
  listaGSanguineos = ['N/S', 'A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-']
  cur = mysql.connection.cursor()
  cur.execute('SELECT secretaria.IdSec, secretaria.NomSec,secretaria.DniSec,secretaria.TelSec,secretaria.DomSec,secretaria.ActSec FROM secretaria')
  listaSecretaria=cur.fetchall()

  return render_template ('gestionarSecretaria.html',listaSecretaria=listaSecretaria,tiposDocSecretaria = listaTiposDoc, nacionalidadSecretaria = listaPaises,tiposDocProfesional = listaTiposDoc, nacionalidadProfesional = listaPaises, especialidadProfesional = listaEspecialidades,
       listaDias = listaDias ,tiposGSPaciente=listaGSanguineos ,listaReligiones=listaReligiones) 


@app.route('/perfilSecre<string:idSecre>', methods=['GET', 'POST'])
def perfilSecre(idSecre):
  idSec = idSecre

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM perfilSecretaria where IdSec="'+idSec+'"')
  perfilSecretaria=cur.fetchall()
  perfilSecretaria=perfilSecretaria[0]

  #ID Localidad Secretaria
  cur = mysql.connection.cursor()
  cur.execute('SELECT IdLoc FROM secretaria where IdSec='+str(idSec)+'')
  idLocalidad = cur.fetchall()
  idLocalidad = str(idLocalidad[0][0])
  print(idLocalidad)
  

  #Id & Nombres Loc, Prov, Pais
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM LocProvPais where IdLoc='+str(idLocalidad)+'')
  LocProvPais = cur.fetchall()
  LocProvPais = LocProvPais[0]
  print(LocProvPais)


  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()
  cur.close()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM paises')
  listaPaises = cur.fetchall()

  cur.execute ('''SELECT *  FROM (paises
              INNER JOIN provincias
              ON paises.IdPais = provincias.IdPais)
              INNER JOIN localidades
              ON localidades.IdProv = provincias.IdProv;''')
  listaPaisProvLoc = cur.fetchall()

  return render_template("perfilSecretaria.html", perfilSecretaria=perfilSecretaria, tiposDocProfesional=listaTiposDoc, nacionalidadProfesional=listaPaises, LocProvPais=LocProvPais, listaPaisProvLoc=listaPaisProvLoc,idSec=idSec)

@app.route('/ModDatosSecre', methods=['GET', 'POST'])
def ModDatosSecre():
  if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    print(data)

    IdSecretaria = str(data['IdSecretaria'])
    NomPac= str(data['NomPac'])
    NumDoc= str(data['NumDoc'])
    TelPac= str(data['TelPac'])
    FecNac= str(data['FecNac'])
    LocPac= str(data['LocPac'])
    DomPac= str(data['DomPac'])
    Estado= str(data['Estado'])

    print(NomPac, NumDoc, TelPac, FecNac,LocPac, DomPac,Estado)

    cur = mysql.connection.cursor()
    cur.execute('UPDATE secretaria SET NomSec="'+NomPac +'",FnaSec="'+FecNac+'",DniSec="'+NumDoc+'",DomSec="'+DomPac+'",IdLoc="'+str(LocPac)+'",TelSec="'+TelPac+'" where IdSec='+str(IdSecretaria)+'')
    cur.connection.commit() 

    return jsonify({'Mensaje':'Correcto'})

@app.route ('/caca', methods=["GET","POST"])
def caca ():
  cur = mysql.connection.cursor()
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


  turnos = cur.fetchall()

  fechaTurno = str (turnos [18][1])
  horaITurno = str (turnos [18][2])
  horaFTurno = str (turnos [18][3])
  EstadoTurno = str (turnos [18][4])
  nombreProfesional = str (turnos [18][10])
  nombrePaciente = str (turnos [18][16])
  dniPaciente  = str (turnos [18][17])
  telefonoPaciente  = str (turnos [18][18])
  EspecialidadProfesional = str (turnos [18][21])
  msjFechaTurno = 'Fecha turno(Año-mes-dia): ' + fechaTurno
  msjHoraITurno = '.                                           Hora inicio turno: ' + horaITurno + 'hs'
  msjHoraFTurno = '.                                                     Hora  fin turno: ' + horaFTurno + 'hs'
  msjEstadoTurno = ''
  msjNombreProfesional = '.                                                                  Profesional: ' + nombreProfesional
  msjNombrePaciente = '.                                                      nombre Paciente: ' + nombrePaciente
  msjDniPaciente  = '.                                                      DNI Paciente: ' + dniPaciente
  msjEspecialidadProfesional = '.                                                       Especialidad: ' + EspecialidadProfesional
  horaAcotada =str(datetime.datetime.strptime(str(horaITurno), "%H:%M:%S").strftime("%H:%M"))
  print ('HORA ACOTADA>>>>>>>>>>>>>>>>', horaAcotada)
  fechaHoy = str (date.today())
  fechaHoyFalsa = str (datetime.date(2020, 3, 22))
  fechaManana = str (date.today() + datetime.timedelta(days=1))
  fechaPasadoManana = str (date.today() + datetime.timedelta(days=2))
  fechaPasadoMananaFalsa = str (datetime.date(2020, 3, 24))
  print ("Fecha turno: ", fechaTurno)
  print ("Fecha hoy: ", fechaHoy)
  print ("Fecha FALSA hoy: ", fechaHoyFalsa)
  print ("Fecha manana: ", fechaManana)
  print ("Fecha pasado manana: ", fechaPasadoManana)
  print ("Fecha FALSA pasado manana: ", fechaPasadoMananaFalsa)
  # America/Argentina/Cordoba
  print ('timezone: ', strftime("%z", gmtime()))
  print ('hora actual:', datetime.datetime.now())
  # if fechaTurno > fechaHoy and fechaTurno < fechaPasadoManana:
  #     print ('la fecha del turno esta bien', fechaTurno)
  # else:
  #     print ('la fecha del turno es vieja,es hoy o no es manana', fechaTurno)
  prefijo = str (54)
  turnosManana = []
  mysql.connection.commit ()
  for turno in turnos:
    if str (turno[1]) == fechaManana or (turno[1]-datetime.timedelta(days=3)).strftime("%A") == 'Friday':
    	 turnosManana.append (turno)
    else:
      # print ('no hay turnos para manana')
      pass
  print (turnosManana, sep="\n")
  return render_template ('caca.html')


@app.route('/gestionarTurnos')
def gestionarTurnos():
  cur = mysql.connection.cursor()

  cur.execute ("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()

  cur.execute ("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()

  cur.execute ('SELECT * FROM paises')
  listaPaises = cur.fetchall ()

  cur.execute ('SELECT * FROM relig')
  listaReligiones =cur.fetchall ()

  listaDias = [[1,'Lunes'],[2,'Martes'],[3,'Miércoles'],[4,'Jueves'],[5,'Viernes'],[6,'Sábado']]
  listaGSanguineos = ['N/S', 'A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-']




  fechaHoy = str(date.today())
  diasasumar = timedelta(days=1)

  diahoy = date.today().strftime("%A")
  diasiguiente = str(date.today()+timedelta(days=1))

##Si hoy es viernes
  if diahoy == 'Friday':
    lunes = str(date.today()+timedelta(days=3))
    sabado = str(date.today()+timedelta(days=1))

    #Si hoy es viernes y el usuario es de tipo 2
    if session['idTusu'] == 2:
      #Usuario a str para la base
      idUsuario = session['idUs']
      idUsuario = str(idUsuario[0])

      #Busco en la vista el Id del Profesional que coincida con el IdUS
      cur = mysql.connection.cursor()
      cur.execute('SELECT IdPro FROM UsProfTipoUs where IdUs="'+idUsuario+'"')
      profesionalUsuario = cur.fetchall()
      profesionalUsuario = str(profesionalUsuario[0][0])

      #Ahora busco los turnos del Profesional para Lunes y sabado de ese profesional
      cur = mysql.connection.cursor()
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
                  ON especialidad.IdEsp = proesp.IdEsp
                  WHERE (turnos.FecTur = %s  or turnos.FecTur = %s )and profesional.IdPro = %s order by turnos.FecTur asc,turnos.HorTur asc""", (sabado, lunes, profesionalUsuario,))
      TurDiasSig = cur.fetchall()
      mysql.connection.commit()

      #TRAIGO LOS TURNOS DE WPP de ese profesional
      cur = mysql.connection.cursor()
      cur.execute('SELECT * from estadoWhatsapps where FecTur="' +
                  sabado+'" or FecTur="'+lunes+'" ')
      wppdiasiguiente = cur.fetchall()
      mysql.connection.commit()

      #Todos los turnos de hoy en adelante
      cur = mysql.connection.cursor()
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
                    ON especialidad.IdEsp = proesp.IdEsp
                    WHERE turnos.FecTur >= %s and profesional.IdPro=%s order by turnos.FecTur asc,turnos.HorTur asc""", (fechaHoy, profesionalUsuario, ))
      listaTurnos = cur.fetchall()
      mysql.connection.commit()

    #Si hoy es viernes y el usuario no es de tipo prof
    else:
      #Ahora busco los turnos de todos para Lunes y sabado de ese profesional
      cur = mysql.connection.cursor()
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
                  ON especialidad.IdEsp = proesp.IdEsp
                  WHERE turnos.FecTur = %s  or turnos.FecTur = %s order by turnos.FecTur asc,turnos.HorTur asc """ , (sabado, lunes,))
      TurDiasSig = cur.fetchall()
      print(TurDiasSig)
      mysql.connection.commit()

    #TRAIGO LOS TURNOS DE WPP de todos
      cur = mysql.connection.cursor()
      cur.execute('SELECT * from estadoWhatsapps where FecTur="' +
                  sabado+'" or FecTur="'+lunes+'"')
      wppdiasiguiente = cur.fetchall()
      mysql.connection.commit()

      #Todos los turnos de hoy en adelante
      cur = mysql.connection.cursor()
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
                    ON especialidad.IdEsp = proesp.IdEsp
                    WHERE turnos.FecTur >= %s order by turnos.FecTur asc,turnos.HorTur asc""", (fechaHoy, ))
      listaTurnos = cur.fetchall()
      mysql.connection.commit()
  else:
    pass

##Si hoy es Sábado
  if diahoy == 'Saturday':
    print('Efectivamente es Sábado')
    lunes = str(date.today()+timedelta(days=2))

    #Si hoy es sabado y el usuario es de tipo 2
    if session['idTusu'] == 2:
      #Usuario a str para la base
      idUsuario = session['idUs']
      idUsuario = str(idUsuario[0])

      #Busco en la vista el Id del Profesional que coincida con el IdUS
      cur = mysql.connection.cursor()
      cur.execute('SELECT IdPro FROM UsProfTipoUs where IdUs="'+idUsuario+'"')
      profesionalUsuario = cur.fetchall()
      profesionalUsuario = str(profesionalUsuario[0][0])

      #Ahora busco los turnos del Profesional para Lunes
      cur = mysql.connection.cursor()
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
                  ON especialidad.IdEsp = proesp.IdEsp
                  WHERE turnos.FecTur = %s and profesional.IdPro = %s order by turnos.FecTur asc,turnos.HorTur asc""", (lunes, profesionalUsuario,))
      TurDiasSig = cur.fetchall()
      print(TurDiasSig)
      mysql.connection.commit()

      #TRAIGO LOS TURNOS DE WPP de ese profesional
      cur = mysql.connection.cursor()
      cur.execute('SELECT * from estadoWhatsapps where FecTur="'+lunes+'"')
      wppdiasiguiente = cur.fetchall()
      mysql.connection.commit()

      #Todos los turnos de hoy en adelante
      cur = mysql.connection.cursor()
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
                    ON especialidad.IdEsp = proesp.IdEsp
                    WHERE turnos.FecTur >= %s and profesional.IdPro=%s order by turnos.FecTur asc,turnos.HorTur asc""", (fechaHoy, profesionalUsuario, ))
      listaTurnos = cur.fetchall()
      mysql.connection.commit()

    #Si hoy es Sábado y el usuario no es de tipo prof
    else:
      #Ahora busco los turnos de todos para Lunes y sabado de ese profesional
      cur = mysql.connection.cursor()
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
                  ON especialidad.IdEsp = proesp.IdEsp
                  WHERE turnos.FecTur = %s order by turnos.FecTur asc,turnos.HorTur asc""", (lunes,))
      TurDiasSig = cur.fetchall()
      mysql.connection.commit()

      #TRAIGO LOS TURNOS DE WPP de todos
      cur = mysql.connection.cursor()
      cur.execute('SELECT * from estadoWhatsapps where FecTur="'+lunes+'"')
      wppdiasiguiente = cur.fetchall()
      mysql.connection.commit()

      #Todos los turnos de hoy en adelante
      cur = mysql.connection.cursor()
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
                    ON especialidad.IdEsp = proesp.IdEsp
                    WHERE turnos.FecTur >= %s order by turnos.FecTur asc,turnos.HorTur asc""", (fechaHoy, ))
      listaTurnos = cur.fetchall()
      mysql.connection.commit()
  else:
    pass

  if diahoy != 'Friday' and diahoy != 'Saturday':
    diasig = str(date.today()+timedelta(days=1))

    #Si hoy NO es sabado y el usuario es de tipo 2
    if session['idTusu'] == 2:
      #Usuario a str para la base
      idUsuario = session['idUs']
      idUsuario = str(idUsuario[0])

      #Busco en la vista el Id del Profesional que coincida con el IdUS
      cur = mysql.connection.cursor()
      cur.execute('SELECT IdPro FROM UsProfTipoUs where IdUs="'+idUsuario+'"')
      profesionalUsuario = cur.fetchall()
      profesionalUsuario = str(profesionalUsuario[0][0])

      #Ahora busco los turnos del Profesional para Lunes
      cur = mysql.connection.cursor()
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
                  ON especialidad.IdEsp = proesp.IdEsp
                  WHERE turnos.FecTur = %s and profesional.IdPro = %s order by turnos.FecTur asc,turnos.HorTur asc""", (diasig, profesionalUsuario,))
      TurDiasSig = cur.fetchall()
      print(TurDiasSig)
      mysql.connection.commit()

      #TRAIGO LOS TURNOS DE WPP de ese profesional
      cur = mysql.connection.cursor()
      cur.execute('SELECT * from estadoWhatsapps where FecTur="'+diasig+'"')
      wppdiasiguiente = cur.fetchall()
      mysql.connection.commit()

      #Todos los turnos de hoy en adelante
      cur = mysql.connection.cursor()
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
                    ON especialidad.IdEsp = proesp.IdEsp
                    WHERE turnos.FecTur >= %s and profesional.IdPro=%s order by turnos.FecTur asc,turnos.HorTur asc""", (fechaHoy, profesionalUsuario, ))
      listaTurnos = cur.fetchall()
      mysql.connection.commit()

    #Si hoy es Sábado y el usuario no es de tipo prof
    else:
      profesionalUsuario = 'profesionalUsuario'
      #Ahora busco los turnos de todos para Lunes y sabado de ese profesional
      cur = mysql.connection.cursor()
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
                  ON especialidad.IdEsp = proesp.IdEsp
                  WHERE turnos.FecTur = %s order by turnos.FecTur asc,turnos.HorTur asc""", (diasig,))
      TurDiasSig = cur.fetchall()
      mysql.connection.commit()

      #TRAIGO LOS TURNOS DE WPP de todos
      cur = mysql.connection.cursor()
      cur.execute('SELECT * from estadoWhatsapps where FecTur="'+diasig+'"')
      wppdiasiguiente = cur.fetchall()
      mysql.connection.commit()

      #Todos los turnos de hoy en adelante
      cur = mysql.connection.cursor()
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
                    ON especialidad.IdEsp = proesp.IdEsp
                    WHERE turnos.FecTur >= %s order by turnos.FecTur asc,turnos.HorTur asc""", (fechaHoy, ))
      listaTurnos = cur.fetchall()
      mysql.connection.commit()
  else:
    pass

  return render_template('gestionarTurnos.html',listaTurnos=listaTurnos, TurSig=TurDiasSig, wppSig=wppdiasiguiente, tiposDocProfesional=listaTiposDoc, nacionalidadProfesional=listaPaises, especialidadProfesional=listaEspecialidades,
                         listaDias=listaDias, tiposGSPaciente=listaGSanguineos, listaReligiones=listaReligiones)

@app.route('/todoslosturnos')
def todoslosturnos():
  cur = mysql.connection.cursor()

  cur.execute ("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()

  cur.execute ("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()

  cur.execute ('SELECT * FROM paises')
  listaPaises = cur.fetchall ()

  cur.execute ('SELECT * FROM relig')
  listaReligiones =cur.fetchall ()

  listaDias = [[1,'Lunes'],[2,'Martes'],[3,'Miércoles'],[4,'Jueves'],[5,'Viernes'],[6,'Sábado']]
  listaGSanguineos = ['N/S', 'A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-']



  if session['idTusu']==2:
    #Usuario a str para la base
    idUsuario=session['idUs']
    idUsuario=str(idUsuario[0])

    #Busco en la vista el Id del Profesional que coincida con el IdUS
    cur = mysql.connection.cursor()
    cur.execute('SELECT IdPro FROM UsProfTipoUs where IdUs="'+idUsuario+'"')
    profesionalUsuario = cur.fetchall()
    profesionalUsuario=str(profesionalUsuario[0][0])

    #Ahora busco los datos del Profesional

    cur.execute('SELECT * FROM profesional where idPro="'+profesionalUsuario+'"')
    profesionalIngreso = cur.fetchall()
    medicos=profesionalIngreso
  else:
    cur = mysql.connection.cursor()
    cur.execute('SELECT IdPro,NomPro FROM profesional')
    medicos = cur.fetchall()
  return render_template('ListadoTurnos.html',medicos=medicos,tiposDocProfesional = listaTiposDoc, nacionalidadProfesional = listaPaises, especialidadProfesional = listaEspecialidades,
       listaDias = listaDias ,tiposGSPaciente=listaGSanguineos,listaReligiones=listaReligiones)


@app.route("/buscarturnos", methods=['POST', 'GET'])
def buscarturnos():
  cur = mysql.connection.cursor()

  cur.execute ("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()

  cur.execute ("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()

  cur.execute ('SELECT * FROM paises')
  listaPaises = cur.fetchall ()

  cur.execute ('SELECT * FROM relig')
  listaReligiones =cur.fetchall ()

  listaDias = [[1,'Lunes'],[2,'Martes'],[3,'Miércoles'],[4,'Jueves'],[5,'Viernes'],[6,'Sábado']]
  listaGSanguineos = ['N/S', 'A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-']


  if request.method == 'POST':
    profesional = str(request.form['profesional'])
    desde = str(request.form['desde'])
    hasta = str(request.form['hasta'])

    if desde == '':
      desde = '2020-01-01'
    else:
      pass

    if hasta == '':
      hasta = '2099-01-01'
    else:
      pass

    if profesional == 'todos':
      cur = mysql.connection.cursor()
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
                    ON especialidad.IdEsp = proesp.IdEsp
                    WHERE turnos.FecTur >= %s and turnos.FecTur<=%s order by turnos.FecTur,turnos.HorTur asc""", (desde, hasta, ))
      turnos = cur.fetchall()
      nombreprofesional = ['Todos los Profesionales', ]

    else:
      cur = mysql.connection.cursor()
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
                    ON especialidad.IdEsp = proesp.IdEsp
                    WHERE (turnos.FecTur >= %s and turnos.FecTur<=%s) and profesional.IdPro=%s order by turnos.FecTur,turnos.HorTur asc""", (desde, hasta, profesional, ))
      turnos = cur.fetchall()

      cur = mysql.connection.cursor()
      cur.execute(
          'Select NomPro from profesional where IdPro="'+profesional+'"')
      nombreprofesional = cur.fetchall()
      nombreprofesional = nombreprofesional[0]

    return render_template('turnosfiltrados.html', turnos=turnos, desde=desde, hasta=hasta, nombreprofesional=nombreprofesional,tiposDocProfesional = listaTiposDoc, nacionalidadProfesional = listaPaises, especialidadProfesional = listaEspecialidades,
       listaDias = listaDias ,tiposGSPaciente=listaGSanguineos,listaReligiones=listaReligiones)








#####################MATIAS##################

@app.route("/calendario", methods=['POST', 'GET'])
def calendario():
  #Si el Usuario es de tipo 2, Profesional
  if session['idTusu'] == 2:
    #Usuario a str para la base
    idUsuario = session['idUs']
    idUsuario = str(idUsuario[0])

    #Busco en la vista el Id del Profesional que coincida con el IdUS
    cur = mysql.connection.cursor()
    cur.execute('SELECT IdPro FROM UsProfTipoUs where IdUs="'+idUsuario+'"')
    profesionalUsuario = cur.fetchall()
    profesionalUsuario = str(profesionalUsuario[0][0])

    #Ahora busco los datos del Profesional

    cur.execute('SELECT * FROM profesional where idPro="' +
                profesionalUsuario+'"')
    profesionalIngreso = cur.fetchall()
    medicos = profesionalIngreso

  #Si no es un usuario de tipo 2, entonces que busque todos los profesionales
  else:
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM profesional where ActPro=0')
    medicos = cur.fetchall()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM prestacion')
  pres = cur.fetchall()
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()
  cur.close()
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()
  cur.close()
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM paises')
  listaPaises = cur.fetchall()
  cur.close()
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM relig')
  listaReligiones = cur.fetchall()
  cur.close()

  cur = mysql.connection.cursor()
  cur.execute('SELECT * from tdni ')
  global tdni
  tdni = cur.fetchall()

  listaDias = [[1, 'Lunes'], [2, 'Martes'], [3, 'Miércoles'],
               [4, 'Jueves'], [5, 'Viernes'], [6, 'Sábado']]
  listaGSanguineos = ['N/S', 'A+', 'A-',
                      'B+', 'B-', '0+', '0-', 'AB+', 'AB-']
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM listadoPacientesjson')
  global res_query
  res_query = cur.fetchall()
  json_dat = {}

  for row in res_query:
    id_paciente = row[0]
    obra_social = {
        "IdPlan": row[9],
        "Plan": row[10],
        "IdOSoc": row[11],
        "NomOSoc": row[12],
        "IdPacPlan": row[13],
        "ActPlan": row[17]
    }
    pac = json_dat.get(id_paciente)

    if pac is not None:
      pac["ObraSocial"].append(obra_social)
    else:
      json_dat[id_paciente] = {
          "IdPaciente": id_paciente,
          "Nombre": row[1],
          "FNac": row[2].strftime("%Y-%m-%d"),
          "Dni": row[3],
          "Domicilio": row[4],
          "Telefono": row[14],
          "Sexo": row[15],
          "Religion": row[16],
          "IdLoc": row[5],
          "NomLoc": row[6],
          "IdPais": row[7],
          "NomPais": row[8],
          "ObraSocial": [obra_social]
      }

  with open('static/paciente.json', 'w') as fp:
      json.dump(list(json_dat.values()), fp, indent=4)
  with open('static/paciente.json') as pacient:
      PacientesC = json.load(pacient)

  return render_template("calendar.html", profesionales=medicos, prestacion=pres, tdni=tdni, tiposDocProfesional=listaTiposDoc, nacionalidadProfesional=listaPaises, especialidadProfesional=listaEspecialidades, listaDias=listaDias, tiposGSPaciente=listaGSanguineos, listaReligiones=listaReligiones)


###CARGA DE PACIENTES

@app.route("/cargarPaciente", methods=['POST', 'GET'])
def cargarPaciente():
  if request.method == 'POST':
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM listadoPacientesjson')
    global res_query
    res_query = cur.fetchall()
    json_dat = {}

    for row in res_query:
      id_paciente = row[0]
      obra_social = {
          "IdPlan": row[9],
          "Plan": row[10],
          "IdOSoc": row[11],
          "NomOSoc": row[12],
          "IdPacPlan": row[13],
          "ActPlan": row[17]
      }
      pac = json_dat.get(id_paciente)

      if pac is not None:
        pac["ObraSocial"].append(obra_social)
      else:
        json_dat[id_paciente] = {
            "IdPaciente": id_paciente,
            "Nombre": row[1],
            "FNac": row[2].strftime("%Y-%m-%d"),
            "Dni": row[3],
            "Domicilio": row[4],
            "Telefono": row[14],
            "Sexo": row[15],
            "Religion": row[16],
            "IdLoc": row[5],
            "NomLoc": row[6],
            "IdPais": row[7],
            "NomPais": row[8],
            "ObraSocial": [obra_social]
        }

    with open('static/paciente.json', 'w') as fp:
        json.dump(list(json_dat.values()), fp, indent=4)
    with open('static/paciente.json') as pacient:
        PacientesC = json.load(pacient)

  return jsonify({'Mensaje': 'Correcto', 'Data': PacientesC})


###

@app.route("/MostrarTurnos", methods=['POST', 'GET'])
def MostrarTurnos():
  if request.method == 'POST':
    global especialidad
    especialidad = []
    global prestacion
    prestacion = []
    data = request.get_json()
    data = data[0]

    profesional = str(data['idProfesional'])

    cur = mysql.connection.cursor()
    cur.execute('SELECT * from TurnosProfesional where IdPro="' +
                (profesional)+'"and EstTur!="2"')
    result = cur.fetchall()
    data = {}
    data = []
    if session['idTusu'] == 1 or session['idTusu'] == 3 or session['idTusu'] == 2:
      global paciente
      paciente = session['idTusu']

      for row in result:
        if row[8] == 0:
          color = '#c9db267e'
        if row[8] == 1:
          color = '#25d873ab'
        if row[8] == 3:
          color = '#225ad3'
        if row[8] == 4:
          color = '#1ca1a6d3'
        horainicio = (str(row[4])).split(':')
        if int(horainicio[0]) > 1 and int(horainicio[0]) < 10:
            hora = '0'+horainicio[0]+':'+horainicio[1]+':'+horainicio[2]
        else:
            hora = horainicio[0]+':'+horainicio[1]+':'+horainicio[2]

        horafin = (str(row[5])).split(':')
        if int(horafin[0]) > 1 and int(horafin[0]) < 10:
          horaf = '0'+horafin[0]+':'+horafin[1]+':'+horafin[2]
        else:
          horaf = horafin[0]+':'+horafin[1]+':'+horafin[2]

        data.append({'id': row[0], 'title': str(row[1]), 'profesional': row[2], 'practica': row[6], 'start': str(
            row[3])+'T'+hora, 'end': str(row[3])+'T'+horaf, 'color': color, 'ObraSocial': row[10]+'-' + row[9]})

      """ with open('static/data.json', 'w') as file:
          json.dump(data, file)
      with open('static/data.json') as datos:
        turnos=json.load(datos)
 """
    else:
      pass

    #Feriados
    cur = mysql.connection.cursor()
    cur.execute('SELECT * from feriados')
    result = cur.fetchall()
    if session['idTusu'] == 1 or session['idTusu'] == 3 or session['idTusu'] == 2:

      for row in result:
        color = 'Red'
        horainicio = str('07:00')
        horafin = str('22:00')

        data.append({'id': row[0], 'title': str(row[1]), 'profesional': 9999, 'practica': 9999, 'start': str(
            row[2])+'T'+horainicio, 'end': str(row[2])+'T'+horafin, 'color': color})

      with open('static/data.json', 'w') as file:
          json.dump(data, file)
      with open('static/data.json') as datos:
        turnos = json.load(datos)


    ###NOMBRE DEL PROFESIONAL
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT NomPro,TatPro from profesional where profesional.IdPro="'+(profesional)+'"')
    result = cur.fetchall()
    global tdAten
    tdAten = result[0][1]
    global nompro
    nompro = result[0][0]

    ###HORARIO ENTRADA SALIDA DEL PROFESIONAL
    ###NOMBRE DEL PROFESIONAL
    cur = mysql.connection.cursor()
    # cur.execute('SELECT * from dha where IdPro="'+(profesional)+'"')
    cur.execute('SELECT * from dha where IdPro= %s and ActDha = %s ', (profesional,0))
    resultado = cur.fetchall()
    horarios = {}
    horarios = []
    for row in resultado:
      horainicio = (str(row[3])).split(':')
      if int(horainicio[0]) > 1 and int(horainicio[0]) < 10:
        start = '0'+horainicio[0]+':'+horainicio[1]+':'+horainicio[2]
      else:
        start = horainicio[0]+':'+horainicio[1]+':'+horainicio[2]

      horafin = (str(row[4])).split(':')
      if int(horafin[0]) > 1 and int(horafin[0]) < 10:
        end = '0'+horafin[0]+':'+horafin[1]+':'+horafin[2]
      else:
        end = horafin[0]+':'+horafin[1]+':'+horafin[2]
      horarios.append(
          {'daysOfWeek': [row[2]], 'startTime': start, 'endTime': end, })
    with open('static/businessHours.json', 'w') as file:
        json.dump(horarios, file)
    with open('static/businessHours.json') as horario:
        Horarios = json.load(horario)

      ###ESPECIALIDADES DEL PROFESIONAL
    cur = mysql.connection.cursor()
    cur.execute('SELECT especialidad.NomEsp,especialidad.IdEsp from proesp INNER JOIN especialidad on proesp.IdEsp=especialidad.IdEsp where proesp.IdPro="'+(profesional)+'"')
    global EspPro
    EspPro = cur.fetchall()
    ###PRACTICA POR ESPECIALIDAD DEL PROFESIONAL
    cur = mysql.connection.cursor()
    cur.execute('SELECT proesp.IdEsp,especialidad.NomEsp, prestacion.IdPrest,prestacion.NomPrest from proesp INNER JOIN especialidad on proesp.IdEsp=especialidad.IdEsp INNER JOIN proesppres on proesppres.IdProEsp=proesp.IdProEsp INNER JOIN prestacion on proesppres.IdPrest=prestacion.IdPrest where proesp.IdPro="' +
                (profesional)+'" ORDER BY especialidad.IdEsp,prestacion.IdPrest asc')
    res = cur.fetchall()

    praespmed = {}
    for row in res:
      Id = row[0]
      Practica = {
          "Id_Practica": row[2],
          "NombrePractica": row[3],
      }
      pract = praespmed.get(Id)
      if pract is not None:
        pract["Practica"].append(Practica)

      else:
        praespmed[Id] = {
            "Id": row[0],
            "Especialidad": row[1],
            "Practica": [Practica]
        }

    with open('static/practica.json', 'w') as fp:
        json.dump(list(praespmed.values()), fp, indent=4)

  #CREACION DEL JSON DATOS DEL PACIENTE DE CADA TURNO PARA LA SECRETARIA

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM listadoPacientesjson')
    global res_query
    res_query = cur.fetchall()
    json_dat = {}

    for row in res_query:
      id_paciente = row[0]
      obra_social = {
          "IdPlan": row[9],
          "Plan": row[10],
          "IdOSoc": row[11],
          "NomOSoc": row[12],
          "IdPacPlan": row[13],
          "ActPlan": row[17]
      }
      pac = json_dat.get(id_paciente)

      if pac is not None:
        pac["ObraSocial"].append(obra_social)
      else:
        json_dat[id_paciente] = {
            "IdPaciente": id_paciente,
            "Nombre": row[1],
            "FNac": row[2].strftime("%Y-%m-%d"),
            "Dni": row[3],
            "Domicilio": row[4],
            "Telefono": row[14],
            "Sexo": row[15],
            "Religion": row[16],
            "IdLoc": row[5],
            "NomLoc": row[6],
            "IdPais": row[7],
            "NomPais": row[8],
            "ObraSocial": [obra_social]
        }

    with open('static/paciente.json', 'w') as fp:
        json.dump(list(json_dat.values()), fp, indent=4)
    with open('static/paciente.json') as pacient:
        PacientesC = json.load(pacient)
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM prestacion')
    pres = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM  especialidad")
    listaEspecialidades = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM  tdni")
    listaTiposDoc = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM paises')
    listaPaises = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM relig')
    listaReligiones = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * from tdni ')
    global tdni
    tdni = cur.fetchall()

    listaDias = [[1, 'Lunes'], [2, 'Martes'], [3, 'Miércoles'],
                 [4, 'Jueves'], [5, 'Viernes'], [6, 'Sábado']]
    listaGSanguineos = ['N/S', 'A+', 'A-',
                        'B+', 'B-', '0+', '0-', 'AB+', 'AB-']

    return jsonify({'Mensaje': 'Correcto', 'Turnos': turnos, 'Horarios': Horarios, 'tiempoprof': '20', 'EspecialidadProfesional': EspPro ,'data':PacientesC})


@app.route("/probando", methods=['POST', 'GET'])
def probando():
  if request.method == "POST":
    data = request.get_json()
    data = data[0]
    DiaTur = data['DiaTur']
    IdPacPlan = data['IdPacPlan']
    HorTur = data['HorTur']
    HorFtur = data['HorFtur']
    IdEsp = str(data['IdEsp'])
    IdProf = str(data['IdProf'])
    IdUs = 6

    print(IdPacPlan)
    ##Obtengo el IdProEsp
    cur = mysql.connection.cursor()
    cur.execute('SELECT IdProEsp from proesp WHERE proesp.IdEsp=' +
                IdEsp+' AND proesp.IdPro='+IdProf+'')
    IdProEsp = cur.fetchall()
    IdProEsp = IdProEsp[0][0]

   #INSERTO EL TURNO

    try:
      cur = mysql.connection.cursor()
      cur.execute('INSERT INTO turnos(FecTur,HorTur,HorFtur,IdProEsp,IdPacPlan,IdUs) values(%s,%s,%s,%s,%s,%s)',
                  (DiaTur, HorTur, HorFtur, IdProEsp, IdPacPlan, IdUs))
      cur.connection.commit()

      profesional = str(data['IdProf'])

      cur = mysql.connection.cursor()
      cur.execute('SELECT * from TurnosProfesional where IdPro="' +
                  (profesional)+'"and EstTur!="2"')
      result = cur.fetchall()
      data = {}
      data = []
      print('Llega  hasta el 1')
      if session['idTusu'] == 1 or session['idTusu'] == 3 or session['idTusu'] == 2:
        global paciente
        paciente = session['idTusu']

        for row in result:
          if row[8] == 0:
            color = '#c9db267e'
          if row[8] == 1:
            color = '#25d873ab'
          if row[8] == 3:
            color = '#225ad3'
          if row[8] == 4:
            color = '#1ca1a6d3'
          horainicio = (str(row[4])).split(':')
          if int(horainicio[0]) > 1 and int(horainicio[0]) < 10:
              hora = '0'+horainicio[0]+':'+horainicio[1]+':'+horainicio[2]
          else:
              hora = horainicio[0]+':'+horainicio[1]+':'+horainicio[2]

          horafin = (str(row[5])).split(':')
          if int(horafin[0]) > 1 and int(horafin[0]) < 10:
            horaf = '0'+horafin[0]+':'+horafin[1]+':'+horafin[2]
          else:
            horaf = horafin[0]+':'+horafin[1]+':'+horafin[2]

          data.append({'id': row[0], 'title': str(row[1]), 'profesional': row[2], 'practica': row[6], 'start': str(
              row[3])+'T'+hora, 'end': str(row[3])+'T'+horaf, 'color': color})

        with open('static/data.json', 'w') as file:
            json.dump(data, file)
        with open('static/data.json') as datos:
          turnos = json.load(datos)

      else:
        pass

        ###NOMBRE DEL PROFESIONAL
      cur = mysql.connection.cursor()
      cur.execute(
          'SELECT NomPro,TatPro from profesional where profesional.IdPro="'+(profesional)+'"')
      result = cur.fetchall()
      global tdAten
      tdAten = result[0][1]
      global nompro
      nompro = result[0][0]

      ###HORARIO ENTRADA SALIDA DEL PROFESIONAL
      ###NOMBRE DEL PROFESIONAL
      cur = mysql.connection.cursor()
      # cur.execute('SELECT * from dha where IdPro="'+(profesional)+'"')
      cur.execute('SELECT * from dha where IdPro= %s and ActDha = %s ', (profesional,0))
      resultado = cur.fetchall()
      horarios = {}
      horarios = []
      for row in resultado:
        horainicio = (str(row[3])).split(':')
        if int(horainicio[0]) > 1 and int(horainicio[0]) < 10:
          start = '0'+horainicio[0]+':'+horainicio[1]+':'+horainicio[2]
        else:
          start = horainicio[0]+':'+horainicio[1]+':'+horainicio[2]

        horafin = (str(row[4])).split(':')
        if int(horafin[0]) > 1 and int(horafin[0]) < 10:
          end = '0'+horafin[0]+':'+horafin[1]+':'+horafin[2]
        else:
          end = horafin[0]+':'+horafin[1]+':'+horafin[2]
        horarios.append(
            {'daysOfWeek': [row[2]], 'startTime': start, 'endTime': end, })
      with open('static/businessHours.json', 'w') as file:
          json.dump(horarios, file)
      with open('static/businessHours.json') as horario:
          Horarios = json.load(horario)

        ###ESPECIALIDADES DEL PROFESIONAL
      cur = mysql.connection.cursor()
      cur.execute('SELECT especialidad.NomEsp,especialidad.IdEsp from proesp INNER JOIN especialidad on proesp.IdEsp=especialidad.IdEsp where proesp.IdPro="'+(profesional)+'"')
      global EspPro
      EspPro = cur.fetchall()
      ###PRACTICA POR ESPECIALIDAD DEL PROFESIONAL
      cur = mysql.connection.cursor()
      cur.execute('SELECT proesp.IdEsp,especialidad.NomEsp, prestacion.IdPrest,prestacion.NomPrest from proesp INNER JOIN especialidad on proesp.IdEsp=especialidad.IdEsp INNER JOIN proesppres on proesppres.IdProEsp=proesp.IdProEsp INNER JOIN prestacion on proesppres.IdPrest=prestacion.IdPrest where proesp.IdPro="' +
                  (profesional)+'" ORDER BY especialidad.IdEsp,prestacion.IdPrest asc')
      res = cur.fetchall()

      praespmed = {}
      for row in res:
        Id = row[0]
        Practica = {
            "Id_Practica": row[2],
            "NombrePractica": row[3],
        }
        pract = praespmed.get(Id)
        if pract is not None:
          pract["Practica"].append(Practica)

        else:
          praespmed[Id] = {
              "Id": row[0],
              "Especialidad": row[1],
              "Practica": [Practica]
          }

      with open('static/practica.json', 'w') as fp:
          json.dump(list(praespmed.values()), fp, indent=4)

      print('Llega  hasta el 2')

    #CREACION DEL JSON DATOS DEL PACIENTE DE CADA TURNO PARA LA SECRETARIA

      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM listadoPacientesjson')
      global res_query
      res_query = cur.fetchall()
      json_dat = {}

      for row in res_query:
        id_paciente = row[0]
        obra_social = {
            "IdPlan": row[9],
            "Plan": row[10],
            "IdOSoc": row[11],
            "NomOSoc": row[12],
            "IdPacPlan": row[13],
            "ActPlan": row[17]
        }
        pac = json_dat.get(id_paciente)

        if pac is not None:
          pac["ObraSocial"].append(obra_social)
        else:
          json_dat[id_paciente] = {
              "IdPaciente": id_paciente,
              "Nombre": row[1],
              "FNac": row[2].strftime("%Y-%m-%d"),
              "Dni": row[3],
              "Domicilio": row[4],
              "Telefono": row[14],
              "Sexo": row[15],
              "Religion": row[16],
              "IdLoc": row[5],
              "NomLoc": row[6],
              "IdPais": row[7],
              "NomPais": row[8],
              "ObraSocial": [obra_social]
          }

      with open('static/paciente.json', 'w') as fp:
          json.dump(list(json_dat.values()), fp, indent=4)
      with open('static/paciente.json') as pacient:
        PacientesC = json.load(pacient)

      print('Llega  hasta el 3')
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM prestacion')
      pres = cur.fetchall()
      cur = mysql.connection.cursor()
      cur.execute("SELECT * FROM  especialidad")
      listaEspecialidades = cur.fetchall()
      cur.close()
      cur = mysql.connection.cursor()
      cur.execute("SELECT * FROM  tdni")
      listaTiposDoc = cur.fetchall()
      cur.close()
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM paises')
      listaPaises = cur.fetchall()
      cur.close()
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM relig')
      listaReligiones = cur.fetchall()
      cur.close()

      cur = mysql.connection.cursor()
      cur.execute('SELECT * from tdni ')
      global tdni
      tdni = cur.fetchall()

      listaDias = [[1, 'Lunes'], [2, 'Martes'], [3, 'Miércoles'],
                   [4, 'Jueves'], [5, 'Viernes'], [6, 'Sábado']]
      listaGSanguineos = ['N/S', 'A+', 'A-',
                          'B+', 'B-', '0+', '0-', 'AB+', 'AB-']

      return jsonify({'Mensaje': 'Correcto', 'Turnos': turnos, 'Horarios': Horarios, 'tiempoprof': '20','data':PacientesC})
    except:
      return jsonify({'Mensaje': 'Algo no salio bien'})


@app.route("/eliminar", methods=['POST', 'GET'])
def eliminar():
  if request.method == 'POST':
    data = request.get_json()
    data = data[0]

    id_del_event = data['id_event']

    ############ Eliminar Turno##########
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM turnos WHERE IdTur="'+(id_del_event)+'"')
    cur.connection.commit()

    profesional = str(data['IdProf'])

    cur = mysql.connection.cursor()
    cur.execute('SELECT * from TurnosProfesional where IdPro="' +
                (profesional)+'"and EstTur!="2"')
    result = cur.fetchall()
    data = {}
    data = []
    print('Llega  hasta el 1')
    if session['idTusu'] == 1 or session['idTusu'] == 3 or session['idTusu'] == 2:
      global paciente
      paciente = session['idTusu']

      for row in result:
        if row[8] == 0:
          color = '#c9db267e'
        if row[8] == 1:
          color = '#25d873ab'
        if row[8] == 3:
          color = '#225ad3'
        if row[8] == 4:
          color = '#1ca1a6d3'
        horainicio = (str(row[4])).split(':')
        if int(horainicio[0]) > 1 and int(horainicio[0]) < 10:
            hora = '0'+horainicio[0]+':'+horainicio[1]+':'+horainicio[2]
        else:
            hora = horainicio[0]+':'+horainicio[1]+':'+horainicio[2]

        horafin = (str(row[5])).split(':')
        if int(horafin[0]) > 1 and int(horafin[0]) < 10:
          horaf = '0'+horafin[0]+':'+horafin[1]+':'+horafin[2]
        else:
          horaf = horafin[0]+':'+horafin[1]+':'+horafin[2]

        data.append({'id': row[0], 'title': str(row[1]), 'profesional': row[2], 'practica': row[6], 'start': str(
            row[3])+'T'+hora, 'end': str(row[3])+'T'+horaf, 'color': color})

      with open('static/data.json', 'w') as file:
          json.dump(data, file)
      with open('static/data.json') as datos:
        turnos = json.load(datos)

    else:
      pass

      ###NOMBRE DEL PROFESIONAL
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT NomPro,TatPro from profesional where profesional.IdPro="'+(profesional)+'"')
    result = cur.fetchall()
    global tdAten
    tdAten = result[0][1]
    global nompro
    nompro = result[0][0]

    ###HORARIO ENTRADA SALIDA DEL PROFESIONAL
    ###NOMBRE DEL PROFESIONAL
    cur = mysql.connection.cursor()
    # cur.execute('SELECT * from dha where IdPro="'+(profesional)+'"')
    cur.execute('SELECT * from dha where IdPro= %s and ActDha = %s ', (profesional,0))
    resultado = cur.fetchall()
    horarios = {}
    horarios = []
    for row in resultado:
      horainicio = (str(row[3])).split(':')
      if int(horainicio[0]) > 1 and int(horainicio[0]) < 10:
        start = '0'+horainicio[0]+':'+horainicio[1]+':'+horainicio[2]
      else:
        start = horainicio[0]+':'+horainicio[1]+':'+horainicio[2]

      horafin = (str(row[4])).split(':')
      if int(horafin[0]) > 1 and int(horafin[0]) < 10:
        end = '0'+horafin[0]+':'+horafin[1]+':'+horafin[2]
      else:
        end = horafin[0]+':'+horafin[1]+':'+horafin[2]
      horarios.append(
          {'daysOfWeek': [row[2]], 'startTime': start, 'endTime': end, })
    with open('static/businessHours.json', 'w') as file:
        json.dump(horarios, file)
    with open('static/businessHours.json') as horario:
        Horarios = json.load(horario)

      ###ESPECIALIDADES DEL PROFESIONAL
    cur = mysql.connection.cursor()
    cur.execute('SELECT especialidad.NomEsp,especialidad.IdEsp from proesp INNER JOIN especialidad on proesp.IdEsp=especialidad.IdEsp where proesp.IdPro="'+(profesional)+'"')
    global EspPro
    EspPro = cur.fetchall()
    ###PRACTICA POR ESPECIALIDAD DEL PROFESIONAL
    cur = mysql.connection.cursor()
    cur.execute('SELECT proesp.IdEsp,especialidad.NomEsp, prestacion.IdPrest,prestacion.NomPrest from proesp INNER JOIN especialidad on proesp.IdEsp=especialidad.IdEsp INNER JOIN proesppres on proesppres.IdProEsp=proesp.IdProEsp INNER JOIN prestacion on proesppres.IdPrest=prestacion.IdPrest where proesp.IdPro="' +
                (profesional)+'" ORDER BY especialidad.IdEsp,prestacion.IdPrest asc')
    res = cur.fetchall()

    praespmed = {}
    for row in res:
      Id = row[0]
      Practica = {
          "Id_Practica": row[2],
          "NombrePractica": row[3],
      }
      pract = praespmed.get(Id)
      if pract is not None:
        pract["Practica"].append(Practica)

      else:
        praespmed[Id] = {
            "Id": row[0],
            "Especialidad": row[1],
            "Practica": [Practica]
        }

    with open('static/practica.json', 'w') as fp:
        json.dump(list(praespmed.values()), fp, indent=4)

  #CREACION DEL JSON DATOS DEL PACIENTE DE CADA TURNO PARA LA SECRETARIA

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM listadoPacientesjson')
    global res_query
    res_query = cur.fetchall()
    json_dat = {}

    for row in res_query:
      id_paciente = row[0]
      obra_social = {
          "IdPlan": row[9],
          "Plan": row[10],
          "IdOSoc": row[11],
          "NomOSoc": row[12],
          "IdPacPlan": row[13],
          "ActPlan": row[17]
      }
      pac = json_dat.get(id_paciente)

      if pac is not None:
        pac["ObraSocial"].append(obra_social)
      else:
        json_dat[id_paciente] = {
            "IdPaciente": id_paciente,
            "Nombre": row[1],
            "FNac": row[2].strftime("%Y-%m-%d"),
            "Dni": row[3],
            "Domicilio": row[4],
            "Telefono": row[14],
            "Sexo": row[15],
            "Religion": row[16],
            "IdLoc": row[5],
            "NomLoc": row[6],
            "IdPais": row[7],
            "NomPais": row[8],
            "ObraSocial": [obra_social]
        }

    with open('static/paciente.json', 'w') as fp:
        json.dump(list(json_dat.values()), fp, indent=4)
    with open('static/paciente.json') as pacient:
        PacientesC = json.load(pacient)

    print('Llega  hasta el 3')
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM prestacion')
    pres = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM  especialidad")
    listaEspecialidades = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM  tdni")
    listaTiposDoc = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM paises')
    listaPaises = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM relig')
    listaReligiones = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * from tdni ')
    global tdni
    tdni = cur.fetchall()

    listaDias = [[1, 'Lunes'], [2, 'Martes'], [3, 'Miércoles'],
                 [4, 'Jueves'], [5, 'Viernes'], [6, 'Sábado']]
    listaGSanguineos = ['N/S', 'A+', 'A-',
                        'B+', 'B-', '0+', '0-', 'AB+', 'AB-']

    return jsonify({'Mensaje': 'Correcto','data':PacientesC, 'Turnos': turnos, 'Horarios': Horarios, 'tiempoprof': '20'})


@app.route("/bloqueardia", methods=['POST', 'GET'])
def bloqueardia():
  if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    diabloqueado = data['diaBloqueado']
    idProfBloq = data['IdProf']
    horadesde = data['bloqueodesde']
    horahasta = data['bloqueohasta']

  #!Busco las especialidades del profesional, para poder acceder a los turnos desde el IdProfEsp
    idsProEsp = []
    especialidades = []
    cur = mysql.connection.cursor()
    cur.execute('SELECT IdProEsp from proesp where IdPro='+idProfBloq+'')
    idsProEsp = list(cur.fetchall())

    for x in idsProEsp:
      especialidades.append(x[0])

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO turnos(FecTur,HorTur,HorFtur,IdProEsp,IdPacPlan,IdUs) values(%s,%s,%s,%s,%s,%s)',
                (diabloqueado, horadesde, horahasta, especialidades[0], 1, '6'))
    cur.connection.commit()

    profesional = str(data['IdProf'])

    cur = mysql.connection.cursor()
    cur.execute('SELECT * from TurnosProfesional where IdPro="' +
                (profesional)+'"and EstTur!="2"')
    result = cur.fetchall()
    data = {}
    data = []

    if session['idTusu'] == 1 or session['idTusu'] == 3 or session['idTusu'] == 2:
      global paciente
      paciente = session['idTusu']

      for row in result:
        if row[8] == 0:
          color = '#c9db267e'
        if row[8] == 1:
          color = '#25d873ab'
        if row[8] == 3:
          color = '#225ad3'
        if row[8] == 4:
          color = '#1ca1a6d3'
        horainicio = (str(row[4])).split(':')
        if int(horainicio[0]) > 1 and int(horainicio[0]) < 10:
            hora = '0'+horainicio[0]+':'+horainicio[1]+':'+horainicio[2]
        else:
            hora = horainicio[0]+':'+horainicio[1]+':'+horainicio[2]

        horafin = (str(row[5])).split(':')
        if int(horafin[0]) > 1 and int(horafin[0]) < 10:
          horaf = '0'+horafin[0]+':'+horafin[1]+':'+horafin[2]
        else:
          horaf = horafin[0]+':'+horafin[1]+':'+horafin[2]

        data.append({'id': row[0], 'title': str(row[1]), 'profesional': row[2], 'practica': row[6], 'start': str(
            row[3])+'T'+hora, 'end': str(row[3])+'T'+horaf, 'color': color})

      with open('static/data.json', 'w') as file:
          json.dump(data, file)
      with open('static/data.json') as datos:
        turnos = json.load(datos)

    else:
      pass

    return jsonify({'Mensaje': 'Correcto', 'Turnos': turnos})



@app.route('/perfilPaciente<string:idPaciente>', methods=['GET', 'POST'])
def perfilpaciente(idPaciente):
  idPac = idPaciente

  #REGENERO EL JSON PARA TENER LOS DATOS ACTUALIZADOS
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM listadoPacientesjson')
  global res_query
  res_query = cur.fetchall()
  json_dat = {}
  print(res_query)

  for row in res_query:
    id_paciente = row[0]
    obra_social = {
        "IdPlan": row[9],
        "Plan": row[10],
        "IdOSoc": row[11],
        "NomOSoc": row[12],
        "IdPacPlan": row[13],
        "ActPlan": row[17]
    }
    pac = json_dat.get(id_paciente)

    if pac is not None:
      pac["ObraSocial"].append(obra_social)
    else:
      json_dat[id_paciente] = {
          "IdPaciente": id_paciente,
          "Nombre": row[1],
          "FNac": row[2].strftime("%Y-%m-%d"),
          "Dni": row[3],
          "Domicilio": row[4],
          "Telefono": row[14],
          "Sexo": row[15],
          "Religion": row[16],
          "IdLoc": row[5],
          "NomLoc": row[6],
          "IdPais": row[7],
          "NomPais": row[8],
          "ObraSocial": [obra_social]
      }

  with open('static/paciente.json', 'w') as fp:
      json.dump(list(json_dat.values()), fp, indent=4)
  with open('static/paciente.json') as pacient:
      PacientesC = json.load(pacient)

  #ID Localidad Paciente
  cur = mysql.connection.cursor()
  cur.execute('SELECT IdLoc FROM paciente where IdPac='+str(idPac)+'')
  idLocalidad = cur.fetchall()
  idLocalidad = str(idLocalidad[0][0])

  #Id & Nombres Loc, Prov, Pais
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM LocProvPais where IdLoc='+str(idLocalidad)+'')
  LocProvPais = cur.fetchall()
  LocProvPais = LocProvPais[0]

  cur.execute('SELECT * FROM prestacion')
  pres = cur.fetchall()

  cur.execute("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()

  cur.execute("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()

  cur.execute('SELECT * FROM paises')
  listaPaises = cur.fetchall()

  cur.execute('SELECT * FROM relig')
  listaReligiones = cur.fetchall()

  cur.execute('SELECT GsaPac FROM paciente where IdPac='+str(idPac)+'')
  GrSgPac = cur.fetchall()
  GrSgPac = GrSgPac[0][0]

  cur.execute('SELECT * from tdni ')
  global tdni
  tdni = cur.fetchall()

  listaDias = [[1, 'Lunes'], [2, 'Martes'], [3, 'Miércoles'],
               [4, 'Jueves'], [5, 'Viernes'], [6, 'Sábado']]
  listaGSanguineos = ['N/S', 'A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-']

  #!Traigo el nombre del paciente, ya que un paciente puede tener varios idPacPlan, filtrare los turnos por el nombre, y no por el IdPacPlan
  cur = mysql.connection.cursor()
  cur.execute('SELECT NomPac from paciente where IdPac='+str(idPac)+'')
  nombrepaciente = cur.fetchall()
  cur.close()

  nombrepaciente = nombrepaciente[0][0]

  cur = mysql.connection.cursor()
  cur.execute('SELECT turnos.IdTur as id,paciente.NomPac as title,profesional.NomPro,turnos.FecTur,turnos.HorTur,turnos.Horftur,especialidad.NomEsp,turnos.EstTur FROM turnos INNER JOIN proesp on turnos.IdProEsp=proesp.IdProEsp	INNER JOIN especialidad	on especialidad.IdEsp=proesp.IdEsp INNER JOIN profesional on proesp.IdPro=profesional.IdPro INNER JOIN pacplan on turnos.IdPacPlan=pacplan.IdPacPlan INNER JOIN paciente on pacplan.IdPac=paciente.IdPac')
  result = cur.fetchall()
  print(result)
  turnos = {}
  turnos = []
  if session['idTusu'] == 1 or session['idTusu'] == 3:
    global paciente
    paciente = session['idTusu']

    for row in result:
      ## Las Horas de Inicio y fin necesito agregarles el 0 siempre que sean menor a las 10 am
      horainicio = (str(row[4])).split(':')
      if int(horainicio[0]) > 1 and int(horainicio[0]) < 10:
        hora = '0'+horainicio[0]+':'+horainicio[1]+':'+horainicio[2]
      else:
        hora = horainicio[0]+':'+horainicio[1]+':'+horainicio[2]

      horafin = (str(row[5])).split(':')
      if int(horafin[0]) > 1 and int(horafin[0]) < 10:
        horaf = '0'+horafin[0]+':'+horafin[1]+':'+horafin[2]
      else:
        horaf = horafin[0]+':'+horafin[1]+':'+horafin[2]

      turnos.append({'id': row[0], 'title': str(row[1]), 'profesional': row[2], 'practica': row[6], 'start': str(
          row[3])+'T'+hora, 'end': str(row[3])+'T'+horaf})
    with open('static/turnos.json', 'w') as file:
        json.dump(turnos, file)

    cur.execute('''SELECT *  FROM (paises
              INNER JOIN provincias
              ON paises.IdPais = provincias.IdPais)
              INNER JOIN localidades
              ON localidades.IdProv = provincias.IdProv;''')
    listaPaisProvLoc = cur.fetchall()

  else:
    pass
  return render_template("perfilPaciente.html", idPac=idPac, tiposDocProfesional=listaTiposDoc, nacionalidadProfesional=listaPaises, especialidadProfesional=listaEspecialidades,
                         listaDias=listaDias, tiposGSPaciente=listaGSanguineos, listaReligiones=listaReligiones, nombrepaciente=nombrepaciente, idPaciente=idPac, LocProvPais=LocProvPais, listaPaisProvLoc=listaPaisProvLoc, GrSgPac=GrSgPac ,PacientesC=PacientesC)


@app.route('/AgObSocPaciente', methods=['GET', 'POST'])
def agregaobrasocialpaciente():
  if request.method == 'POST':
    if not session.get ('usuario'):
      return redirect(url_for('login'))
    
    data = request.get_json()
    data = data[0]
    print(data)

    idPac = str(data['IdPaciente'])
    idPla = str(data['IdPlan'])

    #Verifico que no existan Planes repetidos
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pacplan where IdPac=' +
                idPac+' and IdPlan='+idPla+'')
    resultado = cur.fetchall()
    print(resultado)

    if (len(resultado) > 0):
      print('Ya existe un plan con esos datos')
      return jsonify({'Mensaje': 'Error'})

    #Agrego el Plan al Paciente
    cur = mysql.connection.cursor()
    cur.execute(
        'INSERT INTO pacplan (IdPac,IdPlan) VALUES (%s, %s)', (idPac, idPla))
    cur.connection.commit()

      #REGENERO EL JSON PARA TENER LOS DATOS ACTUALIZADOS
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM listadoPacientesjson')
    global res_query
    res_query = cur.fetchall()
    json_dat = {}
    print(res_query)

    for row in res_query:
      id_paciente = row[0]
      obra_social = {
          "IdPlan": row[9],
          "Plan": row[10],
          "IdOSoc": row[11],
          "NomOSoc": row[12],
          "IdPacPlan": row[13],
          "ActPlan": row[17]
      }
      pac = json_dat.get(id_paciente)

      if pac is not None:
        pac["ObraSocial"].append(obra_social)
      else:
        json_dat[id_paciente] = {
            "IdPaciente": id_paciente,
            "Nombre": row[1],
            "FNac": row[2].strftime("%Y-%m-%d"),
            "Dni": row[3],
            "Domicilio": row[4],
            "Telefono": row[14],
            "Sexo": row[15],
            "Religion": row[16],
            "IdLoc": row[5],
            "NomLoc": row[6],
            "IdPais": row[7],
            "NomPais": row[8],
            "ObraSocial": [obra_social]
        }

      with open('static/paciente.json', 'w') as fp:
          json.dump(list(json_dat.values()), fp, indent=4)
      with open('static/paciente.json') as pacient:
          PacientesC = json.load(pacient)
    return jsonify({'Mensaje': 'Correcto'})


@app.route('/DesactivarOsPaciente', methods=['GET', 'POST'])
def DesactivarOsPaciente():
  if request.method == 'POST':
    if not session.get ('usuario'):
      return redirect(url_for('login'))
    
    data = request.get_json()
    data = data[0]
    print(data)

    idPac = str(data['IdPaciente'])
    idPla = str(data['IdPlan'])

    #Desactivo el Plan Para el Paciente

    cur = mysql.connection.cursor()
    cur.execute('UPDATE pacplan SET AcPacPlan = "1" where IdPac="' +
                idPac+'"and IdPlan="'+idPla+'"')
    cur.connection.commit()
      #REGENERO EL JSON PARA TENER LOS DATOS ACTUALIZADOS
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM listadoPacientesjson')
    global res_query
    res_query = cur.fetchall()
    json_dat = {}
    print(res_query)

    for row in res_query:
      id_paciente = row[0]
      obra_social = {
          "IdPlan": row[9],
          "Plan": row[10],
          "IdOSoc": row[11],
          "NomOSoc": row[12],
          "IdPacPlan": row[13],
          "ActPlan": row[17]
      }
      pac = json_dat.get(id_paciente)

      if pac is not None:
        pac["ObraSocial"].append(obra_social)
      else:
        json_dat[id_paciente] = {
            "IdPaciente": id_paciente,
            "Nombre": row[1],
            "FNac": row[2].strftime("%Y-%m-%d"),
            "Dni": row[3],
            "Domicilio": row[4],
            "Telefono": row[14],
            "Sexo": row[15],
            "Religion": row[16],
            "IdLoc": row[5],
            "NomLoc": row[6],
            "IdPais": row[7],
            "NomPais": row[8],
            "ObraSocial": [obra_social]
        }

      with open('static/paciente.json', 'w') as fp:
          json.dump(list(json_dat.values()), fp, indent=4)
      with open('static/paciente.json') as pacient:
          PacientesC = json.load(pacient)
    return jsonify({'Mensaje': 'Correcto'})


@app.route('/ModDatosPaciente', methods=['GET', 'POST'])
def ModDatosPaciente():
  if request.method == 'POST':
    
    data = request.get_json()
    data = data[0]
    print(data)

    idPac = str(data['IdPaciente'])
    NomPac = str(data['NomPac'])
    TipoDni = str(data['TipoDni'])
    NumDoc = str(data['NumDoc'])
    TelPac = str(data['TelPac'])
    SexoPac = str(data['SexoPac'])
    FecNac = str(data['FecNac'])
    GrupSan = str(data['GrupSan'])
    RelPac = str(data['RelPac'])
    LocPac = str(data['LocPac'])
    DomPac = str(data['DomPac'])
    NacionP = str(data['NacionP'])

    print(NomPac, TipoDni, NumDoc, TelPac, SexoPac,
          FecNac, GrupSan, RelPac, LocPac, DomPac, NacionP)

    cur = mysql.connection.cursor()
    cur.execute('UPDATE paciente SET NomPac="'+NomPac + '", SexPac="'+SexoPac+'",FnacPac="'+FecNac+'",IdTdni="'+TipoDni+'",DniPac="'+NumDoc+'",DomPac="' +
                DomPac+'",IdLoc="'+str(LocPac)+'",GsaPac="'+GrupSan+'",TelPac="'+TelPac+'",IdRel="'+RelPac+'",IdPais="'+NacionP+'" where IdPac='+str(idPac)+'')
    cur.connection.commit()
    return jsonify({'Mensaje': 'Correcto'})


@app.route('/ActivarOsPaciente', methods=['GET', 'POST'])
def ActivarOsPaciente():
  if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    print(data)

    idPac = str(data['IdPaciente'])
    idPla = str(data['IdPlan'])

    cur = mysql.connection.cursor()
    cur.execute('UPDATE pacplan SET AcPacPlan = "0" where IdPac="' +
                idPac+'"and IdPlan="'+idPla+'"')
    cur.connection.commit()
      #REGENERO EL JSON PARA TENER LOS DATOS ACTUALIZADOS
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM listadoPacientesjson')
    global res_query
    res_query = cur.fetchall()
    json_dat = {}
    print(res_query)

    for row in res_query:
      id_paciente = row[0]
      obra_social = {
          "IdPlan": row[9],
          "Plan": row[10],
          "IdOSoc": row[11],
          "NomOSoc": row[12],
          "IdPacPlan": row[13],
          "ActPlan": row[17]
      }
      pac = json_dat.get(id_paciente)

      if pac is not None:
        pac["ObraSocial"].append(obra_social)
      else:
        json_dat[id_paciente] = {
            "IdPaciente": id_paciente,
            "Nombre": row[1],
            "FNac": row[2].strftime("%Y-%m-%d"),
            "Dni": row[3],
            "Domicilio": row[4],
            "Telefono": row[14],
            "Sexo": row[15],
            "Religion": row[16],
            "IdLoc": row[5],
            "NomLoc": row[6],
            "IdPais": row[7],
            "NomPais": row[8],
            "ObraSocial": [obra_social]
        }

      with open('static/paciente.json', 'w') as fp:
          json.dump(list(json_dat.values()), fp, indent=4)
      with open('static/paciente.json') as pacient:
          PacientesC = json.load(pacient)
    return jsonify({'Mensaje': 'Correcto'})


@app.route('/CambioEstado', methods=['GET', 'POST'])
def CambioEstado():
  if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    print(data)

    idturno = str(data['id_event'])
    estadoturno = str(data['estado'])

    print(idturno, estadoturno)

    cur = mysql.connection.cursor()
    cur.execute('UPDATE turnos SET EstTur = "' +
                estadoturno+'" where IdTur="'+idturno+'"')
    cur.connection.commit()
    #REGENERO EL JSON PARA TENER LOS DATOS ACTUALIZADOS
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM listadoPacientesjson')
    global res_query
    res_query = cur.fetchall()
    json_dat = {}
    print(res_query)

    """ for row in res_query:
      id_paciente = row[0]
      obra_social = {
          "IdPlan": row[9],
          "Plan": row[10],
          "IdOSoc": row[11],
          "NomOSoc": row[12],
          "IdPacPlan": row[13],
          "ActPlan": row[17]
      }
      pac = json_dat.get(id_paciente)

      if pac is not None:
        pac["ObraSocial"].append(obra_social)
      else:
        json_dat[id_paciente] = {
            "IdPaciente": id_paciente,
            "Nombre": row[1],
            "FNac": row[2].strftime("%Y-%m-%d"),
            "Dni": row[3],
            "Domicilio": row[4],
            "Telefono": row[14],
            "Sexo": row[15],
            "Religion": row[16],
            "IdLoc": row[5],
            "NomLoc": row[6],
            "IdPais": row[7],
            "NomPais": row[8],
            "ObraSocial": [obra_social]
        }

      with open('static/paciente.json', 'w') as fp:
          json.dump(list(json_dat.values()), fp, indent=4)
      with open('static/paciente.json') as pacient:
          PacientesC = json.load(pacient) """
    return jsonify({'Mensaje': 'Correcto'})


@app.route('/ObSoc')
def ObSoc():
  cur = mysql.connection.cursor()
  #CREAR JSON PARA OBSOCIAL Y PLAN
  os_pl_headers = ['idOS', 'nameOS', 'parent_idOS']
  json_data_os_pl = []
  cur.execute('SELECT IdOs, NomOs, ParentId FROM osocial order by NomOs')
  listaObrasSociales = cur.fetchall()
  for result4 in listaObrasSociales:
      json_data_os_pl.append(dict(zip(os_pl_headers, result4)))
  cur.execute('SELECT IdPlan, NomPlan, IdOs FROM plan order by NomPlan')
  listaPlanes = cur.fetchall()
  for result5 in listaPlanes:
    json_data_os_pl.append(dict(zip(os_pl_headers, result5)))
  with open('static/data/mutual_plan.json', 'w', encoding='utf-8') as obs:
    json.dump(json_data_os_pl, obs, ensure_ascii=False, indent=4)

  cur.execute('SELECT * FROM prestacion')
  pres = cur.fetchall()

  cur.execute("SELECT * FROM  especialidad")
  listaEspecialidades = cur.fetchall()

  cur.execute("SELECT * FROM  tdni")
  listaTiposDoc = cur.fetchall()

  cur.execute('SELECT * FROM paises')
  listaPaises = cur.fetchall()

  cur.execute('SELECT * FROM relig')
  listaReligiones = cur.fetchall()

  cur.execute('SELECT * from tdni ')
  global tdni
  tdni = cur.fetchall()

  listaDias = [[1, 'Lunes'], [2, 'Martes'], [3, 'Miércoles'],
               [4, 'Jueves'], [5, 'Viernes'], [6, 'Sábado']]
  listaGSanguineos = ['N/S', 'A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-']

  return render_template("ObrasSociales.html", tiposDocProfesional=listaTiposDoc, prestacion=pres, tdni=tdni, nacionalidadProfesional=listaPaises, especialidadProfesional=listaEspecialidades,
                         listaDias=listaDias, tiposGSPaciente=listaGSanguineos, listaReligiones=listaReligiones)


@app.route('/NuevosPlanes', methods=['GET', 'POST'])
def NuevosPlanes():
  if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    usuario = session['idUs']
    usuario = str(usuario[0])

    IdOS = str(data['obraSocialPaciente'])
    listaPlanes = data['listaPlanes']
    print(listaPlanes)

    for x in listaPlanes:
      if x=="":
        x="Nombre No Cargado"
      cur = mysql.connection.cursor()
      cur.execute('INSERT INTO plan (NomPlan,IdOs,IdUs) VALUES (%s, %s,%s)', (x, IdOS,usuario))
      cur.connection.commit() 

    #CREAR JSON PARA OBSOCIAL Y PLAN
    cur = mysql.connection.cursor()
    os_pl_headers = ['idOS', 'nameOS', 'parent_idOS']
    json_data_os_pl = []
    cur.execute('SELECT IdOs, NomOs, ParentId FROM osocial order by NomOs')
    listaObrasSociales = cur.fetchall()
    for result4 in listaObrasSociales:
        json_data_os_pl.append(dict(zip(os_pl_headers, result4)))
    cur.execute('SELECT IdPlan, NomPlan, IdOs FROM plan order by NomPlan')
    listaPlanes = cur.fetchall()
    for result5 in listaPlanes:
      json_data_os_pl.append(dict(zip(os_pl_headers, result5)))
    with open('static/data/mutual_plan.json', 'w', encoding='utf-8') as obs:
      json.dump(json_data_os_pl, obs, ensure_ascii=False, indent=4)

    return jsonify({'Mensaje': 'Correcto'})


@app.route('/NuevaObra', methods=['GET', 'POST'])
def NuevaObra():
  if request.method == 'POST':
    usuario = session['idUs']
    data = request.get_json()
    data = data[0]
    print(data)
    usuario = str(usuario[0])

    NomPrest = str(data['NombrePrestador'])
    ContactoPrestador = str(data['ContactoPrestador'])
    TelefonoPrestador = str(data['TelefonoPrestador'])
    EmailPrestador = str(data['EmailPrestador'])
    DireccionPrestador = str(data['DireccionPrestador'])

    cur = mysql.connection.cursor()
    cur.execute('Select * from osocial where NomOs="'+NomPrest+'"')
    result = cur.fetchall()

    if (len(result) > 0):
      print('La obra social ya se encuentra cargada')
      return jsonify({'Mensaje': 'Incorrecto'})
    else:
      cur.execute('INSERT INTO osocial (NomOs, ConOs, TeOs,DirOs,IdUs) VALUES (%s, %s, %s, %s, %s)',
                  (NomPrest, ContactoPrestador, TelefonoPrestador, DireccionPrestador, usuario))
      mysql.connection.commit()

    #CREAR JSON PARA OBSOCIAL Y PLAN
    cur = mysql.connection.cursor()
    os_pl_headers = ['idOS', 'nameOS', 'parent_idOS']
    json_data_os_pl = []
    cur.execute('SELECT IdOs, NomOs, ParentId FROM osocial order by NomOs')
    listaObrasSociales = cur.fetchall()
    for result4 in listaObrasSociales:
        json_data_os_pl.append(dict(zip(os_pl_headers, result4)))
    cur.execute('SELECT IdPlan, NomPlan, IdOs FROM plan order by NomPlan')
    listaPlanes = cur.fetchall()
    for result5 in listaPlanes:
      json_data_os_pl.append(dict(zip(os_pl_headers, result5)))
    with open('static/data/mutual_plan.json', 'w', encoding='utf-8') as obs:
      json.dump(json_data_os_pl, obs, ensure_ascii=False, indent=4)

    return jsonify({'Mensaje': 'Correcto'})




@app.route('/GestOS')
def GestOS():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM prestacion')
    pres = cur.fetchall()

    cur.execute("SELECT * FROM  especialidad")
    listaEspecialidades = cur.fetchall()

    cur.execute("SELECT * FROM  tdni")
    listaTiposDoc = cur.fetchall()

    cur.execute('SELECT * FROM paises')
    listaPaises = cur.fetchall()

    cur.execute('SELECT * FROM relig')
    listaReligiones = cur.fetchall()

   

    cur.execute('SELECT * from tdni ')
    global tdni
    tdni = cur.fetchall()

    listaDias = [[1, 'Lunes'], [2, 'Martes'], [3, 'Miércoles'],
                [4, 'Jueves'], [5, 'Viernes'], [6, 'Sábado']]
    listaGSanguineos = ['N/S', 'A+', 'A-', 'B+', 'B-', '0+', '0-', 'AB+', 'AB-']



    cur = mysql.connection.cursor()
    cur.execute ('Select * from osocial')
    obras=cur.fetchall()

    return render_template("gestionObras.html", obras=obras,tiposDocProfesional=listaTiposDoc, prestacion=pres, tdni=tdni, nacionalidadProfesional=listaPaises, especialidadProfesional=listaEspecialidades,
                         listaDias=listaDias, tiposGSPaciente=listaGSanguineos, listaReligiones=listaReligiones)


@app.route('/EditarObra<string:idObra>')
def EditarObra(idObra):
  IdObra = str(idObra)

  cur = mysql.connection.cursor()
  cur.execute('Select * from osocial where IdOs="'+IdObra+'"')
  datosObra = cur.fetchall()
  datosObra=datosObra[0]

  cur = mysql.connection.cursor()
  cur.execute('Select * from plan where IdOs="'+IdObra+'"')
  planObra = cur.fetchall()

  print(planObra)
  return render_template("EditarObra.html",planObra=planObra,datosObra=datosObra,IdObra=IdObra)

@app.route('/ActivarOsPrestador', methods=['GET', 'POST'])
def ActivarOsPrestador():
  if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    print(data)

    idObra = str(data['IdObra'])
    idPlan = str(data['IdPlan'])
    print(idObra,idPlan)

    cur = mysql.connection.cursor()
    cur.execute('UPDATE plan SET AcPlan = "0" where IdPlan="'+idPlan+'"')
    cur.connection.commit()
    return jsonify({'Mensaje':'Correcto'})

@app.route('/DesactivarOsPrestador', methods=['GET', 'POST'])
def DesactivarOsPrestador():
  if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    print(data)

    idObra = str(data['IdObra'])
    idPlan = str(data['IdPlan'])
    print(idObra,idPlan)

    cur = mysql.connection.cursor()
    cur.execute('UPDATE plan SET AcPlan = "1" where IdPlan="'+idPlan+'"')
    cur.connection.commit()
    return jsonify({'Mensaje':'Correcto'})

@app.route('/CambiosPrestador', methods=['GET', 'POST'])
def CambiosPrestador():
  if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    print(data)

    NomObr = str(data['NomObr'])
    ConObr=str(data['ConObr'])
    TelObr =str(data['TelObr'])
    DirObr =str(data['DirObr'])
    EstObr =str(data['EstObr'])
    IdObra = str(data['idObra'])
    print(IdObra)
  
    cur = mysql.connection.cursor()
    cur.execute('UPDATE osocial SET NomOs="'+NomObr + '", ConOs="'+ConObr+'",TeOs="' +
                TelObr+'",DirOs="'+DirObr+'",AcOs="'+EstObr+'" where IdOs='+str(IdObra)+'')
    cur.connection.commit()
    return jsonify({'Mensaje':'Correcto'})

@app.route('/loginPacientes')
def loginPacientes():
  global pacienteplan
  return render_template("loginPacientes.html")
  #return render_template("paginaNoDisponible.html")


@app.route('/ingresoPacientes', methods=['GET', 'POST'])
def ingresoPacientes():
  if request.method == 'POST':
    dnipaciente=request.form['dnipac']
    
    #Busco si hay coincidencia con algun dni de paciente
    cur = mysql.connection.cursor()
    cur.execute('select * from paciente  where DniPac='+str(dnipaciente)+'')
    resultado=cur.fetchall()
    if len(resultado)==1:
      paciente=resultado[0]
      session['idUs'] = paciente [0],
      session['usuario'] = paciente[1],
      session['idTusu'] = paciente [16]
      global idPaciente
      idPaciente=str(session['idUs'][0])

      cur.execute('SELECT * FROM pacplan INNER JOIN plan on pacplan.IdPlan = plan.IdPlan INNER JOIN osocial on plan.IdOs=osocial.IdOs where pacplan.IdPac='+str(idPaciente)+'')
      global pacienteplan
      pacienteplan=cur.fetchall()
      print('Estos son los planes del paciente',pacienteplan)


      idPaciente=session['idUs'][0]
      global nombrepaciente
      nombrepaciente=session['usuario'][0]
      global tipoUsuario
      tipoUsuario=session['idTusu']
      #return render_template("paginaNoDisponible.html")
      return render_template("bienvenidaPaciente.html", nombrepaciente=nombrepaciente, pacplan=pacienteplan,idPaciente=idPaciente)

    if len(resultado)==0:
      flash ("Lo sentimos, su DNI no se encuentra en el registro de pacientes! - Registrese para continuar", 'danger')
      #return render_template("paginaNoDisponible.html")
      return render_template("registerPacientes.html")
    if len(resultado)>1:
      #return render_template("paginaNoDisponible.html")
      print ('EERRROOOR')

    return render_template("inicio.html")


@app.route('/turnopaciente')
def turnopaciente():
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM profesional where ActPro=0')
  profesionales=cur.fetchall()

  idPaciente=str(session['idUs'][0])

  cur.execute('SELECT * FROM pacplan INNER JOIN plan on pacplan.IdPlan = plan.IdPlan INNER JOIN osocial on plan.IdOs=osocial.IdOs where pacplan.IdPac='+str(idPaciente)+'')
  global pacienteplan
  pacienteplan=cur.fetchall()
  print('Estos son los planes del paciente',pacienteplan)


  idPaciente=session['idUs'][0]
  global nombrepaciente
  nombrepaciente=session['usuario'][0]
  global tipoUsuario
  return render_template("turnopaciente.html", profesionales=profesionales, pacplan=pacienteplan)

@app.route('/EspProf', methods=['GET', 'POST'])
def EspProf():
  if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    idprof=data['IdProf']

    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM proesp INNER JOIN especialidad on proesp.IdEsp=especialidad.IdEsp where IdPro='+str(idprof)+'')
    EspProfesional=cur.fetchall()
    idPaciente=str(session['idUs'][0])

    cur.execute('SELECT * FROM pacplan INNER JOIN plan on pacplan.IdPlan = plan.IdPlan INNER JOIN osocial on plan.IdOs=osocial.IdOs where pacplan.IdPac='+str(idPaciente)+'')
    global pacienteplan
    pacienteplan=cur.fetchall()
    print('Estos son los planes del paciente',pacienteplan)


    idPaciente=session['idUs'][0]
    global nombrepaciente
    nombrepaciente=session['usuario'][0]
    global tipoUsuario

    return jsonify({'Mensaje':'Correcto','Data':EspProfesional})

@app.route('/TraerTurnos', methods=['GET', 'POST'])
def TraerTurnos():
  if request.method == 'POST':
    data = request.get_json()
    data = data
    idProfesional=str(data[0]['idProfesional'])


    cur = mysql.connection.cursor()
    cur.execute('SELECT * from TurnosProfesional where IdPro="' +
                (idProfesional)+'"and EstTur!="2"')
    result = cur.fetchall()
    
    cur.execute('SELECT TatPro from profesional where IdPro="' +(idProfesional)+'"')
    tiempoprof=cur.fetchall()
    tiempoprof=str(tiempoprof[0][0])
    print(tiempoprof)

  
    data = {}
    data = []
    if session['idTusu'] == 4:
      global paciente
      paciente = session['idTusu']

      for row in result:
        horainicio = (str(row[4])).split(':')
        if int(horainicio[0]) > 1 and int(horainicio[0]) < 10:
            hora = '0'+horainicio[0]+':'+horainicio[1]+':'+horainicio[2]
        else:
            hora = horainicio[0]+':'+horainicio[1]+':'+horainicio[2]

        horafin = (str(row[5])).split(':')
        if int(horafin[0]) > 1 and int(horafin[0]) < 10:
          horaf = '0'+horafin[0]+':'+horafin[1]+':'+horafin[2]
        else:
          horaf = horafin[0]+':'+horafin[1]+':'+horafin[2]

        data.append({'id': row[0], 'title': 'Ocupado', 'profesional': row[2], 'practica': row[6], 'start': str(
            row[3])+'T'+hora, 'end': str(row[3])+'T'+horaf, 'color': 'red'})

      else:
        pass
    #Feriados
    cur = mysql.connection.cursor()
    cur.execute('SELECT * from feriados')
    result = cur.fetchall()

    for row in result:
      color = 'Red'
      horainicio = str('07:00')
      horafin = str('22:00')

      data.append({'id': row[0], 'title': str(row[1]), 'profesional': 9999, 'practica': 9999, 'start': str(
          row[2])+'T'+horainicio, 'end': str(row[2])+'T'+horafin, 'color': color})

      with open('static/turnosexternos.json', 'w') as file:
          json.dump(data, file)

      with open('static/turnosexternos.json') as externos:
          turnosexternos = json.load(externos)
      
    ###HORARIO ENTRADA SALIDA DEL PROFESIONAL
    ###NOMBRE DEL PROFESIONAL
    cur = mysql.connection.cursor()
    cur.execute('SELECT * from dha where IdPro= %s and ActDha = %s ',
                (idProfesional, 0))
    resultado = cur.fetchall()
    horarios = {}
    horarios = []
    for row in resultado:
      horainicio = (str(row[3])).split(':')
      if int(horainicio[0]) > 1 and int(horainicio[0]) < 10:
        start = '0'+horainicio[0]+':'+horainicio[1]+':'+horainicio[2]
      else:
        start = horainicio[0]+':'+horainicio[1]+':'+horainicio[2]

      horafin = (str(row[4])).split(':')
      if int(horafin[0]) > 1 and int(horafin[0]) < 10:
        end = '0'+horafin[0]+':'+horafin[1]+':'+horafin[2]
      else:
        end = horafin[0]+':'+horafin[1]+':'+horafin[2]
      horarios.append(
          {'daysOfWeek': [row[2]], 'startTime': start, 'endTime': end, })
    with open('static/businessHours.json', 'w') as file:
        json.dump(horarios, file)
    with open('static/businessHours.json') as horario:
        horariotrabajo = json.load(horario)


    return jsonify({'Mensaje': 'Correcto', 'Turnos': turnosexternos,'Horarios':horariotrabajo,'tiempoprof':tiempoprof})


@app.route('/crearTurnoExterno', methods=['GET', 'POST'])
def crearTurnoExterno():
  if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    #[{'idProfesional': '6', 'idEspecialidad': '20', 'HorTur': '08:45', 'HorFtur': '09:20', 'DiaTur': '2020-05-08', 'idPacientePlan': '2'}]
    idProfesional=str(data['idProfesional'])
    idEspecialidad=str(data['idEspecialidad'])
    DiaTur=str(data['DiaTur'])
    HorTur=str(data['HorTur'])
    HorFtur=str(data['HorFtur'])
    IdPacPlan=str(data['idPacientePlan'])
    IdUs=6

    #Nombre del Paciente para el Email
    cur = mysql.connection.cursor()
    cur.execute('SELECT NomPac from pacplan INNER JOIN paciente ON pacplan.IdPac= paciente.IdPac WHERE IdPacPlan='+str(IdPacPlan)+'')
    NomPac = cur.fetchall()
    NomPac = NomPac[0][0]

    print('Este es el paciente plan',NomPac)


    ##Obtengo el IdProEsp
    cur = mysql.connection.cursor()
    cur.execute('SELECT IdProEsp from proesp WHERE proesp.IdEsp=' +
                idEspecialidad+' AND proesp.IdPro='+idProfesional+'')
    IdProEsp = cur.fetchall()
    IdProEsp = IdProEsp[0][0]

    #Nombre del Profesional para el Email
    cur = mysql.connection.cursor()
    cur.execute('SELECT NomPro from profesional INNER JOIN proesp on proesp.IdPro=profesional.IdPro WHERE IdProEsp='+str(IdProEsp)+'')
    NomPro = cur.fetchall()
    NomPro = NomPro[0][0]

    print('Este es el nombre del profesional',NomPro)

  #Envio el Email del Turno
    nombreEmail = str(NomPac)
    

    me = "environ.get['ME_EMAIL']
    my_password = environ.get['MY_PASSWORD']
    you = environ.get['EMAIL']
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Nuevo Turno"
    msg['From'] = me
    msg['To'] = you

    html = '<html><body><p><b>Nuevo Turno para</b> '+ NomPro +' </p><br><p><b>Paciente :</b> '+ NomPac +'</p><br><p><b>Día Turno : </b>'+ DiaTur +'</p><br><p><b>Hora : </b>'+  HorTur+'</p></body></html>'
    part2 = MIMEText(html, 'html')

    msg.attach(part2)

    # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    # uncomment if interested in the actual smtp conversation
    # s.set_debuglevel(1)
    # do the smtp auth; sends ehlo if it hasn't been sent already
    s.login(me, my_password)

    s.sendmail(me, you, msg.as_string())
    s.quit()

    try:
      cur = mysql.connection.cursor()
      cur.execute('INSERT INTO turnos(FecTur,HorTur,HorFtur,IdProEsp,IdPacPlan,IdUs) values(%s,%s,%s,%s,%s,%s)',
                  (DiaTur, HorTur, HorFtur, IdProEsp, IdPacPlan, IdUs))
      cur.connection.commit()

      flash("Turno Cargado Correctamente. Podra verlo en Mis Turnos","info")
      return jsonify({'Mensaje':'Correcto'})
    except:
      return jsonify({'Mensaje': 'Algo Salio Mal'})
    


@app.route('/consultaturnopaciente<string:idPaciente>', methods=['GET', 'POST'])
def consultaturnopaciente(idPaciente):
  idPaciente=idPaciente
    
  cur = mysql.connection.cursor()
  cur.execute('SELECT NomPac from paciente where IdPac='+str(idPaciente)+'')
  nombrepaciente = cur.fetchall()
  nombrepaciente = str(nombrepaciente[0][0])
  print (nombrepaciente)

  cur = mysql.connection.cursor()
  cur.execute('SELECT turnos.IdTur as id,paciente.NomPac ,profesional.NomPro,turnos.FecTur,turnos.HorTur,turnos.Horftur,especialidad.NomEsp,turnos.EstTur FROM turnos INNER JOIN proesp on turnos.IdProEsp=proesp.IdProEsp	INNER JOIN especialidad	on especialidad.IdEsp=proesp.IdEsp INNER JOIN profesional on proesp.IdPro=profesional.IdPro INNER JOIN pacplan on turnos.IdPacPlan=pacplan.IdPacPlan INNER JOIN paciente on pacplan.IdPac=paciente.IdPac where paciente.NomPac="'+nombrepaciente+'"order by turnos.FecTur,turnos.HorTur asc')
  result = cur.fetchall()
  print (result)

  return render_template('consultaturnopaciente.html',result=result,nombrepaciente=nombrepaciente)


@app.route('/atras')
def atras():
  idPaciente=str(session['idUs'][0])
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM pacplan INNER JOIN plan on pacplan.IdPlan = plan.IdPlan INNER JOIN osocial on plan.IdOs=osocial.IdOs where pacplan.IdPac='+str(idPaciente)+'')
  global pacienteplan
  pacienteplan=cur.fetchall()
  print('Estos son los planes del paciente',pacienteplan)


  idPaciente=session['idUs'][0]
  global nombrepaciente
  nombrepaciente=session['usuario'][0]
  global tipoUsuario
  return render_template("bienvenidaPaciente.html", nombrepaciente=nombrepaciente, pacplan=pacienteplan,idPaciente=idPaciente)


@app.route('/RegistrarPaciente', methods=['GET', 'POST'])
def RegistrarPaciente():
  if request.method == 'POST':
    apellido = request.form['Apellido'].upper()
    nombre = request.form['Nombre'].title()
    nombreComplProfesional = apellido + ', ' + nombre
    dni=str(request.form['dni'])
    fecnac=str(request.form['fecnac'])
    sexo=str(request.form['sexo'])
    telefono=str(request.form['telefono'])
    obraSocial = request.form ['obraSocialPaciente']
    planPaciente = request.form ['planObSoPaciente']
    #print(nombre, dni, fecnac, sexo, telefono, ' id Osocial ',obraSocial, 'id del plan -> ',planPaciente)
    

 
    #INSERTO EL USUARIO
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO paciente (NomPac,SexPac,FnacPac,DniPac,TelPac) values(%s,%s,%s,%s,%s)',
                (nombreComplProfesional, sexo, fecnac, dni, telefono))
    cur.connection.commit()

    #BUSCO EL ID DEL USUARIO INSERTADO
    cur = mysql.connection.cursor()
    cur.execute('SELECT * from paciente where DniPac="'+dni+'"')
    result = cur.fetchall()
    idPAC=str(result[0][0])

    #LE CARGO DE PECHO OS PARTICULAR PLAN BASE
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO pacplan (IdPlan,IdPac) values(%s,%s)',
                (planPaciente, idPAC))
    cur.connection.commit()
  flash ("Muchas Gracias!! Ya se encuentra registrado, ingrese su DNI para continuar","success")
  return render_template("loginPacientes.html")
  #return render_template("paginaNoDisponible.html")



@app.route('/Feriados')
def Feriados():
  cur = mysql.connection.cursor()
  cur.execute('Select * from feriados order by FecFer asc')
  nolaborales=cur.fetchall()

  return render_template('feriados.html', feriados=nolaborales)


@app.route('/CargarFeriado', methods=['GET', 'POST'])
def CargarFeriado():
  if request.method == 'POST':
    DiaFeriado = str(request.form['DiaFeriado'])
    MotivoFeriado=request.form['MotivoFeriado']

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO feriados (FecFer,NomFer) values(%s,%s)',(DiaFeriado, MotivoFeriado))
    cur.connection.commit()

    flash('Dia No Laboral Cargado Correctamente','success')
    return redirect(url_for('Feriados'))

@app.route('/BorrarFeriado<string:idFeriado>', methods=['GET', 'POST'])
def BorrarFeriado(idFeriado):
  idFeriado=str(idFeriado)
  cur = mysql.connection.cursor()
  cur.execute('DELETE FROM feriados where IdFer=%s',(idFeriado))
  cur.connection.commit()

  flash('Dia No Laboral Eliminado Correctamente','danger')
  return redirect(url_for('Feriados'))


@app.route('/cargamasiva')
def cargamasiva():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM profesional")
  listaProf=cur.fetchall()
  

  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM osocial")
  osocial=cur.fetchall()
 

  return render_template("cargamasiva.html" , listaProf=listaProf,osocial=osocial)

@app.route('/TraerPlanes', methods=['GET', 'POST'])
def TraerPlanes():
 if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    idObra=data['idObra']
   
    cur = mysql.connection.cursor()
    cur.execute('SELECT * from plan where IdOs="'+idObra+'"')
    plan=cur.fetchall()
    

    return jsonify({"Mensaje":"ANDA","Planes":plan})
    
@app.route('/LlenarTabla', methods=['GET', 'POST'])
def LlenarTabla():
 if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    planes=[]

    cur = mysql.connection.cursor()
    for x in data['listaplanes']:
      cur.execute('SELECT * from ObraPlan where IdPlan="'+x+'"')
      planes.append(cur.fetchall())
    

    return jsonify({"Mensaje":"ANDA", "ListaPlanes":planes})

@app.route('/InsertPlanes', methods=['GET', 'POST'])
def InsertPlanes():
 if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    prof = data['IdProfesional']
    planes=[]


    #Verifico que ya esten cargados los planes para el profesional
    acargar=[] #Almaceno los que se van a guardar
    nocargar=[] #Almaceno los que NO se van a cargar

    cur = mysql.connection.cursor()
    for x in data['listaplanes']:
      cur.execute('SELECT * from proplan where IdPlan="'+x+'" and IdPro="'+prof+'"')
      resultado=cur.fetchall()
      print (resultado)
      if len(resultado)>0:
        nocargar.append(x)
      else:
        acargar.append(x)

    #Realizo la carga de los planes
    cur = mysql.connection.cursor()
    for p in acargar:
      cur.execute('INSERT INTO proplan (IdPlan,IdPro) values(%s,%s)',(p, prof))
      cur.connection.commit()

    #Obtengo los que se cargaron, y los que no, para retornar y mostrar por pantalla
    cargados=[]
    nocargado=[]

    for x in acargar:
      cur.execute('SELECT * from ObraPlan where IdPlan="'+x+'"')
      cargados.append(cur.fetchall())

    for y in nocargar:
      cur.execute('SELECT * from ObraPlan where IdPlan="'+y+'"')
      nocargado.append(cur.fetchall())

    print(cargados)
    print(nocargado)

    return jsonify({"Mensaje":"ANDA","Cargados":cargados,"NoCargados":nocargado})
    
@app.route('/LlenarTablaInferior', methods=['GET', 'POST'])
def LlenarTablaInferior():
 if request.method == 'POST':
    data = request.get_json()
    data = data[0]
    IdProfesional=str(data['IdProfesional'])

    cur = mysql.connection.cursor()
    cur.execute('SELECT * from plan INNER JOIN proplan on plan.IdPlan=proplan.IdPlan INNER JOIN osocial on osocial.IdOs=plan.IdOs where IdPro="'+IdProfesional+'"')
    planprof=cur.fetchall()
    

    return jsonify({"Mensaje":"ANDA", "PlanProf":planprof})

