# Importamos del archivo main, el objeto declarado, las funciones dataaframes y crear_pdf, y las tablas usadas en el objeto. 
from main import PDF, dataframes, crear_pdf, TABLE_DATA,TABLE_DATA2,TABLE_DATA3
import os, shutil

path = "C:/Users/Merel/Downloads/MOVVTA_FMERELES (33).csv"

_dir = 'output'
_subdir = 'output/merge'
listdir = os.listdir()
path_ejecutable = os.getcwd()

if _dir not in listdir:
    print ('No en el directorio')
    os.mkdir(_dir)
    os.mkdir(_subdir)
else:
    print ("Ya existe, reinicializando la carpeta.")
    try:
        shutil.rmtree(_dir)
        os.mkdir(_dir)
        os.mkdir(_subdir)
    except Exception as e:
        print (f'Ha ocurrido el sig. error:{e}')

data,pl = dataframes(path)

contador = 0

for datos in pl:
    contador +=1
    if contador == 3:
        break

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

    # EJECUTAMOS, RETORNA ELPDF Y LO GUARDAMOS EN EL OUTPUT EN LOS DIRECTORIOS CREADOS ANTERIORMENTE. 
    pdf = crear_pdf(datos,other)
    try:
        pdf.output(f"{path_ejecutable}/{_dir}/HOJARUTA{planilla}.pdf")
#TODO: Hacer que cree la carpeta y de la salida nuevamente. En el directorio de donde sea que se ejecute el comando. 
    except FileNotFoundError:
        print ("Carpeta de salida no encontrada. Creando dir usando libreria os.")
        os.mkdir("output")


for x in os.listdir(path_ejecutable):
    print (path_ejecutable + '/'+ x)
    if os.path.isdir(path_ejecutable+'/'+x):
        print ('Es un dir')
    if os.access(path_ejecutable + '/' + x,mode=2):
        print ("No es un dir")