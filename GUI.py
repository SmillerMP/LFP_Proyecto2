
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from funcionesGUI import *


# Funciones
def editorTexto():
    abrir_Archivo(caja_editor)

def limpiarTexto():
    limpiar(caja_editor)

def guardarTexto():
    guardar(caja_editor)

def guardarComoTexto():
    guardarComo(caja_editor)

def botonAnalizar():
    if analizador(caja_editor) != False:
        
        ventana_comandos = tk.Toplevel(ventana_principal)
        ventana_comandos.geometry("528x456+588+236")
        ventana_comandos.minsize(120, 1)
        ventana_comandos.maxsize(3290, 1061)
        ventana_comandos.resizable(1,  1)
        ventana_comandos.title("Comandos")
        ventana_comandos.configure(background="#FFB84C")
        ventana_comandos.resizable(width=False, height=False)


        Label1_1 = tk.Label(ventana_comandos)
        Label1_1.place(relx=0.0, rely=0.0, height=32, width=536)
        Label1_1.configure(activebackground="#f9f9f9")
        Label1_1.configure(background="#F5EAEA")
        Label1_1.configure(compound='left')
        Label1_1.configure(disabledforeground="#a3a3a3")
        Label1_1.configure(font="-family {Arial} -size 13 -weight bold -slant italic")
        Label1_1.configure(foreground="#000000")
        Label1_1.configure(highlightbackground="#d9d9d9")
        Label1_1.configure(highlightcolor="black")
        Label1_1.configure(text='''Comandos MongoDB''')

        caja_comandos = tk.Text(ventana_comandos)
        caja_comandos.place(relx=0.02, rely=0.1, height=400, relwidth=0.93)
        caja_comandos.configure(font="-family {Calibri} -size 11")

        scrollbarEditor = tk.Scrollbar(ventana_comandos, command=caja_comandos.yview)
        scrollbarEditor.place(x=500, y=46, height=400)
        # configura el widget Text para que use el scrollbar vertical
        caja_comandos.config(yscrollcommand=scrollbarEditor.set)
        printerCaja(caja_comandos)

def actualizar_label():
    linea, columna = caja_editor.index(tk.INSERT).split('.')
    texto = f"Línea: {linea} | Columna: {columna}"
    posicion.config(text=texto)
    caja_editor.after(100, actualizar_label)

ventana_principal = tk.Tk()
ventana_principal.geometry("942x552+401+217")
ventana_principal.minsize(120, 1)
ventana_principal.maxsize(3290, 1061)
ventana_principal.resizable(1,  1)
ventana_principal.title("Ventana Principal")
ventana_principal.configure(background="#FFB84C")
ventana_principal.configure(highlightbackground="#d9d9d9")
ventana_principal.configure(highlightcolor="black")



Label1 = tk.Label()
Label1.place(relx=0.0, rely=0.0, height=42, width=949)
Label1.configure(activebackground="#f9f9f9")
Label1.configure(background="#F5EAEA")
Label1.configure(compound='left')
Label1.configure(disabledforeground="#a3a3a3")
Label1.configure(font="-family {Arial} -size 14 -weight bold -slant italic")
Label1.configure(foreground="#000000")
Label1.configure(highlightbackground="#d9d9d9")
Label1.configure(highlightcolor="black")
Label1.configure(text='''Proyecto 2 Lenguajes Formales''')

posicion = tk.Label(ventana_principal, text="Línea: 1 | Columna: 0")
posicion.place(relx=0.38, rely=0.92)

caja_editor = tk.Text()
caja_editor.place(relx=0.032, rely=0.127, height=438, relwidth=0.471)
caja_editor.configure(font="-family {Calibri} -size 11")
caja_editor.bind("<Key>", lambda event: caja_editor.after(100, actualizar_label))
caja_editor.bind("<Button-1>", lambda event: caja_editor.after(100, actualizar_label))
actualizar_label()

scrollbarEditor = tk.Scrollbar(ventana_principal, command=caja_editor.yview)
scrollbarEditor.place(x=474, y=69, height=439)
# configura el widget Text para que use el scrollbar vertical
caja_editor.config(yscrollcommand=scrollbarEditor.set)



boton_abrir = tk.Button()
boton_abrir.place(relx=0.8, rely=0.13, height=34, width=137)
boton_abrir.configure(activebackground="beige")
boton_abrir.configure(activeforeground="black")
boton_abrir.configure(background="#A459D1")
boton_abrir.configure(compound='left')
boton_abrir.configure(disabledforeground="#a3a3a3")
boton_abrir.configure(font="-family {Arial} -size 11 -weight bold")
boton_abrir.configure(foreground="#000000")
boton_abrir.configure(highlightbackground="#d9d9d9")
boton_abrir.configure(highlightcolor="black")
boton_abrir.configure(pady="0")
boton_abrir.configure(text='''Abrir''')
boton_abrir.configure(command=editorTexto)


boton_guardar = tk.Button()
boton_guardar.place(relx=0.8, rely=0.243, height=34, width=137)
boton_guardar.configure(activebackground="beige")
boton_guardar.configure(activeforeground="black")
boton_guardar.configure(background="#A459D1")
boton_guardar.configure(compound='left')
boton_guardar.configure(disabledforeground="#a3a3a3")
boton_guardar.configure(font="-family {Arial} -size 11 -weight bold")
boton_guardar.configure(foreground="#000000")
boton_guardar.configure(highlightbackground="#d9d9d9")
boton_guardar.configure(highlightcolor="black")
boton_guardar.configure(pady="0")
boton_guardar.configure(text='''Guardar''')
boton_guardar.configure(command=guardarTexto)

boton_guardarComo = tk.Button()
boton_guardarComo.place(relx=0.8, rely=0.353, height=34, width=137)
boton_guardarComo.configure(activebackground="beige")
boton_guardarComo.configure(activeforeground="black")
boton_guardarComo.configure(background="#A459D1")
boton_guardarComo.configure(compound='left')
boton_guardarComo.configure(disabledforeground="#a3a3a3")
boton_guardarComo.configure(font="-family {Arial} -size 11 -weight bold")
boton_guardarComo.configure(foreground="#000000")
boton_guardarComo.configure(highlightbackground="#d9d9d9")
boton_guardarComo.configure(highlightcolor="black")
boton_guardarComo.configure(pady="0")
boton_guardarComo.configure(text='''Guardar Como''')
boton_guardarComo.configure(command=guardarComoTexto)

boton_limpiar = tk.Button()
boton_limpiar.place(relx=0.696, rely=0.466, height=34
        , width=137)
boton_limpiar.configure(activebackground="beige")
boton_limpiar.configure(activeforeground="black")
boton_limpiar.configure(background="#F5EAEA")
boton_limpiar.configure(compound='left')
boton_limpiar.configure(disabledforeground="#a3a3a3")
boton_limpiar.configure(font="-family {Arial} -size 11 -weight bold")
boton_limpiar.configure(foreground="#000000")
boton_limpiar.configure(highlightbackground="#d9d9d9")
boton_limpiar.configure(highlightcolor="black")
boton_limpiar.configure(pady="0")
boton_limpiar.configure(text='''Limpiar''')
boton_limpiar.configure(command=limpiarTexto)


boton_salir = tk.Button()
boton_salir.place(relx=0.824, rely=0.911, height=34
        , width=137)
boton_salir.configure(activebackground="beige")
boton_salir.configure(activeforeground="black")
boton_salir.configure(background="#F5EAEA")
boton_salir.configure(compound='left')
boton_salir.configure(disabledforeground="#a3a3a3")
boton_salir.configure(font="-family {Arial} -size 11 -weight bold")
boton_salir.configure(foreground="#000000")
boton_salir.configure(highlightbackground="#d9d9d9")
boton_salir.configure(highlightcolor="black")
boton_salir.configure(pady="0")
boton_salir.configure(text='''Salir''')
boton_salir.configure(command=ventana_principal.destroy)


boton_analisis = tk.Button()
boton_analisis.place(relx=0.594, rely=0.13, height=34, width=137)
boton_analisis.configure(activebackground="beige")
boton_analisis.configure(activeforeground="black")
boton_analisis.configure(background="#F16767")
boton_analisis.configure(compound='left')
boton_analisis.configure(disabledforeground="#a3a3a3")
boton_analisis.configure(font="-family {Arial} -size 11 -weight bold")
boton_analisis.configure(foreground="#000000")
boton_analisis.configure(highlightbackground="#d9d9d9")
boton_analisis.configure(highlightcolor="black")
boton_analisis.configure(pady="0")
boton_analisis.configure(text='''Análisis''')
boton_analisis.configure(command=botonAnalizar)


boton_tokens = tk.Button()
boton_tokens.place(relx=0.594, rely=0.243, height=34, width=137)
boton_tokens.configure(activebackground="beige")
boton_tokens.configure(activeforeground="black")
boton_tokens.configure(background="#F16767")
boton_tokens.configure(compound='left')
boton_tokens.configure(disabledforeground="#a3a3a3")
boton_tokens.configure(font="-family {Arial} -size 11 -weight bold")
boton_tokens.configure(foreground="#000000")
boton_tokens.configure(highlightbackground="#d9d9d9")
boton_tokens.configure(highlightcolor="black")
boton_tokens.configure(pady="0")
boton_tokens.configure(text='''Menú Tokens''')
boton_tokens.configure(command=tokens)

boton_errores = tk.Button()
boton_errores.place(relx=0.594, rely=0.353, height=34, width=137)
boton_errores.configure(activebackground="beige")
boton_errores.configure(activeforeground="black")
boton_errores.configure(background="#F16767")
boton_errores.configure(compound='left')
boton_errores.configure(disabledforeground="#a3a3a3")
boton_errores.configure(font="-family {Arial} -size 11 -weight bold")
boton_errores.configure(foreground="#000000")
boton_errores.configure(highlightbackground="#d9d9d9")
boton_errores.configure(highlightcolor="black")
boton_errores.configure(pady="0")
boton_errores.configure(text='''Área de errores''')
boton_errores.configure(command=errores)


# boton_simbolos = tk.Button()
# boton_simbolos.place(relx=0.594, rely=0.466, height=34, width=137)
# boton_simbolos.configure(activebackground="beige")
# boton_simbolos.configure(activeforeground="black")
# boton_simbolos.configure(background="#F16767")
# boton_simbolos.configure(compound='left')
# boton_simbolos.configure(disabledforeground="#a3a3a3")
# boton_simbolos.configure(font="-family {Arial} -size 11 -weight bold")
# boton_simbolos.configure(foreground="#000000")
# boton_simbolos.configure(highlightbackground="#d9d9d9")
# boton_simbolos.configure(highlightcolor="black")
# boton_simbolos.configure(pady="0")
# boton_simbolos.configure(text='''Menu Símbolos''')


ventana_principal.resizable(width=False, height=False)
ventana_principal.mainloop()

