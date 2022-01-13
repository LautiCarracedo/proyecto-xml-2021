import xml.etree.ElementTree as ET
from clase_dp_bpc import DetallePagoBPC

from clase_general_bpc import GeneralBPC
from clase_pagos_bpc import PagosBPC
from clase_sucursal_bpc import SucursalBPC


class GeneradorBPC():
    def __init__(self, codbarra1_ok, codbarra2_ok, fecha_rend_ok, fecha_acred_ok, forma_pago_ok, tipos_pagos_ok):
        self.codbarra1 = codbarra1_ok
        self.codbarra2 =  codbarra2_ok
        self.fecharend = fecha_rend_ok
        self.fechaacredit = fecha_acred_ok
        self.forma_pago = forma_pago_ok
        self.tipos_pagos = tipos_pagos_ok

    def generar_xml(self, codbarra1, codbarra2, fecharendicion, fechaacreditacion, formapago, tipopago):
        
        instancia_general_output = GeneralBPC(fecharendicion)
        banco = instancia_general_output.getBanco()
        fecha_rendicion = instancia_general_output.getFechaRendicion()
        nro_rendicion = instancia_general_output.generar_nro_rendicion()
        cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.getCbuCuits()
        cant_registros = instancia_general_output.calcular_cant_registros(codbarra1)
        imp_determinado = instancia_general_output.calcular_importe_determinado_y_pagado(codbarra1, codbarra2)
        imp_pagado = instancia_general_output.calcular_importe_determinado_y_pagado(codbarra1, codbarra2)
        imp_recaudado = instancia_general_output.getImpRecaudado()
        imp_depositado = instancia_general_output.getImpDepositado()
        imp_a_depositar = instancia_general_output.getImpADepositar()
        imp_comision, imp_iva = instancia_general_output.calcular_total_comision_iva()

        #para pagos electronicos
        total_imp_recaudado_depo_gral = instancia_general_output.calcular_importe_recaudado(codbarra1, codbarra2)
        total_imp_depositado_depositar_depo_gral = instancia_general_output.calcular_importe_depositado_adepositar(codbarra1, codbarra2)


        instancia_sucursal_output = SucursalBPC()
        sucursal_id = instancia_sucursal_output.getSucursal()
        cant_registros_sucursal = instancia_sucursal_output.calcular_cant_registros(codbarra1)
        imp_pagado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(codbarra1, codbarra2)
        imp_determinado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(codbarra1, codbarra2)
        imp_recaudado_sucursal = instancia_sucursal_output.getImpRecaudado()
        imp_depositado_sucursal = instancia_sucursal_output.getImpDepositado()
        imp_a_depositar_sucursal = instancia_sucursal_output.getImpADepositar()
        total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal()

        #para pagos electronicos
        total_imp_recaudado_depo_sucursal = instancia_sucursal_output.calcular_importe_recaudado_sucursal(codbarra1, codbarra2)
        total_imp_depositado_depositar_depo_sucursal = instancia_sucursal_output.calcular_importe_depositado_adepositar_sucursal(codbarra1, codbarra2)
        
        instancia_pagos_output = PagosBPC(fechaacreditacion)
        cod_registro = instancia_pagos_output.getCodRegistro(formapago)
        caja = instancia_pagos_output.getCaja()
        cajero = instancia_pagos_output.getCajero()
        lote = instancia_pagos_output.getLote()
        cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos(codbarra1)
        imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(codbarra1, codbarra2)
        imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(codbarra1, codbarra2)
        total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos()
        fec_acreditacion = instancia_pagos_output.getFechaAcreditacion()

        #para deposito
        total_imp_recaudado_depo = instancia_pagos_output.calcular_imp_recaudado_depositos(codbarra1, codbarra2)
        total_imp_depositado_depositar_depo = instancia_pagos_output.calcular_imp_depositado_y_depositar_deposito(codbarra1, codbarra2)


        instancia_dp_output = DetallePagoBPC(codbarra1, codbarra2)
        cod_barra1, cod_barra2 = instancia_dp_output.getCodBarra()
        cod_registro_dp = instancia_dp_output.getCodRegistro(formapago)
        fecha_venc = instancia_dp_output.getFechaVenc(codbarra2)
        nro_registro = instancia_dp_output.getNroRegistro()
        nro_control = instancia_dp_output.getNroControl(codbarra1)
        marca_movimiento = instancia_dp_output.getMarcaMovimiento()
        tipo_operacion = instancia_dp_output.getTipoOperacion()
        tipo_rendicion = instancia_dp_output.getTipoRendicion()
        moneda = instancia_dp_output.getMoneda()
        impuesto = instancia_dp_output.getImpuesto(codbarra1)
        importe = instancia_dp_output.getImporte()
        nro_boleta = instancia_dp_output.getLiquidacion(codbarra1)
        obj_imponible = instancia_dp_output.getObjImponible(codbarra2)
        obligacion = instancia_dp_output.getObligacion(codbarra1) 
        fecha_pago = instancia_dp_output.getFechaPago()
        comision, iva = instancia_dp_output.calculo_comision_iva_x_dp()

        

        #para detalledeposito
        cod_depositante = instancia_dp_output.getCodigoER(codbarra1)
        sucursal_depositante = instancia_dp_output.getSucursalER(codbarra1)
        boleta_ente_depo = instancia_dp_output.getBoletaER(codbarra1)
        nro_control_depo = instancia_dp_output.getNroControlBoletaER(codbarra1)
        imp_recaudado_depo = instancia_dp_output.getImpRecaudadoBoletaER()
        imp_depositado_depo = instancia_dp_output.getImpADepositarYDepositadoER()
        imp_a_depositar_depo = instancia_dp_output.getImpADepositarYDepositadoER()
        imp_comision_depo, imp_iva_depo = instancia_dp_output.getImpComisionEIvaER()
        fecha_deposito_depo = instancia_dp_output.getFechaDepositoBoletaER(fechaacreditacion)
        fecha_emision_depo = instancia_dp_output.getFechaEmisionBoletaER() 

       
        if formapago == "Pagos presenciales":
            general = ET.Element("General",  xmlns="", banco = banco, nroTransaccion = "0", nroRendicion = str(nro_rendicion), fechaRendicion = str(fecha_rendicion) , 
                            cbuOrigen = str(cbu_origen), cuitOrigen = str(cuit_origen), cbuDestino = str(cbu_destino), cuitDestino = str(cuit_destino),
                            registros = str(cant_registros),
                            totalImpDeterminado = str(imp_determinado), totalImpPagado = str(imp_pagado), totalImpRecaudado = str(imp_recaudado), totalImpDepositado = str(imp_depositado),
                            totalImpADepositar = str(imp_a_depositar), totalImpComision = str(imp_comision), totalImpIVA = str(imp_iva))

            sucursal_tag = ET.SubElement(general,"Sucursal", sucursal = sucursal_id, registros = str(cant_registros_sucursal),
                                    totalImpDeterminado = str(imp_determinado_sucursal), totalImpPagado = str(imp_pagado_sucursal),
                                    totalImpRecaudado = str(imp_recaudado_sucursal), totalImpDepositado = str(imp_depositado_sucursal),
                                    totalImpADepositar = str(imp_a_depositar_sucursal), totalImpComision = str(total_comision_sucursal), 
                                    totalImpIVA = str(total_iva_sucursal))  

            pagos = ET.SubElement(sucursal_tag,"Pagos", codigoRegistro = cod_registro, caja = caja, cajero = cajero, fechaAcreditacion = str(fec_acreditacion), lote = lote,
                                registros = str(cant_registros_pagos), totalImpDeterminado = str(imp_determinado_pagos),
                                totalImpPagado = str(imp_pagado_pagos), totalImpComision = str(total_comision_pagos),
                                totalImpIVA = str(total_iva_pagos))  


            for numero in range(len(nro_registro)):
                det_pago = ET.SubElement(pagos,"DetallePago", codigoRegistro = str(cod_registro_dp), nroRegistro = str(numero + 1), impuesto = str(impuesto[numero]), 
                                        fechaVencimiento = str(fecha_venc[numero]), idObjetoImponible = str(obj_imponible[numero]), nroControl = str(nro_control[numero]),
                                        marcaMovimiento = str(marca_movimiento), tipoOperacion = str(tipo_operacion), tipoRendicion = str(tipo_rendicion),
                                        moneda = str(moneda), nroLiquidacionOriginal = str(nro_boleta[numero]), nroLiquidacionActualizado = str(nro_boleta[numero]), 
                                        obligacion = str(obligacion[numero]), barra1 = str(cod_barra1[numero]), barra2 = str(cod_barra2[numero]), fechaPago = str(fecha_pago[numero]), 
                                        impDeterminado = str(importe[numero]), impPagado = str(importe[numero]), impComision = str(comision), 
                                    impIVA = str(iva)
                                    ).text = ' '
        
        elif formapago == "Pagos electronicos":
            general = ET.Element("General",  xmlns="", banco = banco, nroTransaccion = "0", nroRendicion = str(nro_rendicion), fechaRendicion = str(fecha_rendicion) , 
                            cbuOrigen = str(cbu_origen), cuitOrigen = str(cuit_origen), cbuDestino = str(cbu_destino), cuitDestino = str(cuit_destino),
                            registros = str(cant_registros), totalImpDeterminado = "0.0", totalImpPagado = "0.0", 
                            totalImpRecaudado = str(total_imp_recaudado_depo_gral), totalImpDepositado = str(total_imp_depositado_depositar_depo_gral),
                            totalImpADepositar = str(total_imp_depositado_depositar_depo_gral), totalImpComision = str(imp_comision), totalImpIVA = str(imp_iva))

            sucursal_tag = ET.SubElement(general,"Sucursal", sucursal = sucursal_id, registros = str(cant_registros_sucursal),
                                    totalImpDeterminado = "0.0", totalImpPagado = "0.0",
                                    totalImpRecaudado = str(total_imp_recaudado_depo_sucursal), totalImpDepositado = str(total_imp_depositado_depositar_depo_sucursal),
                                    totalImpADepositar = str(total_imp_depositado_depositar_depo_sucursal), totalImpComision = str(total_comision_sucursal), 
                                    totalImpIVA = str(total_iva_sucursal))  
            
            deposito = ET.SubElement(sucursal_tag,"Deposito", codigoRegistro = cod_registro, caja = caja, cajero = cajero, fechaAcreditacion = str(fec_acreditacion), lote = lote,
                                registros = str(cant_registros_pagos), totalImpRecaudado = str(total_imp_recaudado_depo),
                                totalImpDepositado = str(total_imp_depositado_depositar_depo), totalImpADepositar = str(total_imp_depositado_depositar_depo),
                                totalImpComision = str(total_comision_pagos), totalImpIVA = str(total_iva_pagos))  


            for numero in range(len(nro_registro)):
                det_depo = ET.SubElement(deposito,"DetalleDeposito", codigoRegistro = str(cod_registro_dp), nroRegistro = str(numero + 1), codigoER = str(cod_depositante[numero]), 
                                        sucursal = str(sucursal_depositante[numero]), boletaDeposito = str(boleta_ente_depo[numero]), fechaEmision = str(fecha_emision_depo[numero]),
                                        nroControl = str(nro_control_depo[numero]), fechaDeposito = str(fecha_deposito_depo), impRecaudado = str(imp_recaudado_depo[numero]), 
                                        impDepositado = str(imp_depositado_depo[numero]), impADepositar = str(imp_a_depositar_depo[numero]),
                                        impComision = str(comision), impIVA = str(iva)
                                    ).text = ' '
        
        else:
            #cuando se selecciona opc ambos pagos
            cant_registros_detpag, cant_registros_detdep = instancia_general_output.calcular_registros(tipopago)

            #para presenciales
            importe_determ_pagado = instancia_general_output.calcular_imp_determinado_pagado_presencial(codbarra1, codbarra2, tipopago)
            
            #para electronicos
            importe_recaudado, importe_depositado = instancia_general_output.calcular_imp_recaudado_depositado_adepositar_electronico(codbarra1, codbarra2, tipopago)
            

            general = ET.Element("General",  xmlns="", banco = banco, nroTransaccion = "0", nroRendicion = str(nro_rendicion), fechaRendicion = str(fecha_rendicion) , 
                            cbuOrigen = str(cbu_origen), cuitOrigen = str(cuit_origen), cbuDestino = str(cbu_destino), cuitDestino = str(cuit_destino),
                            registros = str(cant_registros), totalImpDeterminado = str(importe_determ_pagado), totalImpPagado = str(importe_determ_pagado), 
                            totalImpRecaudado = str(importe_recaudado), totalImpDepositado = str(importe_depositado),
                            totalImpADepositar = str(importe_depositado), totalImpComision = str(imp_comision), totalImpIVA = str(imp_iva))

            sucursal_tag = ET.SubElement(general,"Sucursal", sucursal = sucursal_id, registros = str(cant_registros_sucursal),
                                totalImpDeterminado = str(importe_determ_pagado), totalImpPagado = str(importe_determ_pagado),
                                totalImpRecaudado = str(importe_recaudado), totalImpDepositado = str(importe_depositado),
                                totalImpADepositar = str(importe_depositado), totalImpComision = str(total_comision_sucursal), 
                                totalImpIVA = str(total_iva_sucursal))  
            
            pagos = ET.SubElement(sucursal_tag,"Pagos", codigoRegistro = cod_registro, caja = caja, cajero = cajero, fechaAcreditacion = str(fec_acreditacion), lote = lote,
                                registros = str(cant_registros_detpag), totalImpDeterminado = str(importe_determ_pagado),
                                totalImpPagado = str(importe_determ_pagado), totalImpComision = str(total_comision_pagos),
                                totalImpIVA = str(total_iva_pagos))  
            
            deposito = ET.SubElement(sucursal_tag,"Deposito", codigoRegistro = cod_registro, caja = caja, cajero = cajero, fechaAcreditacion = str(fec_acreditacion), lote = lote,
                                registros = str(cant_registros_detdep), totalImpRecaudado = str(importe_recaudado),
                                totalImpDepositado = str(importe_depositado), totalImpADepositar = str(importe_depositado),
                                totalImpComision = str(total_comision_pagos), totalImpIVA = str(total_iva_pagos))

            


            for numero in range(len(nro_registro)):
                if tipopago[numero] == "P" or tipopago[numero] == "p":
                        det_pago = ET.SubElement(pagos,"DetallePago", codigoRegistro = str(cod_registro_dp), nroRegistro = str(numero + 1), impuesto = str(impuesto[numero]), 
                                                fechaVencimiento = str(fecha_venc[numero]), idObjetoImponible = str(obj_imponible[numero]), nroControl = str(nro_control[numero]),
                                                marcaMovimiento = str(marca_movimiento), tipoOperacion = str(tipo_operacion), tipoRendicion = str(tipo_rendicion),
                                                moneda = str(moneda), nroLiquidacionOriginal = str(nro_boleta[numero]), nroLiquidacionActualizado = str(nro_boleta[numero]), 
                                                obligacion = str(obligacion[numero]), barra1 = str(cod_barra1[numero]), barra2 = str(cod_barra2[numero]), fechaPago = str(fecha_pago[numero]), 
                                                impDeterminado = str(importe[numero]), impPagado = str(importe[numero]), impComision = str(comision), 
                                            impIVA = str(iva)
                                            ).text = ' '

                if tipopago[numero] == "E" or tipopago[numero] == "e":
                    det_depo = ET.SubElement(deposito,"DetalleDeposito", codigoRegistro = str(cod_registro_dp), nroRegistro = str(numero), codigoER = str(cod_depositante[numero]), 
                                            sucursal = str(sucursal_depositante[numero]), boletaDeposito = str(boleta_ente_depo[numero]), fechaEmision = str(fecha_emision_depo[numero]),
                                            nroControl = str(nro_control_depo[numero]), fechaDeposito = str(fecha_deposito_depo), impRecaudado = str(imp_recaudado_depo[numero]), 
                                            impDepositado = str(imp_depositado_depo[numero]), impADepositar = str(imp_a_depositar_depo[numero]),
                                            impComision = str(comision), impIVA = str(iva)
                                        ).text = ' '


        tree = ET.ElementTree(general)    
        tree.write(fecha_rendicion[0:4] + fecha_rendicion[5:7] + fecha_rendicion[8:10] + '.P1' + '.xml', xml_declaration=True, encoding='utf-8')