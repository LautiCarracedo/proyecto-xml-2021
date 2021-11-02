from lectura_archivo import leer_archivo
import sys

def rellenar_clase_general_input():
    datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo() #leo el archivo

    try:
        if len(datos_generales) == 2: #siempre espero un len de 2(general.banco y general.fechaRendicion).
            if datos_generales[0][0] == 'general.banco': #si esta posicion es general.banco guardo los datos como corresponden.
                banco = datos_generales[0][1]
                fecha_rendicion = datos_generales[1][1]  

            elif datos_generales[0][0] == 'general.fechaRendicion':
                banco = datos_generales[1][1]
                fecha_rendicion = datos_generales[0][1]
            
            if str(banco).isnumeric():
                if ((len(fecha_rendicion) == 10) and (str(fecha_rendicion[0:2]).isnumeric() and fecha_rendicion[2] == '-' and str(fecha_rendicion[3:5]).isnumeric() and fecha_rendicion[5] == '-' and str(fecha_rendicion[6:10]).isnumeric())):
                    valor = True
                else:
                    valor = False
                    print("Campo general.fechaRendicion debe ser fomato DD-MM-AAAA")
            else:
                valor = False
                print("Campo banco debe ser numerico")

            return banco, fecha_rendicion
        else:
            print("Error de carga en los datos de la cabecera general. CAMPOS A INGRESAR: general.banco y general.fechaRendicion")
    except:
        print("Error al llenar la clase GeneralInput")
        
        
