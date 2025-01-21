import gspread.urls
import pandas as pd
# from main import FPDF, crear_pdf, dataframesa
import os,sys
from pypdf import PdfWriter

_dir = 'output'
_subdir = 'output/files'
listdir = os.listdir()

if _dir not in listdir:
    print ('No en el directorio')
    os.mkdir(_dir)
    os.mkdir(_subdir)
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