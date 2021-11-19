import sys
import time

def leer_archivo():
    vector_datos_origen = []
    vector_clave_origen = []
    vector_clave_valor_origen = []
    vector_datos_general = []
    vector_clave_general = []
    vector_clave_valor_general = []
    vector_datos_detallepagos = []
    vector_clave_detallepagos = []
    vector_clave_valor_detallepagos = []
    
    try:
        with open("C:/generador_xml/input_txt.txt","r") as archivo:
            for lineas in archivo.readlines():
                #print(lineas)
                if lineas.strip():
                    datos = lineas.replace(" ", "").strip().split('=')
                    #print(datos)
                    if datos[0] == 'origen':
                        dato_sistema_origen = datos[1]
                        clave_sistema_origen = datos[0]
                        clave_valor_sistema_origen = clave_sistema_origen, dato_sistema_origen
                        vector_datos_origen.append(dato_sistema_origen)
                        vector_clave_origen.append(clave_sistema_origen)
                        vector_clave_valor_origen.append(clave_valor_sistema_origen)

                        #print(vector_clave_valor_origen)

                    if datos[0] == 'general.banco':
                        datos_general = datos[1]
                        clave_general = datos[0]
                        clave_valor_general = clave_general, datos_general
                        #print(datos_general)
                        vector_datos_general.append(datos_general)
                        vector_clave_general.append(clave_general)
                        vector_clave_valor_general.append(clave_valor_general)
                        #print(vector_datos_general)
                    
                    if datos[0] == 'general.fechaRendicion':
                        datos_general = datos[1]
                        clave_general = datos[0]
                        clave_valor_general = clave_general, datos_general
                        vector_datos_general.append(datos_general)
                        vector_clave_general.append(clave_general)
                        vector_clave_valor_general.append(clave_valor_general)
                    

                    if datos[0] == '***detallepago.nroBoleta': #datos[0] tiene las "claves", datos[1] el valor.
                        datos_dp = datos[1]
                        clave_dp = datos[0]
                        clave_valor_dp = clave_dp, datos_dp
                        vector_datos_detallepagos.append(datos_dp)
                        vector_clave_detallepagos.append(clave_dp)
                        vector_clave_valor_detallepagos.append(clave_valor_dp)
                

                    if datos[0] == '***detallepago.fechaPago':
                        datos_dp = datos[1]
                        clave_dp = datos[0]
                        clave_valor_dp = clave_dp, datos_dp
                        vector_datos_detallepagos.append(datos_dp)
                        vector_clave_detallepagos.append(clave_dp)
                        vector_clave_valor_detallepagos.append(clave_valor_dp)

                    if datos[0] == '***detallepago.importe':
                        datos_dp = datos[1]
                        clave_dp = datos[0]
                        clave_valor_dp = clave_dp, datos_dp
                        vector_datos_detallepagos.append(datos_dp)
                        vector_clave_detallepagos.append(clave_dp)
                        vector_clave_valor_detallepagos.append(clave_valor_dp)


                    if datos[0] == '***detallepago.cantCuotas':
                        datos_dp = datos[1]
                        clave_dp = datos[0]
                        clave_valor_dp = clave_dp, datos_dp
                        vector_datos_detallepagos.append(datos_dp)
                        vector_clave_detallepagos.append(clave_dp)
                        vector_clave_valor_detallepagos.append(clave_valor_dp)

                    if datos[0] == '***detallepago.cuotaActual':
                        datos_dp = datos[1]
                        clave_dp = datos[0]
                        clave_valor_dp = clave_dp, datos_dp
                        vector_datos_detallepagos.append(datos_dp)
                        vector_clave_detallepagos.append(clave_dp)
                        vector_clave_valor_detallepagos.append(clave_valor_dp)


            #print("Claves de general: ", vector_clave_general)
            #print("Valores de general: ", vector_datos_general)
            #print(vector_clave_valor_general)

            #print("Claves de dp: ", vector_clave_detallepagos)
            #print("Valores de dp: ", vector_datos_detallepagos)
            #print(vector_clave_valor_detallepagos)        

            #print(len(vector_datos_general))


            #Implementacion cuando vienen mas de dos pagos
            #if len(vector_datos_general) >= 4: #quiere decir que hay mas de un general.banco y se deben generar 2 o mas xml 
            #    vector_general_separados = []
            #    vector_dp_separados = []
            #    for i in range(0, len(vector_datos_general), 2):
            #        vector_general_separados.append(vector_datos_general[i:i+2])
                    #vector_dp_separados.append()
                #print(vector_general_separados)
                #print("Valores de general: ", vector_datos_general)
                #return vector_general_separado

            
            
            return vector_clave_general, vector_datos_general, vector_clave_valor_general, vector_clave_detallepagos, vector_datos_detallepagos, vector_clave_valor_detallepagos, vector_clave_origen, vector_datos_origen, vector_clave_valor_origen
    
    except IOError:
        input("Error de lectura de archivo. Presione enter para salir")
        #time.sleep(3)
        sys.exit()
    
    except:
        input("Error al intentar realizar operaciones con los datos del archivo. Presione enter para salir")
        #time.sleep(3)
        sys.exit()