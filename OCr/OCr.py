import pytesseract
from pdf2image import convert_from_path
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pandas as pd
import io

# Establecer la ruta al ejecutable de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Juan Cruz\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Crear una ventana de Tkinter
Tk().withdraw()

# Mostrar un cuadro de diálogo para seleccionar un archivo
file_path = askopenfilename()

# Convertir el PDF en imágenes
images = convert_from_path(file_path)

all_text = ""

# Aplicar OCR a cada imagen
for i in range(len(images)):
    text = pytesseract.image_to_string(images[i], lang='spa')
    # Reemplazar las comillas dobles por comillas simples
    text = text.replace('"', "'")
    all_text += text

# Intentar detectar y extraer tablas del texto
data = io.StringIO(all_text)
df = pd.read_csv(data, sep="\t")

# Mostrar un cuadro de diálogo para seleccionar dónde guardar el archivo
output_file_path = asksaveasfilename(defaultextension=".csv")

# Guardar la tabla en un archivo CSV
df.to_csv(output_file_path, index=False)