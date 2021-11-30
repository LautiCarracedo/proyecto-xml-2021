
import random

vector = []

class GeneralInput():
    
    def __init__(self, banco, fecha_rendicion):
        vector.append(banco)
        vector.append(fecha_rendicion)
        #print('VECTPR GEMERAL CL;ASSEl ', vector)
        #print(len(vector))
        self.banco = banco
        self.fecha_rendicion = fecha_rendicion
        
    
    #Getters
    def getBanco(self):
        #print('BANCO CLASE: ',self.banco)
        return self.banco  
    
    def getFechaRendicion(self):
        #print('FECHA CLASE: ',self.fecha_rendicion)
        return self.fecha_rendicion



class GeneralOutput(GeneralInput):
    def __init__(self, banco, fecha_rendicion):
        super().__init__(banco, fecha_rendicion)
        self.imp_recaudado = '0.00'
        self.imp_depositado = '0.00'
        self.imp_a_depositar = '0.00'
        self.calcular_cbus_y_cuits()


    #Getters
    def getImpRecaudado(self):
        return self.imp_recaudado

    def getImpDepositado(self):
        return self.imp_depositado

    def getImpADepositar(self):
        return self.imp_a_depositar

    def calcular_cbus_y_cuits(self):
        if self.banco  == '00935' or self.banco == '00202' or self.banco == '00216':
            self.cbu_origen = '0200925801000040012697'
            self.cuit_origen = 30999256712
            self.cbu_destino = '0200900501000000402265'
            self.cuit_destino = 34999230573

        return self.cbu_origen, self.cuit_origen, self.cbu_destino, self.cuit_destino

    def generar_nro_rendicion(self):
        self.nro_rendicion = random.randint(00000,99999)
        return self.nro_rendicion



    def calcular_cant_registros(self, boletas):
        #
        vector_boletas = boletas #vector de boletas
        cantidad_registros = 0
        for cantidad in range(len(vector_boletas)): #por cada boleta en el vector, sumo 1
            cantidad_registros += 1
        return cantidad_registros

    def calcular_importe_determinado_y_pagado(self, importes):
        #
        suma_importes = 0
        for valor_importes in importes:
            suma_importes += float(valor_importes)
        suma_imp_dos_decimales = "{0:.2f}".format(suma_importes)
        return suma_imp_dos_decimales

    def calcular_total_comision_iva(self, banco, boletas, fechapagos, importes, cuotaactual, cantcuotas):
        dp = DetallePagoOutput(banco, boletas, fechapagos, importes, cuotaactual, cantcuotas)
        valores_comisiones, valores_iva = dp.calculo_comision_iva_x_dp(importes, self.banco)
        sumatoria_comision = 0
        sumatoria_iva = 0
        for valor_com in valores_comisiones:
            sumatoria_comision += float(valor_com)
            sumatoria_comision_redondeo = "{0:.2f}".format(sumatoria_comision)


        sumatoria_iva += float(sumatoria_comision_redondeo) * 0.21
        iva_redondeo = "{0:.2f}".format(sumatoria_iva) 

        return sumatoria_comision_redondeo, iva_redondeo



    def informes_general(self, banco, boletas, fechapagos, importes, cuotaactual, cantcuotas):
        dp = DetallePagoOutput(banco, boletas, fechapagos, importes, cuotaactual, cantcuotas)
        vector_comisiones, vector_ivas = dp.calculo_comision_iva_x_dp(importes, banco)
        #
        vector_importes = importes
        suma_importes = 0
        suma_comision = 0
        suma_iva = 0
        iva_general = 0
        for importe in vector_importes:
            suma_importes += float(importe)

        for comision in vector_comisiones:
            suma_comision += float(comision)
            comision_redondeo = "{0:.2f}".format(suma_comision)
        iva_general += float("{0:.2f}".format(float(comision_redondeo) * 0.21))

        for ivas in vector_ivas:
            suma_iva += float(ivas)
            iva_redondeo = "{0:.2f}".format(suma_iva)

        cant_registros = 'Cantidad de registros es igual a cantidad de boletas ingresadas: ' + str(len(vector_importes))
        importes_dp = 'Importes ingresados de cada boleta: ' + str(vector_importes)
        suma_total = 'Sumatoria de los importes de todas las boletas: $ ' + str(suma_importes)
        comisiones_dp = 'Comisiones de cada importe: ' + str(vector_comisiones)
        comision_total = 'La comision total es igual a $: ' + str(comision_redondeo)
        iva_tag_general = 'El iva a nivel del tag general es igual a la comisión total x 0.21, es decir = ' + str(comision_redondeo) + 'x 0.21 = ' + str(iva_general)
        ivas_dp = 'Iva de cada importe (comision de cada importe x 0.21):' + str(vector_ivas)
        ivas_total = 'El iva total es igual a $: ' + str(iva_redondeo)

        return importes_dp, suma_total, comisiones_dp, comision_total, ivas_dp, ivas_total, cant_registros, iva_tag_general


class SucursalOutput():
    def __init__(self):
        self.sucursal = '001'
        self.imp_recaudado = '0.00'
        self.imp_depositado = '0.00'
        self.imp_a_depositar = '0.00'


    #Getters
    def getSucursal(self):
        return self.sucursal

    def getImpRecaudado(self):
        return self.imp_recaudado

    def getImpDepositado(self):
        return self.imp_depositado

    def getImpADepositar(self):
        return self.imp_a_depositar

    def calcular_cant_registros(self, boletas):
        #
        vector_boletas = boletas
        cantidad_registros = 0
        for cantidad in range(len(vector_boletas)):
            cantidad_registros += 1
        return cantidad_registros


    def calcular_importe_determinado_y_pagado(self, importes):
        #
        vector_importes = importes
        suma_importes = 0
        for importe in vector_importes:
            suma_importes += float(importe)
        return suma_importes

    def calcular_total_comision_iva_sucursal(self, banco, boletas, fechapagos, importes, cuotaactual, cantcuotas):
        dp = DetallePagoOutput(banco, boletas, fechapagos, importes, cuotaactual, cantcuotas)
        #print('DP:',dp)
        valores_comisiones, valores_iva = dp.calculo_comision_iva_x_dp(importes, banco)
        sumatoria_comision = 0
        sumatoria_iva = 0
        for valor_com in valores_comisiones:
            sumatoria_comision += float(valor_com)
            sumatoria_comision_redondeo = "{0:.2f}".format(sumatoria_comision)

        for valor_iva in valores_iva:
            sumatoria_iva += float(valor_iva)
            sumatoria_iva_redondeo = "{0:.2f}".format(sumatoria_iva)

        return sumatoria_comision_redondeo, sumatoria_iva_redondeo



class PagosOutput():
    def __init__(self, banco):
        self.cod_registro = '021'
        self.caja = '0000'
        self.cajero = '000000'
        self.lote = banco


    #Getters
    def getCodRegistro(self):
        return self.cod_registro

    def getCaja(self):
        return self.caja

    def getCajero(self):
        return self.cajero

    def getLote(self, banco):
        if banco == '00202' or banco == '00216':
            self.lote = '1'
        else:
            self.lote = '2'
        return self.lote

    def calcular_cant_registros_pagos(self, boletas):
        #
        vector_boletas = boletas
        #print("BOLETAS: ", vector_boletas)
        cantidad_registros = 0
        for cantidad in range(len(vector_boletas)):
            cantidad_registros += 1
            #print("REGISTROS: ", cantidad_registros)
        return cantidad_registros

    def calcular_importe_determinado_y_pagado(self, importes):
        #
        vector_importes = importes
        suma_importes = 0
        for importe in vector_importes:
            suma_importes += float(importe)
        return suma_importes

    def calcular_total_comision_iva_pagos(self, banco, boletas, fechapagos, importes, cuotaactual, cantcuotas):
        dp = DetallePagoOutput(banco, boletas, fechapagos, importes, cuotaactual, cantcuotas)
        valores_comisiones, valores_iva = dp.calculo_comision_iva_x_dp(importes, banco)
        sumatoria_comision = 0
        sumatoria_iva = 0
        for valor_com in valores_comisiones:
            sumatoria_comision += float(valor_com)
            sumatoria_comision_redondeo = "{0:.2f}".format(sumatoria_comision)


        for valor_iva in valores_iva:
            sumatoria_iva += float(valor_iva)
            sumatoria_iva_redondeo = "{0:.2f}".format(sumatoria_iva)

        return sumatoria_comision_redondeo, sumatoria_iva_redondeo


class DetallePagoInput():
    def __init__(self, boletas, fechapagos, importes, cuotaactual, cantcuotas):
        #
        self.boletas = boletas
        self.fecha_pagos = fechapagos
        self.importes = importes
        self.obj_imp = cuotaactual
        self.cuotas = cantcuotas

    #Getters
    def getDatos(self):
        return self.datos



class DetallePagoOutput(DetallePagoInput):
    def __init__(self, banco, boletas, fechapagos, importes, cuotaactual, cantcuotas):
        super().__init__(boletas, fechapagos, importes, cuotaactual, cantcuotas)
        self.cod_registro = '022'
        self.marca_movimiento = 'P'
        self.tipo_operacion = '01'
        self.tipo_rendicion = '01'
        self.moneda = '01'
        self.nro_comercio = banco

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

    def getImporte(self):
        #vector_importes = transformar_importes_dp()
        #print(vector_importes)
        return self.importes

    def getNroBoletas(self):
        #vector_nro_boletas = transformar_nroboletas_dp()
        return self.boletas

    def getCantCuotas(self):
        #vector_cuotas = transformar_cuotas_dp()
        return self.cuotas

    def getObjImponible(self):
        #vector_obj_imponible = transformar_objimponibles_dp()
        return self.obj_imp


    def getFechaPago(self):
        #vector_fechaspagos = transformar_fechaspago_dp()
        return self.fecha_pagos

    def getNroComercio(self, banco):
        if banco == '00935':
            self.nro_comercio = '27426748'
        elif banco == '00202':
            self.nro_comercio = '0023552656'
        elif banco == '00216':
            self.nro_comercio = '18236295'
        return self.nro_comercio

    def calculo_nro_registro_ycontrol(self):
        registros_ycontrol = []
        for numero in range(len(self.boletas)):
            registros_ycontrol.append(numero + 1)
            #print(registros_ycontrol)
        return registros_ycontrol

    def comision_x_ente(self, banco):
        #print('PRINTEO COMISIONXENTE: ', datos_general)
        #instancia_general = GeneralInput(datos_general)
        banco = banco
        #print('BANCO CMISION X ENTE' ,banco)

        if banco == '00935': #cordobesa
            comision = 0.01
        elif banco == '00216': #master
            comision = 0.01
        elif banco == '00202': #visa
            comision = 0.01

        return comision

    def calculo_comision_iva_x_dp(self, importes, banco):
        vector_importes_x_dp = importes
        comision_ente = self.comision_x_ente(banco)
        #print('comision ente', comision_ente)
        comisiones = []
        ivas = []
        comision = 0
        iva = 0
        for valor_importes in vector_importes_x_dp:
            comision = "{0:.2f}".format(float(valor_importes) * comision_ente)
            iva = "{0:.2f}".format(float(comision) * 0.21)    
            comisiones.append(comision)
            ivas.append(iva)
        return comisiones, ivas