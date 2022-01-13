import random

from clase_dp_bpc import DetallePagoBPC


vector = []

class GeneralBPC():
    
    def __init__(self, fecha_rendicion):
        self.imp_recaudado = '0.0'
        self.imp_depositado = '0.0'
        self.imp_a_depositar = '0.0'
        self.fecha_rendicion = fecha_rendicion
        
    
    #Getters
    def getBanco(self):
        banco = "00001"
        return banco 
    
    def getFechaRendicion(self):
        return self.fecha_rendicion


    def getImpRecaudado(self):
        return self.imp_recaudado

    def getImpDepositado(self):
        return self.imp_depositado

    def getImpADepositar(self):
        return self.imp_a_depositar

    def getCbuCuits(self):
        self.cbu_origen = '0000000000000000000000'
        self.cuit_origen = '00000000000'
        self.cbu_destino = '0000000000000000000000'
        self.cuit_destino = '00000000000'

        return self.cbu_origen, self.cuit_origen, self.cbu_destino, self.cuit_destino

    def generar_nro_rendicion(self):
        self.nro_rendicion = random.randint(000000,999999)
        return self.nro_rendicion


    def calcular_cant_registros(self, codbarra1):
        #
        vector_cod_barras = codbarra1 #vector de boletas
        cantidad_registros = 0
        for cantidad in range(len(vector_cod_barras)): #por cada boleta en el vector, sumo 1
            cantidad_registros += 1
        return cantidad_registros

    def calcular_importe_determinado_y_pagado(self, codbarra1, codbarra2): ##para pagos presenciales
        dp_bpc = DetallePagoBPC(codbarra1, codbarra2)
        importes = dp_bpc.getImporte()
        suma_importes = 0
        for importe in importes:
            suma_importes += float(importe)
            suma_imp_dos_decimales = round(suma_importes, 2)
        return suma_imp_dos_decimales


    def calcular_total_comision_iva(self):
        comision = "0.0"
        iva = "0.0"

        return comision, iva


    def calcular_importe_recaudado(self, codbarra1, codbarra2): #para pagos electronicos
        dp_bpc = DetallePagoBPC(codbarra1, codbarra2)
        importes = dp_bpc.getImpRecaudadoBoletaER()
        suma_importes = 0
        for importe in importes:
            suma_importes += float(importe)
            suma_imp_dos_decimales = round(suma_importes, 2)
        return suma_imp_dos_decimales

    def calcular_importe_depositado_adepositar(self, codbarra1, codbarra2): #para pagos electronicos
        dp_bpc = DetallePagoBPC(codbarra1, codbarra2)
        importes = dp_bpc.getImpADepositarYDepositadoER()
        suma_importes = 0
        for importe in importes:
            suma_importes += float(importe)
            suma_imp_dos_decimales = round(suma_importes, 2)
        return suma_imp_dos_decimales
    

    #losmetodos que siguen son para cuando se elije ambos pagos
    def calcular_imp_determinado_pagado_presencial(self, codbarra1, codbarra2, tipopago):
        dp_bpc = DetallePagoBPC(codbarra1, codbarra2)
        importes = dp_bpc.calcular_imp_determinado_pagado(tipopago)
        suma_importes = 0
        for importe in importes:
            suma_importes += float(importe)
            suma_imp_dos_decimales = round(suma_importes, 2)
        return suma_imp_dos_decimales
    
    def calcular_imp_recaudado_depositado_adepositar_electronico(self, codbarra1, codbarra2, tipopago):
        dp_bpc = DetallePagoBPC(codbarra1, codbarra2)
        importes_rec, importes_dep = dp_bpc.calcular_imp_recaudado_depositado_adepostar(tipopago)
        suma_importes_rec = 0
        suma_importes_dep = 0

        for importe in importes_rec:
            suma_importes_rec += float(importe)
            suma_imp_dos_decimales_rec = round(suma_importes_rec, 2)
        
        for importe in importes_dep:
            suma_importes_dep += float(importe)
            suma_imp_dos_decimales_dep = round(suma_importes_dep, 2)

        return suma_imp_dos_decimales_rec, suma_imp_dos_decimales_dep
    
    
    def calcular_registros(self, tipopago):
        contador_registros_detpag = 0
        contador_registros_detdep = 0
        for numero in range(len(tipopago)):
            if tipopago[numero] == "P":
                contador_registros_detpag += 1
            elif tipopago[numero] == "E":
                contador_registros_detdep += 1

        return contador_registros_detpag, contador_registros_detdep
 