import xml.etree.ElementTree as ET
import random
from lectura_archivo import leer_archivo
from func_rellenar_clases import rellenar_clase_general_input, separar_detallespagos, transformar_datos_detallepago, transformar_nroboletas_dp, transformar_fechaspago_dp, transformar_importes_dp, transformar_cuotas_dp, transformar_objimponibles_dp, transformar_obligaciones_dp
import time

class GeneralInput():
    def __init__(self):
        self.banco, self.fecha_rendicion = rellenar_clase_general_input()

    #Getters
    def getBanco(self):
        return self.banco
    
    def getFechaRendicion(self):
        return self.fecha_rendicion
    

    

    

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

    def generar_nro_rendicion(self):
        self.nro_rendicion = random.randint(00000,99999)
        return self.nro_rendicion
    
    def transformar_fecha(self):
        self.fecha_rendicion = self.fecha_rendicion[6:10] + self.fecha_rendicion[5] + self.fecha_rendicion[3:5] + self.fecha_rendicion[2] + self.fecha_rendicion[0:2]
        return self.fecha_rendicion
        
            
    def calcular_cant_registros(self):
        vector_boletas = transformar_nroboletas_dp()
        cantidad_registros = 0
        for cantidad in range(len(vector_boletas)):
            cantidad_registros += 1
        return cantidad_registros
    
    def calcular_importe_determinado_y_pagado(self):
        vector_importes = transformar_importes_dp()
        suma_importes = 0
        for importes in vector_importes:
            suma_importes += float(importes)
        return suma_importes

    def calcular_total_comision_iva(self):
        vector_importes_x_dp = transformar_importes_dp()
        comision = 0
        iva = 0
        for importes in vector_importes_x_dp:
            comision += float(importes) * 0.01
            comision_redondeo = round(comision, 2)
        
        iva += float(comision) * 0.21
        iva_redondeo = round(iva, 2)       
        return comision_redondeo, iva_redondeo


    
    def informes_general(self):
        dp = DetallePagoOutput()
        vector_comisiones, vector_ivas = dp.calculo_comision_iva_x_dp()
        vector_importes = transformar_importes_dp()
        suma_importes = 0
        suma_comision = 0
        suma_iva = 0
        for importe in vector_importes:
            suma_importes += float(importe)
            
        for comision in vector_comisiones:
            suma_comision += float(comision)
            comision_redondeo = round(suma_comision, 2)
        
        for ivas in vector_ivas:
            suma_iva += float(ivas)
            iva_redondeo = round(suma_iva, 2)
        
        cant_registros = 'Cantidad de registros es igual a cantidad de boletas ingresadas: ' + str(len(vector_importes))
        importes_dp = 'Importes ingresados de cada boleta: ' + str(vector_importes)
        suma_total = 'Sumatoria de los importes de todas las boletas: $ ' + str(suma_importes)
        comisiones_dp = 'Comisiones de cada importe: ' + str(vector_comisiones)
        comision_total = 'La comision total es igual a $: ' + str(comision_redondeo)
        ivas_dp = 'Iva de cada importe (comision de cada importe x 0.21):' + str(vector_ivas)
        ivas_total = 'La comision total es igual a $: ' + str(iva_redondeo)
        

        return importes_dp, suma_total, comisiones_dp, comision_total, ivas_dp, ivas_total, cant_registros


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
        vector_boletas = transformar_nroboletas_dp()
        cantidad_registros = 0
        for cantidad in range(len(vector_boletas)):
            cantidad_registros += 1
        return cantidad_registros
        
    
    def calcular_importe_determinado_y_pagado(self):
        vector_importes = transformar_importes_dp()
        suma_importes = 0
        for importe in vector_importes:
            suma_importes += float(importe)
        return suma_importes

    def calcular_total_comision_iva_sucursal(self):
        dp = DetallePagoOutput()
        valores_comisiones, valores_iva = dp.calculo_comision_iva_x_dp()
        sumatoria_comision = 0
        sumatoria_iva = 0
        for valor_com in valores_comisiones:
            sumatoria_comision += valor_com
            sumatoria_comision_redondeo = round(sumatoria_comision, 2)
        
        for valor_iva in valores_iva:
            sumatoria_iva += valor_iva
            sumatoria_iva_redondeo = round(sumatoria_iva, 2)
        
        return sumatoria_comision_redondeo, sumatoria_iva_redondeo
        


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
            
    def calcular_cant_registros_pagos(self):
        vector_boletas = transformar_nroboletas_dp()
        #print("BOLETAS: ", vector_boletas)
        cantidad_registros = 0
        for cantidad in range(len(vector_boletas)):
            cantidad_registros += 1
            #print("REGISTROS: ", cantidad_registros)
        return cantidad_registros
    
    def calcular_importe_determinado_y_pagado(self):
        vector_importes = transformar_importes_dp()
        suma_importes = 0
        for importe in vector_importes:
            suma_importes += float(importe)
        return suma_importes

    def calcular_total_comision_iva_pagos(self):
        dp = DetallePagoOutput()
        valores_comisiones, valores_iva = dp.calculo_comision_iva_x_dp()
        sumatoria_comision = 0
        sumatoria_iva = 0
        for valor_com in valores_comisiones:
            sumatoria_comision += valor_com
            sumatoria_comision_redondeo = round(sumatoria_comision, 2)
            
        
        for valor_iva in valores_iva:
            sumatoria_iva += valor_iva
            sumatoria_iva_redondeo = round(sumatoria_iva, 2)
        
        return sumatoria_comision_redondeo, sumatoria_iva_redondeo


class DetallePagoInput():
    def __init__(self):
        self.boletas = transformar_nroboletas_dp()
        self.fecha_pagos = transformar_fechaspago_dp()
        self.importes = transformar_importes_dp()
        self.cuotas = transformar_cuotas_dp()
        self.obj_imp = transformar_objimponibles_dp()
        self.obligaciones =  transformar_obligaciones_dp()

    #Getters
    def getDatos(self):
        return self.datos



class DetallePagoOutput(DetallePagoInput):
    def __init__(self):
        super().__init__()
        self.cod_registro = '022'
        self.marca_movimiento = 'P'
        self.tipo_operacion = '01'
        self.tipo_rendicion = '01'
        self.moneda = '01'
        self.nro_comercio = '27426748'
    
    def getCodRegistro(self):
        return self.cod_registro
    
    def getMarcaMovimiento(self):
        return self.marca_movimiento
    
    def getTipoOperacion(self):
        return self.tipo_operacion
    
    def getTipoRendicion(self):
        return self.tipo_rendicion
    
    def getMoneda(self):
        return self.moneda
    
    def getImporte(self):
        #vector_importes = transformar_importes_dp()
        #print(vector_importes)
        return self.importes
    
    def getNroBoletas(self):
        #vector_nro_boletas = transformar_nroboletas_dp()
        return self.boletas
    
    def getCantCuotas(self):
        #vector_cuotas = transformar_cuotas_dp()
        return self.cuotas
    
    def getObjImponible(self):
        #vector_obj_imponible = transformar_objimponibles_dp()
        return self.obj_imp
    
    def getObligacion(self):
        #vector_obligacion = transformar_obligaciones_dp()
        return self.obligaciones
    
    def getFechaPago(self):
        #vector_fechaspagos = transformar_fechaspago_dp()
        return self.fecha_pagos
    
    def getNroComercio(self):
        return self.nro_comercio
    
    def calculo_nro_registro_ycontrol(self):
        registros_ycontrol = []
        for numero in range(len(self.boletas)):
            registros_ycontrol.append(numero + 1)
            #print(registros_ycontrol)
        return registros_ycontrol
    
    def calculo_comision_iva_x_dp(self):
        vector_importes_x_dp = transformar_importes_dp()
        comisiones = []
        ivas = []
        comision = 0
        iva = 0
        for importes in vector_importes_x_dp:
            comision = round(float(importes) * 0.01, 2) 
            iva = round(float(comision) * 0.21, 2)           
            comisiones.append(comision)
            ivas.append(iva)
        return comisiones, ivas
        

   

class Generador():
    def generar_xml(self):
        try:
            instancia_general_output = GeneralOutput()
            instancia_sucursal_output = SucursalOutput()
            instancia_pagos_output = PagosOutput()
            instancia_dp_output = DetallePagoOutput()

            banco = instancia_general_output.getBanco()
            nro_rendicion = instancia_general_output.generar_nro_rendicion()
            fecha_rendicion = instancia_general_output.transformar_fecha()
            cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.calcular_cbus_y_cuits()
            cant_registros = instancia_general_output.calcular_cant_registros()
            imp_pagado = instancia_general_output.calcular_importe_determinado_y_pagado()
            imp_determinado = instancia_general_output.calcular_importe_determinado_y_pagado()
            imp_recaudado = instancia_general_output.getImpRecaudado()
            imp_depositado = instancia_general_output.getImpDepositado()
            imp_a_depositar = instancia_general_output.getImpADepositar()
            total_comision, total_iva = instancia_general_output.calcular_total_comision_iva()
            informe_importes, informe_suma_importes, informe_comisiones, informe_suma_comisiones, informe_ivas, informe_suma_ivas, informe_cant_registros = instancia_general_output.informes_general()
            

            sucursal = instancia_sucursal_output.getSucursal()
            cant_registros_sucursal = instancia_sucursal_output.calcular_cant_registros()
            imp_pagado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado()
            imp_determinado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado()
            imp_recaudado_sucursal = instancia_sucursal_output.getImpRecaudado()
            imp_depositado_sucursal = instancia_sucursal_output.getImpDepositado()
            imp_a_depositar_sucursal = instancia_sucursal_output.getImpADepositar()
            total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal()


            cod_registro = instancia_pagos_output.getCodRegistro()
            caja = instancia_pagos_output.getCaja()
            cajero = instancia_pagos_output.getCajero()
            lote = instancia_pagos_output.getLote()
            cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos()
            imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado()
            imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado()
            total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos()

            
            cod_registro_dp = instancia_dp_output.getCodRegistro()
            nro_registro = instancia_dp_output.calculo_nro_registro_ycontrol()
            marca_movimiento = instancia_dp_output.getMarcaMovimiento()
            tipo_operacion = instancia_dp_output.getTipoOperacion()
            tipo_rendicion = instancia_dp_output.getTipoRendicion()
            moneda = instancia_dp_output.getMoneda()
            importe = instancia_dp_output.getImporte()
            nro_boleta = instancia_dp_output.getNroBoletas()
            cuota = instancia_dp_output.getCantCuotas()
            obj_imponible = instancia_dp_output.getObjImponible()
            obligacion = instancia_dp_output.getObligacion()
            fecha_pago = instancia_dp_output.getFechaPago()
            nro_comercio = instancia_dp_output.getNroComercio()
            comision, iva = instancia_dp_output.calculo_comision_iva_x_dp()


            
            #generando estructura xml con los campos
            general = ET.Element("General", totalImpIVA = str(total_iva), totalImpComision = str(total_comision), 
                                    totalImpRecaudado = str(imp_recaudado), totalImpDemositado = str(imp_depositado),
                                    totalImpADepositar = str(imp_a_depositar), totalImpPagado = str(imp_pagado), 
                                    totalImpDeterminado = str(imp_determinado), registros = str(cant_registros), 
                                    cuitDestino = str(cuit_destino), cbuDestino = str(cbu_destino), cuitOrigen = str(cuit_origen), cbuOrigen = str(cbu_origen),
                                    fechaRendicion = fecha_rendicion, nroRendicion = str(nro_rendicion), nroTransaccion = "0", banco = banco, xmlns="")
            
            sucursal = ET.SubElement(general,"Sucursal", totalImpIVAs = str(total_iva_sucursal), totalImpComisions = str(total_comision_sucursal), 
                                    totalImpRecaudados = str(imp_recaudado_sucursal), totalImpDemositados = str(imp_depositado_sucursal),
                                    totalImpADepositars = str(imp_a_depositar_sucursal), totalImpPagados = str(imp_pagado_sucursal), 
                                    totalImpDeterminados = str(imp_determinado_sucursal), registross = str(cant_registros_sucursal), sucursal = sucursal)
                                    
            pagos = ET.SubElement(sucursal,"Pagos",
                                    totalImpIVAp = str(total_iva_pagos), totalImpComisionp = str(total_comision_pagos), 
                                    totalImpPagadop = str(imp_pagado_pagos), 
                                    totalImpDeterminadop = str(imp_determinado_pagos), registrosp = str(cant_registros_pagos),
                                    lote = lote, cajero = cajero, caja = caja, codRegistro = cod_registro
                                    )

                                    
                                    
            
            for numero in range(len(nro_registro)):
                det_pago = ET.SubElement(pagos,"DetallePago", obligacion = str(obligacion[numero]), idObjetoImponible = str(obj_imponible[numero]), 
                                        cantCuotas = str(cuota[numero]), nroComercio = str(nro_comercio), impIVA = str(iva[numero]), impComision = str(comision[numero]), impPagado = str(importe[numero]), impDeterminado = str(importe[numero]), 
                                        fechaPago = str(fecha_pago[numero]), nroLiquidacionActualizado = nro_boleta[numero], nroLiquidacionOriginal = nro_boleta[numero], 
                                        moneda = str(moneda), tipoRendicion = str(tipo_rendicion), tipoOperacion = str(tipo_operacion), 
                                        marcaMovimiento = str(marca_movimiento), nroControl = str(numero + 1), nroRegistro = str(numero + 1), 
                                        codRegistro = str(cod_registro_dp)).text = ' '

            comentario_cant_registros = ET.Comment(informe_cant_registros)
            comentario_importes = ET.Comment(informe_importes)
            comentario_suma_importes = ET.Comment(informe_suma_importes)  
            comentario_comision = ET.Comment(informe_comisiones) 
            comentario_suma_comisiones = ET.Comment(informe_suma_comisiones)
            comentario_iva = ET.Comment(informe_ivas)
            comentario_suma_ivas = ET.Comment(informe_suma_ivas)

            general.insert(0, comentario_suma_ivas)
            general.insert(0, comentario_iva)
            general.insert(0, comentario_suma_comisiones)
            general.insert(0, comentario_comision)
            general.insert(0, comentario_suma_importes)
            general.insert(0, comentario_importes)
            general.insert(0, comentario_cant_registros)
            
            
            
            tree = ET.ElementTree(general)
            tree.write('prueba.xml', xml_declaration=True, encoding='utf-8')
             

        except (TypeError, AttributeError, SystemError):
            print("Error al generar xml")
            time.sleep(5)