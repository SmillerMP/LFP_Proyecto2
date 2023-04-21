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
                    self.index -= 1
                    return identificador
                      
            # A4 -> " A5
            elif estado_actual == 'A4':
                # busqueda de la comilla doble
                estado_actual = self._token('"', 'A4', 'A5')

            # A5 -> JSON A6
            elif estado_actual == 'A5':
                if funcion == "InsertarUnico":
                    sintaxisJson = self.nombre_autor()
                
                elif funcion == "EliminarUnico":
                    sintaxisJson = self.nombre()

                elif funcion == "ActualizarUnico":
                    sintaxisJson = self.nombre_set()

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

    def nombre(self):
        estado_actual = 'N0'
        json = ''

        while self.lineas[self.index] != "":
        
            # IDENTIFICAR SALTO DE LINEA
            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna =0

            # ************************
            #         ESTADOS
            # ************************

            # N0 -> { NS1
            elif estado_actual == 'N0':
                estado_actual = self._token('{', 'N0', 'N1')

            # N1 -> "nombre" NS2
            elif estado_actual == 'N1':
                estado_actual = self._token('"nombre"', 'N1', 'N2')

            # N2 -> : N3
            elif estado_actual == 'N2':
                estado_actual = self._token(':', 'N2', 'N3')

            # N3 -> " N4
            elif estado_actual == 'N3':
                estado_actual = self._token('"', 'N3', 'N4')

            # N4 -> texto N5
            elif estado_actual == 'N4':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:
                    estado_actual = 'N5'  

                else:
                    print("Error en la estructura JSON, nombre")
                    estado_actual = "ERROR"

            # N5 -> " N6
            elif estado_actual == 'N5':
                estado_actual = self._token('"', 'N5', 'N6')

            # N6 -> } N7
            elif estado_actual == 'N6':
                estado_actual = self._token('}', 'N6', 'N7')

            elif estado_actual == 'N7':
                self.index -= 1
                return json
            
            #INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index +=1
            else:
                break


    def nombre_set(self):
        estado_actual = 'NS0'
        json = ''

        while self.lineas[self.index] != "":
        
            # IDENTIFICAR SALTO DE LINEA
            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna =0

            # ************************
            #         ESTADOS
            # ************************

            # NA0 -> { NS1
            elif estado_actual == 'NS0':
                estado_actual = self._token('{', 'NS0', 'NS1')

            # NS1 -> "nombre" NS2
            elif estado_actual == 'NS1':
                estado_actual = self._token('"nombre"', 'NS1', 'NS2')

            # NS2 -> : NS3
            elif estado_actual == 'NS2':
                estado_actual = self._token(':', 'NS2', 'NS3')

            # NS3 -> " NS4
            elif estado_actual == 'NS3':
                estado_actual = self._token('"', 'NS3', 'NS4')

            # NS4 -> texto NS5
            elif estado_actual == 'NS4':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:
                    estado_actual = 'NS5'  

                else:
                    print("Error en la estructura JSON, nombre y set")
                    estado_actual = "ERROR"

            # NS5 -> " NS6
            elif estado_actual == 'NS5':
                estado_actual = self._token('"', 'NS5', 'NS6')

             # NS6 -> } NS7
            elif estado_actual == 'NS6':
                estado_actual = self._token('}', 'NS6', 'NS7')

            # NS7 -> , NS8
            elif estado_actual == 'NS7':
                estado_actual = self._token(',', 'NS7', 'NS8')

            # NS8 -> { NS9
            elif estado_actual == 'NS8':
                estado_actual = self._token('{', 'NS8', 'NS9')

            # NS9 -> $SET NS10
            elif estado_actual == 'NS9':
                estado_actual = self._token('$set', 'NS9', 'NS10')  

            # NS10 -> : NS11
            elif estado_actual == 'NS10':
                estado_actual = self._token(':', 'NS10', 'NS11')

            # NS11 -> { NS12
            elif estado_actual == 'NS11':
                estado_actual = self._token('{', 'NS11', 'NS12')

            # NS12 -> "autor" NS13
            elif estado_actual == 'NS12':
                estado_actual = self._token('"autor"', 'NS12', 'NS13')

            # NS13 -> : NS14
            elif estado_actual == 'NS13':
                estado_actual = self._token(':', 'NS13', 'NS14')

            # NS14 -> " NS15
            elif estado_actual == 'NS14':
                estado_actual = self._token('"', 'NS14', 'NS15')

            # NS15 -> texto NS16
            elif estado_actual == 'NS15':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:

                    #self.index -= 1
                    estado_actual = 'NS16'  

                else:
                    print("Error en la estructura JSON, nombre y autor")
                    estado_actual = "ERROR"

            # NS16 -> " NS17
            elif estado_actual == 'NS16':
                estado_actual = self._token('"', 'NS16', 'NS17')

            # NS17 -> } NS18
            elif estado_actual == 'NS17':
                estado_actual = self._token('}', 'NS17', 'NS18')
            
            # NS18 -> } NS19
            elif estado_actual == 'NS18':
                estado_actual = self._token('}', 'NS18', 'NS19')

            elif estado_actual == 'NS19':
                self.index -= 1
                return json


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

            # NA0 -> { NS1
            elif estado_actual == 'NA0':
                estado_actual = self._token('{', 'NA0', 'NS1')

            # NS1 -> "nombre" NS2
            elif estado_actual == 'NS1':
                estado_actual = self._token('"nombre"', 'NS1', 'NS2')

            # NS2 -> : NS3
            elif estado_actual == 'NS2':
                estado_actual = self._token(':', 'NS2', 'NS3')

            # NS3 -> " NS4
            elif estado_actual == 'NS3':
                estado_actual = self._token('"', 'NS3', 'NS4')

            # NS4 -> texto NS5
            elif estado_actual == 'NS4':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:

                    #self.index -= 1
                    estado_actual = 'NS5'  

                else:
                    print("Error en la estructura JSON, nombre y autor")
                    estado_actual = "ERROR"

            # NS5 -> " NA6
            elif estado_actual == 'NS5':
                estado_actual = self._token('"', 'NS5', 'NA6')

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

                    #self.index -= 1
                    estado_actual = 'NA11'  

                else:
                    print("Error en la estructura JSON, nombre y autor")
                    estado_actual = "ERROR"

            # NA11 -> " NA12
            elif estado_actual == 'NA11':
                estado_actual = self._token('"', 'NA11', 'NA12')

            # NA12 -> } NA13
            elif estado_actual == 'NA12':
                estado_actual = self._token('}', 'NA12', 'NA13')

            elif estado_actual == 'NA13':
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



            if estado_actual == 'S9':
                # es caso de que llegue a este paso debe hacer todas las operaciones
                # y recetear el estado a S0 para que empiece de nuevo
                print("\n ############ COMANDO COMPLETADO ############ \n")  
                estado_actual = 'S0'
                pass

            
            
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