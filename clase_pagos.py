from clase_dp import DetallePagoOutput
from lectura_archivo_config import ArchivoConfig

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
        datos_arc_conf = ArchivoConfig()
        vec_claves_tag, vec_valores = datos_arc_conf.leer_ini_valores_tags_variables(banco)

        return vec_valores[1]


    def calcular_cant_registros_pagos(self, boletas):
        #
        vector_boletas = boletas
        #print("BOLETAS: ", vector_boletas)
        cantidad_registros = 0
        for cantidad in range(len(vector_boletas)):
            cantidad_registros += 1
            #print("REGISTROS: ", cantidad_registros)
        return cantidad_registros

    def calcular_importe_determinado_y_pagado(self, banco, importes, cantcuotas, codbarra2):
        suma_importes = 0
        if banco == '00935': #solo para cordobesa hay que dividir el importe ingresado en la cant cuotas
            for indice in range(len(importes)):
                suma_importes += (float(importes[indice]) / float(cantcuotas[indice]))
                #print(suma_importes)
            suma_imp_dos_decimales = "{0:.2f}".format(suma_importes)
        
        elif banco == '00079' or banco == '00082':
            for importe in codbarra2:
                suma_importes += float(float(importe[30:40]) / 100) #VER EN FUNCION EXTRAER_IMPORTE_CODBARRA2 EN DP
            suma_imp_dos_decimales = "{0:.2f}".format(suma_importes)
        
        else:
            for importe in importes:
                suma_importes += float(importe)
                #print(suma_importes)
            suma_imp_dos_decimales = "{0:.2f}".format(suma_importes)
        return suma_imp_dos_decimales

    def calcular_total_comision_iva_pagos(self, decision_comision, comision_deb, comision_cred, comision_pres, banco, boletas, fechapagos, importes, cuotaactual, cantcuotas, codbarra1, codbarra2):
        dp = DetallePagoOutput(banco, boletas, fechapagos, importes, cuotaactual, cantcuotas, codbarra1, codbarra2)
        valores_comisiones, valores_iva = dp.calculo_comision_iva_x_dp(decision_comision, comision_deb, comision_cred, comision_pres, banco, cantcuotas)
        sumatoria_comision = 0
        sumatoria_iva = 0
        for valor_com in valores_comisiones:
            sumatoria_comision += round(float(valor_com),2)
            sumatoria_comision_redondeo = "{0:.2f}".format(sumatoria_comision)


        for valor_iva in valores_iva:
            sumatoria_iva += round(float(valor_iva),2)
            sumatoria_iva_redondeo = "{0:.2f}".format(sumatoria_iva)
        return sumatoria_comision_redondeo, sumatoria_iva_redondeo

