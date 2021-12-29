from configparser import ConfigParser

from validaciones_datos import validar_banco

archivo_conf_bancos ='C:/generador_xml/configuracion_bancos.ini'
config = ConfigParser()
config.read(archivo_conf_bancos)

def leer_ini_bancos():
    #print(config.sections())
    #print(config.get())
    bancos = config.items('NroBanco')

    #print(tags)
    #banco_selec = str(banco)
    #origen = str(origen)

    #print(banco_selec)
    

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

def leer_ini_comisiones(banco):
    banco_selec = str(banco)
    #print(config.sections())
    #print(config.get())
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

def leer_ini_valores_tags_variables(banco):
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

def leer_ini_tags(origen, banco):
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
    
    print('Elementos tag general: ', tag_general)
    print('Elementos tag sucursal: ', tag_sucursal)
    print('Elementos tag pagos: ', tag_pagos)

    return tag_general, tag_sucursal, tag_pagos, tag_dp



def calcular_comisiones(banco, cantcuotas):  
    vec_claves, vec_comisiones = leer_ini_comisiones(banco)
    nro_bancos, nombres_bancos = leer_ini_bancos()

    #vec_boletas = boletas
    banco = validar_banco(banco)
    vector_comisiones_p_calculo = []
    
    if banco in nro_bancos:
        for valor_cuota in cantcuotas:
            if valor_cuota == 'C' and banco != '00935':
                comision_banco = float(vec_comisiones[0])
                vector_comisiones_p_calculo.append(comision_banco)

            elif valor_cuota == 'D' and banco != '00935':
                comision_banco = float(vec_comisiones[1])
                vector_comisiones_p_calculo.append(comision_banco)

            elif banco == '00935' and (valor_cuota == '12' or valor_cuota == '18'):
                comision_banco = float(vec_comisiones[0])
                vector_comisiones_p_calculo.append(comision_banco)
                
    print('Comisiones de cada dp del banco seleccionado: ', vector_comisiones_p_calculo)#
    return vector_comisiones_p_calculo