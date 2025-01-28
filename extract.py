import gspread.urls
import pandas as pd
# from main import FPDF, crear_pdf, dataframesa
import os,shutil
from pypdf import PdfWriter

_dir = 'output'
_subdir = 'output/merge'
listdir = os.listdir()

# Obtener el working directory del archivo ejecutable. Puede servir cuando el archivo se ejecute de x carpeta.
# Esto permite que no dependa de una variable con la ruta previamente guardada, esto va a generar que
# la salida se cree en cualquier parte de la computadora independientemente de donde se ejecute el archivo. 
  
path = os.getcwd()
print ("listdir = ",listdir)
print ("path = ",path)

if _dir not in listdir:
    print ('No en el directorio')
    os.mkdir(_dir)
    os.mkdir(_subdir)
else:
    if "merge" not in os.listdir(path+'/'+_dir):
        print ('No existe el subdirectorio /merge. Creando...')
        os.mkdir(_subdir)
    # shutil.rmtree(_dir)  -> esta funcion me permite remover recursivamente los archivos del directorio y finalmente el directorio. os.rmdir() solo remueve dir vacios.
    else:
        print("Ya existe la carpeta merge.")

for x in os.listdir(path):
    break
    print (path + '/'+ x)
    if os.path.isdir(path+'/'+x):
        print ('Es un dir')
    if os.access(path + '/' + x,mode=1):
        print ("No es un dir")




files = [x for x in os.listdir(path)]
print ("files is ->", files, os.getcwd())

'''
path = "C:/Users/Merel/Desktop/Python Projects/Proyectos VSC/GeneradorPdf/output"

if 'plmerge.pdf' in os.listdir(path):
    print ('En el directorio')
    os.remove('output/plmerge.pdf')

files = [x for x in os.listdir(path)]

merge = PdfWriter()

for x in files:
    merge.append(path+'/'+x)
    os.remove(path+'/'+x)

merge.write("C:/Users/Merel/Desktop/Python Projects/Proyectos VSC/GeneradorPdf/output/plmerge.pdf")
merge.close()

'''