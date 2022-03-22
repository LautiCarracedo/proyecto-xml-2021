from lectura_archivo_config import ArchivoConfig, ComisionesArchivo

class DetallePagoInput():
    def __init__(self, boletas, fechapagos, importes, cuotaactual, cantcuotas, codbarra1, codbarra2):
        #
        self.boletas = boletas
        self.fecha_pagos = fechapagos
        self.importes = importes
        self.obj_imp = cuotaactual
        self.cuotas = cantcuotas
        self.codbarra1 = codbarra1
        self.codbarra2 = codbarra2


class DetallePagoOutput(DetallePagoInput):
    def __init__(self, banco, boletas, fechapagos, importes, cuotaactual, cantcuotas, codbarra1, codbarra2):
        super().__init__(boletas, fechapagos, importes, cuotaactual, cantcuotas, codbarra1, codbarra2)
        self.cod_registro = '022'
        self.marca_movimiento = 'P'
        self.tipo_operacion = '01'
        self.tipo_rendicion = '01'
        self.moneda = '01'
        self.nro_comercio = banco
        self.impuesto = '501' #para 079 y 082

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

    def getImporte(self, banco, cantcuotas):
        #vector_importes = transformar_importes_dp()
        #print(vector_importes)
        #print(self.importes)
        importe_redeondeado = [] #tengo que devolver vector si o si porque self.importes es un vector para q se realicen todas las operacionces correctamente
        if banco == '00935': #solo para cordobesa hay que dividir el importe ingresado en la cant cuotas
            for indice in range(len(cantcuotas)):
                importes = "{0:.2f}".format(float(self.importes[indice]) / float(cantcuotas[indice]))
                importe_redeondeado.append(importes)
                #print(importe_redeondeado)

        elif banco == '00079' or banco == '00082':
            importes_codbarra = self.extraer_importe_codbarra2()
            for importes in importes_codbarra:
                importe_pago = "{0:.2f}".format(float(importes))
                importe_redeondeado.append(importe_pago)

        else:
            for importes in self.importes:
                importe_pago = "{0:.2f}".format(float(importes))
                importe_redeondeado.append(importe_pago)
        #print(importe_redeondeado)
        return importe_redeondeado

        

    def getNroBoletas(self):
        #vector_nro_boletas = transformar_nroboletas_dp()
        return self.boletas

    def getCantCuotas(self, banco):
        #vector_cuotas = transformar_cuotas_dp()

        cuotas = []
        if banco != '00935':
            for cuota in range(len(self.cuotas)):
                cuotas.append('1') 
        else:
            cuotas = self.cuotas
        return cuotas

    def getObjImponible(self):
        #vector_obj_imponible = transformar_objimponibles_dp()
        return self.obj_imp


    def getFechaPago(self):
        #vector_fechaspagos = transformar_fechaspago_dp()
        return self.fecha_pagos

    def getNroComercio(self, banco):
        datos_archivo_config = ArchivoConfig()
        vec_claves_tag, vec_valores = datos_archivo_config.leer_ini_valores_tags_variables(banco)

        return vec_valores[0]


    def calculo_nro_registro_ycontrol(self, banco):
        registros_ycontrol = []
        for numero in range(len(self.boletas)):
            registros_ycontrol.append(numero + 1)
            #print(registros_ycontrol)
        return registros_ycontrol
    
    def calculo_nro_registro_x_codbarras(self):
        registros = []
        for numero in range(len(self.codbarra1)):
            registros.append(numero + 1)
        return registros
    
    def getNroControl(self, banco): # esto es para 079 y 083 que siempre es un nro fijo, para los demas entes siempre es un numero incremental según la cantidad de boletas ingresadas
        datos_archivo_config = ArchivoConfig()
        vec_claves_tag, vec_valores = datos_archivo_config.leer_ini_valores_tags_variables(banco)

        return vec_valores[2]

    def comision_x_ente(self, banco, cantcuotas):
        #print('PRINTEO COMISIONXENTE: ', datos_general)
        #instancia_general = GeneralInput(datos_general)
        
        #vector_comisiones = Ventana.calcular_comisiones()
        banco = banco
        comisiones_archivo_conf = ComisionesArchivo()
        comisiones_ok, vector_comisiones = comisiones_archivo_conf.calcular_comisiones(banco, cantcuotas)
        #print('BANCO CMISION X ENTE' ,banco)
        #for valor_cuota in cantcuotas:
        #    #print(valor_cuota)
        #    if banco == '00935': #cordobesa
        #        comision = 0.01
        #        vector_comisiones.append(comision)
        #    elif (banco == '00216') and (valor_cuota == 'C' or valor_cuota == 'D'): #master
        #        comision = 0.01
        #        vector_comisiones.append(comision)
        #    elif banco == '00202' and valor_cuota == 'C': #visa
        #        comision = 0.01
        #        vector_comisiones.append(comision)
        #    elif banco == '00202' and valor_cuota == 'D': #visa
        #        comision = 0.0035
        #        vector_comisiones.append(comision)
        ##print(vector_comisiones)
        return vector_comisiones

    def calculo_comision_iva_x_dp(self, banco, cantcuotas):
        vector_importes_x_dp = self.getImporte(banco, cantcuotas)
        vector_comision_ente = self.comision_x_ente(banco, cantcuotas) #Ventana.calcular_comisiones() #self.comision_x_ente(banco, cantcuotas)
        #print('comision ente', comision_ente)
        comisiones = []
        ivas = []
        comision = 0
        iva = 0
        for indice in range(len(vector_importes_x_dp)):
            comision = "{0:.2f}".format(float(vector_importes_x_dp[indice]) * float(vector_comision_ente[indice]))
            iva = "{0:.2f}".format(float(comision) * 0.21)    
            comisiones.append(comision)
            ivas.append(iva)
        return comisiones, ivas
    
    def extraer_obligacion_codbarra1(self):
        obligaciones = []
        for obligacion in self.codbarra1:
            obligaciones.append(obligacion[22:42])  #32:36-36:38-38:40
        return obligaciones
    
    def extraer_fechaVenc_codbarra2(self):
        fechasVenc = []
        for fecha in self.codbarra2:
            fechasVenc.append(fecha[10:18])  #32:36-36:38-38:40
        return fechasVenc
    
    def extraer_objImponible_codbarra2(self):
        obj_imponibles = []
        for obj in self.codbarra2:
            obj_imponibles.append(obj[18:30])  #32:36-36:38-38:40
        return obj_imponibles
    
    def extraer_nroLiquidacion_codbarra1(self): #boletas
        nro_boleta = []
        for boleta in self.codbarra1:
            nro_boleta.append(boleta[3:19])  #32:36-36:38-38:40
        return nro_boleta
    
    def extraer_importe_codbarra2(self):
        importes = []
        importe = 0
        #print("cod barra2",self.codbarra2)
        for numero in self.codbarra2:
            #print(numero[30:40])
        
            importe += float(str(numero[30:40]))
            #print(importe)

            importe_final = importe/100 #de excel
            importes.append(importe_final)
            importe = 0

        return importes
    
    def extraer_fechaVenc_codbarra2(self):
        fechas_vencimiento = []
        for fecha in self.codbarra2:
            fechas_vencimiento.append(str(fecha[14:18]) + "-" + str(fecha[12:14]) +  "-" + str(fecha[10:12])) 
        return fechas_vencimiento

    def getImpuestoEnte079y082(self):
        return self.impuesto
    
    def getCodBarra1(self):
        return self.codbarra1
    
    def getCodBarra2(self):
        return self.codbarra2
    
