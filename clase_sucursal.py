from clase_dp import DetallePagoOutput

class SucursalOutput():
    def __init__(self):
        self.sucursal = '001'
        self.imp_recaudado = '0.00'
        self.imp_depositado = '0.00'
        self.imp_a_depositar = '0.00'


    #Getters
    def getSucursal(self, banco):
        if banco == '00082':
            self.sucursal = '0001'
        elif banco == '00079':
            self.sucursal = '1011'
        else:
            self.sucursal

        return self.sucursal

    def getImpRecaudado(self, banco):
        if banco == "00079":
            imp_recaudado = "000000000000"
        elif banco == "00082":
            imp_recaudado = "0"
        else:
            imp_recaudado = self.imp_recaudado

        return imp_recaudado

    def getImpDepositado(self, banco):
        if banco == "00079":
            imp_depositado = "000000000000"
        elif banco == "00082":
            imp_depositado = "0"
        else:
            imp_depositado = self.imp_depositado

        return imp_depositado

    def getImpADepositar(self, banco):
        if banco == "00079":
            imp_adepositar = "000000000000"
        elif banco == "00082":
            imp_adepositar = "0"
        else:
            imp_adepositar = self.imp_a_depositar

        return imp_adepositar
    
    def getImpAnulacionTim(self, banco):
        if banco == "00079":
            total_imp_anul_timbradoras = "000000000000"
        elif banco == "00082":
            total_imp_anul_timbradoras = "0"
        return total_imp_anul_timbradoras



    def calcular_cant_registros(self, boletas):
        #
        vector_boletas = boletas
        cantidad_registros = 0
        for cantidad in range(len(vector_boletas)):
            cantidad_registros += 1
        return cantidad_registros


    def calcular_importe_determinado_y_pagado(self, banco, importes, cantcuotas, codbarra2):
        suma_importes = 0
        if banco == '00935': #solo para cordobesa hay que dividir el importe ingresado en la cant cuotas
            for indice in range(len(importes)):
                suma_importes += (float(importes[indice]) / float(cantcuotas[indice]))
            suma_imp_dos_decimales = "{0:.2f}".format(suma_importes)
        
        elif banco == '00079' or banco == '00082':
            for importe in codbarra2:
                suma_importes += float(float(importe[30:40]) / 100) #VER EN FUNCION EXTRAER_IMPORTE_CODBARRA2 EN DP
            suma_imp_dos_decimales = "{0:.2f}".format(suma_importes)
        
        else:
            for importe in importes:
                suma_importes += float(importe)
            suma_imp_dos_decimales = "{0:.2f}".format(suma_importes)
        return suma_imp_dos_decimales
        


    def calcular_total_comision_iva_sucursal(self, banco, boletas, fechapagos, importes, cuotaactual, cantcuotas, codbarra1, codbarra2):
        dp = DetallePagoOutput(banco, boletas, fechapagos, importes, cuotaactual, cantcuotas, codbarra1, codbarra2)
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
