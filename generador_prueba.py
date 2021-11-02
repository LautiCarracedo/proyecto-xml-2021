import xml.etree.ElementTree as ET
from lectura_archivo import leer_archivo
from func_rellenar_clases import rellenar_clase_general_input


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
        try:
            self.imp_recaudado = 0.00
            self.imp_depositado = 0.00
            self.imp_a_depositar = 0.00
            self.calcular_cbus_y_cuits()
        except (AttributeError, TypeError):
            print("ERROR al crear general output")

    
    #Getters
    def getImpRecaudado(self):
        return self.imp_recaudado
    
    def getImpDepositado(self):
        return self.imp_depositado
    
    def getImpADepositar(self):
        return self.imp_a_depositar
    
    def calcular_cbus_y_cuits(self):
        try:
            if self.banco  == '00935':
                self.cbu_origen = '0200925801000040012697'
                self.cuit_origen = 30999256712
                self.cbu_destino = '0200900501000000402265'
                self.cuit_destino = 34999230573
            return self.cbu_origen, self.cuit_origen, self.cbu_destino, self.cuit_destino
        except (TypeError, AttributeError, SystemError):
            print("Error al calcular cbus y cuits. Ingresar bien el campo general.banco")

    def generar_nro_transaccion(self):
        pass

    def generar_nro_rendicion(self):
        pass
    
    def transformar_fecha(self):
        try:
            self.fecha_rendicion = self.fecha_rendicion[6:10] + self.fecha_rendicion[5] + self.fecha_rendicion[3:5] + self.fecha_rendicion[2] + self.fecha_rendicion[0:2]
            return self.fecha_rendicion
        except:
            print("Error al formatear fecha. Formato correcto: DD-MM-AAAA")
        
            
        

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
        print(suma_total)
        print(comision_total)
        #print(iva_total)
        return suma_total, comision_total

        


class Generador():
    def generar_xml(self):
        try:
            instancia_general_output = GeneralOutput()

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


            #return banco, fecha_rendicion, cbu_origen, cuit_origen, cbu_destino, cuit_destino, cant_registros, imp_pagado, imp_determinado, imp_recaudado, imp_depositado, imp_a_depositar, total_comision, total_iva

            
            #generando estructura xml con los campos
            general = ET.Element("General",totalImpIVA = str(total_iva), totalImpComision = str(total_comision), 
                                    totalImpRecaudado = str(imp_recaudado), totalImpDemositado = str(imp_depositado),
                                    totalImpADepositar = str(imp_a_depositar), totalImpPagado = str(imp_pagado), 
                                    totalImpDeterminado = str(imp_determinado), registros = str(cant_registros), 
                                    cuitDestino = str(cuit_destino), cbuDestino = str(cbu_destino), cuitOrigen = str(cuit_origen), cbuOrigen = str(cbu_origen),
                                    fechaRendicion = fecha_rendicion, nroRendicion = "123", nroTransaccion = "0", banco = banco)
            sucursal = ET.SubElement(general,"Sucursal")
            pagos = ET.SubElement(sucursal,"Pagos")
            det_pago = ET.SubElement(pagos,"DetallePago").text = ' '
            comentario_suma_general = ET.Comment(informe_suma)  
            comentario_comision_general = ET.Comment(informe_comision)  
            general.insert(0, comentario_suma_general)
            general.insert(0, comentario_comision_general)
            tree = ET.ElementTree(general)
            tree.write('prueba.xml', xml_declaration=True, encoding='utf-8')
             

        except (TypeError, AttributeError, SystemError):
            print("Error al generar xml")






generador = Generador()
generador.generar_xml()



try:
    instance_objeto_general_input = GeneralInput()
    instance_objeto_general = GeneralOutput()
    #no es necesario, es para ver la salida x consola mediante un vector
    vector_general = []
    vector_general = [instance_objeto_general.banco, 0,
                      instance_objeto_general.transformar_fecha(), 
                      instance_objeto_general.cbu_origen, instance_objeto_general.cuit_origen, instance_objeto_general.cbu_destino, instance_objeto_general.cuit_destino, 
                      instance_objeto_general.calcular_cant_registros(), instance_objeto_general.calcular_importe_determinado_y_pagado(),
                      instance_objeto_general.calcular_importe_determinado_y_pagado(), instance_objeto_general.imp_recaudado,
                      instance_objeto_general.imp_depositado, instance_objeto_general.imp_a_depositar,
                      instance_objeto_general.calcular_total_comision(), instance_objeto_general.calcular_iva()]
    print(vector_general)
except (AttributeError, TypeError):
        print("ERROR")


