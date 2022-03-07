from configparser import ConfigParser
import os


directorio_actual = os.getcwd()
archivo_conf_bancos ='configuracion_bpc.ini'
ruta_final = os.path.join(directorio_actual, archivo_conf_bancos)
ruta_final = os.path.abspath(ruta_final)
config = ConfigParser()
config.read(ruta_final)



class ArchivoConfigBPC():

    def leer_ini_bpc_codbarra1_p(self):

        codbarra = config.items('PagoPresencialCodBarra1')
        claves_codbarra1_p = []
        posiciones_codbarra1_p = []
        for indice in codbarra:
            clave = indice[0]
            posicion = indice[1]
            claves_codbarra1_p.append(clave)
            posiciones_codbarra1_p.append(posicion)
        
        return claves_codbarra1_p, posiciones_codbarra1_p
    
    def leer_ini_bpc_codbarra2_p(self):

        codbarra = config.items('PagoPresencialCodBarra2')
        claves_codbarra2_p = []
        posiciones_codbarra2_p = []
        for indice in codbarra:
            clave = indice[0]
            posicion = indice[1]
            claves_codbarra2_p.append(clave)
            posiciones_codbarra2_p.append(posicion)

        return claves_codbarra2_p, posiciones_codbarra2_p
    
    def leer_ini_bpc_codbarra1_e(self):

        codbarra = config.items('PagoElectronicoCodBarra1')
        claves_codbarra1_e = []
        posiciones_codbarra1_e = []
        for indice in codbarra:
            clave = indice[0]
            posicion = indice[1]
            claves_codbarra1_e.append(clave)
            posiciones_codbarra1_e.append(posicion)
        
        return claves_codbarra1_e, posiciones_codbarra1_e
    
    def leer_ini_bpc_codbarra2_e(self):

        codbarra = config.items('PagoElectronicoCodBarra2')
        claves_codbarra2_e = []
        posiciones_codbarra2_e = []
        for indice in codbarra:
            clave = indice[0]
            posicion = indice[1]
            claves_codbarra2_e.append(clave)
            posiciones_codbarra2_e.append(posicion)

        return claves_codbarra2_e, posiciones_codbarra2_e