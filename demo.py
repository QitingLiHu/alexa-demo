from flask import Flask
from firebase import firebase
import json
import random
import datetime


firebase = firebase.FirebaseApplication('https://aws-demo-5c44a-default-rtdb.firebaseio.com/', None)

files = ["onus check", "a2a deposit", "limits"]

app = Flask(__name__)

def getRandomData(id):
	today = datetime.date.today()
	date = str(today.day) + '-' + str(today.month) + '-' + str(today.year)

	datos = {
	'id':int(id) + 1,
	'dia':date,
	'fichero':files[random.randint(0, 2)],
	'tickets':random.randint(1, 2000),
	'status':'ok',
	'tiempo_ejecucion':random.randint(20, 25) }
	return datos

@app.route('/hello')
def index():
    return 'Hello everybody! I see Iudit, Sera, Nera, Cuitin, Fores, Joje, Alex Dinera'

@app.route('/getData')
def getData():
	ejecuciones = firebase.get('/demo/historico','')

	return(ejecuciones)

@app.route('/insertData')
def insertData():
	info = getLastExecutionInformation()
	resultado = firebase.post('/demo/historico',getRandomData(info['id']))
	firebase.post
	return resultado

@app.route('/getLastExecution')
def getLastExecution():
	info = getLastExecutionInformation()

	return('La última ejecución fue la número %s, con fecha %s. Se cargaron %s tickets del fichero %s con un tiempo de ejecución de %s segundos.' % (info['id'], info['dia'], info['tickets'], info['fichero'], info['tiempo_ejecucion']))
 

def getLastExecutionInformation():
	#value_at_index = ejecuciones.values()[len(ejecuciones)]
	#for clave in ejecuciones:
    # Hacer algo con esa clave
	#	print(clave)
	#	print(ejecuciones[clave]['id'])

	ejecuciones = firebase.get('/demo/historico','')
	keys_list = list(ejecuciones)
	num_keys = len(keys_list)
	key = keys_list[num_keys-1]
	print("Last file loaded")
	print(ejecuciones)
	return ejecuciones[key];

app.run(host='0.0.0.0', port=81)




