from logica_negocio_entes.clase_dp import DetallePagoOutput

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
        


    def calcular_total_comision_iva_sucursal(self, banco, boletas, fechapagos, importes, cuotaactual, cantcuotas):
        dp = DetallePagoOutput(banco, boletas, fechapagos, importes, cuotaactual, cantcuotas)
        #print('DP:',dp)
        valores_comisiones, valores_iva = dp.calculo_comision_iva_x_dp(banco, cantcuotas)
        sumatoria_comision = 0
        sumatoria_iva = 0
        for valor_com in valores_comisiones:
            #print(valor_com)
            sumatoria_comision += round(float(valor_com),2)
            sumatoria_comision_redondeo = "{0:.2f}".format(sumatoria_comision)

        for valor_iva in valores_iva:
            #print(valor_iva)
            sumatoria_iva += round(float(valor_iva),2)
            sumatoria_iva_redondeo = "{0:.2f}".format(sumatoria_iva)

        #print(sumatoria_comision_redondeo)
        #print(sumatoria_iva_redondeo)
        return sumatoria_comision_redondeo, sumatoria_iva_redondeo
