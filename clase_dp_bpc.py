class DetallePagoElectronicoBPC():
    def __init__(self, codbarra1_e, codbarra2_e):
        self.codbarra1 = codbarra1_e
        self.codbarra2 = codbarra2_e
        self.cod_registro = '022'
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
        self.cod_registro = '032'
        
        return self.cod_registro
    
    #para pagos electronicos
    def getCodigoER(self, codbarra1):
        codigos = []
        for codigo in codbarra1:
            codigos.append(codigo[3:8])
        return codigos
    
    def getSucursalER(self, codbarra1):
        sucursales = []
        for sucursal in codbarra1:
            sucursales.append(sucursal[8:12])
        return sucursales

    def getBoletaER(self, codbarra1):
        boletas = []
        for boleta in codbarra1:
            boletas.append(boleta[3:19])
        return boletas

    def getFechaEmisionBoletaER(self):
        fechas_emisiones = []
        for fecha in self.codbarra2:
            fechas_emisiones.append(str(fecha[32:36]) + "-" + str(fecha[36:38]) + "-" + str(fecha[38:40]))
        return fechas_emisiones

    def getNroControlBoletaER(self, codbarra1):
        nros_control = []
        for numero in codbarra1:
            nros_control.append(numero[12:19])
        return nros_control
    
    def getFechaDepositoBoletaER(self, fechaacreditacion):
        fecha_deposito = str(fechaacreditacion) + "T00:00:00"
        return fecha_deposito

    def getImpRecaudadoBoletaER(self):
        importes = []
        importe = 0
        #print("cod barra2",self.codbarra2)
        for numero in self.codbarra2:
            #print(numero[30:40])
        
            importe += float(str(numero[0:16]))
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
        importes = []
        importe = 0
        for numero in self.codbarra2:
  
            importe += float(str(numero[19:32]))

            importe_final = importe/100 #de excel
            importes.append(importe_final)
            importe = 0
        
        return importes
    
    def getImpComisionEIvaER(self):
        comision_er = "0.0"
        iva_er = "0.0"

        return comision_er, iva_er
    
    def calcular_imp_determinado_pagado(self, contador_pagos_p): #para pagospresenciales
        importe_por_codbarra = []
        importe = 0

        for numero in range(contador_pagos_p):
            #if tipopago[numero] == "P":

            importe += float(str(self.codbarra2[numero][30:40]))
            importe_final = importe/100 #de excel
            importe_por_codbarra.append(importe_final)
            importe = 0

        return importe_por_codbarra
    
    def calcular_imp_recaudado_depositado_adepostar(self, contador_pagos_p):
        importe_recaudado_por_codbarra = []
        importe_depositado_adepositar_por_codbarra = []
        importe_recaudado = 0
        importe_depositado_adepositar = 0

        for numero in range(contador_pagos_p):
            #if tipopago[numero] == "E":

            importe_recaudado += float(str(self.codbarra2[numero][0:16]))
            importe_final = importe_recaudado/100 #de excel
            importe_recaudado_por_codbarra.append(importe_final)
            importe_recaudado = 0
            importe_depositado_adepositar += float(str(self.codbarra2[numero][19:32]))
            importe_final_1 = importe_depositado_adepositar/100 #de excel
            importe_depositado_adepositar_por_codbarra.append(importe_final_1)
            importe_depositado_adepositar = 0

        return importe_recaudado_por_codbarra, importe_depositado_adepositar_por_codbarra


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
        self.cod_registro = '022'

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
        impuestos = []
        for impuesto in codbarra1:
            impuestos.append(impuesto[4:6])
        return impuestos
    

    def getFechaVenc(self, codbarra2):
        fechas_venc = []
        for fecha in codbarra2:
            fechas_venc.append(str(fecha[14:18]) + "-" + str(fecha[12:14]) + "-" + str(fecha[10:12]))
        return fechas_venc

    def getObjImponible(self, codbarra2):
        obj_imponibles = []
        for obj_imp in codbarra2:
            obj_imponibles.append(obj_imp[18:30])
        return obj_imponibles

    def getNroControl(self, codbarra1):
        nro_control = []
        for numero in codbarra1:
            nro_control.append(numero[1:16])
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
        nro_boletas = []
        for boleta in codbarra1:
            nro_boletas.append(boleta[3:19])
        return nro_boletas
    
    def getNroRegistro(self):
        registros_ycontrol = []
        for numero in range(len(self.codbarra1)):
            registros_ycontrol.append(numero + 1)
            #print(registros_ycontrol)
        return registros_ycontrol

    def getObligacion(self, codbarra1):
        obligaciones = []
        for obligacion in codbarra1:
            obligaciones.append(obligacion[22:43])
        return obligaciones

    def getFechaPago(self):
        fechas_pagos = []
        for fecha in self.codbarra2:
            fechas_pagos.append(str(fecha[14:18]) + "-" + str(fecha[12:14]) + "-" + str(fecha[10:12]) + "T00:00:00")
        return fechas_pagos

    def getImporte(self):        
        importes = []
        importe = 0
        for numero in self.codbarra2:
            #print(numero[30:40])

            importe += float(str(numero[30:40]))
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