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
                    sys.exit()
            else:
                valor = False
                print("Campo general.banco debe ser numerico")
                sys.exit()

            return banco, fecha_rendicion
        else:
            print("Error de carga en los datos de la cabecera general. CAMPOS A INGRESAR: general.banco y general.fechaRendicion")
            sys.exit()
    except:
        print("Error al llenar la clase GeneralInput")
        sys.exit()
        

def transformar_datos_detallepago():
    contador_boletas = 0
    vector_detalle_pago = []
    largo_correspodiente_vector_dp = 0
    datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo() #leo el archivo
    #print(datos_detallepago)
    try:
    #recorro datos_detallepago que viene como [[***detallepago.nroBoleta,xxxxx],[***detallepago.importe,222]]. La idea es generar un vector que solo tenga los valores.
        for datos in datos_detallepago: 
            #print(datos[0], datos[1])
            if datos[0] == '***detallepago.nroBoleta': #datos[0] tiene las "claves", datos[1] el valor.
                contador_boletas += 1
                nro_boleta = datos[1]
                if str(nro_boleta).isnumeric(): #validacion
                    vector_detalle_pago.append(nro_boleta) #guardo en un vector solo los valores, por ej: ['0520823739863094', '12-11-2021', '222.22', '12', '1', '0', '0520250624970392', '12-11-2021', '676.06', '18', '1', '0']
                    #print(f"Boleta nro {contador_boletas}: ", nro_boleta)
                else:
                    print("Campo ***detallepago.nroBoleta debe ser numerico")
                    sys.exit()
                

            if datos[0] == '***detallepago.fechaPago':
                fecha_pago = datos[1]
                if ((len(fecha_pago) == 10) and (str(fecha_pago[0:2]).isnumeric() and fecha_pago[2] == '-' and str(fecha_pago[3:5]).isnumeric() and fecha_pago[5] == '-' and str(fecha_pago[6:10]).isnumeric())):
                    vector_detalle_pago.append(fecha_pago)
                    #print(f"Fecha Pago: ", fecha_pago)
                else:
                    print("Campo ***detallepago.fechaPago debe ser formato DD-MM-AAAA")
                    sys.exit()

            if datos[0] == '***detallepago.importe':
                importe = datos[1]
                if float(importe):
                    vector_detalle_pago.append(importe)
                    #print("Importe: ", importe)
                else:
                    print("Campo ***detallepago.importe debe ser numerico")
                    sys.exit()


            if datos[0] == '***detallepago.cantCuotas':
                cant_cuotas = datos[1]
                if (str(cant_cuotas).isnumeric) and (cant_cuotas >= '0' or cant_cuotas <= '18'):
                    vector_detalle_pago.append(cant_cuotas)
                    #print("Cant cuotas: ", cant_cuotas)
                else:
                    print("Campo ***detallepago.cantCuotas debe estar comprendido entre 1 y 18")
                    sys.exit()

            if datos[0] == '***detallepago.idObjetoImponible':
                id_obj_imponible = datos[1]
                if (str(id_obj_imponible).isnumeric()) and (id_obj_imponible >= '0' or id_obj_imponible <= '18'):
                    vector_detalle_pago.append(id_obj_imponible)
                    #print("Id Obj Imp: ", id_obj_imponible)
                else:
                    print("Campo ***detallepago.idObjetoImponible debe estar comprendido entre 1 y 18")
                    sys.exit()

            if datos[0] == '***detallepago.obligacion':
                obligacion = datos[1]
                if str(obligacion).isnumeric():
                    vector_detalle_pago.append(obligacion)
                    #print("Obligacion: ", obligacion)
                else:
                    print("Campo ***detallepago.obligacion debe ser numerico")
                    sys.exit()
            
        
        #print(datos[0])
        #print("Cant boletas: ", contador_boletas)
        print(vector_detalle_pago)
        #print(nro_boleta)

        largo_correspodiente_vector_dp = len(vector_detalle_pago) % 6 #saco el modulo, de esta forma verifico que siempre sea multiplo de 6 el vector, ya que puede venir 6,12,18, es el formato correcto....
        if largo_correspodiente_vector_dp == 0:
            #print("Correcto")
            return vector_detalle_pago
            
        else:
            print("Revisar los campos ingresados en detalles pagos. Se espera que ingrese 6: ***detallepago.nroBoleta, ***detallepago.fechaPago, ***detallepago.importe, ***detallepago.cantCuotas, ***detallepago.idObjetoImponible y ***detallepago.obligacion")
            sys.exit()


    except:
        print("Error al llenar la clase DetallePagoInput")
        sys.exit()


def transformar_nroboletas_dp():
    #rellenar vector para nro boletas
    vector_dp = transformar_datos_detallepago()
    boletas = []
    fin_vector = len(vector_dp)
    inicio_vector = 0

    while inicio_vector < fin_vector:
        boletas.append(vector_dp[inicio_vector])
        inicio_vector += 6
        if inicio_vector >= fin_vector:
            break
    #print("Boletas: ", boletas)
    return boletas


def transformar_fechaspago_dp():
    #rellenar vector para nro boletas
    vector_dp = transformar_datos_detallepago()
    fechas = []
    fin_vector = len(vector_dp)
    inicio_vector = 1 #posicion en donde se encuentra la fecha, por eso inicio vector = 1

    while inicio_vector < fin_vector:
        fechas.append(vector_dp[inicio_vector])
        inicio_vector += 6
        if inicio_vector >= fin_vector:
            break
    #print("Fechas: ", fechas)
    return fechas


def transformar_importes_dp():
    #rellenar vector para nro boletas
    vector_dp = transformar_datos_detallepago()
    importes = []
    fin_vector = len(vector_dp)
    inicio_vector = 2

    while inicio_vector < fin_vector:
        importes.append(vector_dp[inicio_vector])
        inicio_vector += 6
        if inicio_vector >= fin_vector:
            break
    #print("Importes: ", importes)
    return importes


def transformar_cuotas_dp():
    #rellenar vector para nro boletas
    vector_dp = transformar_datos_detallepago()
    cuotas = []
    fin_vector = len(vector_dp)
    inicio_vector = 3

    while inicio_vector < fin_vector:
        cuotas.append(vector_dp[inicio_vector])
        inicio_vector += 6
        if inicio_vector >= fin_vector:
            break
    #print("Cuotas: ", cuotas)
    return cuotas


def transformar_objimponibles_dp():
    #rellenar vector para nro boletas
    vector_dp = transformar_datos_detallepago()
    obj_imponibles = []
    fin_vector = len(vector_dp)
    inicio_vector = 4

    while inicio_vector < fin_vector:
        obj_imponibles.append(vector_dp[inicio_vector])
        inicio_vector += 6
        if inicio_vector >= fin_vector:
            break
    #print("Obj imponibles: ", obj_imponibles)
    return obj_imponibles


def transformar_obligaciones_dp():
    #rellenar vector para nro boletas
    vector_dp = transformar_datos_detallepago()
    obligaciones = []
    fin_vector = len(vector_dp)
    inicio_vector = 5

    while inicio_vector < fin_vector:
        obligaciones.append(vector_dp[inicio_vector])
        inicio_vector += 6
        if inicio_vector >= fin_vector:
            break
    #print("Obligaciones: ", obligaciones)
    return obligaciones


def rellenar_clase_detallepago_input(): #la idea de esta funcion es recorrer el vector_detalle_pago generado en la funcion rellenar que contiene todos los datos, y generar pequeñas listas que contengan valores de la misma clave. Por ej: si hay 2 boletas, que haya un vector de los nro_boleta, otro vctor con las dos fecha_pago
    nros_boletas = transformar_nroboletas_dp()
    fechas_pago = transformar_fechaspago_dp()
    importes = transformar_importes_dp()
    cant_cuotas = transformar_cuotas_dp()
    obj_imponibles = transformar_objimponibles_dp()
    obligaciones = transformar_obligaciones_dp()

    print(nros_boletas)
    print(fechas_pago)
    print(importes)
    print(cant_cuotas)
    print(obj_imponibles)
    print(obligaciones)

    

    



