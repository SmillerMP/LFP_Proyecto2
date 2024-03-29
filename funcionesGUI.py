import os
from pathlib import *
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox as MessageBox
from analizador import *
from creacionTablas import *

comandos = None
rutaArchivo = None

def temasAyuda():
    os.startfile("Documentos\Temas.pdf")

def visualizarManualTecnico():
    os.startfile("Documentos\Manua_tecnico.pdf")

def visualizarManualUsuario():
    os.startfile("Documentos\Manual_de_Usuario.pdf")


def analizador(cajaTexto):
    contenido = cajaTexto.get('1.0', tk.END)

    if not contenido.strip():
        MessageBox.showerror("Error", "No hay texto por analizar")
        return False
    else:
        global comandos
        comandos = Analizador(contenido)
        comandos._compile()
    

def printerCaja(cajaTexto):
    try:
        cajaTexto.insert(tk.END, f"Se han encotrado {len(comandos.listaComandos)} comandos" + "\n\n\n")
        for x in comandos.listaComandos:
            cajaTexto.insert(tk.END, x + "\n\n")
    except:
        MessageBox.showerror("ERROR", "Asegurese de ingresar datos al editor de texto")
    


def errores():
    try:
        generacionErrores(comandos.ListaErrores)

    except:
        MessageBox.showinfo("Advertencia", "No se ha compilado ningun archivo")


def tokens():
    try:
        generacionTokens(comandos.listaTokens)
    except:
        MessageBox.showinfo("Advertencia", "No se ha compilado ningun archivo")
    

def abrir_Archivo(cajaTexto):

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
            with open(rutaArchivo, 'r', encoding="utf-8") as lineas:
                content = lineas.read()

                #cajaTexto.delete('1.0', tk.END)
                cajaTexto.insert(tk.END, content + "\n")
        except:
            # Mensaje de error en caso que el archivo no se pueda leer
            MessageBox.showerror("Error", "Asegurese de abrir un archivo de tipo texto")

    else:
        MessageBox.showwarning("Alerta", "No se a seleccionado ningun archivo.")
        rutaArchivo = None



# Limpiar la caja de texto
def limpiar(cajaTexto):
    
    # Confirmacion en caso que se desee limpiar
    confirmacion = MessageBox.askyesno("Confirmar", "¿Desea Limpiar la Caja de Texto?")

    if confirmacion:
        cajaTexto.delete('1.0', tk.END)
        try:
            comandos.listaTokens = []
            comandos.ListaErrores = []
            comandos.json = ''
            comandos.tokenAutilizar = ''
            comandos.contadorToken = 0
            MessageBox.showinfo("Mensaje", "Limpieza realizada con Exito!")
        except:
            MessageBox.showinfo("Advertencia", "No se ha compilado ningun archivo. Limpieza realizada con Exito!")
    

# Guardar el texto en la ruta especificada anteriormente
def guardar(cajaTexto):

    global rutaArchivo

    # Verifica que exista una ruta para guardar el archivo
    if rutaArchivo == None:
        MessageBox.showwarning("Sin Ruta", "No hay una ruta especificada para guardar el archivo, Ingrese una nueva ruta")
        
        rutaArchivo = filedialog.asksaveasfilename(
         filetypes={
            ("Todos los archivos", "*.*")
            }
        )

        if rutaArchivo:
            with open(rutaArchivo, 'w', encoding="utf-8") as lineas:
                contenido = cajaTexto.get("1.0", tk.END)
                lineas.write(contenido)
                MessageBox.showinfo("Mensaje", "Se guardo correctamente los datos en la ruta: " + str(rutaArchivo))

        else:
            MessageBox.showwarning("Alerta", "No se completo el guardado")
            rutaArchivo = None

        
        

    # En caso que se haya elegido una nueva ruta para guardar el archivo apartir de ahora guardara en esa ruta
    elif rutaArchivo != None:

        with open(rutaArchivo, 'w', encoding="utf-8") as lineas:
            contenido = cajaTexto.get("1.0", tk.END)
            lineas.write(contenido)
            MessageBox.showinfo("Mensaje", "Se guardo correctamente los datos en la ruta: " + str(rutaArchivo))




# Funcion para elegir el nombre y la ruta para guardar el archivo
def guardarComo(cajaTexto):
    global rutaArchivo

    rutaArchivo = filedialog.asksaveasfilename(
         filetypes={
            ("Todos los archivos", "*.*")
        }
    )

    if rutaArchivo:
        with open(rutaArchivo, 'w', encoding="utf-8") as lineas:
            contenido = cajaTexto.get("1.0", tk.END)
            lineas.write(contenido)
            MessageBox.showinfo("Mensaje", "Se guardo correctamente los datos en la ruta: " + str(rutaArchivo))

    else:
        MessageBox.showwarning("Alerta", "No se completo el guardado")
        rutaArchivo = None

    
