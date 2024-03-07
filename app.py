import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import unidecode

# Función para normalizar texto
def normalize_text(text):
    # Eliminar tildes y convertir a minúsculas
    return unidecode.unidecode(text).lower()

# Cargar los datos
file_path = r'C:\Users\Juan Cruz\Desktop\Cuentas12.csv'
df = pd.read_csv(file_path)

# Convertir la columna 'Nombre de la cuenta' a minúsculas
df['Nombre de la cuenta'] = df['Nombre de la cuenta'].apply(normalize_text)

# Cargar el modelo, el vectorizador y el codificador de etiquetas
with open('modelo.pkl', 'rb') as f:
    clf = pickle.load(f)

with open('vectorizador.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('codificador_etiquetas.pkl', 'rb') as f:
    le = pickle.load(f)

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas en tu aplicación Flask

@app.route('/predict', methods=['POST'])
def predict():
    nombre_cuenta = request.json['nombre_cuenta']
    cuenta_normalizada = normalize_text(nombre_cuenta)
    cuenta_vectorizada = vectorizer.transform([cuenta_normalizada])
    predicted_class = clf.predict(cuenta_vectorizada)
    classification = le.inverse_transform(predicted_class)[0]
    naturaleza = df[df['Nombre de la cuenta'] == cuenta_normalizada]['Naturaleza ampliada'].values[0]
    libros_contables = df[df['Nombre de la cuenta'] == cuenta_normalizada]['Libros contables relevantes'].values[0]
    return jsonify({
        'classification': classification,
        'naturaleza': naturaleza,
        'libros_contables': libros_contables
    })

@app.route('/', methods=['GET'])
def index():
    account = request.args.get('account')
    if account:
        cuenta_normalizada = normalize_text(account)
        cuenta_vectorizada = vectorizer.transform([cuenta_normalizada])
        predicted_class = clf.predict(cuenta_vectorizada)
        classification = le.inverse_transform(predicted_class)[0]
        naturaleza = df[df['Nombre de la cuenta'] == cuenta_normalizada]['Naturaleza ampliada'].values[0]
        libros_contables = df[df['Nombre de la cuenta'] == cuenta_normalizada]['Libros contables relevantes'].values[0]
        return jsonify({
            'classification': classification,
            'naturaleza': naturaleza,
            'libros_contables': libros_contables
        })
    else:
        return 'Por favor, proporcione un parámetro "account" en la solicitud GET.', 400

if __name__ == '__main__':
    app.run(debug=True)
