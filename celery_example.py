from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response, jsonify
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
import os 
import json
from datetime import datetime
from flask_restful import Resource, Api
from flask_celery import make_celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='amqp://localhost',
    CELERY_RESULT_BACKEND='amqp://localhost'
)
celery = make_celery(app)

@app.route ('/')
def index ():
  return render_template ('index.html')

@app.route ('/caca/<name>', methods=["GET","POST"])
def caca (name):
    reverse.delay (name)
    return 'probando resps celery'

@celery.task(name ='celery_example.reverse')
def reverse(string):
    return string [::-1]

if __name__ == '__main__':
    app.secret_key = "privatekeyMellitus"
    app.run(port = 3000, debug = True)
