## NOTA: SE REQUIERE EL ARCHIVO 'nums_para_editar_txt.dat'

# pdf -> txt
pdftotext -layout -raw -q sentencia_ejemplo.PDF salida1.txt

# txt -> txt (párrafos y considerandos marcados)
# args (1) = archivo de origen, (2) = nombre del archivo de destino, (3) ruta del archivo de destino
python2 edit_txt.py salida1.txt salida2.txt ./

