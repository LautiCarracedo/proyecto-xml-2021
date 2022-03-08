import random

from logica_negocio_entes.clase_dp import DetallePagoOutput

vector = []

class GeneralInput():
    
    def __init__(self, banco, fecha_rendicion):
        vector.append(banco)
        vector.append(fecha_rendicion)
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


    #Getters
    def getImpRecaudado(self):
        return self.imp_recaudado

    def getImpDepositado(self):
        return self.imp_depositado

    def getImpADepositar(self):
        return self.imp_a_depositar

    def calcular_cbus_y_cuits(self):
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

    def calcular_importe_determinado_y_pagado(self, banco, importes, cantcuotas):
        suma_importes = 0
        if banco == '00935': #solo para cordobesa hay que dividir el importe ingresado en la cant cuotas
            for indice in range(len(importes)):
                suma_importes += (float(importes[indice]) / float(cantcuotas[indice]))
            suma_imp_dos_decimales = "{0:.2f}".format(suma_importes)
        
        else:
            for importe in importes:
                suma_importes += float(importe)
            suma_imp_dos_decimales = "{0:.2f}".format(suma_importes)
        return suma_imp_dos_decimales

    


    def calcular_total_comision_iva(self, banco, boletas, fechapagos, importes, cuotaactual, cantcuotas):
        dp = DetallePagoOutput(banco, boletas, fechapagos, importes, cuotaactual, cantcuotas)
        valores_comisiones, valores_iva = dp.calculo_comision_iva_x_dp(self.banco, cantcuotas)
        sumatoria_comision = 0
        sumatoria_iva = 0
        for valor_com in valores_comisiones:
            sumatoria_comision += round(float(valor_com),2)
            sumatoria_comision_redondeo = "{0:.2f}".format(sumatoria_comision)


        sumatoria_iva += round(float(sumatoria_comision_redondeo) * 0.21,2)
        iva_redondeo = "{0:.2f}".format(sumatoria_iva) 

        return sumatoria_comision_redondeo, iva_redondeo



    def informes_general(self, banco, boletas, fechapagos, importes, cuotaactual, cantcuotas):
        dp = DetallePagoOutput(banco, boletas, fechapagos, importes, cuotaactual, cantcuotas)
        vector_comisiones, vector_ivas = dp.calculo_comision_iva_x_dp(banco, cantcuotas)
        vector_importes = dp.getImporte(banco, cantcuotas) #los importes ingresados en la interfaz, los guardo aca para calcular la division x el nrocuotas (que es el valor que debes salir en el xml)
        vector_importes_ingresados = importes #son los importes que se ingresan en la interfaz
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
        importes_dp_ing = 'Importes ingresados de cada boleta: ' + str(vector_importes_ingresados)
        importes_dp_calc = 'Importes calculados de cada boleta (importe ingresado / cantcuotas): ' + str(vector_importes)
        suma_total = 'Sumatoria de los importes de todas las boletas: $ ' + str(suma_importes)
        comisiones_dp = 'Comisiones de cada importe: ' + str(vector_comisiones)
        comision_total = 'La comision total es igual a $: ' + str(comision_redondeo)
        iva_tag_general = 'El iva a nivel del tag general es igual a la comisión total x 0.21, es decir = ' + str(comision_redondeo) + 'x 0.21 = ' + str(iva_general)
        ivas_dp = 'Iva de cada importe (comision de cada importe x 0.21):' + str(vector_ivas)
        ivas_total = 'El iva total es igual a $: ' + str(iva_redondeo)

        return importes_dp_ing, importes_dp_calc, suma_total, comisiones_dp, comision_total, ivas_dp, ivas_total, cant_registros, iva_tag_general