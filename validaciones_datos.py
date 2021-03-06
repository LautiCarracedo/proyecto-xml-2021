def validar_fecha_rendicion(fecha_rendicion):
    fecha_rendicion_t = fecha_rendicion.replace(" ", "").replace('/','-')
    if ((len(fecha_rendicion_t) == 10) and (str(fecha_rendicion_t[0:2]).isnumeric() and (int(fecha_rendicion[0:2]) <= 31)) and (fecha_rendicion_t[2] == '-') and (str(fecha_rendicion_t[3:5]).isnumeric() and (int(fecha_rendicion[3:5]) <= 12)) and (fecha_rendicion_t[5] == '-') and (str(fecha_rendicion_t[6:10]).isnumeric())):
        fecha_rendicion_format_ok = True
        fecha_rendicion_t = fecha_rendicion_t[6:10] + fecha_rendicion_t[5] + fecha_rendicion_t[3:5] + fecha_rendicion_t[2] + fecha_rendicion_t[0:2]
    
    else:
        fecha_rendicion_format_ok = False

    return fecha_rendicion_format_ok, fecha_rendicion_t
    
def validar_importes(importes):
    vector_importes = importes.replace(" ", "").split('\n')
    #print('vector importes', vector_importes)
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
    vector_fechapagos = fecha_pagos.replace(" ", "").split('\n')
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
    vector_cantcuotas = cant_cuotas.replace(" ", "").split('\n')
    cuotas_es_numero_cred_deb = False
    for cuota in vector_cantcuotas:
        if (cuota == 'C' or cuota == 'D' or cuota == "P") and banco != '00935':
            cuotas_es_numero_cred_deb = True
        elif banco == '00935' and cuota == '18' or cuota == '12':
            cuotas_es_numero_cred_deb = True
        
        else:
            cuotas_es_numero_cred_deb = False

    #print('vector cantcuotas:', vector_cantcuotas)
    return cuotas_es_numero_cred_deb, vector_cantcuotas


def validar_cuota_actual(banco, boletas, cuota_actual):
    vector_boletas = boletas.replace(" ", "").split('\n')
    vector_cuotaactual = cuota_actual.replace(" ", "").split('\n')
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
    
    #print('VECTOR CTA ACTAL',vector_cuotaactual)
    return cuotaactual_es_numero, vector_cuotaactual
    
def validar_boletas(boletas):
    vector_boletas = boletas.replace(" ", "").split('\n')
    
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
    origen_cargado = True
    if origen == None or origen == "":
        origen_cargado = False
    else:
        origen_cargado = True
    return origen_cargado, origen

def validar_banco(banco_t):
    banco = banco_t
    banco_cargado = True
    if banco == None or banco == "":
        banco_cargado = False
    else:
        banco_cargado = True
    return banco_cargado, banco

def validar_cant_registros(boletas, importes, fecha_pagos, cant_cuotas, cuota_actual):
    if boletas == "" or boletas == " ":
        vector_boletas = []
    else:
        vector_boletas = boletas.replace(" ", "").split('\n')
    
    if importes == "" or importes == " ":
        vector_importes = []
    else:
        vector_importes = importes.replace(" ", "").split('\n')
    
    if fecha_pagos == "" or fecha_pagos == " ":
        vector_fechapagos = []
    else:
        vector_fechapagos = fecha_pagos.replace(" ", "").split('\n')
    
    if cant_cuotas == "" or cant_cuotas == " ":
        vector_cantcuotas = []
    else:
        vector_cantcuotas = cant_cuotas.replace(" ", "").split('\n')
    
    if cuota_actual == "" or cuota_actual == " ":
        vector_cuotaactual = []
    else:
        vector_cuotaactual = cuota_actual.replace(" ", "").split('\n')

    return vector_boletas, vector_importes, vector_fechapagos, vector_cantcuotas, vector_cuotaactual

def validar_codbarra1(codbarras1_p, codbarras1_e):
    bandera_codbarra1_p_ok = False
    bandera_codbarra1_e_ok = False
    vec_codbarra1_p = codbarras1_p.replace(" ", "").split('\n')
    vec_codbarra1_e = codbarras1_e.replace(" ", "").split('\n')
    #print(vec_codbarra1_p)
    #print(vec_codbarra1_e)
    for codigo in vec_codbarra1_p:
        #print(codigo[0:2])
        #print(codigo[1])
        if codigo.isnumeric() and codigo[0:2] == "04":
            bandera_codbarra1_p_ok = True
        else:
            bandera_codbarra1_p_ok = False
            break
    
    for codigo in vec_codbarra1_e:
        if codigo.isnumeric() and codigo[0:2] == "04":
            bandera_codbarra1_e_ok = True
        else:
            bandera_codbarra1_e_ok = False
            break

    return bandera_codbarra1_p_ok, bandera_codbarra1_e_ok, vec_codbarra1_p, vec_codbarra1_e

def validar_codbarra2(codbarras2_p, codbarras2_e):
    bandera_codbarra2_p_ok = False
    bandera_codbarra2_e_ok = False
    vec_codbarra2_p = codbarras2_p.replace(" ", "").split('\n')
    vec_codbarra2_e = codbarras2_e.replace(" ", "").split('\n')
    for codigo in vec_codbarra2_p:
        if codigo.isnumeric():
            bandera_codbarra2_p_ok = True
        else:
            bandera_codbarra2_p_ok = False
            break
    
    for codigo in vec_codbarra2_e:
        if codigo.isnumeric():
            bandera_codbarra2_e_ok = True
        else:
            bandera_codbarra2_e_ok = False
            break

    return bandera_codbarra2_p_ok, bandera_codbarra2_e_ok, vec_codbarra2_p, vec_codbarra2_e

def validar_codbarra_otros_entes(codbarra1, codbarra2):
    bandera_codbarra1_ok = False
    bandera_codbarra2_ok = False
    vec_codbarra1 = codbarra1.replace(" ", "").split('\n')
    vec_codbarra2 = codbarra2.replace(" ", "").split('\n')
    #print(vec_codbarra1_p)
    #print(vec_codbarra1_e)
    for codigo in vec_codbarra1:
        if codigo.isnumeric() and len(codigo) == 42:
            bandera_codbarra1_ok = True
        else:
            bandera_codbarra1_ok = False
            break
    
    for codigo in vec_codbarra2:
        if codigo.isnumeric() and len(codigo) == 42:
            bandera_codbarra2_ok = True
        else:
            bandera_codbarra2_ok = False
            break

    return bandera_codbarra1_ok, bandera_codbarra2_ok, vec_codbarra1, vec_codbarra2

def validar_tipopagos(codbarra1_p, codbarra2_p, codbarra1_e, codbarra2_e, formato_xml):
    bandera_codbarra1_p_ok, bandera_codbarra1_e_ok, vector_codbarra1_p, vector_codbarra1_e = validar_codbarra1(codbarra1_p, codbarra1_e)
    bandera_codbarra2_p_ok, bandera_codbarra2_e_ok, vector_codbarra2_p, vector_codbarra2_e = validar_codbarra2(codbarra2_p, codbarra2_e)
    #bandera_tipospagos_ok, vector_tipopagos = validar_tipopagos(tipopago, formato_xml, codbarra1)
    cant_vectores_ok = False
    
    contador_barras_p = 0
    contador_barras_e = 0

    if formato_xml == "Pagos presenciales":
        if len(vector_codbarra1_p) == len(vector_codbarra2_p):
            contador_barras_p = len(vector_codbarra1_p)
    elif formato_xml == "Pagos electronicos":
        if len(vector_codbarra1_e) == len(vector_codbarra2_e):
            contador_barras_e = len(vector_codbarra1_e)
    else:
        if len(vector_codbarra1_p) == len(vector_codbarra2_p) and len(vector_codbarra1_e) == len(vector_codbarra2_e):
            contador_barras_p = len(vector_codbarra1_p)
            contador_barras_e = len(vector_codbarra1_e)

    return contador_barras_e, contador_barras_p


def validar_igualdad_largo_vector(codbarra1_p, codbarra2_p, codbarra1_e, codbarra2_e, formato_xml):
    bandera_codbarra1_p_ok, bandera_codbarra1_e_ok, vector_codbarra1_p, vector_codbarra1_e = validar_codbarra1(codbarra1_p, codbarra1_e)
    bandera_codbarra2_p_ok, bandera_codbarra2_e_ok, vector_codbarra2_p, vector_codbarra2_e = validar_codbarra2(codbarra2_p, codbarra2_e)
    #bandera_tipospagos_ok, vector_tipopagos = validar_tipopagos(tipopago, formato_xml, codbarra1)
    cant_vectores_ok = False
    
    #print(len(vector_codbarra1_p))
    #print(len(vector_codbarra2_p))
    #print(len(vector_codbarra1_e))
    #print(len(vector_codbarra2_e))
    if formato_xml == "Pagos presenciales":
        if len(vector_codbarra1_p) == len(vector_codbarra2_p):
            cant_vectores_ok = True
        else:
            cant_vectores_ok = False
    
    elif formato_xml == "Pagos electronicos":
        if len(vector_codbarra1_e) == len(vector_codbarra2_e):
            cant_vectores_ok = True
        else:
            cant_vectores_ok = False
    
    else:
        if len(vector_codbarra1_p) == len(vector_codbarra2_p) and len(vector_codbarra1_e) == len(vector_codbarra2_e):
            cant_vectores_ok = True
        else:
            cant_vectores_ok = False
    
    #print(cant_vectores_ok)

    return cant_vectores_ok

def validar_cant_registros_bpc(codbarra1_p, codbarra2_p, codbarra1_e, codbarra2_e):
    if codbarra1_p == "" or codbarra1_p == " ":
        vector_codbarra1_p = []
    else:
        vector_codbarra1_p = codbarra1_p.replace(" ", "").split('\n')
    
    if codbarra2_p == "" or codbarra2_p == " ":
        vector_codbarra2_p = []
    else:
        vector_codbarra2_p = codbarra2_p.replace(" ", "").split('\n')
    
    if codbarra1_e == "" or codbarra1_e == " ":
        vector_codbarra1_e = []
    else:
        vector_codbarra1_e = codbarra1_e.replace(" ", "").split('\n')
    
    if codbarra2_e == "" or codbarra2_e == " ":
        vector_codbarra2_e = []
    else:
        vector_codbarra2_e = codbarra2_e.replace(" ", "").split('\n')

    return vector_codbarra1_p, vector_codbarra2_p, vector_codbarra1_e, vector_codbarra2_e


def validar_campo_formato_xml(formato_xml):
    formato = formato_xml
    formato_cargado = True
    if formato == None or formato == "":
        formato_cargado = False
    else:
        formato_cargado = True
    return formato_cargado, formato

