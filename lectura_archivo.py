import sys

def leer_archivo():
    vector_datos_general = []
    vector_datos_sucursal = []
    vector_datos_pagos = []
    vector_datos_detallepagos = []

    try:
        with open("C:/Users/Lauti/Desktop/generador_prueba/txt_prueba.txt","r") as archivo:
            for lineas in archivo.readlines():
                if lineas.split():
                    while 'general' in lineas:
                        datos_general = lineas.strip().split(' = ')
                        #print(datos_general)
                        vector_datos_general.append(datos_general)
                        if lineas != 'general':
                            break
                        
                    while 'sucursal' in lineas:
                        datos_sucursal = lineas.strip().split(' = ')
                        vector_datos_sucursal.append(datos_sucursal)
                        if lineas != 'sucursal':
                            break
                        
                    while 'pagos' in lineas:
                        datos_pagos = lineas.strip().split(' = ')
                        vector_datos_pagos.append(datos_pagos)
                        if lineas != 'pagos':
                            break
                    while 'detallepago' in lineas:
                        datos_detalles = lineas.strip().split(' = ')
                        vector_datos_detallepagos.append(datos_detalles)
                        if lineas != 'detallepago':
                            break

            return vector_datos_general, vector_datos_sucursal, vector_datos_pagos, vector_datos_detallepagos

    except IOError:
        print("ERROR DE LECTURA DE ARCHIVO")
        sys.exit()
    
    except:
        print("ERROR")
        sys.exit()