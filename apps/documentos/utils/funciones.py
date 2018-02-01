# -*- coding: utf-8 -*-
import nltk
import re

####################################################################################################
####################################################################################################
""" MARCAR CONSIDERANDOS """
####################################################################################################
####################################################################################################

def buscarSaltoLinea(considerandoTexto, inicioResolutivos):
    while inicioResolutivos > 0:
        if considerandoTexto[inicioResolutivos] == '\n':
            break
        inicioResolutivos -= 1
    return inicioResolutivos


def buscaResolutivosAUX2 (considerandoTexto, inicioResolutivos):
    considerando  = considerandoTexto[:inicioResolutivos]
    resolutivo    = considerandoTexto[inicioResolutivos:]

    considerando += "\n\n%=%FIN_CONSIDERANDOS%=%\n\n"
    resolutivo    = resolutivo.replace("E%=%", "E%=%\n\n")

    return (considerando, resolutivo)


def buscaResolutivosAUX (considerandoTexto, pattern):
    i = len(considerandoTexto)-1 #es un texto en parrafos
    while i > 0:
        inicioResolutivos = considerandoTexto[i].rfind(pattern)

        if inicioResolutivos >= 0:
            break
        i -= 1

    if i < 0:
        #No encontramos nada
        return (considerandoTexto, None)
    else:
        inicioResolutivos = buscarSaltoLinea(considerandoTexto[i], inicioResolutivos) #es mayor a cero

        considerandos     = considerandoTexto[:i]
        resolutivos       = considerandoTexto[i+1:]

        ultimoConsi, primerRes = buscaResolutivosAUX2 (considerandoTexto[i], inicioResolutivos)

        considerandos.append(ultimoConsi)
        resolutivos = [primerRes] + resolutivos

        resolutivos=encadena(resolutivos)

        return (considerandos, resolutivos)


def buscaResolutivos(considerandoTexto):
    #recibe un texto en parrafos
    global textPATTERNS
    import ipdb; ipdb.set_trace()
    inicioResolutivos = -1

    if textPATTERNS:
        pattern   = textPATTERNS[-1]
        if re.search(r"R\W*?E\W*?S\W*?U\W*?E\W*?L\W*?V\W*?E\W*?$", pattern, re.IGNORECASE):
            return buscaResolutivosAUX(considerandoTexto, pattern)

    return (considerandoTexto, None)

def traerConsiderandos(text):
    #recibe un texto en parrafos
    text, resolutivos  = buscaResolutivos(text) #obtenemos solo el texto con considerandos
    considerandos      = []
    considerandoTexto  = ""
    considerandoNumber = 0

    for line in text:
        line = line.split('\n')
        for l in line:
            numero = re.search(r"%\=%\d+%\=%", l) #Buscamos los numeros marcados
            print("")
            if numero:
                number = numero.group() #en otra variable x si se necesita recuperar el texto
                            #al buscar las jurisprudencias
                numero = re.search(r"\d+", number).group()
                numero = int(numero)

                if numero-1 == considerandoNumber:
                    #Si esta en el orden correcto
                    considerandoNumber += 1
                    considerandos.append(considerandoTexto)
                    print("considerando: {0}".format(considerandoTexto))
                    considerandoTexto = "\n\n%%=%%CONSIDERANDO_" + str(numero) + "%%=%%\n\n"
                    print("considerando: {0}".format(considerandoTexto))
                else:
                    considerandoTexto += "\n" + number + "\n"
            else:
                considerandoTexto += l
                print("else: ")
                print("considerandoTexto: "+ considerandoTexto)
                print("l: "+l)

        considerandoTexto += "\n\n"

    considerandos.append(considerandoTexto) #agregamos el texto q quedo al final
    if resolutivos:
        considerandos.append(resolutivos) #tambien agregamos los resolutivos

    return considerandos


def jseparaConsiderando(bloqueTexto, pattern):
    aux         = re.search(pattern, bloqueTexto, re.IGNORECASE)
    aux         = aux.group()
    inicioConsi = bloqueTexto.find(aux) #Buscamos donde inician los considerandos
    inicio   = bloqueTexto[:inicioConsi] + "\n\n" #agregamos saltos de linea
    consider = bloqueTexto[inicioConsi:]
    consider = consider.replace(aux, aux+"\n\n")

    return (inicio, consider)



def marcarConsiderandos (text):
    global textPATTERNS

    if len(textPATTERNS) > 1: #encontramos al menos resultando y considerando
        pattern = textPATTERNS[1]
        newText = ""
        i       = 0
        lim     = len(text)
        while text: #Avanzamos en el texto hasta que encontramos los considerandos
            if re.search(pattern, text[0]):
                #separamos el texto donde inician los considerandos
                inicio, text[0] = separaConsiderando(text[0], pattern)
                newText += inicio # agremos la parte inicial de la linea al texto q estamos creando
                #  para trabajar solo con la parte de los considerandos
                break
            else:
                newText += text[0]
                del text[0]
            i += 1
        considerandos = traerConsiderandos(text) #analizamos el texto faltante
        for c in considerandos:
            newText += c
        return newText
    else:
        return encadena(text)


#######################
#######################
""" ACOMODAR TEXTO """
#######################
#######################

def encadena (text):
    cad = ""
    for line in text:
        cad += line
        cad += "\n"
    return cad

def buscarEncabezados (text):
    inicioPags = []
    nextLines  = []
    repeticion = 0
    next       = 1
    i          = 0
    lim        = len(text)

    while i < lim:
        if re.match("^\x0c.*\n$", text[i]):
            if text[i] in inicioPags: #DOCUMENTAR (funciona, elimina encabezados de varias lineas)
                repeticion += 1
                if i+next < lim:
                    if text[i+next] in nextLines:
                        next += 1
                    else:
                        del nextLines[next-1]
                    nextLines.append(text[i+next])

            else:
                inicioPags.append(text[i])
                if i+next < lim:
                    nextLines.append(text[i+next])

        if len(inicioPags) > 4: #si hay mas de 4 incio de páginas, no son encabezados
            return []

        elif repeticion > 5:    #si el encabezado si se repite + de 5 veces
            if len(inicioPags) > 1:
                # si hay mas de un encabezado, no consideramos el primero
                return inicioPags[1:] + nextLines[:-1]
            else: # si sólo hay uno lo regresamos
                return inicioPags + nextLines[:-1]

        i += 1

    return []


def ersteAcomodaTexto (text):
    # primero eliminamos numeros de pagina y ecabezados
    newtext    = []
    ecabezados = buscarEncabezados(text)


    i   = 0
    lim = len(text)
    while i < lim:
        if re.match("^\W*?\d+\W*?\n$", text[i]): # Si encontramos una linea q solo tiene un numero
            if i+1 == lim: 	# y si hemos llegado a la ultima linea
                break

            if (i+2<lim) and text[i] == text[i+1] and (text[i+2].find("\x0c")>=0):
                # Para solucionar el error de numeros de pag repetidos:
                    # si en las 2 ultimas lineas son iguales
                    # y la siguiente linea contine un salto de página
                    # avanzamos 1 para q la función no cambie
                i += 1
                continue

            nextLine = re.match("^\x0c.*\n$", text[i+1])
            if nextLine:    # y si la siguiente linea tiene un salto de pagina
                nextLine = nextLine.group(0)
                if nextLine in ecabezados: # y si la siguiente linea es un encabezado
                    i += 2 # saltamos el num de pag y el encabezado
                    continue

                else:			   # y si la siguiente linea NO es un encabezado

                    # reemplazamos el salto de pagina
                    text[i+1] = text[i+1].replace("\x0c", "")
                    i += 1 # saltamos el num de pag
                    continue

            else:
                if re.match("^\x0c", text[i]):
                    # y esta linea tiene un salto de pagina
                    i += 1
                    continue

                #else
                #si siguiente linea NO tiene un salto de pagina
                #y esta linea tampoco tiene un salto de pagina
                newtext.append(text[i])

        elif text[i] in ecabezados: # encontramos un encabezado
            if (i+1<lim) and (re.match("^\W*?\d+\W*?\n$", text[i+1])):
                # y la linea siguiente es solo un numero
                i += 2
                continue
            #else
            i += 1
            continue

        elif re.match("^\x0c.*\n$", text[i]):
            # la linea tiene un salto de pagina (sin encabezado)
            text[i] = text[i].replace("\x0c", "") #Reemplazamos el salto
            newtext.append(text[i])

        else:	# se trata de una linea de texto
            newtext.append(text[i])

        i += 1


    return newtext


patterns = [r"R\W*?E\W*?S\W*?U\W*?L\W*?T\W*?A\W*?N\W*?D\W*?O\W*?\n$",
            r"C\W*?O\W*?N\W*?S\W*?I\W*?D\W*?E\W*?R\W*?A\W*?N\W*?D\W*?O\W*?\n$",
            r"R\W*?E\W*?S\W*?U\W*?E\W*?L\W*?V\W*?E\W*?\n$"]

textPATTERNS     = [] #VARIABLE GLOBAL PARA UBICAR 'RESULTANDO... CONSIDERANDO... RESUELVE'
dicc_textREPLACE = {} #{(NUMERO NUEVO ex. %=%1%=%, <TARGET TEXT>) : NUMERO ORIGINAL ex. PRIMERO}

def findImpirtantThings(line):
    global patterns

    if (len(patterns)>1) and (re.search(patterns[0], line, re.IGNORECASE)):
        import ipdb; ipdb.set_trace()
        aux = re.search(patterns[0], line, re.IGNORECASE)
        del patterns[0]
        return aux

    elif re.search(patterns[0], line, re.IGNORECASE):
        import ipdb; ipdb.set_trace()
        aux = re.search(patterns[0], line, re.IGNORECASE)
        return aux
    else:
        return None



def isImportantLine(line):
    global textPATTERNS
    aux = findImpirtantThings(line)
    if aux:
        aux  = aux.group()       #ENCONTRADO: 'R E S U L T A N D O'
        xua  = specialStrip(aux) #MODIFICADO: 'RESULTANDO'

        line = line.replace(aux, "\n\n%=%"+xua+"%=%\n\n")
        textPATTERNS.append("%=%"+xua+"%=%")
        return line
    else:
        return line

def isImportantLineII(diccNums, line):
    global textREPLACE
    if len(line)>0 and diccNums.has_key(line[0].lower()):
        finDeNumero, numero = buscaNumero(line, 0, len(line),  diccNums[line[0].lower()]) # info en  buscaNumero
        if numero:
                                                  # 'QUINTO. Estudio de fondo...'
            textOri = line[:finDeNumero]	      # 'QUINTO. '
            textNew = "\n\n" + numero + "\n\n"    # '   %=%5%=%   '
            lineEND = line[finDeNumero:]	      # 'Estudio de fondo...'
            line    = textNew + lineEND       	  # '   %=%5%=%   Estudio de fondo...'

            # diccionario textREPLACE
            key                   = (textNew, lineEND)
            dicc_textREPLACE[key] = textOri



    return line

def zweiteAcomodaTexto(text, ruta):
    #  acomodamos las lineas en parrafos
    #  identificamos partes de la sentencia
    #  y buscamos primero, segundo...

    diccNums  = importarNumeros(ruta)
    parrafos  = []
    parrafo   = ""

    for line in text:
        line = isImportantLine(line)

        if re.search(r".*[.:]\n$", line): #la linea termina con punto o dos puntos
            line = line.strip()
            line = isImportantLineII(diccNums, line)
            parrafo += line
            parrafo += "\n"
            parrafos.append(parrafo)
            parrafo = ""


        else:
            line = line.strip()
            line = isImportantLineII(diccNums, line)
            line += " "
            parrafo += line


    parrafos.append(parrafo)

    return parrafos




def acomodaTexto (text, ruta):
    # se recibe un .txt con documento.readlines()

    # primero eliminamos numeros de pagina y ecabezados
    text = ersteAcomodaTexto(text)
    # despues acomodamos las lineas en parrafos
    #	  identificamos partes de la sentencia
    #	  y buscamos primero, segundo...


    text = zweiteAcomodaTexto(text, ruta)


    return text

def specialStrip(aux) :
    cad = ""
    for letra in aux:
        if re.match("\w", letra):
            cad += letra
    return cad


#########################################################################################
#########################################################################################
""" DICCIONARIO de numeros """
#########################################################################################
#########################################################################################


def importarNumeros (ruta):
    ruta   += "/nums_para_editar_txt.dat"
    numeros = {}
    archivo = open(ruta, "U")
    for num in archivo:
        num = num.replace('\n', '')
        num = num.split("#@%")
        diccionariza(numeros, num[1], num[0])
    archivo.close()
    return numeros


def diccionariza (diccionario, identificador, lista):
    if len(lista) == 1:
        diccionario[lista[0]]={}
        diccionario[lista[0]]["<<fin>>"]="%=%"+identificador+"%=%"
        return

    elif re.match("\W", lista[0]):
        #omitimos los simbolos
        diccionariza(diccionario, identificador, lista[1:])

    elif diccionario.has_key(lista[0]):
        diccionariza(diccionario[lista[0]], identificador, lista[1:])
    else:
        diccionario[lista[0]]={}
        diccionariza(diccionario[lista[0]], identificador, lista[1:])




#argumentos:
        #Texto original "es una cadena de una linea \n"
        #posciónes que se ha avanzado
        #tamaño total de la cadena
        #recorrido en el diccionario, cadena que hasta ese momento se ha encontrado

def buscaNumero(texto, i, tam,  diccionario):
    i = i+1
    if i < tam:
        if re.match("\w", texto[i]): #si se trata de un caracter
            if diccionario.has_key(texto[i].lower()): #si esta en el diccionario
                return buscaNumero(texto, i, tam,  diccionario[texto[i].lower()])

            elif diccionario.has_key("<<fin>>"): #si ya no hay coincidencias
                                                  #y hemos encotrado un numero
                return (i, diccionario["<<fin>>"])

            else:
                return (None, None)


        else: # no consideramos los simbolos
            return buscaNumero(texto, i, tam,  diccionario)

    else:
        # se terminó el texto
        if diccionario.has_key("<<fin>>"):
            return (i, diccionario["<<fin>>"])
        else:
            return (None, None)



####################################################################################################
####################################################################################################
""" FUNCIONES PARA LIMPIAR ARCHIVO """
####################################################################################################
####################################################################################################

# Sustituye todas las ocurrencias del <patron> por <sustit> en <line>
def cambiarCadena(line, patron, sustit=''):  #<line>, <patrón>, <lo que sustituye al patrón (por omisión '')>
    trash = re.findall(patron, line)

    for t in trash:
        line = line.replace(t, sustit, 1)

    return line

def juntarAsteris(line):
    trash = re.search(r"\*\s+?\*", line)

    while trash:
        trash = trash.group()
        line  = line.replace(trash, "**")
        trash = re.search(r"\*\s+?\*", line)

    return line


def limpiarTexto(texto):
    cadena = ""
    texto  = texto.split('\n')

    for line in texto:
        line = line.strip()
        line = line.lstrip('.')
        line = line.lstrip('-')
        line = line.lstrip(',')
        line = line.lstrip(':')

        if line == "":
            continue


        #&#\d*?; quita las etiquetas del html ejemplo: &#160;
        line = cambiarCadena(line, r"&#\d*?;", ' ') #<line>, <patrón>, <lo que sustituye al patrón OPCIONAL>

        #&..;" cambia las etiquetas del html ejemplo: <(&lt;) > (&gt;)
        line = cambiarCadena(line, r"&..;", "--")


        if re.match(r".*[.:]$", line): #se agregan los saltos de linea
            line = eliminasimbolos(line)
            line = line.strip()
            line+='\n\n'

        elif re.match(r".*%=%\W?$", line): #se agregan espacios y saltos de de linea
            if re.match(r"^%%?=%%?.*%%?=%%?\W?$", line):
                line = "\n\n" + line + "\n\n"
            else:
                line = eliminasimbolos(line)
                line = line.strip()
                line+='\n\n'

        else:
            line = eliminasimbolos(line)
            line = line.strip()

        line = cambiarCadena(line, r" {2,}", ' ') #elimina los espacios que estén juntos
        line = juntarAsteris(line)                #junta asteriscos separados
        line = cambiarCadena(line, r"\*{2,}", '****') #elimina los asteriscos de mas
        cadena += line

    return cadena






####################################################################################################
####################################################################################################
""" FUNCIÓN PARA ELMINAR SIMBOLOS """
####################################################################################################
####################################################################################################

chars1 = [':', ',', ';', '.', '!', '?', '<', '>', '+', '%', '$', ' ', 
      '/', '=', '@', '*', '(', ')', '[', ']', '{', '}', '-']

chars2 = [ '\xc3\xb1', '\xc3\x91', '\xc3\xa1', '\xc3\xa9', '\xc3\xad', #acentos
           '\xc3\xb3', '\xc3\xba', '\xc3\x81', '\xc3\x89', '\xc3\x8d',
           '\xc3\x93', '\xc3\x9a', '\xc3\xbc', '\xc3\x9c']

chars3 = ['\xe2\x80\x9c', '\xe2\x80\x9d', '\xe2\x80\x99'] #comillas


charsTOreplace = {'\xc2\xa1': " -! ", '\xc2\xbf': " -? ", '\xc2\x91': ' " '} 

simbolox = ['\xc2', '\xc3', '\xe2'] #inicio de simbolos



#permitimos -> :,;.!?<>+%$/=@*()[]{}- <-
def eliminasimbolos (linea):
                    #Elimina todos los simbolos extraños
                    #Los necesarios los deja o los pone en formato utf 8
                    #no distinguimos entre comillas q abren y cierran

    global chars1, chars2, chars3, charsTOreplace, simbolox

    limite=len(linea)
    actual=""
    i=0

    while i<limite:
        if linea[i] in chars1: #si es alguno de estos -> :,;.!?<>+%$/=@*()[]{}- <-
            actual += ' ' + linea[i] + ' '
            i += 1


        elif linea[i] in simbolox: #si es el inicio de algun otro simbolo permitido
            if i+1 < limite:
                aux = linea[i]+linea[i+1] #juntamos los caracteres i e i+1

                if aux in chars2:       #si es un acento
                    actual += linea[i] + linea[i+1]
                    i += 2

                elif charsTOreplace.has_key(aux): #si es -> ¡¿" <-
                    actual +=  charsTOreplace[aux]
                    i += 2

                elif i+2 < limite:
                    aux += linea[i+2] #juntamos en total i, i+1 e i+2

                    if aux in chars3:  #si es alguna  comilla
                        actual += ' " '
                        i += 3
                    else:
                        i += 1
                else:
                    i += 1
            else:
                i += 1



        #letras
        else:
            #si tenemos letras pegadas a números como "pertenecen7" las separamos
            valorAscii = ord(linea[i])

            #es un número 0=48, 9=57
            if 47 < valorAscii and valorAscii < 58:
                if i+1 < limite:
                    # si el siguiente caracter es un número
                    valorAscii = ord(linea[i+1])
                    if 47 < valorAscii and valorAscii < 58:
                        actual += linea[i]
                        i += 1

                    # si el siguiente caracter NO es un número
                    else:
                        # agregamos un espacio
                        actual +=  linea[i] + ' '
                        i += 1

                #se acabo la cadena
                else:
                    actual += linea[i]
                    i += 1



            #es una letra #A=65, Z=90, a=97, z=122
            elif (64 < valorAscii and valorAscii < 91) or (96 < valorAscii and valorAscii < 123):
                if i+1 < limite:
                    # si el siguiente caracter es una letra
                    valorAscii = ord(linea[i+1])
                    if (64 < valorAscii and valorAscii < 91) or (96 < valorAscii and valorAscii < 123):
                        actual += linea[i]
                        i += 1

                    # si el siguiente caracter es el inicio de algun otro simbolo permitido (ex. acento...)
                    elif linea[i+1] in simbolox:
                        actual += linea[i]
                        i += 1

                    # si el siguiente caracter NO es una letra NI  un simbolo permitido (ex. acento...)
                    else:
                        # agregamos un espacio
                        actual +=  linea[i] + ' '
                        i += 1

                #se acabo la cadena
                else:
                    actual += linea[i]
                    i += 1


            # EL CARACTER NO ES NI UN NÚMERO NI UNA LETRA NI UN SIMBOLO PERMITIDO
            else:
                i+=1



    return actual


#######################################
#### FUNCIÓN PARA RESTAURAR NÚMEROS ###
#######################################
def restaurarNumeros(texto):
    global dicc_textREPLACE
    for k, textOri in dicc_textREPLACE.items():
        textNew, lineEND = k

        lineEND       = limpiarTexto(lineEND)
        textToRestore = textNew + lineEND

        # si el texto no fue modificado -> restauramos
        if texto.find(textToRestore) >= 0:
            textOri = ' ' + limpiarTexto(textOri) + ' ' + lineEND
            texto   = texto.replace(textToRestore, textOri)

    return texto