from clase_dp_bpc import DetallePagoElectronicoBPC, DetallePagoPresencialBPC


class PagosBPC():
    def __init__(self, fecha_acreditacion):
        self.cod_registro = '021'
        self.caja = '0000'
        self.cajero = '000000'
        self.lote = '1'
        self.fecha_acreditacion = fecha_acreditacion


    #Getters
    def getCodRegistro(self, formapago):
        if formapago == "Pagos presenciales":
            self.cod_registro = '021'
        elif formapago == "Pagos electronicos":
            self.cod_registro = '031'
        return self.cod_registro

    def getCaja(self):
        return self.caja

    def getCajero(self):
        return self.cajero

    def getLote(self):
        return self.lote 
    
    def getFechaAcreditacion(self):
        return self.fecha_acreditacion

    def calcular_cant_registros_pagos(self, codbarra1):
        vector_cod_barras = codbarra1 
        cantidad_registros = 0
        for cantidad in range(len(vector_cod_barras)): #por cada boleta en el vector, sumo 1
            cantidad_registros += 1
        return cantidad_registros

    def calcular_importe_determinado_y_pagado(self, codbarra1, codbarra2):
        dp_bpc = DetallePagoPresencialBPC(codbarra1, codbarra2)
        importes = dp_bpc.getImporte()
        suma_importes = 0
        for importe in importes:
            suma_importes += float(importe)
            suma_imp_dos_decimales = round(suma_importes, 2)
        return suma_imp_dos_decimales

    def calcular_total_comision_iva_pagos(self):
        comision = "0.0"
        iva = "0.0"

        return comision, iva
    

    #para depositos (pagos electroncis)
    def calcular_imp_recaudado_depositos(self, codbarra1, codbarra2):
        dp_bpc = DetallePagoElectronicoBPC(codbarra1, codbarra2)
        importes = dp_bpc.getImpRecaudadoBoletaER()
        suma_importes = 0
        for importe in importes:
            suma_importes += float(importe)
            suma_imp_dos_decimales = round(suma_importes, 2)
        return suma_imp_dos_decimales

    def calcular_imp_depositado_y_depositar_deposito(self, codbarra1, codbarra2):
        dp_bpc = DetallePagoElectronicoBPC(codbarra1, codbarra2)
        importes = dp_bpc.getImpADepositarYDepositadoER()
        suma_importes = 0
        for importe in importes:
            suma_importes += float(importe)
            suma_imp_dos_decimales = round(suma_importes, 2)
        return suma_imp_dos_decimales