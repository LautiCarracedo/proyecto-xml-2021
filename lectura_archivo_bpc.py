from configparser import ConfigParser


archivo_conf_bpc ='C:/generador_xml/configuracion_bpc.ini'
config = ConfigParser()
config.read(archivo_conf_bpc)



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
        print(claves_codbarra1_p)
        print(posiciones_codbarra1_p)
        
        
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
        print(claves_codbarra2_p)
        print(posiciones_codbarra2_p)
        
        
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
        print(claves_codbarra1_e)
        print(posiciones_codbarra1_e)
        
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
        print(claves_codbarra2_e)
        print(posiciones_codbarra2_e)
        
        return claves_codbarra2_e, posiciones_codbarra2_e