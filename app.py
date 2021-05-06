from flask import Flask, request
from firebase import firebase
import json
import random
import datetime


firebase = firebase.FirebaseApplication('https://aws-demo-5c44a-default-rtdb.firebaseio.com/', None)

files = ["onus check", "a2a deposit", "limits"]

app = Flask(__name__)

resId = 0

@app.route("/")
def home():
	print("Se ha conectado una persona")
	return 'Welcome to the piece of shit server'

def getContador():
	return firebase.get('/demo/ficheros/contador','')

def updateLZFiles(ficheros):
	print(ficheros)
	contador = getContador() + ficheros

	resultado = firebase.put('/demo/ficheros', 'contador', contador)

	return str(contador)


def getRandomData(id):
	today = datetime.date.today()
	date = str(today.day) + '-' + str(today.month) + '-' + str(today.year)
	global resId
	resId = int(id) + 1
	datos = {
	'id':resId,
	'dia':date,
	'fichero':files[random.randint(0, 2)],
	'tickets':random.randint(1, 2000),
	'status':'ok',
	'tiempo_ejecucion':random.randint(20, 25) }
	return datos

@app.route('/hello')
def index():
    return 'Hello everybody! I see Iudit, Sera, Nera, Cuitin, Fores, Joje, Alex Dinera, Soufia, Tela'

@app.route('/getData')
def getData():
	ejecuciones = firebase.get('/demo/historico','')

	return(ejecuciones)

@app.route('/insertData')
def insertData():
	info = getLastExecutionInformation()
	id = info['id']
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

@app.route('/webhook', methods=['POST'])
def webhook():
	print('webhook')
	req = request.get_json(silent=True, force=True)
	fulfillmentText = ''
	query_result = req.get('queryResult')

	if query_result.get('action') == 'carga_de_alertas':
		if getContador() > 0:
			insertData()
			fulfillmentText = 'He cargado el fichero con id ' + str(resId)
		else:
			fulfillmentText = 'No hay ficheros para cargar.'

	elif query_result.get('action') == 'actualizar_ficheros':
		parameters = query_result.get('parameters')
		operacion = ''
		ficheros = 1
		if parameters.get('actualiza_ficheros') == 'envia':
			operacion = 'Se han añadido '
			if len(str(parameters.get('number-integer'))) > 0:
				ficheros = int(parameters.get('number-integer'))
				updateLZFiles(ficheros)
			else: 
				updateLZFiles(1)
		elif parameters.get('actualiza_ficheros') == 'elimina':
			operacion = 'Se han eliminado '
			if len(str(parameters.get('number-integer'))) > 0:
				ficheros = int(parameters.get('number-integer'))
				updateLZFiles(ficheros * -1)
			else: 
				updateLZFiles(-1)

		ficheros = getContador()

		text = ' ficheros.'
		if ficheros == 1:
			text = 'fichero.'
		fulfillmentText = operacion + str(ficheros) + ' ficheros. Actualmente hay ' + str(getContador()) + text

	elif query_result.get('action') == 'numero_ficheros':
		text = 'ficheros.'
		ficheros = getContador()
		if ficheros == 1:
			text = 'fichero.'
		fulfillmentText = 'Hay ' + str(getContador()) + ' '  + text

	elif query_result.get('action') == 'ejecucion':
		info = getLastExecutionInformation()
		parameters = query_result.get('parameters')
		print(parameters)

		print(info)
		if len(parameters.get('tiempo_ejecucion')) > 0:
			print('tiempo de ejecucion')
			fulfillmentText = 'La última ejecución con id ' + str(info['id']) + ' duró ' + str(info['tiempo_ejecucion']) + ' segundos'
		elif len(parameters.get('numero_alertas')) > 0:
			print('numero de alertas')
			fulfillmentText = 'En la última ejecución con id ' + str(info['id']) + ' se cargaron ' + str(info['tickets']) + ' alertas'

	return {
		"fulfillmentText": fulfillmentText,
		"source": "webhookdata" 
		}

def sendFilesToLZ(ficheros):

	contador = getContador() + ficheros

	resultado = firebase.put('/demo/ficheros', 'contador', contador)

	return str(contador)


if __name__ == "__main__":
	app.run(debug=True)



