from os import replace
from lectura_archivo import leer_archivo
import sys
import time

def det_sistema_origen():
    claves_generales, datos_generales, clave_valor_general, claves_detallepago, datos_detallepago, clave_valor_detallepago, clave_origen, dato_origen, clave_valor_origen = leer_archivo() #leo el archivo
    #print(dato_origen)
    #print(clave_origen)
    try:
        if clave_origen[0] == 'origen':
            if dato_origen[0] == 'PSRM' or dato_origen[0] == 'psrm' or dato_origen[0] == 'OTAX' or dato_origen[0] == 'otax' or dato_origen[0] == 'GANT' or dato_origen[0] == 'gant':
                origen = dato_origen
                return origen
            else:
                input("No existe el sistema origen")
                sys.exit()
        else:
            input("Se espera que ingrese el sistema origen en la primera linea de la siguiente forma: origen = valor")
            sys.exit()

    except(AttributeError, IndexError, TypeError, SystemError):
        input("Error al leer el sistema origen")
        sys.exit()

def rellenar_clase_general_input():
    claves_generales, datos_generales, clave_valor_general, claves_detallepago, datos_detallepago, clave_valor_detallepago, clave_origen, dato_origen, clave_valor_origen = leer_archivo() #leo el archivo

    try:
        if len(claves_generales) == 2: #siempre espero un len de 2(general.banco y general.fechaRendicion).
            if claves_generales[0] == 'general.banco': #si esta posicion es general.banco guardo los datos como corresponden.
                banco = datos_generales[0]
                fecha_rendicion = datos_generales[1] 
                fecha_rendicion_sin_barra = fecha_rendicion.replace('/','-') #si viene con barra (/) se cambia a guion(-)

            elif claves_generales[0] == 'general.fechaRendicion':
                banco = datos_generales[1]
                fecha_rendicion = datos_generales[0]
                fecha_rendicion_sin_barra = fecha_rendicion.replace('/','-') #si viene con barra (/) se cambia a guion(-)
            
            if str(banco).isnumeric():
                if ((len(fecha_rendicion_sin_barra) == 10) and (str(fecha_rendicion_sin_barra[0:4]).isnumeric()) and (fecha_rendicion_sin_barra[4] == '-') and (str(fecha_rendicion_sin_barra[5:7]).isnumeric()) and (fecha_rendicion_sin_barra[7] == '-') and (str(fecha_rendicion_sin_barra[8:10]).isnumeric())):
                    valor = True
                else:
                    valor = False
                    input("Campo general.fechaRendicion debe ser fomato AAAA-MM-DD. Presione enter para continuar")
                    #time.sleep(4)
                    sys.exit()
            else:
                valor = False
                input("Campo general.banco debe ser numerico. Presione enter para continuar")
                #time.sleep(4)
                sys.exit()
            #print(banco, fecha_rendicion)
            return banco, fecha_rendicion_sin_barra
        else:
            input("Error de carga en los datos de la cabecera general. CAMPOS A INGRESAR: general.banco y general.fechaRendicion. Presione enter para continuar")
            #time.sleep(6)
            sys.exit()
    except:
        input("Error al llenar la clase GeneralInput. Enter para salir")
        #time.sleep(2)
        sys.exit()
        


def verificar_orden_dp():
    try:
        claves_generales, datos_generales, clave_valor_general, claves_detallepago, datos_detallepago, clave_valor_detallepago, clave_origen, dato_origen, clave_valor_origen = leer_archivo() #leo el archivo
        inicio_vector = 0
        fin_vector = len(claves_detallepago)
        bandera_ok_orden = False
        while inicio_vector < fin_vector:
            if claves_detallepago[inicio_vector] == '***detallepago.nroBoleta' and claves_detallepago[inicio_vector+1] == '***detallepago.fechaPago' and claves_detallepago[inicio_vector+2] == '***detallepago.importe' and claves_detallepago[inicio_vector+3] == '***detallepago.cantCuotas' and claves_detallepago[inicio_vector+4] == '***detallepago.cuotaActual':
                orden = ('El orden cargado de los detalles de pagos esta bien.')
                #print(orden)
                bandera_ok_orden = True
            else:
                orden = input('El orden cargado de los detalles de pagos esta mal o falta algun campo a cargar. Se espera que ingrese ***detallepago.nroBoleta = valor, ***detallepago.fechaPago = valor, ***detallepago.importe = valor, ***detallepago.cantCuotas = valor, ***detallepago.cuotaActual = valor, ***detallepago.obligacion = valor. Presione enter para salir')
                
                bandera_ok_orden = False
                #time.sleep(7)
                sys.exit()

            inicio_vector += 5
            if inicio_vector >= fin_vector:
                break
            
        return bandera_ok_orden
    except (IndexError, TypeError, AttributeError):
        input("Faltan campos por ingresar en los detalles de pagos. Presione enter para salir")


def transformar_datos_detallepago():
    contador_boletas = 0
    vector_detalle_pago = []
    largo_correspodiente_vector_dp = 0
    ok_orden_dp = verificar_orden_dp()
    claves_generales, datos_generales, clave_valor_general, claves_detallepago, datos_detallepago, clave_valor_detallepago, clave_origen, dato_origen, clave_valor_origen = leer_archivo() #leo el archivo
    #print(clave_valor_detallepago)
    
    
    try:
    #recorro datos_detallepago que viene como [[***detallepago.nroBoleta,xxxxx],[***detallepago.importe,222]]. La idea es generar un vector que solo tenga los valores.
        if ok_orden_dp:
            for datos in clave_valor_detallepago: 
                #print(datos[0], datos[1])
                if datos[0] == '***detallepago.nroBoleta': #datos[0] tiene las "claves", datos[1] el valor.
                    contador_boletas += 1
                    nro_boleta = datos[1]
                    if str(nro_boleta).isnumeric(): #validacion
                        vector_detalle_pago.append(nro_boleta) #guardo en un vector solo los valores, por ej: ['0520823739863094', '12-11-2021', '222.22', '12', '1', '0', '0520250624970392', '12-11-2021', '676.06', '18', '1', '0']
                        #print(f"Boleta nro {contador_boletas}: ", nro_boleta)
                    else:
                        input("Campo ***detallepago.nroBoleta debe ser numerico. . Presione enter para continuar")
                        #time.sleep(5)
                        sys.exit()


                if datos[0] == '***detallepago.fechaPago':
                    fecha_pago = datos[1]
                    fecha_pago_sin_barra = str(fecha_pago.replace('/','-'))
                    if ((len(fecha_pago_sin_barra) == 10) and (str(fecha_pago_sin_barra[0:4]).isnumeric()) and (fecha_pago_sin_barra[4] == '-') and (str(fecha_pago_sin_barra[5:7]).isnumeric()) and (fecha_pago_sin_barra[7] == '-') and (str(fecha_pago_sin_barra[8:10]).isnumeric())):
                        if (int(fecha_pago_sin_barra[8:10]) <= 31 and int(fecha_pago_sin_barra[5:7]) <= 12):
                            #fecha_pago = fecha_pago[6:10] + fecha_pago[5] + fecha_pago[3:5] + fecha_pago[2] + fecha_pago[0:2]
                            vector_detalle_pago.append(fecha_pago_sin_barra + 'T09:30:00.000')
                            #print(f"Fecha Pago: ", fecha_pago)
                        else:
                            input("Error en ***detallepago.fechaPago: Debe ser formato AAAA-MM-DD. Los días menor a 31 y los meses menor a 12")
                            sys.exit()
                    else:
                        input("Campo ***detallepago.fechaPago debe ser formato AAAA-MM-DD. Presione enter para continuar")
                        #time.sleep(5)
                        sys.exit()

                if datos[0] == '***detallepago.importe':
                    importe = datos[1]
                    importe_con_punto = str(float(importe.replace(',','.'))) #para reemplazar si viene coma por punto
                    if float(importe_con_punto):
                        vector_detalle_pago.append(importe_con_punto)
                        #print("Importe: ", importe)
                    else:
                        input("Campo ***detallepago.importe debe ser numerico. Presione enter para continuar")
                        #time.sleep(5)
                        sys.exit()


                if datos[0] == '***detallepago.cantCuotas':
                    cant_cuotas = datos[1]
                    if (str(cant_cuotas).isnumeric()):
                        if int(cant_cuotas) >= 0 and int(cant_cuotas) <= 18:
                            vector_detalle_pago.append(cant_cuotas)
                            #print("Cant cuotas: ", cant_cuotas)
                        else:
                            input("Campo ***detallepago.cantCuotas debe estar comprendido entre 0 y 18. Presione enter para continuar")
                            #time.sleep(5)
                            sys.exit()
                    else:
                        input("Campo ***detallepago.cantCuotas debe estar numerico. Presione enter para continuar")
                        #time.sleep(5)
                        sys.exit()

                if datos[0] == '***detallepago.cuotaActual':
                    id_obj_imponible = datos[1]
                    if (str(id_obj_imponible).isnumeric()):
                        if int(id_obj_imponible) >= 0 and int(id_obj_imponible) <= 18:
                            vector_detalle_pago.append(id_obj_imponible)
                            #print("Id Obj Imp: ", id_obj_imponible)
                        else:
                            input("Campo ***detallepago.cuotaActual debe estar comprendido entre 0 y 18. Presione enter para continuar")
                            #time.sleep(5)
                            sys.exit()
                    else:
                        input("Campo ***detallepago.cuotaActual debe ser numerico. Presione enter para continuar")
                        #time.sleep(5)
                        sys.exit()


            #print(datos[0])
            #print("Cant boletas: ", contador_boletas)
            #print(vector_detalle_pago)
            #print(nro_boleta)

            largo_correspodiente_vector_dp = len(vector_detalle_pago) % 5 #saco el modulo, de esta forma verifico que siempre sea multiplo de 6 el vector, ya que puede venir 6,12,18, es el formato correcto....
            if largo_correspodiente_vector_dp == 0:
                #print("Correcto")
                return vector_detalle_pago

            else:
                input("Revisar los campos ingresados en detalles pagos. Se espera que ingrese 5: ***detallepago.nroBoleta, ***detallepago.fechaPago, ***detallepago.importe, ***detallepago.cantCuotas y ***detallepago.cuotaActual. Presione enter para continuar")
                #time.sleep(5)
                sys.exit()


    except:
        input("Error al llenar la clase DetallePagoInput. Presione enter para salir")
        #time.sleep(5)
        sys.exit()


#def separar_detallespagos(): #lo que hace esta funcion es tomar el vector_detallepago que viene con todos los datos, y los divide en subvectores de detalles indeptes
#    try:
#        lista_dp = transformar_datos_detallepago()
#
#        lista_dp_unitario_anidados = []
#        for i in range(0, len(lista_dp), 6):
#            lista_dp_unitario_anidados.append(lista_dp[i:i+6])
#        #print(lista_dp_unitario_anidados)
#        return lista_dp_unitario_anidados
#    except (TypeError, IndexError):
#        print("Falta algun elemento de los detalles de pagos. Presione enter para salir")
#        #time.sleep(4)
#        sys.exit()



def transformar_nroboletas_dp():
    #try:    
        ok_orden_dp = verificar_orden_dp()
        if ok_orden_dp:
            #rellenar vector para nro boletas
            vector_dp = transformar_datos_detallepago()
            boletas = []
            fin_vector = len(vector_dp)
            inicio_vector = 0

            while inicio_vector < fin_vector:
                boletas.append(vector_dp[inicio_vector])
                inicio_vector += 5
                if inicio_vector >= fin_vector:
                    break
            #print("Boletas: ", boletas)
            return boletas
        else:
            sys.exit()
    #except (TypeError, IndexError):
    #    input("Falta algun elemento de los detalles de pagos. Presione enter para salir")
    #    #time.sleep(4)
    #    sys.exit()


def transformar_fechaspago_dp():
    #try:
        ok_orden_dp = verificar_orden_dp()
        if ok_orden_dp:
            #rellenar vector para nro boletas
            vector_dp = transformar_datos_detallepago()
            fechas = []
            fin_vector = len(vector_dp)
            inicio_vector = 1 #posicion en donde se encuentra la fecha, por eso inicio vector = 1

            while inicio_vector < fin_vector:
                fechas.append(vector_dp[inicio_vector])
                inicio_vector += 5
                if inicio_vector >= fin_vector:
                    break
            #print("Fechas: ", fechas)
            return fechas
        else:
            sys.exit()
    #except (TypeError, IndexError, AttributeError):
    #    input("Falta algun elemento de los detalles de pagos. Presione enter para salir")
    #    #time.sleep(4)
    #    sys.exit()


def transformar_importes_dp():
    #try:
        ok_orden_dp = verificar_orden_dp()
        if ok_orden_dp:
            #rellenar vector para nro boletas
            vector_dp = transformar_datos_detallepago()
            importes = []
            fin_vector = len(vector_dp)
            inicio_vector = 2

            while inicio_vector < fin_vector:
                importes.append(vector_dp[inicio_vector])
                inicio_vector += 5
                if inicio_vector >= fin_vector:
                    break
            #print("Importes: ", importes)
            return importes
        else:
            sys.exit()
    #except (TypeError, IndexError, AttributeError):
    #    input("Falta algun elemento de los detalles de pagos. Presione enter para salir")
    #    #time.sleep(4)
    #    sys.exit()


def transformar_cuotas_dp():
    #try:
        ok_orden_dp = verificar_orden_dp()
        if ok_orden_dp:
            #rellenar vector para nro boletas
            vector_dp = transformar_datos_detallepago()
            cuotas = []
            fin_vector = len(vector_dp)
            inicio_vector = 3

            while inicio_vector < fin_vector:
                cuotas.append(vector_dp[inicio_vector])
                inicio_vector += 5
                if inicio_vector >= fin_vector:
                    break
            #print("Cuotas: ", cuotas)
            return cuotas
        else:
            sys.exit()
    #except (TypeError, IndexError, AttributeError):
    #    input("Falta algun elemento de los detalles de pagos. Presione enter para salir")
    #    #time.sleep(4)
    #    sys.exit()


def transformar_objimponibles_dp():
    #try:
        ok_orden_dp = verificar_orden_dp()
        if ok_orden_dp:
            #rellenar vector para nro boletas
            vector_dp = transformar_datos_detallepago()
            obj_imponibles = []
            fin_vector = len(vector_dp)
            inicio_vector = 4

            while inicio_vector < fin_vector:
                obj_imponibles.append(vector_dp[inicio_vector])
                inicio_vector += 5
                if inicio_vector >= fin_vector:
                    break
            #print("Obj imponibles: ", obj_imponibles)
            return obj_imponibles
        else:
            sys.exit()
    #except (TypeError, IndexError, AttributeError):
    #    input("Falta algun elemento de los detalles de pagos. Presione enter para salir")
    #    #time.sleep(4)
    #    sys.exit()


