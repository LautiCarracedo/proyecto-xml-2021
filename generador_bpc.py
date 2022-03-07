import xml.etree.ElementTree as ET

from numpy import isnat
from clase_dp_bpc import DetallePagoElectronicoBPC, DetallePagoPresencialBPC
from clase_general_bpc import GeneralBPC
from clase_pagos_bpc import PagosBPC
from clase_sucursal_bpc import SucursalBPC

import zipfile


class GeneradorBPC():
    def __init__(self, codbarra1_p_ok, codbarra2_p_ok, codbarra1_e_ok, codbarra2_e_ok, fecha_rend_ok, formato_ok, contador_barras_p_ok, contador_barras_e_ok):
        self.codbarra1_p = codbarra1_p_ok
        self.codbarra2_p =  codbarra2_p_ok
        self.codbarra1_e = codbarra1_e_ok
        self.codbarra2_e =  codbarra2_e_ok
        self.fecharend = fecha_rend_ok
        self.formato = formato_ok
        self.contador_pagos_p = contador_barras_p_ok
        self.contador_pagos_e = contador_barras_e_ok
                    
    def generar_xml(self, codbarra1_p, codbarra2_p, codbarra1_e, codbarra2_e, fecharendicion, formapago, contador_pagos_p, contador_pagos_e):
        if formapago == "Pagos presenciales":
            #para pagos presenciales
            instancia_general_output = GeneralBPC(fecharendicion)
            banco = instancia_general_output.getBanco()
            fecha_rendicion = instancia_general_output.getFechaRendicion()
            nro_rendicion = instancia_general_output.generar_nro_rendicion()
            cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.getCbuCuits()
            cant_registros = instancia_general_output.calcular_cant_registros(codbarra1_p)
            imp_determinado = instancia_general_output.calcular_importe_determinado_y_pagado(codbarra1_p, codbarra2_p)
            imp_pagado = instancia_general_output.calcular_importe_determinado_y_pagado(codbarra1_p, codbarra2_p)
            imp_recaudado = instancia_general_output.getImpRecaudado()
            imp_depositado = instancia_general_output.getImpDepositado()
            imp_a_depositar = instancia_general_output.getImpADepositar()
            imp_comision, imp_iva = instancia_general_output.calcular_total_comision_iva()

            instancia_sucursal_output = SucursalBPC()
            sucursal_id = instancia_sucursal_output.getSucursal()
            cant_registros_sucursal= instancia_sucursal_output.calcular_cant_registros(codbarra1_p)
            imp_pagado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(codbarra1_p, codbarra2_p)
            imp_determinado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(codbarra1_p, codbarra2_p)
            imp_recaudado_sucursal = instancia_sucursal_output.getImpRecaudado()
            imp_depositado_sucursal = instancia_sucursal_output.getImpDepositado()
            imp_a_depositar_sucursal = instancia_sucursal_output.getImpADepositar()
            total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal()
            
            instancia_pagos_output = PagosBPC(fecharendicion)
            cod_registro = instancia_pagos_output.getCodRegistro(formapago)
            caja = instancia_pagos_output.getCaja()
            cajero = instancia_pagos_output.getCajero()
            lote = instancia_pagos_output.getLote()
            cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos(codbarra1_p)
            imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(codbarra1_p, codbarra2_p)
            imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(codbarra1_p, codbarra2_p)
            total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos()
            fec_acreditacion = instancia_pagos_output.getFechaAcreditacion()

            instancia_dp_output = DetallePagoPresencialBPC(codbarra1_p, codbarra2_p)
            cod_barra1, cod_barra2 = instancia_dp_output.getCodBarra()
            cod_registro_dp = instancia_dp_output.getCodRegistro()
            fecha_venc = instancia_dp_output.getFechaVenc(codbarra2_p)
            nro_registro = instancia_dp_output.getNroRegistro()
            nro_control = instancia_dp_output.getNroControl(codbarra1_p)
            marca_movimiento = instancia_dp_output.getMarcaMovimiento()
            tipo_operacion = instancia_dp_output.getTipoOperacion()
            tipo_rendicion = instancia_dp_output.getTipoRendicion()
            moneda = instancia_dp_output.getMoneda()
            impuesto = instancia_dp_output.getImpuesto(codbarra1_p)
            importe = instancia_dp_output.getImporte()
            nro_boleta = instancia_dp_output.getLiquidacion(codbarra1_p)
            obj_imponible = instancia_dp_output.getObjImponible(codbarra2_p)
            obligacion = instancia_dp_output.getObligacion(codbarra1_p) 
            fecha_pago = instancia_dp_output.getFechaPago()
            comision, iva = instancia_dp_output.calculo_comision_iva_x_dp()
        
            general = ET.Element("General", banco = banco, nroTransaccion = "0", nroRendicion = str(nro_rendicion), fechaRendicion = str(fecha_rendicion) , 
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
                                    impIVA = str(iva))
        
        elif formapago == "Pagos electronicos":

            instancia_general_output = GeneralBPC(fecharendicion)
            banco = instancia_general_output.getBanco()
            fecha_rendicion = instancia_general_output.getFechaRendicion()
            nro_rendicion = instancia_general_output.generar_nro_rendicion()
            cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.getCbuCuits()
            cant_registros = instancia_general_output.calcular_cant_registros(codbarra1_e)
            imp_comision, imp_iva = instancia_general_output.calcular_total_comision_iva()

            total_imp_recaudado_depo_gral = instancia_general_output.calcular_importe_recaudado(codbarra1_e, codbarra2_e)
            total_imp_depositado_depositar_depo_gral = instancia_general_output.calcular_importe_depositado_adepositar(codbarra1_e, codbarra2_e)

            instancia_sucursal_output = SucursalBPC()
            sucursal_id = instancia_sucursal_output.getSucursal()
            cant_registros_sucursal= instancia_sucursal_output.calcular_cant_registros(codbarra2_e)
            imp_recaudado_sucursal = instancia_sucursal_output.calcular_importe_recaudado_sucursal(codbarra1_e, codbarra2_e)
            imp_depositado_sucursal = instancia_sucursal_output.calcular_importe_depositado_adepositar_sucursal(codbarra1_e, codbarra2_e)
            imp_a_depositar_sucursal = instancia_sucursal_output.calcular_importe_depositado_adepositar_sucursal(codbarra1_e, codbarra2_e)
            total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal()
            
            instancia_pagos_output = PagosBPC(fecharendicion)
            cod_registro = instancia_pagos_output.getCodRegistro(formapago)
            caja = instancia_pagos_output.getCaja()
            cajero = instancia_pagos_output.getCajero()
            lote = instancia_pagos_output.getLote()
            cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos(codbarra2_e)
            imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(codbarra1_e, codbarra2_e)
            imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(codbarra1_e, codbarra2_e)
            total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos()
            fec_acreditacion = instancia_pagos_output.getFechaAcreditacion()

            instancia_dp_output = DetallePagoElectronicoBPC(codbarra1_e, codbarra2_e)
            nro_registro = instancia_dp_output.getNroRegistro()
            cod_registro_dp = instancia_dp_output.getCodRegistro()
            cod_depositante = instancia_dp_output.getCodigoER(codbarra1_e)
            sucursal_depositante = instancia_dp_output.getSucursalER(codbarra1_e)
            boleta_ente_depo = instancia_dp_output.getBoletaER(codbarra1_e)
            nro_control_depo = instancia_dp_output.getNroControlBoletaER(codbarra1_e)
            imp_recaudado_depo = instancia_dp_output.getImpRecaudadoBoletaER()
            imp_depositado_depo = instancia_dp_output.getImpADepositarYDepositadoER()
            imp_a_depositar_depo = instancia_dp_output.getImpADepositarYDepositadoER()
            fecha_deposito_depo = instancia_dp_output.getFechaDepositoBoletaER(fecharendicion)
            fecha_emision_depo = instancia_dp_output.getFechaEmisionBoletaER()
            comision, iva = instancia_dp_output.getImpComisionEIvaER()
            
            general = ET.Element("General", banco = banco, nroTransaccion = "0", nroRendicion = str(nro_rendicion), fechaRendicion = str(fecha_rendicion) , 
                            cbuOrigen = str(cbu_origen), cuitOrigen = str(cuit_origen), cbuDestino = str(cbu_destino), cuitDestino = str(cuit_destino),
                            registros = str(cant_registros), totalImpDeterminado = "0.0", totalImpPagado = "0.0", 
                            totalImpRecaudado = str(total_imp_recaudado_depo_gral), totalImpDepositado = str(total_imp_depositado_depositar_depo_gral),
                            totalImpADepositar = str(total_imp_depositado_depositar_depo_gral), totalImpComision = str(imp_comision), totalImpIVA = str(imp_iva))

            sucursal_tag = ET.SubElement(general,"Sucursal", sucursal = sucursal_id, registros = str(cant_registros_sucursal),
                                    totalImpDeterminado = "0.0", totalImpPagado = "0.0",
                                    totalImpRecaudado = str(imp_recaudado_sucursal), totalImpDepositado = str(imp_depositado_sucursal),
                                    totalImpADepositar = str(imp_depositado_sucursal), totalImpComision = str(total_comision_sucursal), 
                                    totalImpIVA = str(total_iva_sucursal))  
            
            deposito = ET.SubElement(sucursal_tag,"Deposito", codigoRegistro = cod_registro, caja = caja, cajero = cajero, fechaAcreditacion = str(fec_acreditacion), lote = lote,
                                registros = str(cant_registros_pagos), totalImpRecaudado = str(total_imp_recaudado_depo_gral), #totalImpRecaudado es igual a total_imo_rec-Depo_gral porque es el mismo calculo
                                totalImpDepositado = str(imp_depositado_sucursal), totalImpADepositar = str(imp_depositado_sucursal),
                                totalImpComision = str(total_comision_pagos), totalImpIVA = str(total_iva_pagos))  


            for numero in range(len(nro_registro)):
                det_depo = ET.SubElement(deposito,"DetalleDeposito", codigoRegistro = str(cod_registro_dp), nroRegistro = str(numero + 1), codigoER = str(cod_depositante[numero]), 
                                        sucursal = str(sucursal_depositante[numero]), boletaDeposito = str(boleta_ente_depo[numero]), fechaEmision = str(fecha_emision_depo[numero]),
                                        nroControl = str(nro_control_depo[numero]), fechaDeposito = str(fecha_deposito_depo), impRecaudado = str(imp_recaudado_depo[numero]), 
                                        impDepositado = str(imp_depositado_depo[numero]), impADepositar = str(imp_a_depositar_depo[numero]),
                                        impComision = str(comision), impIVA = str(iva)
                                    )

        elif formapago == "Ambos pagos":
            instancia_general_output = GeneralBPC(fecharendicion)
            banco = instancia_general_output.getBanco()
            fecha_rendicion = instancia_general_output.getFechaRendicion()
            nro_rendicion = instancia_general_output.generar_nro_rendicion()
            cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.getCbuCuits()
            #cant_registros = instancia_general_output.calcular_cant_registros(codbarra1_p) lo haceoms con la suma de codbarras elec + prese
            imp_determinado = instancia_general_output.calcular_importe_determinado_y_pagado(codbarra1_p, codbarra2_p)
            imp_pagado = instancia_general_output.calcular_importe_determinado_y_pagado(codbarra1_p, codbarra2_p)
            total_imp_recaudado_depo_gral = instancia_general_output.calcular_importe_recaudado(codbarra1_e, codbarra2_e)
            
            total_imp_depositado_depositar_depo_gral = instancia_general_output.calcular_importe_depositado_adepositar(codbarra1_e, codbarra2_e)
            imp_comision, imp_iva = instancia_general_output.calcular_total_comision_iva()


            instancia_sucursal_output = SucursalBPC()
            sucursal_id = instancia_sucursal_output.getSucursal()
            #cant_registros_sucursal= instancia_sucursal_output.calcular_cant_registros(codbarra1_p)
            imp_pagado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(codbarra1_p, codbarra2_p)
            imp_determinado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(codbarra1_p, codbarra2_p)
            imp_recaudado_sucursal = instancia_sucursal_output.calcular_importe_recaudado_sucursal(codbarra1_e, codbarra2_e)
            imp_depositado_sucursal = instancia_sucursal_output.calcular_importe_depositado_adepositar_sucursal(codbarra1_e, codbarra2_e)
            imp_a_depositar_sucursal = instancia_sucursal_output.calcular_importe_depositado_adepositar_sucursal(codbarra1_e, codbarra2_e)
            total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal()


            instancia_pagos_output = PagosBPC(fecharendicion)
            cod_registro = instancia_pagos_output.getCodRegistro(formapago)
            caja = instancia_pagos_output.getCaja()
            cajero = instancia_pagos_output.getCajero()
            lote = instancia_pagos_output.getLote()
            cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos(codbarra1_p)
            imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(codbarra1_p, codbarra2_p)
            imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(codbarra1_p, codbarra2_p)
            total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos()
            fec_acreditacion = instancia_pagos_output.getFechaAcreditacion()


            instancia_depositos_output = PagosBPC(fecharendicion)
            cod_registro_depo = instancia_depositos_output.getCodRegistro(formapago)
            caja = instancia_depositos_output.getCaja()
            cajero = instancia_depositos_output.getCajero()
            lote = instancia_depositos_output.getLote()
            cant_registros_pagos = instancia_depositos_output.calcular_cant_registros_pagos(codbarra2_e)
            imp_pagado_depo = instancia_depositos_output.calcular_importe_determinado_y_pagado(codbarra1_e, codbarra2_e) #njo se usa
            imp_determinado_depo = instancia_depositos_output.calcular_importe_determinado_y_pagado(codbarra1_e, codbarra2_e) #no se usa
            total_comision_pagos, total_iva_pagos = instancia_depositos_output.calcular_total_comision_iva_pagos()
            fec_acreditacion = instancia_depositos_output.getFechaAcreditacion()


            instancia_dp_output = DetallePagoPresencialBPC(codbarra1_p, codbarra2_p)
            cod_barra1, cod_barra2 = instancia_dp_output.getCodBarra()
            cod_registro_dp = instancia_dp_output.getCodRegistro()
            fecha_venc = instancia_dp_output.getFechaVenc(codbarra2_p)
            nro_registro = instancia_dp_output.getNroRegistro()
            nro_control = instancia_dp_output.getNroControl(codbarra1_p)
            marca_movimiento = instancia_dp_output.getMarcaMovimiento()
            tipo_operacion = instancia_dp_output.getTipoOperacion()
            tipo_rendicion = instancia_dp_output.getTipoRendicion()
            moneda = instancia_dp_output.getMoneda()
            impuesto = instancia_dp_output.getImpuesto(codbarra1_p)
            importe = instancia_dp_output.getImporte()
            nro_boleta = instancia_dp_output.getLiquidacion(codbarra1_p)
            obj_imponible = instancia_dp_output.getObjImponible(codbarra2_p)
            obligacion = instancia_dp_output.getObligacion(codbarra1_p) 
            fecha_pago = instancia_dp_output.getFechaPago()
            comision, iva = instancia_dp_output.calculo_comision_iva_x_dp()

            instancia_dpe_output = DetallePagoElectronicoBPC(codbarra1_e, codbarra2_e)
            nro_registro = instancia_dpe_output.getNroRegistro()
            cod_registro_dp = instancia_dpe_output.getCodRegistro()
            cod_depositante = instancia_dpe_output.getCodigoER(codbarra1_e)
            sucursal_depositante = instancia_dpe_output.getSucursalER(codbarra1_e)
            boleta_ente_depo = instancia_dpe_output.getBoletaER(codbarra1_e)
            nro_control_depo = instancia_dpe_output.getNroControlBoletaER(codbarra1_e)
            imp_recaudado_depo = instancia_dpe_output.getImpRecaudadoBoletaER()
            imp_depositado_depo = instancia_dpe_output.getImpADepositarYDepositadoER()
            imp_a_depositar_depo = instancia_dpe_output.getImpADepositarYDepositadoER()
            fecha_deposito_depo = instancia_dpe_output.getFechaDepositoBoletaER(fecharendicion)
            fecha_emision_depo = instancia_dpe_output.getFechaEmisionBoletaER()
            comision, iva = instancia_dpe_output.getImpComisionEIvaER()

            general = ET.Element("General", banco = banco, nroTransaccion = "0", nroRendicion = str(nro_rendicion), fechaRendicion = str(fecha_rendicion) , 
                            cbuOrigen = str(cbu_origen), cuitOrigen = str(cuit_origen), cbuDestino = str(cbu_destino), cuitDestino = str(cuit_destino),
                            registros = str(contador_pagos_p + contador_pagos_e), totalImpDeterminado = str(imp_determinado), totalImpPagado = str(imp_pagado), 
                            totalImpRecaudado = str(total_imp_recaudado_depo_gral), totalImpDepositado = str(total_imp_depositado_depositar_depo_gral),
                            totalImpADepositar = str(total_imp_depositado_depositar_depo_gral), totalImpComision = str(imp_comision), totalImpIVA = str(imp_iva))

            sucursal_tag = ET.SubElement(general,"Sucursal", sucursal = sucursal_id, registros = str(contador_pagos_e + contador_pagos_p),
                                totalImpDeterminado = str(imp_determinado_sucursal), totalImpPagado = str(imp_pagado_sucursal),
                                totalImpRecaudado = str(imp_recaudado_sucursal), totalImpDepositado = str(imp_depositado_sucursal),
                                totalImpADepositar = str(imp_a_depositar_sucursal), totalImpComision = str(total_comision_sucursal), 
                                totalImpIVA = str(total_iva_sucursal))  
            
            pagos = ET.SubElement(sucursal_tag,"Pagos", codigoRegistro = "021", caja = caja, cajero = cajero, fechaAcreditacion = str(fec_acreditacion), lote = lote,
                                registros = str(contador_pagos_p), totalImpDeterminado = str(imp_determinado_pagos),
                                totalImpPagado = str(imp_pagado_pagos), totalImpComision = str(total_comision_pagos),
                                totalImpIVA = str(total_iva_pagos))  
            
            deposito = ET.SubElement(sucursal_tag,"Deposito", codigoRegistro = "031", caja = caja, cajero = cajero, fechaAcreditacion = str(fec_acreditacion), lote = lote,
                                registros = str(contador_pagos_e), totalImpRecaudado = str(total_imp_recaudado_depo_gral),
                                totalImpDepositado = str(imp_depositado_sucursal), totalImpADepositar = str(imp_a_depositar_sucursal),
                                totalImpComision = str(total_comision_pagos), totalImpIVA = str(total_iva_pagos))


            for numero in range(contador_pagos_p):
                det_pago = ET.SubElement(pagos,"DetallePago", codigoRegistro = "022", nroRegistro = str(numero + 1), impuesto = str(impuesto[numero]), 
                                        fechaVencimiento = str(fecha_venc[numero]), idObjetoImponible = str(obj_imponible[numero]), nroControl = str(nro_control[numero]),
                                        marcaMovimiento = str(marca_movimiento), tipoOperacion = str(tipo_operacion), tipoRendicion = str(tipo_rendicion),
                                        moneda = str(moneda), nroLiquidacionOriginal = str(nro_boleta[numero]), nroLiquidacionActualizado = str(nro_boleta[numero]), 
                                        obligacion = str(obligacion[numero]), barra1 = str(cod_barra1[numero]), barra2 = str(cod_barra2[numero]), fechaPago = str(fecha_pago[numero]), 
                                        impDeterminado = str(importe[numero]), impPagado = str(importe[numero]), impComision = str(comision), 
                                    impIVA = str(iva)
                                    )
            
            for numero in range(contador_pagos_e):
                det_depo = ET.SubElement(deposito,"DetalleDeposito", codigoRegistro = "032", nroRegistro = str(numero + 1), codigoER = str(cod_depositante[numero]), 
                                        sucursal = str(sucursal_depositante[numero]), boletaDeposito = str(boleta_ente_depo[numero]), fechaEmision = str(fecha_emision_depo[numero]),
                                        nroControl = str(nro_control_depo[numero]), fechaDeposito = str(fecha_deposito_depo), impRecaudado = str(imp_recaudado_depo[numero]), 
                                        impDepositado = str(imp_depositado_depo[numero]), impADepositar = str(imp_a_depositar_depo[numero]),
                                        impComision = str(comision), impIVA = str(iva)
                                    )


        tree = ET.ElementTree(general)    
        tree.write(fecha_rendicion[0:4] + fecha_rendicion[5:7] + fecha_rendicion[8:10] + '.P1', xml_declaration=True, encoding='utf-8')

        with zipfile.ZipFile(f"{fecha_rendicion[0:4] + fecha_rendicion[5:7] + fecha_rendicion[8:10]}" + '.P1' + ".zip", 'w') as zf:
            tree = ET.ElementTree(general)    
            tree.write(fecha_rendicion[0:4] + fecha_rendicion[5:7] + fecha_rendicion[8:10] + '.P1', xml_declaration=True, encoding='utf-8')
            zf.write(fecha_rendicion[0:4] + fecha_rendicion[5:7] + fecha_rendicion[8:10] + '.P1')