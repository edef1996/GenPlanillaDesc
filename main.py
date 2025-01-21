from fpdf import FPDF
import pandas as pd
from fpdf.enums import TableSpan
from fpdf.fonts import FontFace
from pypdf import PdfMerger
import os,sys

class PDF(FPDF):
    
    def __init__(self, orientation = "portrait", unit = "mm", format = "A4", font_cache_dir = "DEPRECATED", n_pla: str = 'None', canal_vta : str = 'None', fecha_emi : str = 'None' ):
        super().__init__(orientation, unit, format, font_cache_dir)
        self.n_pla: str = n_pla
        self.canal_vta : str = canal_vta
        self.fecha_emi : str = fecha_emi
    
    def header(self):
        self.image("C:/Users/Merel/Desktop/Python Projects/Proyectos VSC/GeneradorPdf/CCU_LOGO.png",x=2,y=2,w=15,h=6)
        # FUENTE  DEL TITULO
        self.set_font("helvetica", "B", 11)
        # Printing title:
        self.cell(w=0,
                  h=7,
                  text="PLANILLA DE DESCARGA: RECHAZOS Y DEVOLUCIONES",
                  border='BT',
                  align='C',fill=False)
        self.ln(10)
        self.set_font("helvetica", "i", 8)
        self.cell(w=30, h=6,text="PLANILLA N:",border='BTL', align="R")
        self.cell(w=25, h=6, text= str(self.n_pla), border='BTR', align="L")
        self.cell(w=30, h=6, text="CANAL DE VENTA:",border='BTL', align="R")
        self.cell(w=40, h=6, text=self.canal_vta,border='BTR', align="L")
        self.cell(w=40, h=6, text="FECHA DE EMISION:",border='BTL', align="R")
        self.cell(w=0,  h=6, text=str(self.fecha_emi),border='BTR', align="L")
        self.ln(10)
    
    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

# TABLAS PARA AGREGAR AL PRINCIPIO Y AL FINAL DEL PDF
TABLE_DATA = [
    ["OP. LOGISTICO:","TB","LOGISTICA DEL INT.","RECARGA: [ ] "],
    ["PATENTE:",                           "",TableSpan.COL,TableSpan.COL],
    ["CHOFER:",                           "",TableSpan.COL,TableSpan.COL],]

TABLE_DATA2 = [
    ["ENVASES Y PALETAS",TableSpan.COL,TableSpan.COL,TableSpan.COL],
    ["CODIGO:", "DESCRIPCION","CANTIDAD","OBSERVACIONES"],
    ["14058","PALETAS PERIMETRALES","", ""],
    ["16105","BOT. PROPIETARIA 1000 RET X12","", ""],
    ["14501","CANASTO PLASTICO 1/1","", ""],
    ["16110","BOTELLA PROPIETARIA 1000 RET X1","",  ""],
    ["14103","BARRIL x 30lts","",""],
    ["14104","BARRIL x 50lts","",""],
    ["","BARRIL x 15lts","",""]]

TABLE_DATA3 = [
    ["CONTROLO ->","GUARDIA SEGURIDAD","SUPERVISOR","CHOFER"],
    ["FIRMA",                          "","",""],
    ["ACLARACION",                           TableSpan.ROW,TableSpan.ROW,TableSpan.ROW]
    ]

# PATH DE DIRECCION DONDE APUNTA EL ARCHIVO. 
path = "C:/Users/Merel/Downloads/MOVVTA_FMERELES (33).csv"

# GENERACION DE LOS DATAFRAMES
def dataframes (path: str) -> pd.DataFrame:
    
    df = pd.DataFrame(pd.read_csv(path, encoding='UTF-8',skiprows=3, delimiter=';'))
    planillas = df[['Planilla','Canal de venta','Fecha de Emision']].drop_duplicates().values.tolist()
    data = df.iloc[:,[20,43,44,45,50]]
    return data, planillas

# FUNCION PARA CREAR LOS PDFS. (ENCABEZADOS, CON LAS TABLAS PARA LOS DATOS.)
def crear_pdf(planilla: list, data: list) -> PDF:

    pdf = PDF (n_pla=planilla[0],canal_vta=planilla[1],fecha_emi=planilla[2])
    pdf.add_page()
    pdf.set_font("helvetica", "I", 7)
    test_color = (150,150,150)

    firtsheadings_style = FontFace(family='Times',fill_color=test_color, color=(2,2,2),emphasis='B')

    headings_style = FontFace(family='Times',fill_color=test_color, color=(2,2,2),emphasis='B')

    with pdf.table(TABLE_DATA, text_align="CENTER",headings_style=firtsheadings_style, cell_fill_color=(230,230,230),cell_fill_mode='ALL'):
        pass
    pdf.ln(3)

    with pdf.table(TABLE_DATA2, text_align="CENTER", col_widths=(10,27,10,30), num_heading_rows=2, headings_style=headings_style):
        pass

    with pdf.table(data,text_align="CENTER",col_widths=(5,30,6,6,6.5,20),headings_style=headings_style):
        pass
    pdf.ln(3)  

    with pdf.table(TABLE_DATA3, text_align="CENTER",headings_style=headings_style, cell_fill_color=(230,230,230),cell_fill_mode='ALL'):
        pass 

    return pdf

data,pl = dataframes(path)

merger = PdfMerger()

for datos in pl:
    planilla = datos[0]

    # EMPEZAMOS FILTRANDO EL DATAFRAME POR EL NUMERO DE PLANILLA  Y SELECCIONAMOS LAS COL. QUE VAMOS A USAR.
    data_filter = data[data['Planilla']==planilla].iloc[:,[2,3,4]]

    # AGRUPAMOS LA DATA POR PRODUCTO Y NOMBRE DE PRODUCTO, USAMOS LA MEDIDA SUM PARA SUMAR CANTIDAD. EN EL CASO DE PREVENTA. 
    data_agrupada = data_filter.groupby(['Producto','Nombre Producto'])[['Cantidad']].sum()

    # AGREGAMOS LAS COLUMNAS DE SUBSTANDAR DE CAJAS, DE UNIDADES Y OBSERVACIONES.
    data_agrupada[['S.STD CJ','S.STD UN.','OBSERVACIONES']] = ""

    # DECLARAMOS LA LISTA DE ENCABEZADOS QUE SE VA A INICIALIZAR CON CARA ITERACION
    other = [['SKU','DESCRIPCION','Cantidad','S.STD CJ','S.STD UN.','OBSERVACIONES']]

    # ITERAMOS CON EL DATAFRAME SUMANDO TODOS LOS REGISTROS A LA LISTA INICIALIZADA ANTERIORMENTE.
    for registros in data_agrupada.itertuples():
        other.append([str(registros[0][0]),registros[0][1]] + [str(registros[1])]+list(registros[2:]))

    # EJECUTAMOS, RETORNA ELPDF Y LO GUARDAMOS EN EL OUTPUT PASADO. 
    pdf = crear_pdf(datos,other)
    try:
        pdf.output(f"C:/Users/Merel/Desktop/Python Projects/Proyectos VSC/GeneradorPdf/output/hoja{planilla}.pdf")
#TODO: Hacer que cree la carpeta y de la salida nuevamente. En el directorio de donde sea que se ejecute el comando. 
    except FileNotFoundError:
        print ("Carpeta de salida no encontrada. Creando dir usando libreria os.")
        os.mkdir("output")


print ('@hola')
# TODO: Queda pendiente una vez que generamos todos los pdfs en la salida, iterar con todos y mergear en un solo pdf. 