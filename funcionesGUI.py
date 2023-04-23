import os
from pathlib import *
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox as MessageBox
from analizador import *

rutaArchivo = None
rutaGuardado = None

def temasAyuda():
    os.startfile("Documentos\Temas.pdf")

def visualizarManualTecnico():
    os.startfile("Documentos\Manua_tecnico.pdf")

def visualizarManualUsuario():
    os.startfile("Documentos\Manual_de_Usuario.pdf")


def analizador(cajaTexto):
    contenido = cajaTexto.get('1.0', tk.END)


def abrir_Archivo(cajaTexto):

    # Variable global para uso en otras funciones
    global rutaArchivo

    rutaArchivo = filedialog.askopenfilename(
        # Archivos compatibles
        filetypes={
            ("Archivos de texto", "*.txt"),
            ("Todos los archivos", "*.*")
        }
    )

    if rutaArchivo:
        try:
            # Lectura del archivo y escritura en la caja de texto
            with open(rutaArchivo, 'r') as lineas:
                content = lineas.read()

                #cajaTexto.delete('1.0', tk.END)
                cajaTexto.insert(tk.END, content + "\n")
        except:
            # Mensaje de error en caso que el archivo no se pueda leer
            MessageBox.showerror("Error", "Asegurese de abrir un archivo de tipo texto")

    else:
        MessageBox.showwarning("Alerta", "No se a seleccionado ningun archivo.")



# Limpiar la caja de texto
def limpiar(cajaTexto):
    
    # Confirmacion en caso que se desee limpiar
    confirmacion = MessageBox.askyesno("Confirmar", "¿Desea Limpiar la Caja de Texto?")

    if confirmacion:
        cajaTexto.delete('1.0', tk.END)
        MessageBox.showinfo("Mensaje", "Limpieza realizada con Exito!")



# Guardar el texto en la ruta especificada anteriormente
def guardar(cajaTexto):

    # Verifica que exista una ruta para guardar el archivo
    if rutaArchivo == None:
        MessageBox.showerror("Error", "No se ha encontrado una ruta para guardar el archivo!")

    # En caso que se haya elegido una nueva ruta para guardar el archivo apartir de ahora guardara en esa ruta
    elif rutaGuardado != None:

        with open(rutaGuardado, 'w') as lineas:
            contenido = cajaTexto.get("1.0", tk.END)
            lineas.write(contenido)
            MessageBox.showinfo("Mensaje", "Se guardo correctamente los datos en la ruta: " + str(rutaGuardado))

    else:
        # Abre el archivo y escribe todos los datos existentes en la caja de texto, en caso de que sea la ruta del archivo cargado
        with open(rutaArchivo, 'w') as lineas:
            contenido = cajaTexto.get("1.0", tk.END)
            lineas.write(contenido)
            MessageBox.showinfo("Mensaje", "Se guardo correctamente los datos en la ruta: " + str(rutaArchivo))



# Funcion para elegir el nombre y la ruta para guardar el archivo
def guardarComo(cajaTexto):

    global rutaGuardado

    rutaGuardado = filedialog.asksaveasfilename(
         filetypes={
            ("Todos los archivos", "*.*")
        }
    )

    if rutaGuardado:

        with open(rutaGuardado, 'w') as lineas:
            contenido = cajaTexto.get("1.0", tk.END)
            lineas.write(contenido)
            MessageBox.showinfo("Mensaje", "Se guardo correctamente los datos en la ruta: " + str(rutaGuardado))

    else:
        MessageBox.showwarning("Alerta", "No se completo el guardado")

    
