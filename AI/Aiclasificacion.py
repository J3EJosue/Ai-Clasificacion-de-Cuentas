import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Verificar si los archivos del modelo, el vectorizador y el codificador de etiquetas existen
if os.path.exists('modelo.pkl') and os.path.exists('vectorizador.pkl') and os.path.exists('codificador_etiquetas.pkl'):
    # Cargar el modelo, el vectorizador y el codificador de etiquetas
    with open('modelo.pkl', 'rb') as f:
        clf = pickle.load(f)

    with open('vectorizador.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    with open('codificador_etiquetas.pkl', 'rb') as f:
        le = pickle.load(f)
else:
    # Cargar los datos
    df = pd.read_csv('C:\\Users\\Juan Cruz\\Desktop\\Cuentas.csv.txt')

    # Crear el transformador TF-IDF
    vectorizer = TfidfVectorizer()

    # Ajustar el transformador a los datos y transformarlos
    X = vectorizer.fit_transform(df['Nombre de la cuenta'])

    # Codificar las etiquetas
    le = LabelEncoder()
    y = le.fit_transform(df['Categoría'])

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear un modelo de clasificación
    clf = LogisticRegression()

    # Entrenar el modelo
    clf.fit(X_train, y_train)

    # Guardar el modelo, el vectorizador y el codificador de etiquetas
    with open('modelo.pkl', 'wb') as f:
        pickle.dump(clf, f)

    with open('vectorizador.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)

    with open('codificador_etiquetas.pkl', 'wb') as f:
        pickle.dump(le, f)