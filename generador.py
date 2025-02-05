# Importamos del archivo main, el objeto declarado, las funciones dataaframes y crear_pdf, y las tablas usadas en el objeto. 
from main import PDF, dataframes, crear_pdf, TABLE_DATA,TABLE_DATA2,TABLE_DATA3
import os, shutil
from pypdf import PdfWriter

path = "C:/Users/Merel/Downloads/MOVVTA_FMERELES (34).csv"

_dir = 'output'
_subdir = 'output\\merge'
listdir = os.listdir()
path_exe = os.getcwd()
path_output = path_exe + "\\" + _dir
path_merge = path_exe + "\\" + _subdir + '\\'

if _dir not in listdir:
    print ('No en el directorio. Creando carpeta...')
    os.mkdir(_dir)
    os.mkdir(_subdir)
    print ("Creada con exito.")
else:
    print ("Ya existe, reinicializando la carpeta...")
    try:
        shutil.rmtree(_dir)
        os.mkdir(_dir)
        os.mkdir(_subdir)
        print ("Proceso exitoso.")
    except Exception as e:
        print (f'Ha ocurrido el sig. error:{e}')

data,pl = dataframes(path)

for datos in pl:

    planilla = datos[0]

    # EMPEZAMOS FILTRANDO EL DATAFRAME POR EL NUMERO DE PLANILLA  Y SELECCIONAMOS LAS COL. QUE VAMOS A USAR.
    data_filter = data[data['Planilla']==planilla].iloc[:,[2,3,4]]

    # AGRUPAMOS LA DATA POR PRODUCTO Y NOMBRE DE PRODUCTO, USAMOS LA MEDIDA SUM PARA SUMAR CANTIDAD. EN EL CASO DE PREVENTA. 
    data_agrupada = data_filter.groupby(['Producto','Nombre Producto'])[['Cantidad']].sum()

    # AGREGAMOS LAS COLUMNAS DE SUBSTANDAR DE CAJAS, DE UNIDADES Y OBSERVACIONES.
    data_agrupada[['S.STD CJ','S.STD UN.','OBSERVACIONES']] = ""

    # DECLARAMOS LA LISTA DE ENCABEZADOS QUE SE VA A INICIALIZAR CON CARA ITERACION
    other = [['SKU','DESCRIPCION','CANTIDAD','RETORNO','SUBSTD','OBSERVACIONES']]

    # ITERAMOS CON EL DATAFRAME SUMANDO TODOS LOS REGISTROS A LA LISTA INICIALIZADA ANTERIORMENTE.
    for registros in data_agrupada.itertuples():
        other.append([str(registros[0][0]),registros[0][1]] + [str(registros[1])]+list(registros[2:]))

    # EJECUTAMOS, RETORNA ELPDF Y LO GUARDAMOS EN EL OUTPUT EN LOS DIRECTORIOS CREADOS ANTERIORMENTE. 
    pdf = crear_pdf(datos,other)
    pdf.output(f"{path_output}/HOJARUTA{planilla}.pdf")

pl_gen = []




for x in os.listdir(path_output):
    print (path_output + '\\'+ x)
    if os.path.isdir(path_output+'\\'+x):
        print ('Es un dir')
    else:
        pl_gen.append(x)
        print ("No es un dir")

print (f"pl_gen is-> {pl_gen}")
# TODO Ahora sigue iterar sobre el dir pasado reconociendo si es dir o ejecutable e ir agregando las hojas a una lista para mergear todas luego. y guardar todas en una carpeta.

merge = PdfWriter()

for hojas_gen in pl_gen:

    merge.append(f"{path_output}//{hojas_gen}")

merge.write(f"{path_merge}merge.pdf")
merge.close()