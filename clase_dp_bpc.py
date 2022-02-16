from lectura_archivo_bpc import ArchivoConfigBPC


class DetallePagoElectronicoBPC():
    def __init__(self, codbarra1_e, codbarra2_e):
        self.codbarra1 = codbarra1_e
        self.codbarra2 = codbarra2_e
        self.cod_registro = '032'
        self.marca_movimiento = 'P' 
        self.tipo_operacion = '01'
        self.tipo_rendicion = '01'
        self.moneda = '01'
    
    def getMarcaMovimiento(self):
        return self.marca_movimiento

    def getTipoOperacion(self):
        return self.tipo_operacion

    def getTipoRendicion(self):
        return self.tipo_rendicion

    def getMoneda(self):
        return self.moneda
    
    def getNroComercio(self):
        nro_comercio = "2341234"
        return nro_comercio
    
    def getCodRegistro(self):
        self.cod_registro
        
        return self.cod_registro
    
    #para pagos electronicos
    def getCodigoER(self, codbarra1):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra1_e()
        codigos = []
        for codigo in codbarra1:
            codigos.append(codigo[int(posiciones[0])-1:int(posiciones[1])])
        return codigos
    
    def getSucursalER(self, codbarra1):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra1_e()
        sucursales = []
        for sucursal in codbarra1:
            sucursales.append(sucursal[int(posiciones[2])-1:int(posiciones[3])])
        return sucursales

    def getBoletaER(self, codbarra1):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra1_e()
        boletas = []
        for boleta in codbarra1:
            boletas.append(boleta[int(posiciones[4])-1:int(posiciones[5])])
        return boletas

    def getFechaEmisionBoletaER(self):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra2_e()
        fechas_emisiones = []
        for fecha in self.codbarra2:
            fechas_emisiones.append(str(fecha[int(posiciones[0])-1:int(posiciones[0])+3]) + "-" + str(fecha[int(posiciones[0])+3:int(posiciones[0])+5]) + "-" + str(fecha[int(posiciones[0])+5:int(posiciones[1])]))  #32:36-36:38-38:40
        return fechas_emisiones

    def getNroControlBoletaER(self, codbarra1):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra1_e()
        nros_control = []
        for numero in codbarra1:
            nros_control.append(numero[int(posiciones[6])-1:int(posiciones[7])])
        return nros_control
    
    def getFechaDepositoBoletaER(self, fechaacreditacion): #es la fecha acreditacion o rendicion
        fecha_deposito = str(fechaacreditacion) + "T00:00:00"
        return fecha_deposito

    def getImpRecaudadoBoletaER(self):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra2_e()
        importes = []
        importe = 0
        #print("cod barra2",self.codbarra2)
        for numero in self.codbarra2:
            #print(numero[30:40])
        
            importe += float(str(numero[int(posiciones[2])-1:int(posiciones[3])]))
            #print(importe)

            importe_final = importe/100 #de excel
            importes.append(importe_final)
            importe = 0

        return importes
    
    def getNroRegistro(self):
        registros_ycontrol = []
        for numero in range(len(self.codbarra1)):
            registros_ycontrol.append(numero + 1)
            #print(registros_ycontrol)
        return registros_ycontrol

    def getImpADepositarYDepositadoER(self):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra2_e()
        importes = []
        importe = 0
        for numero in self.codbarra2:
  
            importe += float(str(numero[int(posiciones[4])-1:int(posiciones[5])]))

            importe_final = importe/100 #de excel
            importes.append(importe_final)
            importe = 0
        
        return importes
    
    def getImpComisionEIvaER(self):
        comision_er = "0.0"
        iva_er = "0.0"

        return comision_er, iva_er
    
    #def calcular_imp_determinado_pagado(self, contador_pagos_p): #para pagospresenciales
    #    importe_por_codbarra = []
    #    importe = 0
#
    #    for numero in range(contador_pagos_p):
    #        #if tipopago[numero] == "P":
#
    #        importe += float(str(self.codbarra2[numero][30:40]))
    #        importe_final = importe/100 #de excel
    #        importe_por_codbarra.append(importe_final)
    #        importe = 0
#
    #    return importe_por_codbarra
    #
    #def calcular_imp_recaudado_depositado_adepostar(self, contador_pagos_p):
    #    importe_recaudado_por_codbarra = []
    #    importe_depositado_adepositar_por_codbarra = []
    #    importe_recaudado = 0
    #    importe_depositado_adepositar = 0
#
    #    for numero in range(contador_pagos_p):
    #        #if tipopago[numero] == "E":
#
    #        importe_recaudado += float(str(self.codbarra2[numero][0:16]))
    #        importe_final = importe_recaudado/100 #de excel
    #        importe_recaudado_por_codbarra.append(importe_final)
    #        importe_recaudado = 0
    #        importe_depositado_adepositar += float(str(self.codbarra2[numero][19:32]))
    #        importe_final_1 = importe_depositado_adepositar/100 #de excel
    #        importe_depositado_adepositar_por_codbarra.append(importe_final_1)
    #        importe_depositado_adepositar = 0
#
    #    return importe_recaudado_por_codbarra, importe_depositado_adepositar_por_codbarra


class DetallePagoPresencialBPC():
    def __init__(self, codbarra1_p, codbarra2_p):
        self.codbarra1 = codbarra1_p
        self.codbarra2 = codbarra2_p
        self.cod_registro = '022'
        self.marca_movimiento = 'P' 
        self.tipo_operacion = '01'
        self.tipo_rendicion = '01'
        self.moneda = '01'

    def getCodBarra(self):
        return self.codbarra1, self.codbarra2

    def getCodRegistro(self):
        return self.cod_registro

    def getMarcaMovimiento(self):
        return self.marca_movimiento

    def getTipoOperacion(self):
        return self.tipo_operacion

    def getTipoRendicion(self):
        return self.tipo_rendicion

    def getMoneda(self):
        return self.moneda
    
    def getNroComercio(self):
        nro_comercio = "2341234"
        return nro_comercio
    
    def getImpuesto(self, codbarra1):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra1_p()
        impuestos = []
        for impuesto in codbarra1:
            impuestos.append(impuesto[int(posiciones[0])-1:int(posiciones[1])])
        return impuestos
    

    def getFechaVenc(self, codbarra2):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra2_p()
        fechas_venc = []
        for fecha in codbarra2:
            fechas_venc.append(str(fecha[int(posiciones[4])+3:int(posiciones[5])]) + "-" + str(fecha[int(posiciones[4])+1:int(posiciones[4])+3]) + "-" + str(fecha[int(posiciones[4])-1:int(posiciones[4])+1]))
        return fechas_venc

    def getObjImponible(self, codbarra2):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra2_p()
        obj_imponibles = []
        for obj_imp in codbarra2:
            obj_imponibles.append(obj_imp[int(posiciones[2])-1:int(posiciones[3])])
        return obj_imponibles

    def getNroControl(self, codbarra1):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra1_p()
        nro_control = []
        for numero in codbarra1:
            nro_control.append(numero[int(posiciones[2])-1:int(posiciones[3])])
        return nro_control

    def getMarcaMovimiento(self):
        marca_mov = "P"
        return marca_mov

    def getTipoOperacion(self):
        tipo_op = "01"
        return tipo_op

    def getTipoRendicion(self):
        tipo_rendicion = "01"
        return tipo_rendicion

    def getMoneda(self):
        tipo_moneda = "01"
        return tipo_moneda

    def getLiquidacion(self, codbarra1): #liq original y actualizada
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra1_p()
        nro_boletas = []
        for boleta in codbarra1:
            nro_boletas.append(boleta[int(posiciones[4])-1:int(posiciones[5])])
        return nro_boletas
    
    def getNroRegistro(self):
        registros_ycontrol = []
        for numero in range(len(self.codbarra1)):
            registros_ycontrol.append(numero + 1)
            #print(registros_ycontrol)
        return registros_ycontrol

    def getObligacion(self, codbarra1):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra1_p()
        obligaciones = []
        for obligacion in codbarra1:
            obligaciones.append(obligacion[int(posiciones[6])-1:int(posiciones[7])])
        return obligaciones

    def getFechaPago(self):
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra2_p()
        fechas_pagos = []
        for fecha in self.codbarra2:
            fechas_pagos.append(str(fecha[int(posiciones[4])+3:int(posiciones[5])]) + "-" + str(fecha[int(posiciones[4])+1:int(posiciones[4])+3]) + "-" + str(fecha[int(posiciones[4])-1:int(posiciones[4])+1]) + "T00:00:00")   #14:18-12:14-10:12
        return fechas_pagos

    def getImporte(self): 
        config_bpc = ArchivoConfigBPC()
        claves, posiciones = config_bpc.leer_ini_bpc_codbarra2_p()
        importes = []
        importe = 0
        for numero in self.codbarra2:
            #print(numero[30:40])

            importe += float(str(numero[int(posiciones[6])-1:int(posiciones[7])]))
            #print(importe)
            importe_final = importe/100 #de excel
            importes.append(importe_final)
            importe = 0

        return importes

    
    def calculo_comision_iva_x_dp(self):
        comisiones = "0.0"
        ivas = "0.0"
        return comisiones, ivas


class DetallePagoAmbosPagosBPC():
    pass