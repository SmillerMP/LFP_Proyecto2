import os

def generacionTokens(lista):
    #lista = get_listaTokens()

    with open("Reports/Tokens.dot", "w", encoding="utf-8") as grafo_dot:
        grafo_dot.write('digraph { \n')
        grafo_dot.write(f'graph [label="Tabla de Tokens", labelloc=top]\n')
        grafo_dot.write('rankdir = LR \n' )
        grafo_dot.write('ranksep=1.5 \n' )
        grafo_dot.write(f'node[shape=none, style="filled" fontname="Arial", fontsize=12] \n\n')
        
        # creara el encabezado en graphviz
        grafo_dot.write(f'''
        
    n{1} [ label = <
        <table>
            <tr><td bgcolor="#e74c3c"> Correlativo </td><td bgcolor="#f39c12 "> Lexema </td><td bgcolor="#f1c40f"> Token </td><td bgcolor="#27ae60"> Fila </td> <td bgcolor="#3498db"> Columna </td></tr>
                    ''')

        # Recorre la lista con diccionarios, donde se ecuentra cada uno de los tokens encontrados
        for diccionario in lista:
            grafo_dot.write(f'''     
            <tr><td bgcolor="#f1948a "> {diccionario["contador"]} </td><td bgcolor="#f8c471 "> {diccionario["lexema"]} </td><td bgcolor="#f7dc6f"> {diccionario["token"]} </td> <td bgcolor="#7dcea0"> {diccionario["fila"]} </td> <td bgcolor="#85c1e9"> {diccionario["columna"]} </td></tr>                
                            ''')
                            
                    
        # Cierra la tabla
        grafo_dot.write(f'''
        </table>
    > ]
                    ''')
                    

        grafo_dot.write('\n\n}')

    os.system("dot.exe -Tpdf Reports/Tokens.dot -o  Reports/Tokens.pdf")
    os.startfile("Reports\Tokens.pdf")



def generacionErrores(lista):

    with open("Reports/Errores.dot", "w", encoding="utf-8") as grafo_dot:
        grafo_dot.write('digraph { \n')
        grafo_dot.write(f'graph [label="Tabla de Errores", labelloc=top]\n')
        grafo_dot.write('rankdir = LR \n' )
        grafo_dot.write('ranksep=1.5 \n' )
        grafo_dot.write(f'node[shape=none, style="filled" fontname="Arial", fontsize=12] \n\n')
        
        # creara el encabezado en graphviz
        grafo_dot.write(f'''
        
    n{1} [ label = <
        <table>
            <tr><td bgcolor="#2c3e50"> Correlativo </td><td bgcolor="#34495e"> Token Error </td><td bgcolor="#7f8c8d"> Token Esperado </td><td bgcolor="#95a5a6"> Tipo de Error </td><td bgcolor="#2980b9"> Fila </td> <td bgcolor="#8e44ad"> Columna </td></tr>
                    ''')

        # Recorre la lista con diccionarios, donde se ecuentra cada uno de los tokens encontrados
        for diccionario in lista:
            grafo_dot.write(f'''     
            <tr><td bgcolor="#808b96"> {diccionario["contador"]} </td><td bgcolor="#85929e"> {diccionario["token_Error"]} </td><td bgcolor="#b2babb"> {diccionario["token_esperado"]} </td><td bgcolor="#bfc9ca"> {diccionario["tipoError"]} </td><td bgcolor="#7fb3d5"> {diccionario["fila"]} </td> <td bgcolor="#bb8fce"> {diccionario["columna"]} </td></tr>                
                            ''')
                            
                    
        # Cierra la tabla
        grafo_dot.write(f'''
        </table>
    > ]
                    ''')
                    

        grafo_dot.write('\n\n}')

    os.system("dot.exe -Tpdf Reports/Errores.dot -o  Reports/Errores.pdf")
    os.startfile("Reports\Errores.pdf")