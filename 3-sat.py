
import random
"""
Emiliano Javier Gómez Jiménez A01377235
Luis Jonathan Rosas Ramos A01377942
Zabdiel Valentin Garduño Vivanco A01377950
"""


# Leer de un archivo txt y guardar en un diccionario las clausulas.
def leerArchivo():
    bitStream = [] # 20 Variables generate randomly
    clausulas = {} # Dictionary of clauses 91 clasulas
    Arreglo = [] #cada linea del txt
    try:
        print(
            "Bienvenido, introduce el nombre del archivo con su formato .txt ,\n asegúrate de que el archivo se encuentre en el mismo directorio.\n Ejemplo: input.txt\n")
        fileh = input("Nombre del archivo: ")
        archivo = open(fileh, "r")
        lineas = archivo.readlines()



        # Lee las lineas del txt y corrige el formato
        #Ejemplo: Arreglo= ['c This Formular is generated by mcnf', 'p cnf 20  91 ', ' 4 -18 19 0', '3 18 -5 0',
        for i in range(0, len(lineas)):
            lineas[i] = lineas[i].replace("\n", "")
            linea = lineas[i]
            Arreglo.append(linea)

        ''' '''
        # Inventa un bitstream inicial de 20 variables
        #Ejemplo: bitStream=[1,0,0,0,0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0]
        for i in range(20):
            bitStream.append(random.randint(0,1))
        #print(Arreglo)


        # Asigna las clausulas a un diccionario
        #Ejemplo: clausulas={0:[9,-3,16],1:[4,-16,20]}
        c = 0
        for x in range(2, len(Arreglo)-3):
            #Eliminar espacio en blanco al inicio de la clausula
            #Ex:" 4 -18 19 0"
            if(Arreglo[x][0]==' '):
                Arreglo[x]=Arreglo[x][1:]

            clausula = Arreglo[x].split(" ")
            clausulas[c] = []
            for y in range(0, len(clausula) - 1):
                clausulas[c].append(int(clausula[y]))
            c = c + 1
        #print(clausulas)


    except:
        print("Error, el archivo no se encuentra en la carpeta o no se especifico su formato '.txt': Ex: 'input.txt'")
    return clausulas, bitStream


#Regresa todas las clausulas con sus bits
def clausulasSatisfechas(bitStream, clausulas):
    #Diccionario con los bits ya traducidos
    clausulas2={}

    #Traduce los indices por bits
    for x in range(0, len(clausulas)):#Por cada clausula
        for y in range(0,3):# Porque solo hay 3 variables por clausula
            if clausulas2.get(x)==None:
                clausulas2[x]=[]
            valor=clausulas[x][y]
            bit=bitStream[abs(valor)-1]
            #print('valor '+str(valor)+', bit '+str(bit)+', en llave ' +str(x))
            if(valor<0):
                if(bit==0):
                    clausulas2[x].append(1)
                if(bit==1):
                    clausulas2[x].append(0)
            else:
                clausulas2[x].append(bit)
    return clausulas2

def filtrarClausulas(clausulas):
    clasulasSatisfechas={}
    clasulasNoSatisfechas={}
    for clave in clausulas:
        valor = clausulas[clave]
        if(any(valor)):# any([1,0,0]) == true
            clasulasSatisfechas[clave] = valor 
        else:# any([0,0,0]) == false
            clasulasNoSatisfechas[clave] = valor 
    #print(clasulasSatisfechas)
    #print("----------------------")
    #print(clasulasNoSatisfechas)

    return clasulasSatisfechas,clasulasNoSatisfechas

def escogerClausulaNoSatisfecha(clausulasNoSatisfecha):
    llaveRandom=random.choice(list(clausulasNoSatisfecha))
    #print("Clausula a cambiar: ", llaveRandom, ", Valor:", clausulasNoSatisfecha[llaveRandom])
    indiceDeVariable=random.randint(0,2)
    #print(indiceDeVariable)
    return llaveRandom,indiceDeVariable

def imprimirClausulas(clausulas, f):
    for llave in clausulas:
        valor = clausulas[llave]
        f.write(str(llave) + ': ' + str(valor) + '\n')

def main():
    #uf20-01.txt
    #uf20-02.txt
    #uf20-03.txt
    
    clausulas,bitStream=leerArchivo()
    f = open('pruebas.txt', 'r+')
    
    f.write('Clausulas Generadas: \n')
    imprimirClausulas(clausulas, f)

    f.write('Bit Stream Generado: ')
    f.write(str(bitStream) + '\n')


    for i in range(0,20*3):
        f.write('Intento numero: [ ' + str(i + 1) + ' ]' + '\n')
        diccionarioDeClausulas = clausulasSatisfechas(bitStream, clausulas)
        f.write("------------------\n")
        clausulasCumplidas, clausulasNoSatisechas = filtrarClausulas(diccionarioDeClausulas)
        f.write('Clausulas satisfechas: \n')
        imprimirClausulas(clausulasCumplidas, f)
        f.write('Clausulas no satisfechas: \n')
        imprimirClausulas(clausulasNoSatisechas, f)
        if i == 10:
            clausulasNoSatisechas = {}
        if(len(clausulasNoSatisechas) == 0):
            f.write('¡Caso resuelto!\n')
            f.write('Bit Stream Final: ' + str(bitStream) + '\n')
            break
        llaveRandom,indiceDeVariable = escogerClausulaNoSatisfecha(clausulasNoSatisechas)
        f.write('Clausula random a cambiar :  ' + str(llaveRandom) + '. Elemento a cambiar: ' + str(indiceDeVariable + 1) + '\n')
        #Modificar variables originales
        bitStreamACambiar = abs(clausulas[llaveRandom][indiceDeVariable])
        f.write('Bit Stream a Cambiar: ' + str(bitStreamACambiar) + ' \t\n')
        f.write('Bit Stream antes de cambio: ' + str(bitStream) + '\t\n')
        if(bitStream[bitStreamACambiar-1] == 1):
            bitStream[bitStreamACambiar-1] = 0
        else:
            bitStream[bitStreamACambiar-1] = 1

        f.write('Bit Stream Modificado:      '  + str(bitStream) + '\n')
    
    f.close()

    


main()
