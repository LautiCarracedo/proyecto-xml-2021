import xml.etree.ElementTree as ET
import datetime

diccionario = {'nombre':'carlos'}
with open("C:/Users/Lauti/Desktop/generador_prueba/txt_prueba.txt","r") as archivo:
    lineas = archivo.readlines()
  

nro_banco = lineas[0][16:20]
fecha = lineas[1][25:35]
cbu_origen = lineas[2][20:42]
cuit_origen = lineas[3][21:32]
cbu_destino = lineas[4][21:43]
cuit_destino = lineas[5][22:33]




class GeneralInput():
    def __init__(self, banco, cbu_origen, cuit_origen, cbu_destino,cuit_destino, fecha_rendicion):
        self.banco = banco
        self.cbu_origen = cbu_origen
        self.cuit_origen = cuit_origen
        self.cbu_destino = cbu_destino
        self.cuit_destino = cuit_destino
        self.fecha_rendicion = fecha_rendicion

class GeneralOutput(GeneralInput):
    def __init__(self, banco, cbu_origen, cuit_origen, cbu_destino, cuit_destino, fecha_rendicion):
        super().__init__(banco, cbu_origen, cuit_origen, cbu_destino, cuit_destino, fecha_rendicion)
        self.imp_recaudado = 0.00
        self.imp_depositado = 0.00
        self.imp_a_depositar = 0.00

    def generar_nro_transaccion(self):
        pass
    
    def transformar_fecha(self, fecha):
        fecha_rendicion = fecha[6:10] + fecha[5] + fecha[3:5] + fecha[2] + fecha[0:2]
        #print(fecha_rendicion)
        return fecha_rendicion
        

    def calcular_cant_registros(self):
        contador = 1
        if lineas[22] != " ":
            contador += 1
        #print(contador)
        return contador
    
    def calcular_importe_determinado_y_pagado(self):
        suma = float(lineas[15][25:31])
        if lineas[28] != " ":
            suma = suma + float(lineas[28][25:31])
        return suma

    def calcular_total_comision(self):
        total_comision = float(lineas[15][25:31]) * 0.01
        if lineas[28] != " ":
            total_comision = round(total_comision + (float(lineas[28][25:31]) * 0.01), 2)
        return total_comision

    def calcular_iva(self):
        total_comision = float(lineas[15][25:31]) * 0.01
        if lineas[28] != " ":
            total_comision = round(total_comision + (float(lineas[28][25:31]) * 0.01), 2)
        iva = round(total_comision * 0.21, 2)
        return iva
        


    def generar_tag_cabecera(self):
        pass
        
        


class Generador():
    def generar_xml(self):
        pass
        



instance_objeto_general_input = GeneralInput(nro_banco,cbu_origen, cuit_origen, cbu_destino, cuit_destino, fecha)
instance_objeto_general = GeneralOutput(instance_objeto_general_input.banco, instance_objeto_general_input.cbu_origen, instance_objeto_general_input.cuit_origen, instance_objeto_general_input.cbu_destino, instance_objeto_general_input.cuit_destino, instance_objeto_general_input.fecha_rendicion)

#instance_objeto_general = GeneralOutput(nro_banco,cbu_origen, cuit_origen, cbu_destino, fecha)

#generador = Generador()
#generador.generar_xml()




fecha_rendicion_bien = instance_objeto_general.transformar_fecha(instance_objeto_general.fecha_rendicion)
cantidad_registros = instance_objeto_general.calcular_cant_registros()

#no es necesario, es para ver la salida x consola mediante un vector
vector_general = []
vector_general = [instance_objeto_general.banco, 0, instance_objeto_general.cbu_origen, instance_objeto_general.cuit_origen,
                  instance_objeto_general.cbu_destino, instance_objeto_general.cuit_destino,
                  fecha_rendicion_bien, cantidad_registros, instance_objeto_general.calcular_importe_determinado_y_pagado(),
                  instance_objeto_general.calcular_importe_determinado_y_pagado(), instance_objeto_general.imp_recaudado,
                  instance_objeto_general.imp_depositado, instance_objeto_general.imp_a_depositar,
                  instance_objeto_general.calcular_total_comision(), instance_objeto_general.calcular_iva()]
print(vector_general)

#generando estructura xml con los campos
general = ET.Element("General",totalImpIVA = str(instance_objeto_general.calcular_iva()), totalImpComision = str(instance_objeto_general.calcular_total_comision()), totalImpRecaudado = str(instance_objeto_general.imp_recaudado), totalImpDemositado = str(instance_objeto_general.imp_depositado),
                        totalImpADepositar = str(instance_objeto_general.imp_a_depositar), totalImpPagado = str(instance_objeto_general.calcular_importe_determinado_y_pagado()), totalImpDeterminado = str(instance_objeto_general.calcular_importe_determinado_y_pagado()), registros = str(cantidad_registros),
                        cuitDestino = instance_objeto_general.cuit_destino, cbuDestino = instance_objeto_general.cbu_destino, cuitOrigen = instance_objeto_general.cuit_origen, cbuOrigen = instance_objeto_general.cbu_origen, 
                        fechaRendicion = fecha_rendicion_bien, nroTransaccion = "0", banco = instance_objeto_general.banco)
sucursal = ET.SubElement(general,"Sucursal")
pagos = ET.SubElement(sucursal,"Pagos")
det_pago = ET.SubElement(pagos,"DetallePago").text = ' '
tree = ET.ElementTree(general)
tree.write('prueba.xml', xml_declaration=True, encoding='utf-8')

