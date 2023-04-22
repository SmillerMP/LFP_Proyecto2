import os
#from analizador import get_listaTokens

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