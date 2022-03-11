from abc import ABC, abstractmethod
from logica_negocio_entes.clase_general import GeneralOutput
from logica_negocio_entes.clase_sucursal import SucursalOutput
from logica_negocio_entes.clase_pagos import PagosOutput
from logica_negocio_entes.clase_dp import DetallePagoOutput

from logica_negocio_bpc.clase_dp_bpc import DetallePagoElectronicoBPC, DetallePagoPresencialBPC
from logica_negocio_bpc.clase_general_bpc import GeneralBPC
from logica_negocio_bpc.clase_pagos_bpc import PagosBPC
from logica_negocio_bpc.clase_sucursal_bpc import SucursalBPC

from lectura_archivo_config import ArchivoConfig

import xml.etree.ElementTree as ET

import zipfile



class Generadorr:
    def __init__(self, origen_ok, banco_ok, fecha_rendicion_ok, vector_boletas_ok, vector_importes_ok, vector_fechapagos_ok, vector_cantcuotas_ok, vector_cuotaactual_ok, codbarra1_p, codbarra2_p, codbarra1_e, codbarra2_e, fecharendicion, formapago, contador_pagos_p, contador_pagos_e):
        self.origen = origen_ok
        self.banco = banco_ok
        self.fecharendicion = fecha_rendicion_ok
        self.boletas = vector_boletas_ok
        self.importes = vector_importes_ok
        self.fechapagos = vector_fechapagos_ok
        self.cuotas = vector_cantcuotas_ok
        self.cuotaactual = vector_cuotaactual_ok
        self.codbarra1p = codbarra1_p
        self.codbarra2p = codbarra2_p
        self.codbarra1e = codbarra1_e
        self.codbarra2e = codbarra2_e
        self.fecharendicionbpc = fecharendicion
        self.formapagobpc = formapago
        self.contadorpagospresenciales = contador_pagos_p
        self.contadorpagoselectronicos = contador_pagos_e
      

    @abstractmethod
    def generar_xml(self):
        pass

class GeneradorrBPC(Generadorr):
    def __init__(self, origen_ok, banco_ok, fecha_rendicion_ok, vector_boletas_ok, vector_importes_ok, vector_fechapagos_ok, vector_cantcuotas_ok, vector_cuotaactual_ok, codbarra1_p, codbarra2_p, codbarra1_e, codbarra2_e, fecharendicion, formapago, contador_pagos_p, contador_pagos_e):
        super().__init__(origen_ok, banco_ok, fecha_rendicion_ok, vector_boletas_ok, vector_importes_ok, vector_fechapagos_ok, vector_cantcuotas_ok, vector_cuotaactual_ok, codbarra1_p, codbarra2_p, codbarra1_e, codbarra2_e, fecharendicion, formapago, contador_pagos_p, contador_pagos_e)
        #self.forma_pago = "Pagos presenciales"
    
    def generar_xml(self):
        if self.formapagobpc == "Pagos presenciales":
            #para pagos presenciales
            instancia_general_output = GeneralBPC(self.fecharendicionbpc)
            banco = instancia_general_output.getBanco()
            fecha_rendicion = instancia_general_output.getFechaRendicion()
            nro_rendicion = instancia_general_output.generar_nro_rendicion()
            cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.getCbuCuits()
            cant_registros = instancia_general_output.calcular_cant_registros(self.codbarra1p)
            imp_determinado = instancia_general_output.calcular_importe_determinado_y_pagado(self.codbarra1p, self.codbarra2p)
            imp_pagado = instancia_general_output.calcular_importe_determinado_y_pagado(self.codbarra1p, self.codbarra2p)
            imp_recaudado = instancia_general_output.getImpRecaudado()
            imp_depositado = instancia_general_output.getImpDepositado()
            imp_a_depositar = instancia_general_output.getImpADepositar()
            imp_comision, imp_iva = instancia_general_output.calcular_total_comision_iva()

            instancia_sucursal_output = SucursalBPC()
            sucursal_id = instancia_sucursal_output.getSucursal()
            cant_registros_sucursal= instancia_sucursal_output.calcular_cant_registros(self.codbarra1p)
            imp_pagado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(self.codbarra1p, self.codbarra2p)
            imp_determinado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(self.codbarra1p, self.codbarra2p)
            imp_recaudado_sucursal = instancia_sucursal_output.getImpRecaudado()
            imp_depositado_sucursal = instancia_sucursal_output.getImpDepositado()
            imp_a_depositar_sucursal = instancia_sucursal_output.getImpADepositar()
            total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal()
            
            instancia_pagos_output = PagosBPC(self.fecharendicionbpc)
            cod_registro = instancia_pagos_output.getCodRegistro(self.formapagobpc)
            caja = instancia_pagos_output.getCaja()
            cajero = instancia_pagos_output.getCajero()
            lote = instancia_pagos_output.getLote()
            cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos(self.codbarra1p)
            imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(self.codbarra1p, self.codbarra2p)
            imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(self.codbarra1p, self.codbarra2p)
            total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos()
            fec_acreditacion = instancia_pagos_output.getFechaAcreditacion()

            instancia_dp_output = DetallePagoPresencialBPC(self.codbarra1p, self.codbarra2p)
            cod_barra1, cod_barra2 = instancia_dp_output.getCodBarra()
            cod_registro_dp = instancia_dp_output.getCodRegistro()
            fecha_venc = instancia_dp_output.getFechaVenc(self.codbarra2p)
            nro_registro = instancia_dp_output.getNroRegistro()
            nro_control = instancia_dp_output.getNroControl(self.codbarra1p)
            marca_movimiento = instancia_dp_output.getMarcaMovimiento()
            tipo_operacion = instancia_dp_output.getTipoOperacion()
            tipo_rendicion = instancia_dp_output.getTipoRendicion()
            moneda = instancia_dp_output.getMoneda()
            impuesto = instancia_dp_output.getImpuesto(self.codbarra1p)
            importe = instancia_dp_output.getImporte()
            nro_boleta = instancia_dp_output.getLiquidacion(self.codbarra1p)
            obj_imponible = instancia_dp_output.getObjImponible(self.codbarra2p)
            obligacion = instancia_dp_output.getObligacion(self.codbarra1p) 
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
        
        elif self.formapagobpc == "Pagos electronicos":

            instancia_general_output = GeneralBPC(self.fecharendicionbpc)
            banco = instancia_general_output.getBanco()
            fecha_rendicion = instancia_general_output.getFechaRendicion()
            nro_rendicion = instancia_general_output.generar_nro_rendicion()
            cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.getCbuCuits()
            cant_registros = instancia_general_output.calcular_cant_registros(self.codbarra1e)
            imp_comision, imp_iva = instancia_general_output.calcular_total_comision_iva()

            total_imp_recaudado_depo_gral = instancia_general_output.calcular_importe_recaudado(self.codbarra1e, self.codbarra2e)
            total_imp_depositado_depositar_depo_gral = instancia_general_output.calcular_importe_depositado_adepositar(self.codbarra1e, self.codbarra2e)

            instancia_sucursal_output = SucursalBPC()
            sucursal_id = instancia_sucursal_output.getSucursal()
            cant_registros_sucursal= instancia_sucursal_output.calcular_cant_registros(self.codbarra2e)
            imp_recaudado_sucursal = instancia_sucursal_output.calcular_importe_recaudado_sucursal(self.codbarra1e, self.codbarra2e)
            imp_depositado_sucursal = instancia_sucursal_output.calcular_importe_depositado_adepositar_sucursal(self.codbarra1e, self.codbarra2e)
            imp_a_depositar_sucursal = instancia_sucursal_output.calcular_importe_depositado_adepositar_sucursal(self.codbarra1e, self.codbarra2e)
            total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal()
            
            instancia_pagos_output = PagosBPC(self.fecharendicionbpc)
            cod_registro = instancia_pagos_output.getCodRegistro(self.formapagobpc)
            caja = instancia_pagos_output.getCaja()
            cajero = instancia_pagos_output.getCajero()
            lote = instancia_pagos_output.getLote()
            cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos(self.codbarra2e)
            imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(self.codbarra1e, self.codbarra2e)
            imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(self.codbarra1e, self.codbarra2e)
            total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos()
            fec_acreditacion = instancia_pagos_output.getFechaAcreditacion()

            instancia_dp_output = DetallePagoElectronicoBPC(self.codbarra1e, self.codbarra2e)
            nro_registro = instancia_dp_output.getNroRegistro()
            cod_registro_dp = instancia_dp_output.getCodRegistro()
            cod_depositante = instancia_dp_output.getCodigoER(self.codbarra1e)
            sucursal_depositante = instancia_dp_output.getSucursalER(self.codbarra1e)
            boleta_ente_depo = instancia_dp_output.getBoletaER(self.codbarra1e)
            nro_control_depo = instancia_dp_output.getNroControlBoletaER(self.codbarra1e)
            imp_recaudado_depo = instancia_dp_output.getImpRecaudadoBoletaER()
            imp_depositado_depo = instancia_dp_output.getImpADepositarYDepositadoER()
            imp_a_depositar_depo = instancia_dp_output.getImpADepositarYDepositadoER()
            fecha_deposito_depo = instancia_dp_output.getFechaDepositoBoletaER(self.fecharendicionbpc)
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

        elif self.formapagobpc == "Ambos pagos":
            instancia_general_output = GeneralBPC(self.fecharendicionbpc)
            banco = instancia_general_output.getBanco()
            fecha_rendicion = instancia_general_output.getFechaRendicion()
            nro_rendicion = instancia_general_output.generar_nro_rendicion()
            cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.getCbuCuits()
            #cant_registros = instancia_general_output.calcular_cant_registros(codbarra1_p) lo haceoms con la suma de codbarras elec + prese
            imp_determinado = instancia_general_output.calcular_importe_determinado_y_pagado(self.codbarra1p, self.codbarra2p)
            imp_pagado = instancia_general_output.calcular_importe_determinado_y_pagado(self.codbarra1p, self.codbarra2p)
            total_imp_recaudado_depo_gral = instancia_general_output.calcular_importe_recaudado(self.codbarra1e, self.codbarra2e)
            
            total_imp_depositado_depositar_depo_gral = instancia_general_output.calcular_importe_depositado_adepositar(self.codbarra1e, self.codbarra2e)
            imp_comision, imp_iva = instancia_general_output.calcular_total_comision_iva()


            instancia_sucursal_output = SucursalBPC()
            sucursal_id = instancia_sucursal_output.getSucursal()
            #cant_registros_sucursal= instancia_sucursal_output.calcular_cant_registros(codbarra1_p)
            imp_pagado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(self.codbarra1p, self.codbarra2p)
            imp_determinado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(self.codbarra1p, self.codbarra2p)
            imp_recaudado_sucursal = instancia_sucursal_output.calcular_importe_recaudado_sucursal(self.codbarra1e, self.codbarra2e)
            imp_depositado_sucursal = instancia_sucursal_output.calcular_importe_depositado_adepositar_sucursal(self.codbarra1e, self.codbarra2e)
            imp_a_depositar_sucursal = instancia_sucursal_output.calcular_importe_depositado_adepositar_sucursal(self.codbarra1e, self.codbarra2e)
            total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal()


            instancia_pagos_output = PagosBPC(self.fecharendicionbpc)
            cod_registro = instancia_pagos_output.getCodRegistro(self.formapagobpc)
            caja = instancia_pagos_output.getCaja()
            cajero = instancia_pagos_output.getCajero()
            lote = instancia_pagos_output.getLote()
            cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos(self.codbarra1p)
            imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(self.codbarra1p, self.codbarra2p)
            imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(self.codbarra1p, self.codbarra2p)
            total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos()
            fec_acreditacion = instancia_pagos_output.getFechaAcreditacion()


            instancia_depositos_output = PagosBPC(self.fecharendicionbpc)
            cod_registro_depo = instancia_depositos_output.getCodRegistro(self.formapagobpc)
            caja = instancia_depositos_output.getCaja()
            cajero = instancia_depositos_output.getCajero()
            lote = instancia_depositos_output.getLote()
            cant_registros_pagos = instancia_depositos_output.calcular_cant_registros_pagos(self.codbarra2e)
            imp_pagado_depo = instancia_depositos_output.calcular_importe_determinado_y_pagado(self.codbarra1e, self.codbarra2e) #njo se usa
            imp_determinado_depo = instancia_depositos_output.calcular_importe_determinado_y_pagado(self.codbarra1e, self.codbarra2e) #no se usa
            total_comision_pagos, total_iva_pagos = instancia_depositos_output.calcular_total_comision_iva_pagos()
            fec_acreditacion = instancia_depositos_output.getFechaAcreditacion()


            instancia_dp_output = DetallePagoPresencialBPC(self.codbarra1p, self.codbarra2p)
            cod_barra1, cod_barra2 = instancia_dp_output.getCodBarra()
            cod_registro_dp = instancia_dp_output.getCodRegistro()
            fecha_venc = instancia_dp_output.getFechaVenc(self.codbarra2p)
            nro_registro = instancia_dp_output.getNroRegistro()
            nro_control = instancia_dp_output.getNroControl(self.codbarra1p)
            marca_movimiento = instancia_dp_output.getMarcaMovimiento()
            tipo_operacion = instancia_dp_output.getTipoOperacion()
            tipo_rendicion = instancia_dp_output.getTipoRendicion()
            moneda = instancia_dp_output.getMoneda()
            impuesto = instancia_dp_output.getImpuesto(self.codbarra1p)
            importe = instancia_dp_output.getImporte()
            nro_boleta = instancia_dp_output.getLiquidacion(self.codbarra1p)
            obj_imponible = instancia_dp_output.getObjImponible(self.codbarra2p)
            obligacion = instancia_dp_output.getObligacion(self.codbarra1p) 
            fecha_pago = instancia_dp_output.getFechaPago()
            comision, iva = instancia_dp_output.calculo_comision_iva_x_dp()

            instancia_dpe_output = DetallePagoElectronicoBPC(self.codbarra1e, self.codbarra2e)
            nro_registro = instancia_dpe_output.getNroRegistro()
            cod_registro_dp = instancia_dpe_output.getCodRegistro()
            cod_depositante = instancia_dpe_output.getCodigoER(self.codbarra1e)
            sucursal_depositante = instancia_dpe_output.getSucursalER(self.codbarra1e)
            boleta_ente_depo = instancia_dpe_output.getBoletaER(self.codbarra1e)
            nro_control_depo = instancia_dpe_output.getNroControlBoletaER(self.codbarra1e)
            imp_recaudado_depo = instancia_dpe_output.getImpRecaudadoBoletaER()
            imp_depositado_depo = instancia_dpe_output.getImpADepositarYDepositadoER()
            imp_a_depositar_depo = instancia_dpe_output.getImpADepositarYDepositadoER()
            fecha_deposito_depo = instancia_dpe_output.getFechaDepositoBoletaER(self.fecharendicionbpc)
            fecha_emision_depo = instancia_dpe_output.getFechaEmisionBoletaER()
            comision, iva = instancia_dpe_output.getImpComisionEIvaER()

            general = ET.Element("General", banco = banco, nroTransaccion = "0", nroRendicion = str(nro_rendicion), fechaRendicion = str(fecha_rendicion) , 
                            cbuOrigen = str(cbu_origen), cuitOrigen = str(cuit_origen), cbuDestino = str(cbu_destino), cuitDestino = str(cuit_destino),
                            registros = str(self.contadorpagospresenciales + self.contadorpagoselectronicos), totalImpDeterminado = str(imp_determinado), totalImpPagado = str(imp_pagado), 
                            totalImpRecaudado = str(total_imp_recaudado_depo_gral), totalImpDepositado = str(total_imp_depositado_depositar_depo_gral),
                            totalImpADepositar = str(total_imp_depositado_depositar_depo_gral), totalImpComision = str(imp_comision), totalImpIVA = str(imp_iva))

            sucursal_tag = ET.SubElement(general,"Sucursal", sucursal = sucursal_id, registros = str(self.contadorpagoselectronicos + self.contadorpagospresenciales),
                                totalImpDeterminado = str(imp_determinado_sucursal), totalImpPagado = str(imp_pagado_sucursal),
                                totalImpRecaudado = str(imp_recaudado_sucursal), totalImpDepositado = str(imp_depositado_sucursal),
                                totalImpADepositar = str(imp_a_depositar_sucursal), totalImpComision = str(total_comision_sucursal), 
                                totalImpIVA = str(total_iva_sucursal))  
            
            pagos = ET.SubElement(sucursal_tag,"Pagos", codigoRegistro = "021", caja = caja, cajero = cajero, fechaAcreditacion = str(fec_acreditacion), lote = lote,
                                registros = str(self.contadorpagospresenciales), totalImpDeterminado = str(imp_determinado_pagos),
                                totalImpPagado = str(imp_pagado_pagos), totalImpComision = str(total_comision_pagos),
                                totalImpIVA = str(total_iva_pagos))  
            
            deposito = ET.SubElement(sucursal_tag,"Deposito", codigoRegistro = "031", caja = caja, cajero = cajero, fechaAcreditacion = str(fec_acreditacion), lote = lote,
                                registros = str(self.contadorpagoselectronicos), totalImpRecaudado = str(total_imp_recaudado_depo_gral),
                                totalImpDepositado = str(imp_depositado_sucursal), totalImpADepositar = str(imp_a_depositar_sucursal),
                                totalImpComision = str(total_comision_pagos), totalImpIVA = str(total_iva_pagos))


            for numero in range(self.contadorpagospresenciales):
                det_pago = ET.SubElement(pagos,"DetallePago", codigoRegistro = "022", nroRegistro = str(numero + 1), impuesto = str(impuesto[numero]), 
                                        fechaVencimiento = str(fecha_venc[numero]), idObjetoImponible = str(obj_imponible[numero]), nroControl = str(nro_control[numero]),
                                        marcaMovimiento = str(marca_movimiento), tipoOperacion = str(tipo_operacion), tipoRendicion = str(tipo_rendicion),
                                        moneda = str(moneda), nroLiquidacionOriginal = str(nro_boleta[numero]), nroLiquidacionActualizado = str(nro_boleta[numero]), 
                                        obligacion = str(obligacion[numero]), barra1 = str(cod_barra1[numero]), barra2 = str(cod_barra2[numero]), fechaPago = str(fecha_pago[numero]), 
                                        impDeterminado = str(importe[numero]), impPagado = str(importe[numero]), impComision = str(comision), 
                                    impIVA = str(iva)
                                    )
            
            for numero in range(self.contadorpagoselectronicos):
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

class GeneradorrOtrosEntes(Generadorr):
    def __init__(self, origen_ok, banco_ok, fecha_rendicion_ok, vector_boletas_ok, vector_importes_ok, vector_fechapagos_ok, vector_cantcuotas_ok, vector_cuotaactual_ok, codbarra1_p, codbarra2_p, codbarra1_e, codbarra2_e, fecharendicion, formapago, contador_pagos_p, contador_pagos_e):
        super().__init__(origen_ok, banco_ok, fecha_rendicion_ok, vector_boletas_ok, vector_importes_ok, vector_fechapagos_ok, vector_cantcuotas_ok, vector_cuotaactual_ok, codbarra1_p, codbarra2_p, codbarra1_e, codbarra2_e, fecharendicion, formapago, contador_pagos_p, contador_pagos_e)
        #self.forma_pago = "Pagos electronicos"
    
    def generar_xml(self):
        datos_arc_config = ArchivoConfig()

        vec_claves, vec_comisiones = datos_arc_config.leer_ini_comisiones(self.banco)
        nro_bancos, nombres_bancos = datos_arc_config.leer_ini_bancos()
        tag_general, tag_sucursal, tag_pagos, tag_dp = datos_arc_config.leer_ini_tags(self.origen, self.banco)

        instancia_general_output = GeneralOutput(self.banco, self.fecharendicion)
        banco = instancia_general_output.getBanco()
        fecha_rendicion = instancia_general_output.getFechaRendicion()
        nro_rendicion = instancia_general_output.generar_nro_rendicion()
        cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.calcular_cbus_y_cuits()
        registros = instancia_general_output.calcular_cant_registros(self.boletas)
        imp_determinado = instancia_general_output.calcular_importe_determinado_y_pagado(self.banco, self.boletas, self.cuotas)
        imp_pagado = instancia_general_output.calcular_importe_determinado_y_pagado(self.banco, self.importes, self.cuotas)
        imp_recaudado = instancia_general_output.getImpRecaudado()
        imp_depositado = instancia_general_output.getImpDepositado()
        imp_a_depositar = instancia_general_output.getImpADepositar()
        imp_comision, imp_iva = instancia_general_output.calcular_total_comision_iva(self.banco, self.boletas, self.fechapagos, self.importes, self.cuotaactual, self.cuotas)


        instancia_sucursal_output = SucursalOutput()
        sucursal_id = instancia_sucursal_output.getSucursal()
        cant_registros_sucursal = instancia_sucursal_output.calcular_cant_registros(self.boletas)
        imp_pagado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(self.banco, self.importes, self.cuotas)
        imp_determinado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(self.banco, self.importes, self.cuotas)
        imp_recaudado_sucursal = instancia_sucursal_output.getImpRecaudado()
        imp_depositado_sucursal = instancia_sucursal_output.getImpDepositado()
        imp_a_depositar_sucursal = instancia_sucursal_output.getImpADepositar()
        total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal(self.banco, self.boletas, self.fechapagos, self.importes, self.cuotaactual, self.cuotas)

        instancia_pagos_output = PagosOutput(self.banco)
        cod_registro = instancia_pagos_output.getCodRegistro()
        caja = instancia_pagos_output.getCaja()
        cajero = instancia_pagos_output.getCajero()
        lote = instancia_pagos_output.getLote(self.banco)
        cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos(self.boletas)
        imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(self.banco, self.importes, self.cuotas)
        imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(self.banco, self.importes, self.cuotas)
        total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos(self.banco, self.boletas, self.fechapagos, self.importes, self.cuotaactual, self.cuotas)


        instancia_dp_output = DetallePagoOutput(self.banco, self.boletas, self.fechapagos, self.importes, self.cuotaactual, self.cuotas)
        cod_registro_dp = instancia_dp_output.getCodRegistro()
        nro_registro = instancia_dp_output.calculo_nro_registro_ycontrol()
        marca_movimiento = instancia_dp_output.getMarcaMovimiento()
        tipo_operacion = instancia_dp_output.getTipoOperacion()
        tipo_rendicion = instancia_dp_output.getTipoRendicion()
        moneda = instancia_dp_output.getMoneda()
        importe = instancia_dp_output.getImporte(self.banco, self.cuotas)
        nro_boleta = instancia_dp_output.getNroBoletas()
        cuota = instancia_dp_output.getCantCuotas(self.banco)
        obj_imponible = instancia_dp_output.getObjImponible()
        obligacion = instancia_dp_output.getNroBoletas() #obligacion es el nroBoleta para gant. para psrm y otax es 0
        fecha_pago = instancia_dp_output.getFechaPago()
        nro_comercio = instancia_dp_output.getNroComercio(self.banco)
        comision, iva = instancia_dp_output.calculo_comision_iva_x_dp(self.banco, self.cuotas)


        claves_vector_general = ['banco', 'nroTransaccion', 'nroRendicion', 'fechaRendicion', 
                            'cbuOrigen', 'cuitOrigen', 'cbuDestino', 'cuitDestino', 'registros', 
                            'totalImpDeterminado', 'totalImpPagado', 'totalImpRecaudado', 'totalImpDepositado',
                            'totalImpADepositar', 'totalImpComision', 'totalImpIVA']

        vector_general = [banco, '0', str(nro_rendicion), fecha_rendicion, cbu_origen, str(cuit_origen), cbu_destino, str(cuit_destino),
                        str(registros), imp_determinado, imp_pagado, imp_recaudado, imp_depositado, imp_a_depositar, imp_comision, imp_iva]


        vector_con_claves_a_mostrar_general = []
        vector_con_indices_a_mostrar_gral = []
        vector_general_datos_a_mostrar = []

        for clave in tag_general:
            if clave in claves_vector_general:
                vector_con_claves_a_mostrar_general.append(clave)
                indice_clave = claves_vector_general.index(clave)
                vector_con_indices_a_mostrar_gral.append(indice_clave)
                vector_general_datos_a_mostrar.append(vector_general[indice_clave])

        #print(vector_con_claves_a_mostrar_general)
        #print(vector_con_indices_a_mostrar_gral)
        #print(vector_general_datos_a_mostrar)

        ############################################################################################333

        claves_vector_sucursal = ['sucursal', 'registros', 'totalImpDeterminado', 'totalImpPagado', 
                                'totalImpRecaudado', 'totalImpDepositado', 'totalImpADepositar', 'totalImpComision', 'totalImpIVA']

        vector_sucursal = [sucursal_id, str(cant_registros_sucursal), imp_determinado_sucursal, imp_pagado_sucursal,
                        imp_recaudado_sucursal, imp_depositado_sucursal, imp_a_depositar_sucursal, total_comision_sucursal, total_iva_sucursal]

        vector_con_claves_a_mostrar_sucursal = []
        vector_con_indices_a_mostrar_sucursal = []
        vector_sucursal_datos_a_mostrar = []

        for clave in tag_sucursal:
            if clave in claves_vector_sucursal:
                vector_con_claves_a_mostrar_sucursal.append(clave)
                indice_clave = claves_vector_sucursal.index(clave)
                vector_con_indices_a_mostrar_sucursal.append(indice_clave)
                vector_sucursal_datos_a_mostrar.append(vector_sucursal[indice_clave])

        ##################################################################################################

        claves_vector_pagos = ['codigoRegistro', 'caja', 'cajero', 'lote', 
                                'registros', 'totalImpDeterminado', 'totalImpPagado', 'totalImpComision', 'totalImpIVA']

        vector_pagos = [cod_registro, caja, cajero, lote,
                        str(cant_registros_pagos), imp_pagado_pagos, imp_determinado_pagos, total_comision_pagos, total_iva_pagos]


        vector_con_claves_a_mostrar_pagos = []
        vector_con_indices_a_mostrar_pagos = []
        vector_pagos_datos_a_mostrar = []


        for clave in tag_pagos:
            if clave in claves_vector_pagos:
                vector_con_claves_a_mostrar_pagos.append(clave)
                indice_clave = claves_vector_pagos.index(clave)
                vector_con_indices_a_mostrar_pagos.append(indice_clave)
                vector_pagos_datos_a_mostrar.append(vector_pagos[indice_clave])

        ###################################################################################################


        general = ET.Element("General",  xmlns="")
        for indice in range(len(vector_con_claves_a_mostrar_general)):
            general.attrib[vector_con_claves_a_mostrar_general[indice]] = vector_general_datos_a_mostrar[indice]

        sucursal_tag = ET.SubElement(general,"Sucursal")
        for indice in range(len(vector_con_claves_a_mostrar_sucursal)):
            sucursal_tag.attrib[vector_con_claves_a_mostrar_sucursal[indice]] = vector_sucursal_datos_a_mostrar[indice]   


        pagos = ET.SubElement(sucursal_tag,"Pagos")
        for indice in range(len(vector_con_claves_a_mostrar_pagos)):
            pagos.attrib[vector_con_claves_a_mostrar_pagos[indice]] = vector_pagos_datos_a_mostrar[indice]   


        for numero in range(len(nro_registro)):

            vector_con_claves_a_mostrar_dp = []
            vector_con_indices_a_mostrar_dp = []
            vector_dp_datos_a_mostrar = []

            claves_vector_dp = ['codigoRegistro', 'nroRegistro', 'nroControl', 'marcaMovimiento', 
                                'tipoOperacion', 'tipoRendicion', 'moneda', 
                                'nroLiquidacionOriginal', 'nroLiquidacionActualizado', 'fechaPago',
                                'impDeterminado', 'impPagado', 'impComision', 'impIVA', 'nroComercio',
                                'cantCuotas', 'idObjetoImponible', 'obligacion']

            if self.origen == 'GANT':
                vector_dp = [cod_registro_dp, str(nro_registro[numero]), str(nro_registro[numero]), marca_movimiento,
                            tipo_operacion, tipo_rendicion, moneda, '0', '0', fecha_pago[numero],
                            importe[numero], importe[numero], comision[numero], iva[numero], nro_comercio,
                            cuota[numero], str(obj_imponible[numero]), obligacion[numero]]

            else:
                vector_dp = [cod_registro_dp, str(nro_registro[numero]), str(nro_registro[numero]), marca_movimiento,
                            tipo_operacion, tipo_rendicion, moneda, nro_boleta[numero], nro_boleta[numero], fecha_pago[numero],
                            importe[numero], importe[numero], comision[numero], iva[numero], nro_comercio,
                            cuota[numero], str(obj_imponible[numero]), '0']

            for clave in tag_dp:
                if clave in claves_vector_dp:
                    vector_con_claves_a_mostrar_dp.append(clave)
                    indice_clave = claves_vector_dp.index(clave)
                    vector_con_indices_a_mostrar_dp.append(indice_clave)
                    vector_dp_datos_a_mostrar.append(vector_dp[indice_clave])

            det_pago = ET.SubElement(pagos,"DetallePago")
            det_pago.text = " "
            #det_pago.attrib[vector_con_claves_a_mostrar_dp[0]] = vector_dp_datos_a_mostrar[0]
            for indice in range(len(vector_con_claves_a_mostrar_dp)):
                det_pago.attrib[vector_con_claves_a_mostrar_dp[indice]] = vector_dp_datos_a_mostrar[indice]   


        #print(vector_con_claves_a_mostrar_dp)
        #print(vector_con_indices_a_mostrar_dp)
        #print(vector_dp_datos_a_mostrar)

        tree = ET.ElementTree(general)    
        tree.write(self.fecharendicion[0:4] + self.fecharendicion[5:7] + self.fecharendicion[8:10] + '.P' + self.banco[2:5], xml_declaration=True, encoding='utf-8')

        with zipfile.ZipFile(f"{self.fecharendicion[0:4] + self.fecharendicion[5:7] + self.fecharendicion[8:10] + '.P' + self.banco[2:5]}" + ".zip", 'w') as zf:
            tree = ET.ElementTree(general)    
            tree.write(self.fecharendicion[0:4] + self.fecharendicion[5:7] + self.fecharendicion[8:10] + '.P' + self.banco[2:5], xml_declaration=True, encoding='utf-8')
            zf.write(self.fecharendicion[0:4] + self.fecharendicion[5:7] + self.fecharendicion[8:10] + '.P' + self.banco[2:5])


def generar_xml(generador : Generadorr):
    generador.generar_xml()