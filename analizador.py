from creacionTablas import generacionTokens

texto = ''
with open('archivoprueba.txt', 'r', encoding='utf-8') as archivo:
    # for lineas in archivo.readlines():
    #     texto += lineas
    texto = archivo.read()
        
# for x in texto:
#     print(x)

class Analizador:
    def __init__(self, entrada:str):
        self.lineas = entrada # Texto analizar
        self.index = 0 # Poscicion dentro de todo el texto
        self.fila = 1 # Fila Actual
        self.columna = 1 # Columna Actual
        self.ListaErrores = [] # Lista de errores
        
        self.tokenAutilizar = '' # Token utilizado en el momentos
        self.json = '' # sintaxis json para el comando mongoDb
        self.identificador = ''  # indentificador para el comando
        self.contadorToken = 0  # Contador de tokens encontrados
        self.listaTokens  = []  # Lista con todos los tokens
        self.textoError = ''    # 
        self.listaComandos = []
        
        self.tipoDeError = ''  # Guarda el tipo de error, lexico o sintactico
        self.contadorErrores = 0
        # Una lista con todos los posibles tokens
        self.listaTodosTokes = ['CrearBD','EliminarBD','CrearColeccion', 'EliminarColeccion', 'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 
                                'BuscarUnico', 'nueva', '"', '=', '(', ')', ':', ';', ',', '$set', '{', '}', '/*', '*/', '---']

    def _token(self, token:str, estado_actual:str, estado_sig:str):
        lexema = ''
        if self.lineas[self.index] != " ":
            text = self._juntar(self.index, len(token))
            token_encontrado = self._analizar(token, text)
            if token_encontrado != False:
                self.index += len(token)-1
                self.columna += len(token)
                self.tokenAutilizar = token_encontrado
                self.contadorToken += 1
                self.guardadoTokens(self.tokenAutilizar, lexema)

                return estado_sig
            else:
                if token == '/*' or token == '---':
                    return 'ERROR'
                else:
                    self.tokenAutilizar = token
                    return 'ERROR'
                
        else:
            self.columna += 1
            return estado_actual

    def _leer_eternamente(self):
        lexema = ''
        while self.lineas[self.index] != "":
            if self.index+1 < len(self.lineas):
                if self.lineas[self.index] != "*" and self.lineas[self.index+1] != "/":
                    if self.lineas[self.index] != "\n":
                        self.index += 1
                        self.columna += 1
                    else:
                        self.fila += 1
                        self.columna = 1
                        self.index += 1

                else:
                    self.index += 2
                    self.columna += 2
                    self.tokenAutilizar = '*/'
                    self.contadorToken += 1
                    self.guardadoTokens(self.tokenAutilizar, lexema)
                    break
            else:
                break

    def _salto_linea(self):   
        while self.lineas[self.index] != "":
            if self.index+1 < len(self.lineas):
                if self.lineas[self.index] != "\n":
                    self.index += 1
                    self.columna += 1
                else:
                    self.columna = 1
                    
                    break
            else:
                break
 

    def _juntar_comillas(self):
        lexema = 'si'
        try:
            tmp = ''
            while self.lineas[self.index] != '"':
                if self.lineas[self.index] != '\n':
                    tmp += self.lineas[self.index]
                    self.index += 1
                    self.columna += 1
                
                else:
                    tmp = ''
                    return 'ERROR'
        
            #print(f'********** ENCONTRE - {tmp} ***************')
            self.index -= 1
            self.tokenAutilizar = tmp
            self.contadorToken += 1
            self.guardadoTokens(self.tokenAutilizar, lexema)
            return tmp
        except:
            return None

        
    def juntar_texto(self):
        lexema = 'si'
        try:
            tmp = ''
            self.index += 1
            self.columna += 1
            while self.lineas[self.index] != ' ':
                if self.lineas[self.index] != '"':
                    if self.lineas[self.index] != '\n':
                        tmp += self.lineas[self.index]
                        self.index += 1
                        self.columna += 1
                    
                    else:
                        tmp = ''
                        return 'ERROR'
                else:
                    break
            #print(f'********** ENCONTRE - {tmp} ***************')
            self.columna += 1
            self.tokenAutilizar = tmp
            self.contadorToken += 1
            self.guardadoTokens(self.tokenAutilizar, lexema)
            return tmp
        except:
            return None

        
    def _juntar(self,_index:int, _count:int):
        try:
            tmp = ''
            for i in range(_index, _index + _count):
                if self.lineas[i] != ' ':
                    tmp += self.lineas[i]
                else:
                    break
            return tmp
        except:
            return None
        
    def _analizar(self, token, texto):
        try:
            count = 0
            tokem_tmp = ""
            if len(str(token)) == len(str(texto)):
                for i in texto:
                    #CUANDO LA LETRA HAGA MATCH CON EL TOKEN ENTRA
                    #print('COMBINACION -> ',i , '==', token[count])
                    if str(i) == str(token[count]):
                        tokem_tmp += i  
                        count += 1 
                    else:
                        #print('ERROR1')
                        encontrado = False
                        for x in self.listaTodosTokes:
                            if x == texto:
                                encontrado = True
                                self.tipoDeError = 'Sintactico'
                                break
                        if encontrado == False:
                            self.tipoDeError = 'Lexico'

                        self.textoError = texto
                        return False
                    
                #print(f'********** ENCONTRE - {tokem_tmp} ***************')
                return tokem_tmp
            else:
                # Error en caso de que el tama;o del token no sea el mismo que el tama;o del texto
                encontrado = False
                for x in self.listaTodosTokes:
                    if x == texto:
                        encontrado = True
                        self.tipoDeError = 'Sintactico'
                        break
                if encontrado == False:
                    self.tipoDeError = 'Lexico'

                self.textoError = texto
                return False
        except:
            #print('ERROR2')
            return False
    

    def _atributo(self, funcion):
        estado_actual = 'A0'
        identificador = ''
        sintaxisJson = ''

        while self.lineas[self.index] != "":            
            # Identifica saltos de linea
            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna = 1


            # A0 -> " A1
            elif estado_actual == 'A0':
                # busqueda de la comilla doble
                estado_actual = self._token('"', 'A0', 'A1')

            elif estado_actual == 'A1':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:

                    # nombre del identificador
                    identificador = estado_actual
                    self.identificador = identificador
                    print(identificador)
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

                # Guarda la sitaxis del JSON
                self.json = sintaxisJson
                estado_actual = 'A6'


            # A6 -> " A7
            elif estado_actual == 'A6':
                # busqueda de la comilla doble
                estado_actual = self._token('"', 'A6', 'A7')


            elif estado_actual == 'A7':
                self.index -= 1
                return identificador

            
            # if estado_actual == 'ERROR':
            #     return estado_actual
            
            # Retornar error a la funcion al metodo compilador
            if estado_actual == 'ERROR' or sintaxisJson == 'ERROR':
                print('\n\n+++++++++++++++ ERROR +++++++++++++++\n\n')
                return 'ERROR'

            #INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index +=1
            else:
                break

    # Retorna el JSON, o error al metodo atributo
    def nombre(self):
        estado_actual = 'N0'
        json = ''
        lista_estadoUsados = []

        while self.lineas[self.index] != "":
        
            # Identifica saltos de linea
            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna = 1


            # ************************
            #         ESTADOS
            # ************************

            # N0 -> { N1
            elif estado_actual == 'N0':
                estado_actual = self._token('{', 'N0', 'N1')

            # N1 -> " N2
            elif estado_actual == 'N1':
                estado_actual = self._token('"', 'N1', 'N2')

            # N2 -> texto N3
            elif estado_actual == 'N2':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:
                    estado_actual = 'N3'  

                else:
                    print("Error en la estructura JSON, nombre")
                    estado_actual = "ERROR"

            # N3 -> " N4
            elif estado_actual == 'N3':
                estado_actual = self._token('"', 'N3', 'N4')


            # N4 -> : N5
            elif estado_actual == 'N4':
                estado_actual = self._token(':', 'N4', 'N5')

            # N5 -> " N6
            elif estado_actual == 'N5':
                estado_actual = self._token('"', 'N5', 'N6')

            # N6 -> texto N7
            elif estado_actual == 'N6':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:
                    estado_actual = 'N7'  

                else:
                    print("Error en la estructura JSON, nombre")
                    estado_actual = "ERROR"

            # N7 -> " N8
            elif estado_actual == 'N7':
                estado_actual = self._token('"', 'N7', 'N8')

            # N8 -> } N9
            elif estado_actual == 'N8':
                estado_actual = self._token('}', 'N8', 'N9')

            elif estado_actual == 'N9':
                self.index -= 1
                return json
            
            
            # Retornar error a la funcion al metodo compilador
            if estado_actual == 'ERROR':
                print('\n\n+++++++++++++++ ERROR +++++++++++++++\n\n')
                return 'ERROR'
            

            encontrado = False
            for x in lista_estadoUsados:
                if x == estado_actual:
                    encontrado = True
            if encontrado == False:
                lista_estadoUsados.append(estado_actual)
                json += self.tokenAutilizar
            
            #INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index +=1
            else:
                break

    # Retorna el JSON, o error al metodo atributo
    def nombre_set(self):
        estado_actual = 'NS0'
        json = ''
        lista_estadoUsados = []

        while self.lineas[self.index] != "":
        
            # Identifica saltos de linea
            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna = 1



            # ************************
            #         ESTADOS
            # ************************

            # NS0 -> { NS1
            elif estado_actual == 'NS0':
                estado_actual = self._token('{', 'NS0', 'NS1')

            # NS1 -> " NS2
            elif estado_actual == 'NS1':
                estado_actual = self._token('"', 'NS1', 'NS2')

            # NS2 -> texto NS3
            elif estado_actual == 'NS2':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:
                    estado_actual = 'NS3'  
                else:
                    print("Error en la estructura JSON, nombre y set")
                    estado_actual = "ERROR"

            # NS3 -> " NS4
            elif estado_actual == 'NS3':
                estado_actual = self._token('"', 'NS3', 'NS4')     

            # NS4 -> : NS5
            elif estado_actual == 'NS4':
                estado_actual = self._token(':', 'NS4', 'NS5')

            # NS5 -> " NS6
            elif estado_actual == 'NS5':
                estado_actual = self._token('"', 'NS5', 'NS6')

            # NS6 -> texto NS7
            elif estado_actual == 'NS6':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:
                    estado_actual = 'NS7'  

                else:
                    print("Error en la estructura JSON, nombre y set")
                    estado_actual = "ERROR"

            # NS7 -> " NS8
            elif estado_actual == 'NS7':
                estado_actual = self._token('"', 'NS7', 'NS8')

             # NS8 -> } NS9
            elif estado_actual == 'NS8':
                estado_actual = self._token('}', 'NS8', 'NS9')

            # NS9 -> , NS10
            elif estado_actual == 'NS9':
                estado_actual = self._token(',', 'NS9', 'NS10')

            # NS10 -> { NS11
            elif estado_actual == 'NS10':
                estado_actual = self._token('{', 'NS10', 'NS11')

            # NS11 -> $SET NS12
            elif estado_actual == 'NS11':
                estado_actual = self._token('$set', 'NS11', 'NS12')  

            # NS12 -> : NS13
            elif estado_actual == 'NS12':
                estado_actual = self._token(':', 'NS12', 'NS13')

            # NS13 -> { NS14
            elif estado_actual == 'NS13':
                estado_actual = self._token('{', 'NS13', 'NS14')

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

            # NS17 -> : NS18
            elif estado_actual == 'NS17':
                estado_actual = self._token(':', 'NS17', 'NS18')

            # NS18 -> " NS19
            elif estado_actual == 'NS18':
                estado_actual = self._token('"', 'NS18', 'NS19')

            # NS19 -> texto NS20
            elif estado_actual == 'NS19':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:

                    #self.index -= 1
                    estado_actual = 'NS20'  

                else:
                    print("Error en la estructura JSON, nombre y autor")
                    estado_actual = "ERROR"

            # NS20 -> " NS21
            elif estado_actual == 'NS20':
                estado_actual = self._token('"', 'NS20', 'NS21')

            # NS21 -> } NS22
            elif estado_actual == 'NS21':
                estado_actual = self._token('}', 'NS21', 'NS22')
            
            # NS22 -> } NS23
            elif estado_actual == 'NS22':
                estado_actual = self._token('}', 'NS22', 'NS23')

            elif estado_actual == 'NS23':
                self.index -= 1
                return json
            

            # Retornar error a la funcion al metodo compilador
            if estado_actual == 'ERROR':
                print('\n\n+++++++++++++++ ERROR +++++++++++++++\n\n')
                return 'ERROR'
            
            encontrado = False
            for x in lista_estadoUsados:
                if x == estado_actual:
                    encontrado = True
            if encontrado == False:
                lista_estadoUsados.append(estado_actual)
                json += self.tokenAutilizar

            
            #INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index +=1
            else:
                break


    # Retorna el JSON, o error al metodo atributo
    def nombre_autor(self):
        estado_actual = 'NA0'
        json = ''
        lista_estadoUsados = []


        while self.lineas[self.index] != "":
        
            # Identifica saltos de linea
            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna = 1

            # ************************
            #         ESTADOS
            # ************************

            # NA0 -> { NA1
            elif estado_actual == 'NA0':
                estado_actual = self._token('{', 'NA0', 'NA1')
                
            # NA1 -> " NA2
            elif estado_actual == 'NA1':
                estado_actual = self._token('"', 'NA1', 'NA2')

            # NA2 -> texto NA3
            elif estado_actual == 'NA2':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:

                    estado_actual = 'NA3'  

                else:
                    print("Error en la estructura JSON, nombre y autor")
                    estado_actual = "ERROR"

             # NA3 -> " NA4
            elif estado_actual == 'NA3':
                estado_actual = self._token('"', 'NA3', 'NA4')


            # NA4 -> : NA5
            elif estado_actual == 'NA4':
                estado_actual = self._token(':', 'NA4', 'NA5')

            # NA5 -> " NA6
            elif estado_actual == 'NA5':
                estado_actual = self._token('"', 'NA5', 'NA6')

            # NA6 -> texto NA7
            elif estado_actual == 'NA6':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:

                    estado_actual = 'NA7'  

                else:
                    print("Error en la estructura JSON, nombre y autor")
                    estado_actual = "ERROR"

            # NA7 -> " NA8
            elif estado_actual == 'NA7':
                estado_actual = self._token('"', 'NA7', 'NA8')

            # NA8 -> , NA9
            elif estado_actual == 'NA8':
                estado_actual = self._token(',', 'NA8', 'NA9')

            

            # NA9 -> " NA10
            elif estado_actual == 'NA9':
                estado_actual = self._token('"', 'NA9', 'NA10')

            # NA10 -> texto NA11
            elif estado_actual == 'NA10':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:
                    estado_actual = 'NA11'  
                else:
                    print("Error en la estructura JSON, nombre y autor")
                    estado_actual = "ERROR"

             # NA11 -> " NA12
            elif estado_actual == 'NA11':
                estado_actual = self._token('"', 'NA11', 'NA12')

            # NA12 -> : NA13
            elif estado_actual == 'NA12':
                estado_actual = self._token(':', 'NA12', 'NA13')

            # NA13 -> " NA14
            elif estado_actual == 'NA13':
                estado_actual = self._token('"', 'NA13', 'NA14')

            # NA14 -> texto NA15
            elif estado_actual == 'NA14':
                estado_actual = self._juntar_comillas()
                if estado_actual != None:

                    #self.index -= 1
                    estado_actual = 'NA15'  

                else:
                    print("Error en la estructura JSON, nombre y autor")
                    estado_actual = "ERROR"

            # NA15 -> " NA16
            elif estado_actual == 'NA15':
                estado_actual = self._token('"', 'NA15', 'NA16')

            # NA16 -> } NA17
            elif estado_actual == 'NA16':
                estado_actual = self._token('}', 'NA16', 'NA17')

            elif estado_actual == 'NA17':
                self.index -= 1
                print(json)
                return json

            if estado_actual == 'ERROR':
                print('\n\n+++++++++++++++ ERROR +++++++++++++++\n\n')
                return 'ERROR'
            
            
            # va agregando al json cada uno de los tokens encontrados
            encontrado = False
            for x in lista_estadoUsados:
                if x == estado_actual:
                    encontrado = True
            if encontrado == False:
                lista_estadoUsados.append(estado_actual)
                json += self.tokenAutilizar
            
            #INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index +=1
            else:
                break

            
            
    def _compile(self):
        estado_actual = 'S0'
        funcionUsar = ''
        nombreBase = ''
        contador_comandos = 0
        while self.lineas[self.index] != "":
            #print(f'CARACTER11 - {self.lineas[self.index] } | ESTADO - {estado_actual} | FILA - {self.fila}  | COLUMNA - {self.columna}')
            
            # Identifica saltos de linea
            if self.lineas[self.index] == '\n':
                self.fila += 1
                # Resetea el contador de columna a 1
                self.columna = 1

            # ************************
            #         ESTADOS
            # ************************


            # S0 -> "Funcion" S1
            elif estado_actual == 'S0':
                # Verificacion de comentarios
                comentario = self._token('---', 'S0', 'S0')
                if comentario != 'ERROR':
                    self._salto_linea()
                    continue

                comentario = self._token('/*', 'S0', 'S0')
                if comentario != 'ERROR':
                    self.index +=1
                    self._leer_eternamente()
                    continue

                funciones = ['CrearBD','EliminarBD','CrearColeccion', 'EliminarColeccion', 'InsertarUnico', 
                             'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico', '0_Coincidencias']
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
                    nombreBase = estado_actual
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


            # S5 -> ( S6
            elif estado_actual == 'S5':
                # busqueda del parentesis de apertura
                estado_actual = self._token('(', 'S5', 'S6')


            # S6 -> ) S8
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
                contador_comandos += 1
                print(f"\n ############ COMANDO COMPLETADO ######  {contador_comandos} ###### \n")  
                self.creadorComando(funcionUsar, nombreBase, self.identificador, self.json)
                estado_actual = 'S0'
                

            
            
            # ERRORES 
            if estado_actual == 'ERROR':
                print('\n\n+++++++++++++++ ERROR +++++++++++++++\n\n')
                self.contadorErrores += 1
                self.guardarErrores(self.contadorErrores, self.textoError, self.tokenAutilizar, self.tipoDeError, self.fila, self.columna)
                funcionUsar = ''
                estado_actual = 'S0'
                self._salto_linea()
                continue
            
            #INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index +=1
            else:
                break

    # Esta funcion crea los comandos traducidos a MongoDB
    def creadorComando(self, funcionUso, nombreBase, nombre, json):
        
        # Cada if compara la funcion que encontro, y la traduce a lenguaje MongoDB
        # en los casos donde el comando necesita de mas informacion, se le brinda a 
        # travez de las variables nombre y json

        # Json contiene la estrucutura que necesitan algunos comandos para funcionar
        comando = ''
        if funcionUso == 'CrearBD':
            comando = f"use('{nombreBase}');"
        elif funcionUso == 'EliminarBD':
            comando = f'db.dropDatabase();'
        elif funcionUso == 'CrearColeccion':
            comando = f"db.createCollection('{nombre}')"
        elif funcionUso == 'EliminarColeccion':
            comando = f'db.{nombre}.drop();'
        elif funcionUso == 'InsertarUnico':
            comando = f'db.{nombre}.insertOne({json});'
        elif funcionUso == 'ActualizarUnico':
            comando = f'db.{nombre}.updateOne({json});'
        elif funcionUso == 'EliminarUnico':
            comando = f'db.{nombre}.deleteOne({json});'
        elif funcionUso == 'BuscarTodo':
            comando = f'db.{nombre}.find();'
        elif funcionUso == 'BuscarUnico':
            comando = f'db.{nombre}.findOne();'

        print(comando)
        self.listaComandos.append(comando)
        

    # Esta funcion guarda cada uno de los tokens encontrados durante el programa
    # Los guada en una lista para ser recorridos posterioremente y graficarlos en una tabla
    def guardadoTokens(self,tokenAnalisis, lexema):

        # cada elif compara el token y asigna su lexema
        if lexema != 'si':
            if tokenAnalisis == '"':
                lexema = 'comillas dobles'
            elif tokenAnalisis == '=':
                lexema = 'igual'
            elif tokenAnalisis == '(':
                lexema = 'parentesis de apertura'
            elif tokenAnalisis == ')':
                lexema = 'parentesis de cierre'
            elif tokenAnalisis == ':':
                lexema = 'dos puntos'
            elif tokenAnalisis == ';':
                lexema = 'punto y coma'
            elif tokenAnalisis == ',':
                lexema = 'coma'
            elif tokenAnalisis == '$set':
                lexema = 'set'
            elif tokenAnalisis == '{':
                lexema = 'llave de apertura'
            elif tokenAnalisis == '}':
                lexema = 'llave de cierre'
            elif tokenAnalisis == '/*':
                lexema = 'inicio comentario multilinea'
            elif tokenAnalisis == '*/':
                lexema = 'cierre comentario multilinea'
            elif tokenAnalisis == '---':
                lexema = 'comentario simple'
            elif tokenAnalisis == 'nueva':
                lexema = 'nueva'
            else:
                # en caso de que no exista un lexema para el token, el lexema sera igual al token
                lexema = tokenAnalisis
        else: 
            lexema = 'cadena de texto'

        # Guarda en un diccionario temporal el contador, lexema del token, el token y su informacion de donde fue encontrado (fila y columna)
        tempDiccionario = {'contador': self.contadorToken, 'lexema': lexema, 'token': tokenAnalisis, 'fila': self.fila, 'columna': self.columna}
        
        # todos los diccionarios se agregan al final de la lista
        self.listaTokens.append(tempDiccionario)
        

    def guardarErrores(self, contador, tokenError, tokenEsperado, tipoDeError, fila, columna):
        self.ListaErrores.append({'contador': contador, "token_Error":tokenError, 'token_esperado':tokenEsperado, 'tipoError':tipoDeError ,"fila": fila, "columna":columna})



a = Analizador(texto)
a._compile()
for x in a.listaTokens:
    print(x)
# generacionTokens(a.listaTokens)

for i in a.ListaErrores:
    print(i)