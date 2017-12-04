# -*- coding: utf-8 -*-

import os
import subprocess
from django.core.management.base import BaseCommand, CommandError
from apps.documentos.models import Anotacion
import json

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
    #    parser.add_argument('archivo', required=False, default=False)

    def handle(self, *args, **options):
        print(args)
        print(options)
        #if options['archivo']:
        #    print(options['archivo'])
        anotaciones = Anotacion.objects.all()
        #print(anotaciones)
        print(os.getcwd())
        root_path = os.getcwd()
        for anotacion in anotaciones:
            print(anotacion)
            #INVOCAMOS EL COMANDO PARA GENERAR EL TEXTO PLANO DE UN ARCHIVO PDF
            #pdftotext -layout -raw -q documentos texto.txt
            #import ipdb; ipdb.set_trace()
            filepath = anotacion.get_url_file()
            filepath_prov = "{0}.prov".format(filepath.split('/')[-1])

            command = ["pdftotext", "-layout", "-raw", "-q",
                       root_path + filepath,
                       filepath_prov
                       ]
            print(" ".join(command))
            proceso = subprocess.Popen(command, stdout=subprocess.PIPE)
            exit_code = proceso.wait()
            print(exit_code)
            #pdftotext -layout -raw -nopgbrk -q /home/thrasher/PycharmProjects/web_tagger/media/documentos/sentencia_ejemplo.PDF a.demo
            _file = open(os.path.join(root_path, filepath_prov))
            all_lines = list()
            all_words = list()
            dict_words = dict()
            import ipdb; ipdb.set_trace()
            i=0
            for line in _file.readlines():
                #Abrir el nuevo archivo generado
                #Limpiando los caracteres raros y lineas vacias
                prov_line = line.replace('\xef\x81\xa1', '').replace('\n','').replace('\xef\x82\xb7','')
                print(prov_line)
                if prov_line:
                    all_lines.append(prov_line)
                    all_words += prov_line.split(' ')

                    #Agregando prov_line
                    for word in prov_line.split(' '):
                        dict_words[i] = word
                        i+=1

                continue



            #print(all_words)
            print("TOTAL DE LINEAS: ")
            print(len(all_lines))
            print("TOTAL DE PALABRAS: ")
            print(len(all_words))
            print("TOTAL Longitud texto(array): ")
            print(len(str(all_words)))


            print("TOTAL PALABRAS(dict): ")
            print(len(dict_words))
            print("LEN PALABRAS(dict): ")
            print(len(str(dict_words)))


            #print(prov_line)
            #print(type(anotacion.get_texto()))
            #print(type(list(anotacion.get_texto())))
            #import ipdb; ipdb.set_trace()
            #print(str(anotacion.get_texto()))
            #print(len(anotacion.get_texto()))
            #print(list(anotacion.get_texto()))

            #anotacion.set_texto(json.dumps(['ESTO','es','una','lista','de','palabras','alv',':v']))
            anotacion.set_texto(json.dumps(all_words))
            anotacion.save_documento()

            #LINEAS  DE TEST PARA POPEN
            #proceso = subprocess.Popen(["echo", "This_is_a_testing"], stdout=subprocess.PIPE)
            #proceso2 = subprocess.Popen(["grep", "-c", "test"], stdin=p1.stdout, stdout=subprocess.PIPE)

        try:
            self.stdout.write(self.style.SUCCESS('Comando custom by "%s"' % 'METALLICA GREEN'))
        except Exception as e:
            raise CommandError('Error " %s " ' % str(e))

        #self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))