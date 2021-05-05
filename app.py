from flask import Flask
from firebase import firebase
import json
import random
import datetime


firebase = firebase.FirebaseApplication('https://aws-demo-5c44a-default-rtdb.firebaseio.com/', None)

files = ["onus check", "a2a deposit", "limits"]

app = Flask(__name__)

id = 0

@app.route("/")
def home():
	print("Se ha conectado una persona")
	return 'Welcome to the piece of shit server'

	
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
	print('fine so far')
	if query_result.get('action') == 'carga_de_alertas':
		insertData()
		fulfillmentText = 'He cargado el fichero con id '
	return {
		"fulfillmentText": fulfillmentText,
		"source": "webhookdata" 
		}


if __name__ == "__main__":
	app.run(debug=True)




