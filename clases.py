import xml.etree.ElementTree as ET
from lectura_archivo import leer_archivo
from func_rellenar_clases import rellenar_clase_detallepago_input, rellenar_clase_general_input, transformar_datos_detallepago


class GeneralInput():
    def __init__(self):
        self.banco, self.fecha_rendicion = rellenar_clase_general_input()

    #Getters
    def getBanco(self):
        return self.banco
    
    def getFechaRendicion(self):
        return self.fecha_rendicion
    
    #Setters
    def setBanco(self, bancoX):
        self.banco = bancoX

    def setFechaRendicion(self, fecha_rendicionX):
        self.fecha_rendicion = fecha_rendicionX
    

    

class GeneralOutput(GeneralInput):
    def __init__(self):
        super().__init__()
        self.imp_recaudado = 0.00
        self.imp_depositado = 0.00
        self.imp_a_depositar = 0.00
        self.calcular_cbus_y_cuits()

    
    #Getters
    def getImpRecaudado(self):
        return self.imp_recaudado
    
    def getImpDepositado(self):
        return self.imp_depositado
    
    def getImpADepositar(self):
        return self.imp_a_depositar
    
    def calcular_cbus_y_cuits(self):
        if self.banco  == '00935':
            self.cbu_origen = '0200925801000040012697'
            self.cuit_origen = 30999256712
            self.cbu_destino = '0200900501000000402265'
            self.cuit_destino = 34999230573
        return self.cbu_origen, self.cuit_origen, self.cbu_destino, self.cuit_destino

    def generar_nro_transaccion(self):
        pass

    def generar_nro_rendicion(self):
        pass
    
    def transformar_fecha(self):
        self.fecha_rendicion = self.fecha_rendicion[6:10] + self.fecha_rendicion[5] + self.fecha_rendicion[3:5] + self.fecha_rendicion[2] + self.fecha_rendicion[0:2]
        return self.fecha_rendicion
        
            
        

    def calcular_cant_registros(self):
        datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo()
        contador = 1
        #print(len(datos_detallepago))
        
        if datos_detallepago[7][0] != " ":
            contador += 1
        #print(contador)
        return contador
    
    def calcular_importe_determinado_y_pagado(self):
        datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo()
        suma = float(datos_detallepago[2][1])
        if datos_detallepago[6][0] != " ":
            suma = suma + float(datos_detallepago[8][1])
        return suma

    def calcular_total_comision(self):
        datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo()
        total_comision = float(datos_detallepago[2][1]) * 0.01
        if datos_detallepago[6][0] != " ":
            total_comision = round(total_comision + (float(datos_detallepago[8][1]) * 0.01), 2)
        return total_comision

    def calcular_iva(self):
        datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo()
        total_comision = float(datos_detallepago[2][1]) * 0.01
        if datos_detallepago[6][0] != " ":
            total_comision = round(total_comision + (float(datos_detallepago[8][1]) * 0.01), 2)
        iva = round(total_comision * 0.21, 2)
        return iva
    
    def informes_general(self):
        datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo()
        suma_total = 'Sumatoria de importes de los detallepago ingresados: ' + str(datos_detallepago[2][1]) + ' + ' + str(datos_detallepago[8][1])
        comision_total = 'La comision total es igual a: (' + str(datos_detallepago[2][1]) + '* 0.01)' + ' + (' + str(datos_detallepago[8][1]) + '* 0.01)'
        #iva_total = 'Iva total es igual a: ' + str(round(float(comision_total),2)) + ' * ' + '0.21'
        #print(suma_total)
        #print(comision_total)
        #print(iva_total)
        return suma_total, comision_total


class SucursalOutput():
    def __init__(self):
        self.sucursal = '001'
        self.imp_recaudado = 0.00
        self.imp_depositado = 0.00
        self.imp_a_depositar = 0.00

    
    #Getters
    def getSucursal(self):
        return self.sucursal
    
    def getImpRecaudado(self):
        return self.imp_recaudado
    
    def getImpDepositado(self):
        return self.imp_depositado
    
    def getImpADepositar(self):
        return self.imp_a_depositar
            
    def calcular_cant_registros(self):
        datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo()
        contador = 1
        #print(len(datos_detallepago))
        
        if datos_detallepago[7][0] != " ":
            contador += 1
        #print(contador)
        return contador
    
    def calcular_importe_determinado_y_pagado(self):
        datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo()
        suma = float(datos_detallepago[2][1])
        if datos_detallepago[6][0] != " ":
            suma = suma + float(datos_detallepago[8][1])
        return suma

    def calcular_total_comision(self):
        datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo()
        total_comision = float(datos_detallepago[2][1]) * 0.01
        if datos_detallepago[6][0] != " ":
            total_comision = round(total_comision + (float(datos_detallepago[8][1]) * 0.01), 2)
        return total_comision

    def calcular_iva(self):
        pass
        


class PagosOutput():
    def __init__(self):
        self.cod_registro = '021'
        self.caja = '0000'
        self.cajero = '000000'
        self.lote = '2'

    
    #Getters
    def getCodRegistro(self):
        return self.cod_registro
    
    def getCaja(self):
        return self.caja
    
    def getCajero(self):
        return self.cajero
    
    def getLote(self):
        return self.lote
            
    def calcular_cant_registros(self):
        datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo()
        contador = 1
        #print(len(datos_detallepago))
        
        if datos_detallepago[7][0] != " ":
            contador += 1
        #print(contador)
        return contador
    
    def calcular_importe_determinado_y_pagado(self):
        datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo()
        suma = float(datos_detallepago[2][1])
        if datos_detallepago[6][0] != " ":
            suma = suma + float(datos_detallepago[8][1])
        return suma

    def calcular_total_comision(self):
        datos_generales, datos_sucursal, datos_pagos, datos_detallepago = leer_archivo()
        total_comision = float(datos_detallepago[2][1]) * 0.01
        if datos_detallepago[6][0] != " ":
            total_comision = round(total_comision + (float(datos_detallepago[8][1]) * 0.01), 2)
        return total_comision

    def calcular_iva(self):
        pass


class DetallePagoInput():
    def __init__(self):
        vector_dp_input = rellenar_clase_detallepago_input()
        #print(vector_dp_input)


    #Getters
    def getNroBoleta(self):
        return self.nro_boleta
    
    def getFechaPago(self):
        return self.fecha_pago
    
    def getImporte(self):
        return self.importe
    
    def getCantCuotas(self):
        return self.cant_cuotas

    def getIdObjImponible(self):
        return self.id_obj_imponible

    def getObligacion(self):
        return self.obligacion    


class Generador():
    def generar_xml(self):
        try:
            instancia_general_output = GeneralOutput()
            instancia_sucursal_output = SucursalOutput()
            instancia_pagos_output = PagosOutput()

            banco = instancia_general_output.getBanco()
            fecha_rendicion = instancia_general_output.transformar_fecha()
            cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.calcular_cbus_y_cuits()
            cant_registros = instancia_general_output.calcular_cant_registros()
            imp_pagado = instancia_general_output.calcular_importe_determinado_y_pagado()
            imp_determinado = instancia_general_output.calcular_importe_determinado_y_pagado()
            imp_recaudado = instancia_general_output.getImpRecaudado()
            imp_depositado = instancia_general_output.getImpDepositado()
            imp_a_depositar = instancia_general_output.getImpADepositar()
            total_comision = instancia_general_output.calcular_total_comision()
            total_iva = instancia_general_output.calcular_iva()
            informe_suma, informe_comision = instancia_general_output.informes_general()


            sucursal = instancia_sucursal_output.getSucursal()
            cant_registros_sucursal = instancia_sucursal_output.calcular_cant_registros()
            imp_pagado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado()
            imp_determinado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado()
            imp_recaudado_sucursal = instancia_sucursal_output.getImpRecaudado()
            imp_depositado_sucursal = instancia_sucursal_output.getImpDepositado()
            imp_a_depositar_sucursal = instancia_sucursal_output.getImpADepositar()
            total_comision_sucursal = instancia_sucursal_output.calcular_total_comision()
            #total_iva = instancia_sucursal_output.calcular_iva()


            cod_registro = instancia_pagos_output.getCodRegistro()
            caja = instancia_pagos_output.getCaja()
            cajero = instancia_pagos_output.getCajero()
            lote = instancia_pagos_output.getLote()
            cant_registros_pagos = instancia_pagos_output.calcular_cant_registros()
            imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado()
            imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado()
            total_comision_pagos = instancia_pagos_output.calcular_total_comision()
            #total_iva_pagos = instancia_pagos_output.calcular_iva()


            
            #generando estructura xml con los campos
            general = ET.Element("General",totalImpIVA = str(total_iva), totalImpComision = str(total_comision), 
                                    totalImpRecaudado = str(imp_recaudado), totalImpDemositado = str(imp_depositado),
                                    totalImpADepositar = str(imp_a_depositar), totalImpPagado = str(imp_pagado), 
                                    totalImpDeterminado = str(imp_determinado), registros = str(cant_registros), 
                                    cuitDestino = str(cuit_destino), cbuDestino = str(cbu_destino), cuitOrigen = str(cuit_origen), cbuOrigen = str(cbu_origen),
                                    fechaRendicion = fecha_rendicion, nroRendicion = "123", nroTransaccion = "0", banco = banco)
            
            sucursal = ET.SubElement(general,"Sucursal", totalImpIVA = "None", totalImpComision = str(total_comision_pagos), 
                                    totalImpRecaudado = str(imp_recaudado_sucursal), totalImpDemositado = str(imp_depositado_sucursal),
                                    totalImpADepositar = str(imp_a_depositar_sucursal), totalImpPagado = str(imp_pagado_sucursal), 
                                    totalImpDeterminado = str(imp_determinado_sucursal), registros = str(cant_registros_sucursal), sucursal = sucursal)
                                    
            pagos = ET.SubElement(sucursal,"Pagos", totalImpIVA = "None", totalImpComision = str(total_comision_pagos), 
                                    totalImpPagado = str(imp_pagado_pagos), 
                                    totalImpDeterminado = str(imp_determinado_pagos), registros = str(cant_registros_pagos),
                                    lote = lote, cajero = cajero, caja = caja, codRegistro = cod_registro)
                                    
            det_pago = ET.SubElement(pagos,"DetallePago").text = ' '
            comentario_suma_general = ET.Comment(informe_suma)  
            comentario_comision_general = ET.Comment(informe_comision)  
            general.insert(0, comentario_suma_general)
            general.insert(0, comentario_comision_general)
            tree = ET.ElementTree(general)
            tree.write('prueba.xml', xml_declaration=True, encoding='utf-8')
             

        except (TypeError, AttributeError, SystemError):
            print("Error al generar xml")