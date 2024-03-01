from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas en tu aplicación Flask

# Cargar el modelo, el vectorizador y el codificador de etiquetas
with open('modelo.pkl', 'rb') as f:
    clf = pickle.load(f)

with open('vectorizador.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('codificador_etiquetas.pkl', 'rb') as f:
    le = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    nombre_cuenta = request.json['nombre_cuenta']
    cuenta_vectorizada = vectorizer.transform([nombre_cuenta])
    predicted_class = clf.predict(cuenta_vectorizada)
    return le.inverse_transform(predicted_class)[0]

@app.route('/', methods=['GET'])
def index():
    account = request.args.get('account')
    if account:
        cuenta_vectorizada = vectorizer.transform([account])
        predicted_class = clf.predict(cuenta_vectorizada)
        classification = le.inverse_transform(predicted_class)[0]
        return jsonify({'classification': classification})
    else:
        return 'Por favor, proporcione un parámetro "account" en la solicitud GET.', 400

if __name__ == '__main__':
    app.run(debug=True)
