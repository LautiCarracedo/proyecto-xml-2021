from clase_general import GeneralOutput
from clase_sucursal import SucursalOutput
from clase_pagos import PagosOutput
from clase_dp import DetallePagoOutput

from lectura_archivo_config import ArchivoConfig

import xml.etree.ElementTree as ET

import zipfile

class Generador():
    def __init__(self, origen_ok, banco_ok, fecha_rendicion_ok, decision_comision, comision_deb, comision_cred, comision_pres, vector_boletas_ok, vector_importes_ok, vector_fechapagos_ok, vector_cantcuotas_ok, vector_cuotaactual_ok, vector_codbarra1_ok, vector_codbarra2_ok):
        self.origen = origen_ok
        self.banco = banco_ok
        self.fecha_rendicion = fecha_rendicion_ok
        self.decision_comision = decision_comision
        self.comision_deb_ingresada = comision_deb
        self.comision_cred_ingresada = comision_cred
        self.comision_pres_ingresada = comision_pres
        self.boletas = vector_boletas_ok
        self.importes = vector_importes_ok
        self.fechas_pagos = vector_fechapagos_ok
        self.cant_cuotas = vector_cantcuotas_ok
        self.cuotas_acuales = vector_cuotaactual_ok
        self.codbarra1 = vector_codbarra1_ok
        self.codbarra2 = vector_codbarra2_ok

    def generar_xml(self, origen_ok, banco_ok, fecha_rendicion_ok, decision_comision, comision_deb, comision_cred, comision_pres, vector_boletas_ok, vector_importes_ok, vector_fechapagos_ok, vector_cantcuotas_ok, vector_cuotaactual_ok, vector_codbarra1_ok, vector_codbarra2_ok):
        datos_arc_config = ArchivoConfig()

        vec_claves, vec_comisiones = datos_arc_config.leer_ini_comisiones(banco_ok)
        nro_bancos, nombres_bancos = datos_arc_config.leer_ini_bancos()
        tag_general, tag_sucursal, tag_pagos, tag_dp = datos_arc_config.leer_ini_tags(origen_ok, banco_ok)

        if banco_ok == "00079" or banco_ok == "00082":
            instancia_general_output = GeneralOutput(banco_ok, fecha_rendicion_ok)
            banco = instancia_general_output.getBanco()
            fecha_rendicion = instancia_general_output.getFechaRendicion()
            nro_rendicion = instancia_general_output.generar_nro_rendicion()
            cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.calcular_cbus_y_cuits()
            registros = instancia_general_output.calcular_cant_registros(vector_codbarra1_ok)
            imp_determinado = instancia_general_output.calcular_importe_determinado_y_pagado(banco_ok, vector_importes_ok, vector_cantcuotas_ok, vector_codbarra2_ok)
            imp_pagado = instancia_general_output.calcular_importe_determinado_y_pagado(banco_ok, vector_importes_ok, vector_cantcuotas_ok, vector_codbarra2_ok)
            imp_recaudado = instancia_general_output.getImpRecaudado()
            imp_depositado = instancia_general_output.getImpDepositado()
            imp_a_depositar = instancia_general_output.getImpADepositar()
            imp_anul_timbradora = instancia_general_output.getImpAnulacionTimbradoras()
            imp_comision, imp_iva = instancia_general_output.calcular_total_comision_iva(decision_comision, comision_deb, comision_cred, comision_pres, banco_ok, vector_boletas_ok, vector_fechapagos_ok, vector_importes_ok, vector_cuotaactual_ok, vector_cantcuotas_ok, vector_codbarra1_ok, vector_codbarra2_ok)


            instancia_sucursal_output = SucursalOutput()
            sucursal_id = instancia_sucursal_output.getSucursal(banco_ok)
            cant_registros_sucursal = instancia_sucursal_output.calcular_cant_registros(vector_codbarra1_ok)
            imp_pagado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(banco_ok, vector_importes_ok, vector_cantcuotas_ok, vector_codbarra2_ok)
            imp_determinado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(banco_ok, vector_importes_ok, vector_cantcuotas_ok, vector_codbarra2_ok)
            imp_recaudado_sucursal = instancia_sucursal_output.getImpRecaudado(banco_ok)
            imp_depositado_sucursal = instancia_sucursal_output.getImpDepositado(banco_ok)
            imp_a_depositar_sucursal = instancia_sucursal_output.getImpADepositar(banco_ok)
            imp_anul_timbradora_sucursal = instancia_sucursal_output.getImpAnulacionTim(banco_ok)
            total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal(decision_comision, comision_deb, comision_cred, comision_pres, banco_ok, vector_boletas_ok, vector_fechapagos_ok, vector_importes_ok, vector_cuotaactual_ok, vector_cantcuotas_ok, vector_codbarra1_ok, vector_codbarra2_ok)


            instancia_pagos_output = PagosOutput(banco_ok)
            cod_registro = instancia_pagos_output.getCodRegistro()
            caja = instancia_pagos_output.getCaja()
            cajero = instancia_pagos_output.getCajero()
            lote = instancia_pagos_output.getLote(banco_ok)
            cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos(vector_codbarra1_ok)
            imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(banco_ok, vector_importes_ok, vector_cantcuotas_ok, vector_codbarra2_ok)
            imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(banco_ok, vector_importes_ok, vector_cantcuotas_ok, vector_codbarra2_ok)
            total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos(decision_comision, comision_deb, comision_cred, comision_pres, banco_ok, vector_boletas_ok, vector_fechapagos_ok, vector_importes_ok, vector_cuotaactual_ok, vector_cantcuotas_ok, vector_codbarra1_ok, vector_codbarra2_ok)
            fechaAcreditacion = "0001-01-01"

            instancia_dp_output = DetallePagoOutput(banco_ok, vector_boletas_ok, vector_fechapagos_ok, vector_importes_ok, vector_cuotaactual_ok, vector_cantcuotas_ok, vector_codbarra1_ok, vector_codbarra2_ok)
            cod_registro_dp = instancia_dp_output.getCodRegistro()
            nro_registro = instancia_dp_output.calculo_nro_registro_x_codbarras()
            nro_control = instancia_dp_output.getNroControl(banco_ok)
            marca_movimiento = instancia_dp_output.getMarcaMovimiento()
            tipo_operacion = instancia_dp_output.getTipoOperacion()
            tipo_rendicion = instancia_dp_output.getTipoRendicion()
            moneda = instancia_dp_output.getMoneda()
            importe = instancia_dp_output.extraer_importe_codbarra2()
            nro_boleta = instancia_dp_output.extraer_nroLiquidacion_codbarra1()
            cuota = instancia_dp_output.getCantCuotas(banco_ok)
            obligacion = instancia_dp_output.extraer_obligacion_codbarra1()
            fecha_pago = instancia_dp_output.getFechaPago()
            comision, iva = instancia_dp_output.calculo_comision_iva_x_dp(decision_comision, comision_deb, comision_cred, comision_pres, banco_ok, vector_cantcuotas_ok)
            impuesto = instancia_dp_output.getImpuestoEnte079y082()
            id_obj_imp = instancia_dp_output.extraer_objImponible_codbarra2()
            codbarra1 = instancia_dp_output.getCodBarra1()
            codbarra2 = instancia_dp_output.getCodBarra2()
            fecha_venc = instancia_dp_output.extraer_fechaVenc_codbarra2()


            claves_vector_general = ['banco', 'nroTransaccion', 'nroRendicion', 'fechaRendicion', 
                                'cbuOrigen', 'cuitOrigen', 'cbuDestino', 'cuitDestino', 'registros', 
                                'totalImpDeterminado', 'totalImpPagado', 'totalImpRecaudado', 'totalImpDepositado',
                                'totalImpADepositar', 'totalImpAnulacionTimbradoras', 'totalImpComision', 'totalImpIVA']
    
            vector_general = [banco, '0000000000000000', str(nro_rendicion), fecha_rendicion, cbu_origen, str(cuit_origen), cbu_destino, str(cuit_destino),
                            str(registros), imp_determinado, imp_pagado, imp_recaudado, imp_depositado, imp_a_depositar, imp_anul_timbradora, imp_comision, imp_iva]
    
    
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
                                    'totalImpRecaudado', 'totalImpDepositado', 'totalImpADepositar', 'totalImpAnulacionTimbradoras', 'totalImpComision', 'totalImpIVA']
    
            vector_sucursal = [sucursal_id, str(cant_registros_sucursal), imp_determinado_sucursal, imp_pagado_sucursal,
                            imp_recaudado_sucursal, imp_depositado_sucursal, imp_a_depositar_sucursal, imp_anul_timbradora_sucursal, total_comision_sucursal, total_iva_sucursal]
    
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
    
            claves_vector_pagos = ['codigoRegistro', 'caja', 'cajero', 'fechaAcreditacion', 'lote', 
                                    'registros', 'totalImpDeterminado', 'totalImpPagado', 'totalImpComision', 'totalImpIVA']
    
            vector_pagos = [cod_registro, caja, cajero, fechaAcreditacion, lote,
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
    
                claves_vector_dp = ['codigoRegistro', 'nroRegistro', 'impuesto','fechaVencimiento','idObjetoImponible',
                                     'nroControl', 'marcaMovimiento', 
                                    'tipoOperacion', 'tipoRendicion', 'moneda', 
                                    'nroLiquidacionOriginal', 'nroLiquidacionActualizado','obligacion', 'barra1', 'barra2', 
                                    'fechaPago',
                                    'impDeterminado', 'impPagado', 'impComision', 'impIVA']
    
                if origen_ok == 'GANT':
                    vector_dp = [cod_registro_dp, str(nro_registro[numero]), str(impuesto[numero]), str(fecha_venc[numero]), str(id_obj_imp[numero]),
                                str(nro_control), marca_movimiento,
                                tipo_operacion, tipo_rendicion, moneda, str(nro_boleta[numero]), str(nro_boleta[numero]),str(obligacion[numero]),
                                str(codbarra1[numero]), str(codbarra2[numero]), fecha_pago[numero],
                                str(importe[numero]), str(importe[numero]), comision[numero], iva[numero]]
    
                else:
                    vector_dp = [cod_registro_dp, str(nro_registro[numero]), str(impuesto), str(fecha_venc[numero]), str(id_obj_imp[numero]),
                                str(nro_control), marca_movimiento,
                                tipo_operacion, tipo_rendicion, moneda, str(nro_boleta[numero]), str(nro_boleta[numero]),str(obligacion[numero]),
                                str(codbarra1[numero]), str(codbarra2[numero]), fecha_pago[numero],
                                str(importe[numero]), str(importe[numero]), comision[numero], iva[numero]]
    
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

        else:

            instancia_general_output = GeneralOutput(banco_ok, fecha_rendicion_ok)
            banco = instancia_general_output.getBanco()
            fecha_rendicion = instancia_general_output.getFechaRendicion()
            nro_rendicion = instancia_general_output.generar_nro_rendicion()
            cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.calcular_cbus_y_cuits()
            registros = instancia_general_output.calcular_cant_registros(vector_boletas_ok)
            imp_determinado = instancia_general_output.calcular_importe_determinado_y_pagado(banco_ok, vector_importes_ok, vector_cantcuotas_ok, vector_codbarra2_ok)
            imp_pagado = instancia_general_output.calcular_importe_determinado_y_pagado(banco_ok, vector_importes_ok, vector_cantcuotas_ok, vector_codbarra2_ok)
            imp_recaudado = instancia_general_output.getImpRecaudado()
            imp_depositado = instancia_general_output.getImpDepositado()
            imp_a_depositar = instancia_general_output.getImpADepositar()
            imp_comision, imp_iva = instancia_general_output.calcular_total_comision_iva(decision_comision, comision_deb, comision_cred, comision_pres, banco_ok, vector_boletas_ok, vector_fechapagos_ok, vector_importes_ok, vector_cuotaactual_ok, vector_cantcuotas_ok, vector_codbarra1_ok, vector_codbarra2_ok)


            instancia_sucursal_output = SucursalOutput()
            sucursal_id = instancia_sucursal_output.getSucursal(banco_ok)
            cant_registros_sucursal = instancia_sucursal_output.calcular_cant_registros(vector_boletas_ok)
            imp_pagado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(banco_ok, vector_importes_ok, vector_cantcuotas_ok, vector_codbarra2_ok)
            imp_determinado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(banco_ok, vector_importes_ok, vector_cantcuotas_ok, vector_codbarra2_ok)
            imp_recaudado_sucursal = instancia_sucursal_output.getImpRecaudado(banco_ok)
            imp_depositado_sucursal = instancia_sucursal_output.getImpDepositado(banco_ok)
            imp_a_depositar_sucursal = instancia_sucursal_output.getImpADepositar(banco_ok)
            total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal(decision_comision, comision_deb, comision_cred, comision_pres, banco_ok, vector_boletas_ok, vector_fechapagos_ok, vector_importes_ok, vector_cuotaactual_ok, vector_cantcuotas_ok, vector_codbarra1_ok, vector_codbarra2_ok)

            instancia_pagos_output = PagosOutput(banco_ok)
            cod_registro = instancia_pagos_output.getCodRegistro()
            caja = instancia_pagos_output.getCaja()
            cajero = instancia_pagos_output.getCajero()
            lote = instancia_pagos_output.getLote(banco_ok)
            cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos(vector_boletas_ok)
            imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(banco_ok, vector_importes_ok, vector_cantcuotas_ok, vector_codbarra2_ok)
            imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(banco_ok, vector_importes_ok, vector_cantcuotas_ok, vector_codbarra2_ok)
            total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos(decision_comision, comision_deb, comision_cred, comision_pres, banco_ok, vector_boletas_ok, vector_fechapagos_ok, vector_importes_ok, vector_cuotaactual_ok, vector_cantcuotas_ok, vector_codbarra1_ok, vector_codbarra2_ok)


            instancia_dp_output = DetallePagoOutput(banco_ok, vector_boletas_ok, vector_fechapagos_ok, vector_importes_ok, vector_cuotaactual_ok, vector_cantcuotas_ok, vector_codbarra1_ok, vector_codbarra2_ok)
            cod_registro_dp = instancia_dp_output.getCodRegistro()
            nro_registro = instancia_dp_output.calculo_nro_registro_ycontrol()
            marca_movimiento = instancia_dp_output.getMarcaMovimiento()
            tipo_operacion = instancia_dp_output.getTipoOperacion()
            tipo_rendicion = instancia_dp_output.getTipoRendicion()
            moneda = instancia_dp_output.getMoneda()
            importe = instancia_dp_output.getImporte(banco_ok, vector_cantcuotas_ok)
            nro_boleta = instancia_dp_output.getNroBoletas()
            cuota = instancia_dp_output.getCantCuotas(banco_ok)
            obj_imponible = instancia_dp_output.getObjImponible()
            obligacion = instancia_dp_output.getNroBoletas() #obligacion es el nroBoleta para gant. para psrm y otax es 0
            fecha_pago = instancia_dp_output.getFechaPago()
            nro_comercio = instancia_dp_output.getNroComercio(banco_ok)
            comision, iva = instancia_dp_output.calculo_comision_iva_x_dp(decision_comision, comision_deb, comision_cred, comision_pres, banco_ok, vector_cantcuotas_ok)

   
            


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

                claves_vector_dp = ['codigoRegistro', 'nroRegistro','nroControl', 'marcaMovimiento', 
                                    'tipoOperacion', 'tipoRendicion', 'moneda', 
                                    'nroLiquidacionOriginal', 'nroLiquidacionActualizado','fechaPago',
                                    'impDeterminado', 'impPagado', 'impComision', 'impIVA', 'nroComercio',
                                    'cantCuotas', 'idObjetoImponible', 'obligacion']

                if origen_ok == 'GANT':
                    vector_dp = [cod_registro_dp, str(nro_registro[numero]), str(nro_registro[numero]), marca_movimiento,
                                tipo_operacion, tipo_rendicion, moneda, '0', '0', fecha_pago[numero],
                                importe[numero], importe[numero], comision[numero], iva[numero], nro_comercio,
                                cuota[numero], str(obj_imponible[numero]), obligacion[numero]]

                else:
                    vector_dp = [cod_registro_dp, str(nro_registro[numero]), str(nro_registro[numero]), marca_movimiento,
                                tipo_operacion, tipo_rendicion, moneda, nro_boleta[numero], nro_boleta[numero], 
                                fecha_pago[numero],
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
        tree.write(fecha_rendicion_ok[0:4] + fecha_rendicion_ok[5:7] + fecha_rendicion_ok[8:10] + '.P' + banco_ok[2:5], xml_declaration=True, encoding='utf-8')

        with zipfile.ZipFile(f"{fecha_rendicion_ok[0:4] + fecha_rendicion_ok[5:7] + fecha_rendicion_ok[8:10] + '.P' + banco_ok[2:5]}" + ".zip", 'w') as zf:
            tree = ET.ElementTree(general)    
            tree.write(fecha_rendicion_ok[0:4] + fecha_rendicion_ok[5:7] + fecha_rendicion_ok[8:10] + '.P' + banco_ok[2:5], xml_declaration=True, encoding='utf-8')
            zf.write(fecha_rendicion_ok[0:4] + fecha_rendicion_ok[5:7] + fecha_rendicion_ok[8:10] + '.P' + banco_ok[2:5])
                       
 
            