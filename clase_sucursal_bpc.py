from clase_dp_bpc import DetallePagoPresencialBPC, DetallePagoElectronicoBPC


class SucursalBPC():
    def __init__(self):
        self.sucursal = '1'
        self.imp_recaudado = '0.0'
        self.imp_depositado = '0.0'
        self.imp_a_depositar = '0.0'


    #Getters
    def getSucursal(self):
        return self.sucursal

    def getImpRecaudado(self):
        return self.imp_recaudado

    def getImpDepositado(self):
        return self.imp_depositado

    def getImpADepositar(self):
        return self.imp_a_depositar

    def calcular_cant_registros(self, codbarra1):
        vector_cod_barras = codbarra1 #vector de boletas
        cantidad_registros = 0
        for cantidad in range(len(vector_cod_barras)): #por cada boleta en el vector, sumo 1
            cantidad_registros += 1
        return cantidad_registros


    def calcular_importe_determinado_y_pagado(self, codbarra1, codbarra2): #pagos presenciales
        dp_bpc = DetallePagoPresencialBPC(codbarra1, codbarra2)
        importes = dp_bpc.getImporte()
        suma_importes = 0
        for importe in importes:
            suma_importes += float(importe)
            suma_imp_dos_decimales = round(suma_importes, 2)
        return suma_imp_dos_decimales
        


    def calcular_total_comision_iva_sucursal(self):
        comision = "0.0"
        iva = "0.0"

        return comision, iva

    
    def calcular_importe_recaudado_sucursal(self, codbarra1, codbarra2): #para pagos electronicos
        dp_bpc = DetallePagoElectronicoBPC(codbarra1, codbarra2)
        importes = dp_bpc.getImpRecaudadoBoletaER()
        suma_importes = 0
        for importe in importes:
            suma_importes += float(importe)
            suma_imp_dos_decimales = round(suma_importes, 2)
        return suma_imp_dos_decimales

    def calcular_importe_depositado_adepositar_sucursal(self, codbarra1, codbarra2): #para pagos electronicos
        dp_bpc = DetallePagoElectronicoBPC(codbarra1, codbarra2)
        importes = dp_bpc.getImpADepositarYDepositadoER()
        suma_importes = 0
        for importe in importes:
            suma_importes += float(importe)
            suma_imp_dos_decimales = round(suma_importes, 2)
        return suma_imp_dos_decimales
