from lectura_archivo import leer_archivo
import sys

def rellenar_clase_general_input():
    datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo() #leo el archivo

    try:
        if len(datos_generales) == 2: #siempre espero un len de 2(general.banco y general.fechaRendicion).
            if datos_generales[0][0] == 'general.banco': #si esta posicion es general.banco guardo los datos como corresponden.
                banco = datos_generales[0][1]
                fecha_rendicion = datos_generales[1][1]
                if banco.isnumeric(): #aca faltaria una expresion regular que evalue como ingresan la fecha
                    valor = True
                else:
                    valor = False
                    print("Campo banco debe ser numerico")
                    sys.exit()

            elif datos_generales[0][0] == 'general.fechaRendicion':
                banco = datos_generales[1][1]
                fecha_rendicion = datos_generales[0][1]
                if banco.isnumeric(): #aca faltaria una expresion regular que evalue como ingresan la fecha
                    valor = True
                else:
                    valor = False
                    print("Campo banco debe ser numerico")
                    sys.exit()

            return banco, fecha_rendicion
        else:
            print("Error de carga en los datos de la cabecera general. CAMPOS A INGRESAR: general.banco y general.fechaRendicion")
    except:
        print("ERROR AL LLENAR LA CLASE GENERAL INPUT")
        
        
