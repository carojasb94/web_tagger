# -*- coding: utf-8 -*-

""" """

import ipdb; ipdb.set_trace()
import sys
import funciones
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('BASIC')
logging.basicConfig(level=logging.DEBUG)

#logger.setLevel(logging.DEBUG)

try:
	print("INICIO SCRIPT")
	logger.debug("INICIO SCRIPT debug")
	if len(sys.argv) == 4:
			arch = open (sys.argv[1], "r")
			text = arch.readlines()
			arch.close()
			ruta  = sys.argv[3]
			ruta  = ruta

			texto = funciones.acomodaTexto(text, ruta)
			texto = funciones.marcarConsiderandos(texto)
			texto = funciones.limpiarTexto(texto)
			texto = funciones.restaurarNumeros(texto)

			arch = open (sys.argv[2], "w")
			arch.write(texto)
			arch.close()
	else:
		print ("Error al tratar el archivo x")
except Exception as e:
	print("Error al procesar {0}".format(e))

print("HOLA SCRIPT")
if __name__ == '__main__':
	"""
	es un arreglo comienza por cero
	[0] nombre del programa
	[1] ruta del archivo.txt
	[2] nombre del archivo con el que se va a gurardar el documento (ruta)
	[3] ruta del programa
	"""
	pass
	try:
		print("INICIO SCRIPT")
		import ipdb; ipdb.set_trace()
		logger.debug("INICIO SCRIPT debug")
		if len(sys.argv) == 4:
				arch = open (sys.argv[1], "r")
				text = arch.readlines()
				arch.close()
				ruta  = sys.argv[3]
				ruta  = ruta

				texto = funciones.acomodaTexto(text, ruta)
				texto = funciones.marcarConsiderandos(texto)
				texto = funciones.limpiarTexto(texto)
				texto = funciones.restaurarNumeros(texto)

				arch = open (sys.argv[2], "w")
				arch.write(texto)
				arch.close()
		else:
			print ("Error al tratar el archivo x")
	except Exception as e:
		print("Error al procesar {0}".format(e))
