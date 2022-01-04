def validar_fecha_rendicion(fecha_rendicion):
    fecha_rendicion_t = fecha_rendicion.replace('/','-')
    if ((len(fecha_rendicion_t) == 10) and (str(fecha_rendicion_t[0:2]).isnumeric() and (int(fecha_rendicion[0:2]) <= 31)) and (fecha_rendicion_t[2] == '-') and (str(fecha_rendicion_t[3:5]).isnumeric() and (int(fecha_rendicion[3:5]) <= 12)) and (fecha_rendicion_t[5] == '-') and (str(fecha_rendicion_t[6:10]).isnumeric())):
        fecha_rendicion_format_ok = True
        fecha_rendicion_t = fecha_rendicion_t[6:10] + fecha_rendicion_t[5] + fecha_rendicion_t[3:5] + fecha_rendicion_t[2] + fecha_rendicion_t[0:2]
    
    else:
        fecha_rendicion_format_ok = False

    return fecha_rendicion_format_ok, fecha_rendicion_t
    
def validar_importes(importes):
    vector_importes = importes.split('\n')
    print('vector importes', vector_importes)
    vector_importes_format_ok = []
    importes_es_float = False
    for importes in vector_importes:
        importes_format_punto_miles = importes.replace('.','').replace('$','')
        importes_format_coma_decimal = importes_format_punto_miles.replace(',','.')
        if float(importes_format_coma_decimal):
            importes_es_float = True
            vector_importes_format_ok.append(importes_format_coma_decimal)
        else:
            importes_es_float = False
    
    return importes_es_float, vector_importes_format_ok
    
def validar_fechapagos(fecha_pagos):
    vector_fechapagos = fecha_pagos.split('\n')
    vector_fechapagos_format_ok = []
    format_fechas = False
    for fechas in vector_fechapagos:
        fechas_format = fechas.replace('/','-')
        if ((len(fechas_format) == 10) and (str(fechas_format[0:2]).isnumeric() and (int(fechas_format[0:2]) <= 31)) and (fechas_format[2] == '-') and (str(fechas_format[3:5]).isnumeric() and (int(fechas_format[3:5]) <= 12)) and (fechas_format[5] == '-') and (str(fechas_format[6:10]).isnumeric())):
            fechas_format = fechas_format[6:10] + fechas_format[5] + fechas_format[3:5] + fechas_format[2] + fechas_format[0:2] + 'T09:30:00.000'
            vector_fechapagos_format_ok.append(fechas_format)
            format_fechas = True
        else:
            format_fechas = False
    return format_fechas, vector_fechapagos_format_ok
    
def validar_cant_cuotas(banco, cant_cuotas):
    vector_cantcuotas = cant_cuotas.split('\n')
    #vector_dp_calculos = []
    cuotas_es_numero_cred_deb = False
    for cuota in vector_cantcuotas:
        if (cuota == 'C' or cuota == 'D') and banco != '00935':
            cuotas_es_numero_cred_deb = True
        elif banco == '00935' and cuota == '18' or cuota == '12':
            cuotas_es_numero_cred_deb = True
        #elif (cuota == 'C' or cuota == 'D' or cuota.isnumeric()):
        #    cuotas_es_numero_cred_deb = True
        else:
            cuotas_es_numero_cred_deb = False

    print('vector cantcuotas:', vector_cantcuotas)
    return cuotas_es_numero_cred_deb, vector_cantcuotas
    

def validar_cuota_actual(banco, boletas, cuota_actual):
    vector_boletas = boletas.split('\n')
    vector_cuotaactual = cuota_actual.split('\n')
    cuotaactual_es_numero = False
    if (banco != '00935'): 
        # como los text aunque no carguemos nada lo toma como len=1, para el caso de visa y master 
        # que no utilizamos estos campos lo cargamos en cero y se desactiva para no pdoer cargar
        vector_cuotaactual.pop()
        for boleta in range(len(vector_boletas)):
            vector_cuotaactual.append('0')
            cuotaactual_es_numero = True
            
    elif (banco == '00935'):   
        for c_act in vector_cuotaactual:
            if c_act.isnumeric():
                cuotaactual_es_numero = True
            else:
                cuotaactual_es_numero = False
    
    print('VECTOR CTA ACTAL',vector_cuotaactual)
    return cuotaactual_es_numero, vector_cuotaactual
    
def validar_boletas(boletas):
    vector_boletas = boletas.split('\n')
    
    return vector_boletas
    
def validar_cant_vectores_dp(banco, boletas, importes, fecha_pagos, cant_cuotas, cuota_actual):
    vector_boletas = validar_boletas(boletas)
    bandera_importes_ok, vector_importes = validar_importes(importes)
    bandera_fechas_ok, vector_fechapagos = validar_fechapagos(fecha_pagos)
    bandera_cantcuotas_ok, vector_cantcuotas = validar_cant_cuotas(banco, cant_cuotas)
    bandera_cuotaactual_ok, vector_cuotaactual = validar_cuota_actual(banco, boletas, cuota_actual)
    cant_vectores_dp_ok = False
    #print(len(vector_boletas), len(vector_importes), len(vector_fechapagos), len(vector_cantcuotas), len(vector_cuotaactual))
    if len(vector_boletas) == len(vector_importes) == len(vector_fechapagos) == len(vector_cantcuotas) == len(vector_cuotaactual):
        cant_vectores_dp_ok = True
    else:
        cant_vectores_dp_ok = False

    return cant_vectores_dp_ok
    
def validar_origen(origen_t):
    origen = origen_t
    return origen

def validar_banco(banco_t):
    banco = banco_t
    return banco

def validar_cant_registros(boletas, importes, fecha_pagos, cant_cuotas, cuota_actual):
    vector_boletas = boletas.split('\n')
    vector_importes = importes.split('\n')
    vector_fechapagos = fecha_pagos.split('\n')
    vector_cantcuotas = cant_cuotas.split('\n')
    vector_cuotaactual = cuota_actual.split('\n')

    return vector_boletas, vector_importes, vector_fechapagos, vector_cantcuotas, vector_cuotaactual



