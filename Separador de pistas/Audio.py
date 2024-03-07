import os
import subprocess
import tkinter as tk
from tkinter import filedialog

def process_file(filepath, output_folder):
    # Llama al script de separación de Demucs desde la línea de comandos
    # Modifica --two-stems para separar solo las pistas que no son batería ni piano
    # Usa la ruta completa al ejecutable de Demucs
    demucs_path = "C:/Users/Juan Cruz/AppData/Roaming/Python/Python312/Scripts/demucs"
    command = f"{demucs_path} --two-stems=other -o {output_folder} {filepath}"
    subprocess.run(command, shell=True)
    print(f"Separación completada. Los archivos separados se han guardado en '{output_folder}'.")

def choose_file():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter

    # Abre el diálogo para seleccionar el archivo de audio
    filepath = filedialog.askopenfilename(title="Selecciona un archivo de audio", filetypes=(("Archivos de audio", "*.mp3 *.wav"), ("Todos los archivos", "*.*")))

    # Abre el diálogo para seleccionar la carpeta de destino
    output_folder = filedialog.askdirectory(title="Selecciona la carpeta de destino")

    if filepath and output_folder:
        process_file(filepath, output_folder)

if __name__ == "__main__":
    choose_file()
