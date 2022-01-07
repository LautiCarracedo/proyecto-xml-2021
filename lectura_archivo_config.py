from configparser import ConfigParser
from tkinter import messagebox
from tkinter.constants import E

from validaciones_datos import validar_cant_cuotas

archivo_conf_bancos ='C:/generador_xml/configuracion_bancos.ini'
config = ConfigParser()
config.read(archivo_conf_bancos)



class ArchivoConfig():

    def leer_ini_bancos(self):

        bancos = config.items('NroBanco')
        nro_bancos = []
        nombres_bancos = []
        for indice in bancos:
            banco = indice[0]
            nombre = indice[1]
            nro_bancos.append(banco)
            nombres_bancos.append(nombre)
        print(nro_bancos)
        print(nombres_bancos)
        
        
        return nro_bancos, nombres_bancos

    def leer_ini_comisiones(self, banco):
        try:
            banco_selec = str(banco)
    
            comisiones = config.items('Comisiones' + str(banco_selec))

            vec_claves = []
            vec_comisiones = []
            for indice in comisiones:
                clave = indice[0]
                comision = indice[1]
                vec_claves.append(clave)
                vec_comisiones.append(comision)

            print(vec_claves)
            print(vec_comisiones)

            return vec_claves, vec_comisiones

        except:
           return 0,0 #esto devuelve un typerror al querer calcular las comisiones en calcular_comisiones. lo capturamos en el archivo ventana.
        
    def leer_ini_valores_tags_variables(self, banco):
        try:
            banco_selec = str(banco)
            clave_valores = config.items('Valores' + str(banco_selec))

            vec_claves_tag = []
            vec_valores = []
            for indice in clave_valores:
                clave = indice[0]
                valor = indice[1]
                vec_claves_tag.append(clave)
                vec_valores.append(valor)

            return vec_claves_tag, vec_valores
        
        except:
            return 0,0

    def leer_ini_tags(self, origen, banco):
        try:
            banco_selec = str(banco)    

            tag_general = []
            tag_sucursal = []
            tag_pagos = []
            tag_dp = []

            if origen == 'PSRM':
                tags = config.items('ElementosPSRM' + str(banco_selec))

                for tag in tags:
                    clave = tag[0]
                    valor = tag[1]
                    while 'general' in clave:
                        tag_general.append(valor)
                        break
                    while 'sucursal' in clave:
                        tag_sucursal.append(valor)
                        break
                    while 'pagos' in clave:
                        tag_pagos.append(valor)
                        break
                    while 'detpagos' in clave:
                        tag_dp.append(valor)
                        break

            if origen == 'OTAX':
                tags = config.items('ElementosOTAX' + str(banco_selec))

                for tag in tags:
                    clave = tag[0]
                    valor = tag[1]
                    while 'general' in clave:
                        tag_general.append(valor)
                        break
                    while 'sucursal' in clave:
                        tag_sucursal.append(valor)
                        break
                    while 'pagos' in clave:
                        tag_pagos.append(valor)
                        break
                    while 'detpagos' in clave:
                        tag_dp.append(valor)
                        break

            elif origen == 'GANT':
                tags = config.items('ElementosGANT' + str(banco_selec))

                for tag in tags:
                    clave = tag[0]
                    valor = tag[1]
                    while 'general' in clave:
                        tag_general.append(valor)
                        break
                    while 'sucursal' in clave:
                        tag_sucursal.append(valor)
                        break
                    while 'pagos' in clave:
                        tag_pagos.append(valor)
                        break
                    while 'detpagos' in clave:
                        tag_dp.append(valor)
                        break
                    
            #print('Elementos tag general: ', tag_general)
            #print('Elementos tag sucursal: ', tag_sucursal)
            #print('Elementos tag pagos: ', tag_pagos)

            return tag_general, tag_sucursal, tag_pagos, tag_dp
        
        except:
            return 0,0,0,0


class ComisionesArchivo():
    def calcular_comisiones(self, banco, cantcuotas):
        
        datos_archivo_config = ArchivoConfig()
        vec_claves, vec_comisiones = datos_archivo_config.leer_ini_comisiones(banco)
        #comisiones_ok, vector_comisiones_claves = validar_cant_cuotas(banco, cantcuotas)
        #nro_bancos, nombres_bancos = datos_archivo_config.leer_ini_bancos()
        vector_comisiones_p_calculo = []
        vector_comisiones_calculo_ok = False
        vector_cant_cuotas = cantcuotas
        print('cOMISIONES',vec_comisiones)
        for valor_cuota in vector_cant_cuotas:
            if (valor_cuota == 'C') and (banco != '00935'):
                vector_comisiones_calculo_ok = True
                vector_comisiones_p_calculo.append(vec_comisiones[0])
            elif (valor_cuota == 'D') and (banco != '00935'):
                vector_comisiones_calculo_ok = True
                vector_comisiones_p_calculo.append(vec_comisiones[1])
            elif (valor_cuota == '12' or valor_cuota == '18') and (banco == '00935'):
                vector_comisiones_calculo_ok = True
                vector_comisiones_p_calculo.append(vec_comisiones[0])
            else:
                vector_comisiones_calculo_ok = False
        print('Comisiones de cada dp del banco seleccionado: ', vector_comisiones_p_calculo)#
        return vector_comisiones_calculo_ok, vector_comisiones_p_calculo
        
        