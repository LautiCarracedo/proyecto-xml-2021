from configparser import ConfigParser
from tkinter import *
from tkinter import ttk
from tkinter.constants import CENTER, N
from tkinter import messagebox

from clase_general import GeneralOutput
from clase_sucursal import SucursalOutput
from clase_pagos import PagosOutput
from clase_dp import DetallePagoOutput

import xml.etree.ElementTree as ET

#from clases import DetallePagoOutput, GeneralOutput, PagosOutput, SucursalOutput

class Ventana:
    def __init__(self, master):
        self.frame = Frame(master)
        self.label_origen = Label(self.frame, bg='grey', text='ORIGEN: ')
        self.label_origen.grid(row=0, column=0, pady=20, sticky= 'WE')

        self.cbbox_origen = ttk.Combobox(self.frame, width=17, state="readonly")
        self.cbbox_origen.place(x=163,y=20)
        opc = ["PSRM","OTAX","GANT"]
        self.cbbox_origen["values"] = opc

        #General
        self.titulo_general = Label(self.frame,bg='grey',text='GENERAL' )
        self.titulo_general.grid(row=2,column=0,sticky= 'WE')

        self.label_nrobanco = Label(self.frame,text='Número de banco:',padx=20,pady=20 )
        self.label_nrobanco.grid(row=3, column=0)
        
        self.cbbox_nrobanco = ttk.Combobox(self.frame, width=17, state="readonly")
        self.cbbox_nrobanco.place(x=163,y=100)
        opc_bancos, comisiones, banco_elementos, tag_general, tag_sucursal, tag_pagos, tag_dp  = self.leer_ini()
        self.cbbox_nrobanco["values"] = opc_bancos

        self.cbbox_nrobanco.bind("<<ComboboxSelected>>", self.mostrar_nombre_banco)

        

        #fecha de rendicion
        self.label_fecharendicion = Label(self.frame,text='Fecha de rendición:',padx=20,pady=20 )
        self.label_fecharendicion.grid(row=3,column=3,sticky='W')

        self.input_fecharendicion = ttk.Entry(self.frame,width=20,justify=CENTER)
        self.input_fecharendicion.grid(row=3, column=4, )

        #Detalle de pago

        self.titulo_dp = Label(self.frame,text='DETALLE DE PAGO',bg='grey')
        self.titulo_dp.grid(row=4,column=0,sticky= 'WE')

        #Nro de boleta
        self.label_nroboleta = Label(self.frame,text='Número de boleta:',pady=10,padx=20)
        self.label_nroboleta.grid(row=5,column=0,sticky='N' )
  
        self.input_nroboleta = Text(self.frame, height = 15, width = 23)
        self.input_nroboleta.grid(row=5, column=1)

        #Importe
        self.label_importe = Label(self.frame,text='Importe $:',pady=10,padx=20)
        self.label_importe.grid(row=5,column=2,sticky='N')


        self.input_importe = Text(self.frame, height = 15, width = 15)
        self.input_importe.grid(row=5, column=3)
 
        #Fecha de pago
        self.label_fechapago = Label(self.frame,text='Fecha de pago:',pady=10,padx=20 )
        self.label_fechapago.grid(row=5,column=4,sticky='N')

        self.input_fechapago = Text(self.frame, height = 15, width = 20)
        self.input_fechapago.grid(row=5, column=5, sticky='N')

        #Cant cuotas
        self.label_cant_cuotas = Label(self.frame,text='Cantidad de cuotas:',pady=10,padx=20 )
        self.label_cant_cuotas.grid(row=5,column=6,sticky='N')

        self.input_cant_cuotas = Text(self.frame, height = 15, width = 10)
        self.input_cant_cuotas.grid(row=5, column=7, sticky='N')

        #Cuota Actual
        self.label_cuotaactual = Label(self.frame,text='Cuota Actual:',pady=10,padx=20, state="disabled")
        self.label_cuotaactual.grid(row=5,column=8,sticky='N')

        self.input_cuotaactual = Text(self.frame, height = 15, width = 10, state="disabled")
        self.input_cuotaactual.grid(row=5, column=9)
        
        
        self.btn_generarXML = Button(self.frame, text="Generar XML", command=self.generar_xml, width=13, height=2)
        self.btn_generarXML.grid(row=8, column=3, pady=10)

        #self.btn_verificar_cantregistros = Button(self.frame, text="Verif cant registros", command=self.verificar_cant_registros, width=13, height=2)
        #self.btn_verificar_cantregistros.grid(row=8, column=4, pady=10)

        self.frame.pack()
    
    def calcular_comisiones(self):  
        nro_bancos, vec_comisiones, banco_elementos, tag_general, tag_sucursal, tag_pagos, tag_dp = self.leer_ini()
        vec_boletas = self.validar_boletas()
        banco = self.validar_banco()
        vector_comision_p_calculo = []

        if banco in nro_bancos:
            indice_banco = nro_bancos.index(banco)
            comision_banco = vec_comisiones[indice_banco]
        
        for indice in range(len(vec_boletas)):
            vector_comision_p_calculo.append(comision_banco)




        #print('Origen: ', origen)
        #print('Banco seleccionado: ', banco_t)
        print('Comision banco seleccionado: ', vector_comision_p_calculo)

        return vector_comision_p_calculo





    def leer_ini(self):
        
        archivo_conf_bancos ='C:/Users/Lauti/Desktop/config_bancos_tags/probando_config_bancos.ini'
        config = ConfigParser()
        config.read(archivo_conf_bancos)
        #print(config.sections())
        #print(config.get())
        comisiones_y_bancos = config.items('NroBanco')

        #print(tags)
        banco_elementos = str(self.cbbox_nrobanco.get())
        origen = str(self.cbbox_origen.get())

        tag_general = []
        tag_sucursal = []
        tag_pagos = []
        tag_dp = []

        if origen == 'PSRM':
            tags = config.items('ElementosPSRM' + str(banco_elementos))

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
        elif origen == 'OTAX':
            tags = config.items('ElementosOTAX' + str(banco_elementos))

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
            tags = config.items('ElementosGANT' + str(banco_elementos))

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
                
                
        print(banco_elementos)
        print('Elementos tag general: ', tag_general)
        print('Elementos tag sucursal: ', tag_sucursal)
        print('Elementos tag pagos: ', tag_pagos)

        calculo = []
        nro_bancos = []
        vec_comisiones = []
        for banco in comisiones_y_bancos:
            bancos = banco[0]
            comisiones = banco[1]
            suma = float(comisiones) + 10
            nro_bancos.append(bancos)
            calculo.append(suma)
            vec_comisiones.append(comisiones)
        print(calculo)
        print(nro_bancos)
        print(vec_comisiones)

        return nro_bancos, vec_comisiones, banco_elementos, tag_general, tag_sucursal, tag_pagos, tag_dp

    def tomar_datos(self):
        #toma de datos origen
        origen = self.cbbox_origen.get()
        #toma de datos general
        vector_datos_general = []
        banco_t = str(self.cbbox_nrobanco.get())
        vector_datos_general.append(banco_t)
        fecha_rendicion = str(self.input_fecharendicion.get())
        #vector_datos_general.append(fecha_rendicion_t)

        #toma de datos dp
        boletas = self.input_nroboleta.get("1.0","end-1c") 
        importes = self.input_importe.get("1.0","end-1c")
        fecha_pagos = self.input_fechapago.get("1.0","end-1c")
        cant_cuotas = self.input_cant_cuotas.get("1.0","end-1c")
        cuota_actual = self.input_cuotaactual.get("1.0","end-1c")
        return origen, banco_t, fecha_rendicion, boletas, importes, fecha_pagos, cant_cuotas, cuota_actual
    
    def validar_fecha_rendicion(self):
        origen, banco_t, fecha_rendicion, boletas, importes, fecha_pagos, cant_cuotas, cuota_actual = self.tomar_datos()
        fecha_rendicion_t = fecha_rendicion.replace('/','-')
        if ((len(fecha_rendicion_t) == 10) and (str(fecha_rendicion_t[0:2]).isnumeric() and (int(fecha_rendicion[0:2]) <= 31)) and (fecha_rendicion_t[2] == '-') and (str(fecha_rendicion_t[3:5]).isnumeric() and (int(fecha_rendicion[3:5]) <= 12)) and (fecha_rendicion_t[5] == '-') and (str(fecha_rendicion_t[6:10]).isnumeric())):
            fecha_rendicion_format_ok = True
            fecha_rendicion_t = fecha_rendicion_t[6:10] + fecha_rendicion_t[5] + fecha_rendicion_t[3:5] + fecha_rendicion_t[2] + fecha_rendicion_t[0:2]
        
        else:
            fecha_rendicion_format_ok = False

        return fecha_rendicion_format_ok, fecha_rendicion_t
    
    def validar_importes(self):
        origen, banco_t, fecha_rendicion, boletas, importes, fecha_pagos, cant_cuotas, cuota_actual = self.tomar_datos()
        vector_importes = importes.split('\n')
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
    
    def validar_fechapagos(self):
        origen, banco_t, fecha_rendicion, boletas, importes, fecha_pagos, cant_cuotas, cuota_actual = self.tomar_datos()
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
    
    def validar_cant_cuotas(self):
        origen, banco, fecha_rendicion, boletas, importes, fecha_pagos, cant_cuotas, cuota_actual = self.tomar_datos()
        vector_cantcuotas = cant_cuotas.split('\n')
        cuotas_es_numero_cred_deb = False
        for cuota in vector_cantcuotas:
            if banco == '00935':
                if cuota == '18' or cuota == '12':
                    cuotas_es_numero_cred_deb = True
            else:
                if (cuota == 'C' or cuota == 'D') and (banco == '00202c' or banco == '00202d' or banco == '00216'):
                    cuotas_es_numero_cred_deb = True
                else:
                    if cuota.isnumeric():
                        cuotas_es_numero_cred_deb = True
                    else:
                        cuotas_es_numero_cred_deb = False
        return cuotas_es_numero_cred_deb, vector_cantcuotas

    def validar_cuota_actual(self):
        origen, banco, fecha_rendicion, boletas, importes, fecha_pagos, cant_cuotas, cuota_actual = self.tomar_datos()
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
    
    def validar_boletas(self):
        origen, banco_t, fecha_rendicion, boletas, importes, fecha_pagos, cant_cuotas, cuota_actual = self.tomar_datos()
        vector_boletas = boletas.split('\n')
        
        return vector_boletas
    
    def validar_cant_vectores_dp(self):
        vector_boletas = self.validar_boletas()
        bandera_importes_ok, vector_importes = self.validar_importes()
        bandera_fechas_ok, vector_fechapagos = self.validar_fechapagos()
        bandera_cantcuotas_ok, vector_cantcuotas = self.validar_cant_cuotas()
        bandera_cuotaactual_ok, vector_cuotaactual = self.validar_cuota_actual()
        cant_vectores_dp_ok = False
        #print(len(vector_boletas), len(vector_importes), len(vector_fechapagos), len(vector_cantcuotas), len(vector_cuotaactual))
        if len(vector_boletas) == len(vector_importes) == len(vector_fechapagos) == len(vector_cantcuotas) == len(vector_cuotaactual):
            cant_vectores_dp_ok = True
        else:
            cant_vectores_dp_ok = False

        return cant_vectores_dp_ok
    
    def validar_origen(self):
        origen, banco_t, fecha_rendicion, boletas, importes, fecha_pagos, cant_cuotas, cuota_actual = self.tomar_datos()
        origen = origen
        return origen

    def validar_banco(self):
        origen, banco_t, fecha_rendicion, boletas, importes, fecha_pagos, cant_cuotas, cuota_actual = self.tomar_datos()
        banco = banco_t
        return banco
    
    def mostrar_nombre_banco(self, event):
        banco_selec = str(self.cbbox_nrobanco.get())
        
        if banco_selec == "00202c" or banco_selec == "00202d":
            self.label_nombrebanco = Label(self.frame,text='             Visa           ',padx=1,pady=1 )
            self.label_nombrebanco.grid(row=3, column=2)

            self.label_cuotaactual = Label(self.frame,text='Cuota Actual:',pady=10,padx=20, state="disabled")
            self.label_cuotaactual.grid(row=5,column=8,sticky='N')

            self.input_cuotaactual = Text(self.frame, height = 15, width = 10, state="disabled")
            self.input_cuotaactual.grid(row=5, column=9)

        elif banco_selec == "00216":
            
            self.label_nombrebanco = Label(self.frame,text='    Mastercard       ',padx=1,pady=1 )
            self.label_nombrebanco.grid(row=3, column=2)

            self.label_cuotaactual = Label(self.frame,text='Cuota Actual:',pady=10,padx=20, state="disabled")
            self.label_cuotaactual.grid(row=5,column=8,sticky='N')

            self.input_cuotaactual = Text(self.frame, height = 15, width = 10, state="disabled")
            self.input_cuotaactual.grid(row=5, column=9)

        elif banco_selec == "00935":
            
            self.label_nombrebanco = Label(self.frame,text='Cordobesa 12-18',padx=1,pady=1 )
            self.label_nombrebanco.grid(row=3, column=2)

            self.label_cuotaactual = Label(self.frame,text='Cuota Actual:',pady=10,padx=20)
            self.label_cuotaactual.grid(row=5,column=8,sticky='N')

            self.input_cuotaactual = Text(self.frame, height = 15, width = 10)
            self.input_cuotaactual.grid(row=5, column=9)
        
        else:
            self.label_nombrebanco = Label(self.frame,text='          ',padx=1,pady=1 )
            self.label_nombrebanco.grid(row=3, column=2)

            self.label_cuotaactual = Label(self.frame,text='Cuota Actual:',pady=10,padx=20, state="disabled")
            self.label_cuotaactual.grid(row=5,column=8,sticky='N')

            self.input_cuotaactual = Text(self.frame, height = 15, width = 10, state="disabled")
            self.input_cuotaactual.grid(row=5, column=9)
       
    def generar_xml(self):
        try:
            nro_bancos, vec_comisiones, banco_elementos, tag_general, tag_sucursal, tag_pagos, tag_dp = self.leer_ini()
            cuotaactual_es_numero, vector_cuotaactual = self.validar_cuota_actual()
            cuotas_es_numero_cred_deb, vector_cantcuotas = self.validar_cant_cuotas()
            importes_es_float, vector_importes_format_ok = self.validar_importes()
            format_fechas, vector_fechapagos_format_ok = self.validar_fechapagos()
            fecha_rendicion_format_ok, fecha_rendicion_t = self.validar_fecha_rendicion()
            cant_igual_vectores_dp = self.validar_cant_vectores_dp()
            banco_t = self.validar_banco()
            vector_boletas = self.validar_boletas()
            origen = self.validar_origen()

            if cuotaactual_es_numero:
                if cuotas_es_numero_cred_deb:
                    if importes_es_float:
                        if format_fechas:
                            if fecha_rendicion_format_ok:
                                if cant_igual_vectores_dp:
                                
                                    print(vector_importes_format_ok)
                                    instancia_general_output = GeneralOutput(banco_t, fecha_rendicion_t)
                                    banco = instancia_general_output.getBanco()
                                    fecha_rendicion = instancia_general_output.getFechaRendicion()
                                    nro_rendicion = instancia_general_output.generar_nro_rendicion()
                                    cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.calcular_cbus_y_cuits()
                                    registros = instancia_general_output.calcular_cant_registros(vector_boletas)
                                    imp_determinado = instancia_general_output.calcular_importe_determinado_y_pagado(banco_t, vector_importes_format_ok, vector_cantcuotas)
                                    imp_pagado = instancia_general_output.calcular_importe_determinado_y_pagado(banco_t, vector_importes_format_ok, vector_cantcuotas)
                                    imp_recaudado = instancia_general_output.getImpRecaudado()
                                    imp_depositado = instancia_general_output.getImpDepositado()
                                    imp_a_depositar = instancia_general_output.getImpADepositar()
                                    #imp_comision, imp_iva = instancia_general_output.calcular_total_comision_iva(banco_t, vector_boletas, vector_fechapagos_format_ok, vector_importes_format_ok, vector_cuotaactual, vector_cantcuotas)


                                    instancia_sucursal_output = SucursalOutput()
                                    sucursal_id = instancia_sucursal_output.getSucursal()
                                    cant_registros_sucursal = instancia_sucursal_output.calcular_cant_registros(vector_boletas)
                                    imp_pagado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(banco_t, vector_importes_format_ok, vector_cantcuotas)
                                    imp_determinado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(banco_t, vector_importes_format_ok, vector_cantcuotas)
                                    imp_recaudado_sucursal = instancia_sucursal_output.getImpRecaudado()
                                    imp_depositado_sucursal = instancia_sucursal_output.getImpDepositado()
                                    imp_a_depositar_sucursal = instancia_sucursal_output.getImpADepositar()
                                    #total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal(banco_t, vector_boletas, vector_fechapagos_format_ok, vector_importes_format_ok, vector_cuotaactual, vector_cantcuotas)

                                    instancia_pagos_output = PagosOutput(banco_t)
                                    cod_registro = instancia_pagos_output.getCodRegistro()
                                    caja = instancia_pagos_output.getCaja()
                                    cajero = instancia_pagos_output.getCajero()
                                    lote = instancia_pagos_output.getLote(banco_t)
                                    cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos(vector_boletas)
                                    imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(banco_t, vector_importes_format_ok, vector_cantcuotas)
                                    imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(banco_t, vector_importes_format_ok, vector_cantcuotas)
                                    #total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos(banco_t, vector_boletas, vector_fechapagos_format_ok, vector_importes_format_ok, vector_cuotaactual, vector_cantcuotas)


                                    instancia_dp_output = DetallePagoOutput(banco_t, vector_boletas, vector_fechapagos_format_ok, vector_importes_format_ok, vector_cuotaactual, vector_cantcuotas)
                                    cod_registro_dp = instancia_dp_output.getCodRegistro()
                                    nro_registro = instancia_dp_output.calculo_nro_registro_ycontrol()
                                    #print('cant registros', nro_registro)
                                    marca_movimiento = instancia_dp_output.getMarcaMovimiento()
                                    tipo_operacion = instancia_dp_output.getTipoOperacion()
                                    tipo_rendicion = instancia_dp_output.getTipoRendicion()
                                    moneda = instancia_dp_output.getMoneda()
                                    importe = instancia_dp_output.getImporte(banco_t, vector_cantcuotas)
                                    nro_boleta = instancia_dp_output.getNroBoletas()
                                    cuota = instancia_dp_output.getCantCuotas(banco_t)
                                    obj_imponible = instancia_dp_output.getObjImponible()
                                    obligacion = instancia_dp_output.getNroBoletas() #obligacion es el nroBoleta para gant. para psrm y otax es 0
                                    fecha_pago = instancia_dp_output.getFechaPago()
                                    nro_comercio = instancia_dp_output.getNroComercio(banco_t)
                                    #comision, iva = instancia_dp_output.calculo_comision_iva_x_dp(banco_t, vector_cantcuotas)


                                    if banco_t in nro_bancos:
                                        indice_banco = nro_bancos.index(banco_t)
                                        comision_banco = vec_comisiones[indice_banco]


                                    self.calcular_comisiones()
                                    print('Origen: ', origen)
                                    print('Banco seleccionado: ', banco_t)
                                    print('Comision banco: ', comision_banco)



                                    claves_vector_general = ['banco', 'nroTransaccion', 'nroRendicion', 'fechaRendicion', 
                                                            'cbuOrigen', 'cuitOrigen', 'cbuDestino', 'cuitDestino', 'registros', 
                                                            'totalImpDeterminado', 'totalImpPagado', 'totalImpRecaudado', 'totalImpDepositado',
                                                            'totalImpADepositar', 'totalImpComision', 'totalImpIVA']

                                    vector_general = [banco, '0', str(nro_rendicion), fecha_rendicion, cbu_origen, str(cuit_origen), cbu_destino, str(cuit_destino),
                                                    str(registros), imp_determinado, imp_pagado, imp_recaudado, imp_depositado, imp_a_depositar, '0','0']


                                    vector_con_claves_a_mostrar_general = []
                                    vector_con_indices_a_mostrar_gral = []
                                    vector_general_datos_a_mostrar = []

                                    for clave in tag_general:
                                        if clave in claves_vector_general:
                                            vector_con_claves_a_mostrar_general.append(clave)
                                            indice_clave = claves_vector_general.index(clave)
                                            vector_con_indices_a_mostrar_gral.append(indice_clave)
                                            vector_general_datos_a_mostrar.append(vector_general[indice_clave])

                                    print(vector_con_claves_a_mostrar_general)
                                    print(vector_con_indices_a_mostrar_gral)
                                    print(vector_general_datos_a_mostrar)

                                    ############################################################################################333

                                    claves_vector_sucursal = ['sucursal', 'registros', 'totalImpDeterminado', 'totalImpPagado', 
                                                            'totalImpRecaudado', 'totalImpDepositado', 'totalImpADepositar', 'totalImpComision', 'totalImpIVA']

                                    vector_sucursal = [sucursal_id, str(cant_registros_sucursal), imp_determinado_sucursal, imp_pagado_sucursal,
                                                    imp_recaudado_sucursal, imp_depositado_sucursal, imp_a_depositar_sucursal, '0','0']

                                    vector_con_claves_a_mostrar_sucursal = []
                                    vector_con_indices_a_mostrar_sucursal = []
                                    vector_sucursal_datos_a_mostrar = []

                                    for clave in tag_sucursal:
                                        if clave in claves_vector_sucursal:
                                            vector_con_claves_a_mostrar_sucursal.append(clave)
                                            indice_clave = claves_vector_sucursal.index(clave)
                                            vector_con_indices_a_mostrar_sucursal.append(indice_clave)
                                            vector_sucursal_datos_a_mostrar.append(vector_sucursal[indice_clave])

                                    ##################################################################################################

                                    claves_vector_pagos = ['codigoRegistro', 'caja', 'cajero', 'lote', 
                                                            'registros', 'totalImpDeterminado', 'totalImpPagado', 'totalImpComision', 'totalImpIVA']

                                    vector_pagos = [cod_registro, caja, cajero, lote,
                                                    str(cant_registros_pagos), imp_pagado_pagos, imp_determinado_pagos, '0','0']


                                    vector_con_claves_a_mostrar_pagos = []
                                    vector_con_indices_a_mostrar_pagos = []
                                    vector_pagos_datos_a_mostrar = []


                                    for clave in tag_pagos:
                                        if clave in claves_vector_pagos:
                                            vector_con_claves_a_mostrar_pagos.append(clave)
                                            indice_clave = claves_vector_pagos.index(clave)
                                            vector_con_indices_a_mostrar_pagos.append(indice_clave)
                                            vector_pagos_datos_a_mostrar.append(vector_pagos[indice_clave])

                                    ###################################################################################################


                                    general = ET.Element("General",  xmlns="")
                                    for indice in range(len(vector_con_claves_a_mostrar_general)):
                                        general.attrib[vector_con_claves_a_mostrar_general[indice]] = vector_general_datos_a_mostrar[indice]

                                    sucursal_tag = ET.SubElement(general,"Sucursal")
                                    for indice in range(len(vector_con_claves_a_mostrar_sucursal)):
                                        sucursal_tag.attrib[vector_con_claves_a_mostrar_sucursal[indice]] = vector_sucursal_datos_a_mostrar[indice]   


                                    pagos = ET.SubElement(sucursal_tag,"Pagos")
                                    for indice in range(len(vector_con_claves_a_mostrar_pagos)):
                                        pagos.attrib[vector_con_claves_a_mostrar_pagos[indice]] = vector_pagos_datos_a_mostrar[indice]   


                                    for numero in range(len(nro_registro)):

                                        vector_con_claves_a_mostrar_dp = []
                                        vector_con_indices_a_mostrar_dp = []
                                        vector_dp_datos_a_mostrar = []

                                        claves_vector_dp = ['codigoRegistro', 'nroRegistro', 'nroControl', 'marcaMovimiento', 
                                                            'tipoOperacion', 'tipoRendicion', 'moneda', 
                                                            'nroLiquidacionOriginal', 'nroLiquidacionActualizado', 'fechaPago',
                                                            'impDeterminado', 'impPagado', 'impComision', 'impIVA', 'nroComercio',
                                                            'cantCuotas', 'idObjetoImponible', 'obligacion']

                                        if origen == 'GANT':
                                            vector_dp = [cod_registro_dp, str(nro_registro[numero]), str(nro_registro[numero]), marca_movimiento,
                                                        tipo_operacion, tipo_rendicion, moneda, '0', '0', fecha_pago[numero],
                                                        importe[numero], importe[numero], '0', '0', nro_comercio,
                                                        cuota[numero], str(obj_imponible[numero]), obligacion[numero]]

                                        else:
                                            vector_dp = [cod_registro_dp, str(nro_registro[numero]), str(nro_registro[numero]), marca_movimiento,
                                                        tipo_operacion, tipo_rendicion, moneda, nro_boleta[numero], nro_boleta[numero], fecha_pago[numero],
                                                        importe[numero], importe[numero], '0', '0', nro_comercio,
                                                        cuota[numero], str(obj_imponible[numero]), '0']

                                        for clave in tag_dp:
                                            if clave in claves_vector_dp:
                                                vector_con_claves_a_mostrar_dp.append(clave)
                                                indice_clave = claves_vector_dp.index(clave)
                                                vector_con_indices_a_mostrar_dp.append(indice_clave)
                                                vector_dp_datos_a_mostrar.append(vector_dp[indice_clave])

                                        det_pago = ET.SubElement(pagos,"DetallePago")
                                        det_pago.text = " "
                                        #det_pago.attrib[vector_con_claves_a_mostrar_dp[0]] = vector_dp_datos_a_mostrar[0]
                                        for indice in range(len(vector_con_claves_a_mostrar_dp)):
                                            det_pago.attrib[vector_con_claves_a_mostrar_dp[indice]] = vector_dp_datos_a_mostrar[indice]   


                                    print(vector_con_claves_a_mostrar_dp)
                                    print(vector_con_indices_a_mostrar_dp)
                                    print(vector_dp_datos_a_mostrar)

                                    tree = ET.ElementTree(general)    
                                    tree.write('prueba.xml', xml_declaration=True, encoding='utf-8')
                                else:
                                    messagebox.showerror(message="Los campos de los detalles de pagos tienen que tener la misma cantidad de items", title="Error en los detalles de pagos")
                            else:
                                messagebox.showerror(message="El formato de la fecha de rendicion debe ser DD/MM/AAAA o DD-MM-AAAA. DD hasta 31. MM hasta 12", title="Error en fecha de rendicion (General)")   

                        else:
                            messagebox.showerror(message="El formato de la fecha de pago (detallepago) debe ser DD/MM/AAAA o DD-MM-AAAA. DD hasta 31. MM hasta 12", title="Error en las fechas de detalles de pagos")
                    else:
                        messagebox.showerror(message="Los importes deben ser numericos", title="Error en las importes")
                else:
                    messagebox.showerror(message="Para Cordobesa debe ingresar 12 o 18. Para 00202 y 00216 en cant cuotas debe ingresar C o D según si es crédito o debito(siempre será 1 pago).", title="Error en las cantidad cuotas")
            else:
                messagebox.showerror(message="Campo cuota actual deben ser todos numericos", title="Error en campo cuota actual")

        except(SystemError):
            messagebox.showerror(message="Ingrese cada detalle por fila según corresponda. Revise comas decimales. Revise valor del numero banco", title="Error")
       
   
ventana = Tk()
ventana.geometry('1450x520')
ventana.title('XMLGenerator')
aplicacion = Ventana(ventana)
ventana.mainloop()