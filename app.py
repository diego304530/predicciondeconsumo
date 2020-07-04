from flask import Flask, render_template, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import pandas
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle
import pandas as pd
from sklearn.metrics import classification_report

app = Flask(__name__)

app.secret_key="C89QRZbCtjG3o3thfyPY7135dV20WnnL"

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/_inicio/')
def _inicio():
	return render_template('inicio.js')

@app.route('/_datos/')
def _datos():
	return render_template('datos.html')

@app.route('/_recoleccion/')
def _recoleccion():
	return render_template('datos.js')

@app.route('/_encontrar/')
def _encontrar(iden):

	db = pymysql.connect("localhost", "root", "", "proyectotg")
	cursor = db.cursor()
	sql="SELECT * FROM datos WHERE identificacion = %s"
	cursor.execute(sql, (iden))
	result = cursor.fetchall();
	db.close();
	return result

@app.route('/_predict/')
def _predict(cigarrillo, invitacion, famili, edad, rupturas):

	url = "https://raw.githubusercontent.com/diego304530/dataset-drogas/master/encuestaBinaria.csv"
	names = ['Cigarrillo','Invitacion_drogas','Familiares_consumidores','Edad','Rupturas_amorosas']
	dataframe = pd.read_csv(url)
	array = dataframe.values
	X = dataframe[names]
	Y = array[:,13]
	test_size = 0.9
	seed = 7
	validation_size = 0.70
	X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X,Y, test_size = validation_size )
	# Fit the model on training set
	model = LogisticRegression()
	model.fit(X, Y)
	result = model.score(X_test, Y_test)
	

	DatosConsola = pd.DataFrame({'Cigarrillo': [cigarrillo],'Invitacion_drogas': [invitacion],'Familiares_consumidores': [famili], 'Edad': [edad],'Rupturas_amorosas': [rupturas]})
	respuesta= [int(model.predict(DatosConsola)), round(result*100)]
	return respuesta

@app.route('/_agregar/', methods=['POST'])
def _agregar():
	identificacion=request.form['identificacion']
	casosde= _encontrar(identificacion);
	if len(casosde) != 0 :
		return "False"
		
	else:
		cigarrillo= request.form['fumar']
		invitacion= request.form['psicoactivos']
		famili= request.form['familiares']
		edad= request.form['edad']
		rupturas=request.form['rupturas']
		
		nombre= request.form['nombre']
		apellido=request.form['apellido']
		colegio=request.form['colegio']
		caso = _predict(cigarrillo, invitacion, famili, edad, rupturas)
		db = pymysql.connect("localhost", "root", "", "proyectotg")
		cursor = db.cursor()
		sql="INSERT INTO datos VALUES(%s,%s,%s,%s,%s,%s,%s)"
		cursor.execute(sql, (identificacion, nombre, apellido, edad, colegio, caso[0], int(caso[1])))
		db.commit();
		db.close();
		return "True"
	
	
	
@app.route('/_tomardatos/', methods=['POST'])
def _tomardatos():

	db = pymysql.connect("localhost", "root", "", "proyectotg")
	cursor = db.cursor()
	sql="SELECT * FROM datos WHERE colegio = %s"
	cursor.execute(sql,(session['colegio']))
	result = cursor.fetchall();
	db.close();
	return jsonify(result)

@app.route('/_iniciarsesion/', methods=['POST'])
def _iniciarsesion():

	db = pymysql.connect("localhost", "root", "", "proyectotg")
	cursor = db.cursor()
	usuario= request.form['usuario']
	contraseña= request.form['contrasenia']
	sql="SELECT * FROM usuarios WHERE usuario= %s"
	cursor.execute(sql, (usuario))	
	result = cursor.fetchall();
	db.close();
	if len(result) == 0:
		return "False"
	else:
		resp = check_password_hash(result[0][4], contraseña)
		if resp:

			session['usuario']= result[0][3]
			session['colegio']= result[0][5]

			return "True"
		else:
			return "False"


@app.route('/_verificar/', methods=['POST'])
def _verificar():
	if 'usuario' in session:
		return jsonify(session['usuario'])
	else:
		return jsonify("False")

@app.route('/_cerrarsesion/', methods=['POST'])
def _cerrarsesion():
	session.clear()
	return "True"

	
		



	
	

	

if __name__ == "__main__":
    app.run(debug=True)
