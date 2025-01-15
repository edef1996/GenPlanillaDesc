import gspread.urls
import pandas as pd
# from main import FPDF, crear_pdf, dataframesa
import os,sys

x = sys.argv

for y in x:
    _b = y.split("/")
    sub_list = _b[:-1]
    _sub = print (*sub_list,'output',sep="/")
    os.rmdir(str(_sub))


