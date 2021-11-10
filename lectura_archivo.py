import sys
import time

def leer_archivo():
    vector_datos_general = []
    vector_clave_general = []
    vector_clave_valor_general = []
    vector_datos_detallepagos = []
    vector_clave_detallepagos = []
    vector_clave_valor_detallepagos = []
    
    try:
        with open("C:/Users/Lauti/Desktop/generador_prueba/txt_prueba.txt","r") as archivo:
            for lineas in archivo.readlines():
                #print(lineas)
                if lineas.strip():
                    datos = lineas.replace(" ", "").strip().split('=')
                    #print(datos)
                    if datos[0] == 'general.banco':
                        datos_general = datos[1]
                        clave_general = datos[0]
                        clave_valor_general = clave_general, datos_general
                        #print(datos_general)
                        ##print(datos_general)
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

                    if datos[0] == '***detallepago.idObjetoImponible':
                        datos_dp = datos[1]
                        clave_dp = datos[0]
                        clave_valor_dp = clave_dp, datos_dp
                        vector_datos_detallepagos.append(datos_dp)
                        vector_clave_detallepagos.append(clave_dp)
                        vector_clave_valor_detallepagos.append(clave_valor_dp)

                    if datos[0] == '***detallepago.obligacion':
                        datos_dp = datos[1]
                        clave_dp = datos[0]
                        clave_valor_dp = clave_dp, datos_dp
                        vector_datos_detallepagos.append(datos_dp)
                        vector_clave_detallepagos.append(clave_dp)
                        vector_clave_valor_detallepagos.append(clave_valor_dp)

            #print("Claves de general: ", vector_clave_general)
            #print("Valores de general: ", vector_datos_general)
            #print(vector_clave_valor_general)
#
            #print("Claves de dp: ", vector_clave_detallepagos)
            #print("Valores de dp: ", vector_datos_detallepagos)
            #print(vector_clave_valor_detallepagos)        
            
            
            return vector_clave_general, vector_datos_general, vector_clave_valor_general, vector_clave_detallepagos, vector_datos_detallepagos, vector_clave_valor_detallepagos
    
    except IOError:
        print("Error de lectura de archivo")
        time.sleep(3)
        sys.exit()
    
    except:
        print("Error al intentar realizar operaciones con los datos del archivo.")
        time.sleep(3)
        sys.exit()