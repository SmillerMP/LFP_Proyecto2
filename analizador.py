texto = ''
with open('little.txt', 'r', encoding='utf-8') as archivo:
    # for lineas in archivo.readlines():
    #     texto += lineas
    texto = archivo.read()
        
# for x in texto:
#     print(x)


class Analizador:
    def __init__(self, entrada:str):
        self.lineas = entrada #ENTRADA
        self.index = 0 #POSICION DE CARACTERES EN LA ENTRADA
        self.fila = 1 #FILA ACTUAL
        self.columna = 1 #COLUMNA ACTUAL
        self.ListaErrores = [] # LISTA PARA GUARDAR ERRORES

    def _token(self, token:str, estado_actual:str, estado_sig:str):
        if self.lineas[self.index] != " ":
            text = self._juntar(self.index, len(token))
            if self._analizar(token, text):
                self.index += len(token) - 1
                self.columna += len(token) - 1
                return estado_sig
            else:
                return 'ERROR'
        else:
            return estado_actual

    def _salto_linea(self):   
        
        while self.lineas[self.index] != "":
            if self.index+1 < len(self.lineas):
                if self.lineas[self.index] != "\n":
                    self.index += 1
                else:
                    self.fila += 1
                    break
            else:
                break


    def _juntar_comillas(self):
        try:
            tmp = ''
            while self.lineas[self.index] != '"':
                if self.lineas[self.index] != '\n':
                    tmp += self.lineas[self.index]
                    self.index += 1
                
                else:
                    tmp = ''
                    return 'ERROR'
        
            print(f'********** ENCONTRE - {tmp} ***************')
            self.index -= 1
            return tmp
        except:
            return None

        
    def juntar_texto(self):
        try:
            tmp = ''
            self.index += 1
            while self.lineas[self.index] != ' ':
                if self.lineas[self.index] != '"':
                    if self.lineas[self.index] != '\n':
                        tmp += self.lineas[self.index]
                        self.index += 1
                    
                    else:
                        tmp = ''
                        return 'ERROR'
                else:
                    break
            print(f'********** ENCONTRE - {tmp} ***************')
            return tmp
        except:
            return None

        
    def _juntar(self,_index:int, _count:int):
        try:
            tmp = ''
            for i in range(_index, _index + _count):
                tmp += self.lineas[i]
            return tmp
        except:
            return None
        
    def _analizar(self, token, texto):
        try:
            count = 0
            tokem_tmp = ""
            for i in texto:
                #CUANDO LA LETRA HAGA MATCH CON EL TOKEN ENTRA
                #print('COMBINACION -> ',i , '==', token[count])
                if str(i) == str(token[count]):
                    tokem_tmp += i  
                    count += 1 
                else:
                    #print('ERROR1')
                    return False
                
            print(f'********** ENCONTRE - {tokem_tmp} ***************')
            return True
        except:
            #print('ERROR2')
            return False
    

    def _operaciones(self, estado_sig):
        estado_actual = 'S1'
        hijo_derecho = ""
        hijo_izquierdo = ""
        operador = ""
        funcionUsar = ''
        while self.lineas[self.index] != "":
            #print(f'CARACTER OP - {self.lineas[self.index] } | ESTADO - {estado_actual} | FILA - {self.fila}  | COLUMNA - {self.columna}')
            print(self.lineas[self.index])
            # IDENTIFICAR SALTO DE LINEA
            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna =0

            # ************************
            #         ESTADOS
            # ************************

            
            # S1 -> "Funcion" S2
            elif estado_actual == 'S1':
                funciones = ['"CrearBD"','"EliminarBD"','"CrearColeccion"', '"EliminarColeccion"', '"InsertarUnico"', 
                             '"ActualizarUnico"', '"EliminarUnico"', '"BuscarTodo"', '"BuscarUnico"']
                for x in funciones:
                    estado_actual = self._token(x, 'S1', 'S2')
                    if estado_actual != 'ERROR':
                        
                        #Funcion encontrada satisfactoriamente
                        funcionUsar = x
                    
                        
            
            # S2 -> : S3
            elif estado_actual == 'S2':
                estado_actual = self._token(':', 'S2', 'S3')

            # S3 -> OPERADOR S4
            elif estado_actual == 'S3':
                operadores = ['"Suma"','"Resta"','"Multiplicacion"', '"Inverso"', '"Seno"']
                for i in operadores:
                    estado_actual = self._token(i, 'S3', 'S4')
                    if estado_actual != 'ERROR':
                        operador = i
                        break

            # S4 -> "Valor1" S5
            elif estado_actual == 'S4':
                estado_actual = self._token('"Valor1"', 'S4', 'S5')

            # S5 -> : S6
            elif estado_actual == 'S5':
                estado_actual = self._token(':', 'S5', 'S6')

            # S6 -> DIGITO S9 
            #    | [ S7
            elif estado_actual == 'S6':
                estado_actual = self._token('[','S6','S7')
                if estado_actual == 'ERROR':
                    estado_actual = 'S9'
                    a = self._digito('S9')
                    if "ERROR" == a[0]:
                        estado_actual = 'ERROR'
                    elif a[0] == 'S9':
                        hijo_izquierdo = a[1]

            # S7 -> S1 S8
            elif estado_actual == 'S7':
                a = self._operaciones('S8')
                estado_actual = a[0]
                hijo_izquierdo = a[1]

            # S8 -> ] S9
            elif estado_actual == 'S8':
                estado_actual = self._token(']','S8','S9')
                

            # S9 -> "Valor2" S10
            elif estado_actual == 'S9':
                if operador == '"Inverso"' or operador == '"Seno"':
                    self.index -= 1
                    # REALIZAR LA OPERACION ARITMETICA Y DEVOLVER UN SOLO VALOR
                    print("\t*****OPERACION ARITMETICA*****")
                    print('\t',operador ,'(',hijo_izquierdo ,')' )
                    print('\t*******************************\n')
                    op = operador +'('+hijo_izquierdo +')'
                    return ['S14', op]  
                else:
                    estado_actual = self._token('"Valor2"', 'S9', 'S10')

            # S10 -> : S11
            elif estado_actual == 'S10':
                estado_actual = self._token(':', 'S10', 'S11')

            # S11 -> DIGITO S14 
            #    | [ S12
            elif estado_actual == 'S11':
                estado_actual = self._token('[','S11','S12')
                if estado_actual == 'ERROR':
                    estado_actual = 'S14'
                    a = self._digito('S14')
                    if "ERROR" == a[0]:
                        estado_actual = 'ERROR'
                    elif 'S14' == a[0]:
                        hijo_derecho = a[1]
                        # REALIZAR LA OPERACION ARITMETICA Y DEVOLVER UN SOLO VALOR
                        print("\t*****OPERACION ARITMETICA*****")
                        print('\t',hijo_izquierdo , operador, hijo_derecho)
                        print('\t*******************************\n')
                        op = hijo_izquierdo + operador + hijo_derecho
                        return [estado_sig, op]  

            # S12 -> S1 S13
            elif estado_actual == 'S12':
                estado_actual = 'S13'
                a = self._operaciones('S13')
                hijo_derecho = a[1]
                if "ERROR" == a[0]:
                    estado_actual = 'ERROR'

            # S13 -> ] S14
            elif estado_actual == 'S13':
                estado_actual = self._token(']','S13','S14')

                # REALIZAR LA OPERACION ARITMETICA Y DEVOLVER UN SOLO VALOR
                print("\t*****OPERACION ARITMETICA*****")
                print('\t',hijo_izquierdo , operador, hijo_derecho)
                print('\t*******************************\n')
                op = hijo_izquierdo + operador + hijo_derecho
                return [estado_sig, op]  



            
            # ERRORES 
            if estado_actual == 'ERROR':
                print("********************************")
                print("\tERROR")
                print("********************************")
                # ERROR
                self.guardarErrores(self.lineas[self.index], self.fila, self.columna)
                return ['ERROR', -1]
            
            #INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index +=1
            else:
                break

    def _atributo(self, funcion):
        estado_actual = 'A0'
        identificador = ''

        while self.lineas[self.index] != "":
            #print(f'CARACTER11 - {self.lineas[self.index] } | ESTADO - {estado_actual} | FILA - {self.fila}  | COLUMNA - {self.columna}')
            
            # IDENTIFICAR SALTO DE LINEA
            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna =0

            # A0 -> " A1
            elif estado_actual == 'A0':
                # busqueda de la comilla doble
                estado_actual = self._token('"', 'A0', 'A1')

            elif estado_actual == 'A1':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:

                    # nombre del identificador
                    identificador = estado_actual
                    #self.index -= 1
                    estado_actual = 'A2'  

                else:
                    print("error en la lectura de texto")
                    estado_actual = "ERROR"


            # A2 -> " A3
            elif estado_actual == 'A2':
                # busqueda de la comilla doble
                estado_actual = self._token('"', 'A2', 'A3')

            # A3 -> , A4
            #   | Unicamente Identificador
            elif estado_actual == 'A3':
                # busqueda de la coma
                estado_actual = self._token(',', 'A3', 'A4')
                if estado_actual == 'ERROR':
                    #self.index -= 1
                    return identificador
                      
            # A4 -> " A5
            elif estado_actual == 'A4':
                # busqueda de la comilla doble
                estado_actual = self._token('"', 'A4', 'A5')

            
            elif estado_actual == 'A5':
                
                if funcion == "InsertarUnico":
                    sintaxisJson = self.nombre_autor()

                estado_actual = 'A6'

                
            # A6 -> " A7
            elif estado_actual == 'A6':
                # busqueda de la comilla doble
                estado_actual = self._token('"', 'A6', 'A7')


            elif estado_actual == 'A7':
                self.index -= 1
                return identificador

            if estado_actual == 'ERROR':
                return estado_actual
            

            #INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index +=1
            else:
                break

    
    def nombre_autor(self):
        estado_actual = 'NA0'
        json = ''

        while self.lineas[self.index] != "":
        
            # IDENTIFICAR SALTO DE LINEA
            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna =0

            # ************************
            #         ESTADOS
            # ************************

            # NA0 -> { NA1
            elif estado_actual == 'NA0':
                estado_actual = self._token('{', 'NA0', 'NA1')

            # NA1 -> "nombre" NA2
            elif estado_actual == 'NA1':
                estado_actual = self._token('"nombre"', 'NA1', 'NA2')

            # NA2 -> : NA3
            elif estado_actual == 'NA2':
                estado_actual = self._token(':', 'NA2', 'NA3')

            # NA3 -> " NA4
            elif estado_actual == 'NA3':
                estado_actual = self._token('"', 'NA3', 'NA4')

            # NA4 -> texto NA5
            elif estado_actual == 'NA4':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:

                    self.index -= 1
                    estado_actual = 'NA5'  

                else:
                    print("error en la lectura de texto")
                    estado_actual = "ERROR"

            # NA5 -> " NA6
            elif estado_actual == 'NA5':
                estado_actual = self._token('"', 'NA5', 'NA6')

            # NA6 -> , NA7
            elif estado_actual == 'NA6':
                estado_actual = self._token(',', 'NA6', 'NA7')

            # NA7 -> "autor" NA8
            elif estado_actual == 'NA7':
                estado_actual = self._token('"autor"', 'NA7', 'NA8')

            # NA8 -> : NA9
            elif estado_actual == 'NA8':
                estado_actual = self._token(':', 'NA8', 'NA9')

            #NA9 -> " NA10
            elif estado_actual == 'NA9':
                estado_actual = self._token('"', 'NA9', 'NA10')

            # NA10 -> texto NA11
            elif estado_actual == 'NA10':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:

                    self.index -= 1
                    estado_actual = 'NA11'  

                else:
                    print("error en la lectura de texto")
                    estado_actual = "ERROR"

            # NA11 -> " NA12
            elif estado_actual == 'NA11':
                estado_actual = self._token('"', 'NA11', 'NA12')

            elif estado_actual == 'NA12':
                self.index -= 1
                return json


            #INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index +=1
            else:
                break

    def _compile(self):
        estado_actual = 'S0'
        funcionUsar = ''
        nombre = ''
        while self.lineas[self.index] != "":
            #print(f'CARACTER11 - {self.lineas[self.index] } | ESTADO - {estado_actual} | FILA - {self.fila}  | COLUMNA - {self.columna}')
            
            # IDENTIFICAR SALTO DE LINEA
            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna =0

            # ************************
            #         ESTADOS
            # ************************


            # S0 -> "Funcion" S1
            elif estado_actual == 'S0':
                funciones = ['CrearBD','EliminarBD','CrearColeccion', 'EliminarColeccion', 'InsertarUnico', 
                             'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico']
                for x in funciones:
                    estado_actual = self._token(x, 'S0', 'S1')
                    if estado_actual != 'ERROR':
                        
                        #Funcion encontrada satisfactoriamente
                        funcionUsar = x
                        break

            # S1 -> ID S2
            elif estado_actual == 'S1':
                #print("ESTO DE ULTIMO")
                estado_actual = self.juntar_texto()
                if estado_actual != None:

                    # nombre de la nueva accion
                    nombre = estado_actual
                    estado_actual = 'S2'
                
                else:
                    print("error en la lectura de texto")
                    estado_actual = "ERROR"


            # S2 -> '=' S3
            elif estado_actual == 'S2':
                # Busqueda del signo igual
                estado_actual = self._token('=', 'S2', 'S3')
            

            # S3 -> nueva S4
            elif estado_actual == 'S3':
                # Busqueda de la palabra nueva
                estado_actual = self._token('nueva', 'S3', 'S4')

            
            # S4 -> Funcion S5
            elif estado_actual == 'S4':
                # busqeuda de la palabra funcion
                estado_actual = self._token(funcionUsar, 'S4', 'S5')


            # S5 -> Funcion S6
            elif estado_actual == 'S5':
                # busqueda del parentesis de apertura
                estado_actual = self._token('(', 'S5', 'S6')


            # S6 -> Funcion S8
            elif estado_actual == 'S6':
                # busqueda del parentesis de cerrar
                estado_actual = self._token(')', 'S6', 'S8')
                if estado_actual == 'ERROR':
                    opcion_atributo = self._atributo(funcionUsar)
                    if opcion_atributo == 'ERROR':
                        estado_actual = 'ERROR'

                    else:
                        estado_actual = 'S6'


            # S8 -> ; S9
            elif estado_actual == 'S8':
                # Busqueda del punto y coma ; de final
                estado_actual = self._token(';', 'S8', 'S9')


            elif estado_actual == 'S9':
                # es caso de que llegue a este paso debe hacer todas las operaciones
                # y recetear el estado a S0 para que empiece de nuevo
                pass

            # S14 -> }
            elif estado_actual == 'S14':
                #print("ESTO DE ULTIMO")
                estado_actual = self._token('}', 'S14', 'S15')
                

            # S15 -> ,
            elif estado_actual == 'S15':
                if self.lineas[self.index] != ' ':
                    estado_actual = self._token(',', 'S16', 'S0')
                    
            elif estado_actual == 'S16':  
                break
            
            # ERRORES 
            if estado_actual == 'ERROR':
                #print('\t AQUI OCURRIO UN ERROR')
                funcionUsar = ''
                estado_actual = 'S0'
                self._salto_linea()
            
            #INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index +=1
            else:
                break

            
    def guardarErrores(self, token, fila, columna):
        self.ListaErrores.append({"token":token, "fila": fila, "columna":columna})


a = Analizador(texto)
a._compile()