from os import remove
from tkinter import *
from tkinter import ttk
from tkinter.constants import CENTER, N
from tkinter import messagebox

import xml.etree.ElementTree as ET

from clases import GeneralOutput, SucursalOutput, PagosOutput, DetallePagoOutput

class Ventana:
    def verificar_cant_registros(self):
        try:
            #toma de datos origen
            origen = self.cbbox_origen.get()
            #print(origen)

            #toma de datos general
            vector_datos_general = []
            banco_t = str(self.cbbox_nrobanco.get())
            vector_datos_general.append(banco_t)

            fecha_rendicion = str(self.input_fecharendicion.get())
            fecha_rendicion_t = fecha_rendicion.replace('/','-')

            vector_datos_general.append(fecha_rendicion_t)
            #print(vector_datos_general)
       
            #toma de datos dp
            boletas = self.input_nroboleta.get("1.0","end-1c")
            vector_boletas = boletas.split('\n')
            #print(vector_boletas)

            importes = self.input_importe.get("1.0","end-1c")
            vector_importes = importes.split('\n')
            vector_importes_format_ok = []
            for importes in vector_importes:
                importes_format_punto_miles = importes.replace('.','')
                importes_format_coma_decimal = importes_format_punto_miles.replace(',','.')
                vector_importes_format_ok.append(importes_format_coma_decimal)

            #print(vector_importes_format_ok)

            fecha_pagos = self.input_fechapago.get("1.0","end-1c")
            vector_fechapagos = fecha_pagos.split('\n')
            vector_fechapagos_format_ok = []
            format_fechas = False
            for fechas in vector_fechapagos:
                fechas_format = fechas.replace('/','-')
                if ((len(fechas_format) == 10) and (str(fechas_format[0:4]).isnumeric()) and (fechas_format[4] == '-') and (str(fechas_format[5:7]).isnumeric()) and (fechas_format[7] == '-') and (str(fechas_format[8:10]).isnumeric())):
                    fechas_format += 'T09:30:00.000'
                    vector_fechapagos_format_ok.append(fechas_format)
                    format_fechas = True
                else:
                    format_fechas = False
            #print(vector_fechapagos_format_ok)

            cant_cuotas = self.input_cant_cuotas.get("1.0","end-1c")
            vector_cantcuotas = cant_cuotas.split('\n')

            cuota_actual = self.input_cuotaactual.get("1.0","end-1c")
            vector_cuotaactual = cuota_actual.split('\n')
            #print(vector_cuotaactual)

            #self.label_nroboleta = Label(self.frame,text='Número de boleta:',pady=10,padx=20)
            #self.label_nroboleta.grid(row=5,column=0,sticky='N' )

            cant_boletas = Label(self.frame, text='Cant registros: ' + str(len(vector_boletas)), pady=10,padx=20 )
            cant_boletas.grid(row=6, column=1)

            cant_importes = Label(self.frame, text='Cant registros: ' + str(len(vector_importes)), pady=10,padx=20 )
            cant_importes.grid(row=6, column=3)

            cant_pagos = Label(self.frame, text='Cant registros: ' + str(len(vector_fechapagos)), pady=10,padx=20 )
            cant_pagos.grid(row=6, column=5)

            cant_cantcuotas = Label(self.frame, text='Cant registros: ' + str(len(vector_cantcuotas)), pady=10,padx=20 )
            cant_cantcuotas.grid(row=6, column=7)

            cant_cuotaactual = Label(self.frame, text='Cant: ' + str(len(vector_cuotaactual)), pady=10,padx=20 )
            cant_cuotaactual.grid(row=6, column=9)



        except:
            messagebox.showerror(message='Error al calcular registros. Pruebe nevamente', title='Error')

    
    
    def tomar_datos(self):
        try:
            #toma de datos origen
            origen = self.cbbox_origen.get()
            #print(origen)

            #toma de datos general
            vector_datos_general = []
            banco_t = str(self.cbbox_nrobanco.get())
            vector_datos_general.append(banco_t)

            fecha_rendicion = str(self.input_fecharendicion.get())
            fecha_rendicion_t = fecha_rendicion.replace('/','-')
            if ((len(fecha_rendicion_t) == 10) and (str(fecha_rendicion_t[0:2]).isnumeric()) and (fecha_rendicion_t[2] == '-') and (str(fecha_rendicion_t[3:5]).isnumeric()) and (fecha_rendicion_t[5] == '-') and (str(fecha_rendicion_t[6:10]).isnumeric())):
                fecha_rendicion_format_ok = True
                fecha_rendicion_t = fecha_rendicion_t[6:10] + fecha_rendicion_t[5] + fecha_rendicion_t[3:5] + fecha_rendicion_t[2] + fecha_rendicion_t[0:2] + 'T09:30:00.000'
            else:
                fecha_rendicion_format_ok = False

            vector_datos_general.append(fecha_rendicion_t)
            #print(vector_datos_general)
            #else:
            #    messagebox.showerror(message="Error al cargar la fecha. Debe ser formato AAAA/MM/DD", title="Error en la fecha")

            #toma de datos dp
            boletas = self.input_nroboleta.get("1.0","end-1c")
            vector_boletas = boletas.split('\n')
            #print(vector_boletas)

            importes = self.input_importe.get("1.0","end-1c")
            vector_importes = importes.split('\n')
            vector_importes_format_ok = []
            importes_es_float = False
            for importes in vector_importes:
                importes_format_punto_miles = importes.replace('.','')
                importes_format_coma_decimal = importes_format_punto_miles.replace(',','.')
                if float(importes_format_coma_decimal):
                    importes_es_float = True
                    vector_importes_format_ok.append(importes_format_coma_decimal)
                else:
                    importes_es_float = False

            #print(vector_importes_format_ok)

            fecha_pagos = self.input_fechapago.get("1.0","end-1c")
            vector_fechapagos = fecha_pagos.split('\n')
            vector_fechapagos_format_ok = []
            format_fechas = False
            for fechas in vector_fechapagos:
                fechas_format = fechas.replace('/','-')
                if ((len(fechas_format) == 10) and (str(fechas_format[0:2]).isnumeric()) and (fechas_format[2] == '-') and (str(fechas_format[3:5]).isnumeric()) and (fechas_format[5] == '-') and (str(fechas_format[6:10]).isnumeric())):
                    fechas_format = fechas_format[6:10] + fechas_format[5] + fechas_format[3:5] + fechas_format[2] + fechas_format[0:2] + 'T09:30:00.000'
                    vector_fechapagos_format_ok.append(fechas_format)
                    format_fechas = True
                else:
                    format_fechas = False
            #print(vector_fechapagos_format_ok)

            cant_cuotas = self.input_cant_cuotas.get("1.0","end-1c")
            vector_cantcuotas = cant_cuotas.split('\n')
            cuotas_es_numero_cred_deb = False
            for cuota in vector_cantcuotas:
                if banco_t == '00935':
                    if cuota == '18' or cuota == '12':
                        cuotas_es_numero_cred_deb = True
                else:
                    if cuota == 'C' or cuota == 'D':
                        cuotas_es_numero_cred_deb = True
                    else:
                        cuotas_es_numero_cred_deb = False
            #print(cuotas_es_numero_cred_deb)


            
            cuota_actual = self.input_cuotaactual.get("1.0","end-1c")
            vector_cuotaactual = cuota_actual.split('\n')
            cuotaactual_es_numero = False
            if (banco_t == '00202' or banco_t == '00216') and len(vector_cuotaactual) == 1: 
                # como los text aunque no carguemos nada lo toma como len=1, para el caso de visa y master 
                # que no utilizamos estos campos lo cargamos en cero y se desactiva para no pdoer cargar
                vector_cuotaactual.pop()
                for boleta in range(len(vector_boletas)):
                    vector_cuotaactual.append('0')
            #print(vector_cuotaactual)
                    
              
            for c_act in vector_cuotaactual:
                if c_act.isnumeric():
                    cuotaactual_es_numero = True
                else:
                    cuotaactual_es_numero = False
                
            #print(vector_cuotaactual)

            if cuotaactual_es_numero:
                if cuotas_es_numero_cred_deb:
                    if importes_es_float:
                        if format_fechas:
                            if banco_t.isnumeric():
                                if fecha_rendicion_format_ok:
                                    if len(vector_boletas) == len(vector_importes) == len(vector_fechapagos) == len(vector_cantcuotas) == len(vector_cuotaactual):
                                    
                                        instancia_general_output = GeneralOutput(banco_t, fecha_rendicion_t)
                                        instancia_sucursal_output = SucursalOutput()
                                        instancia_pagos_output = PagosOutput(banco_t)
                                        instancia_dp_output = DetallePagoOutput(banco_t, vector_boletas, vector_fechapagos_format_ok, vector_importes_format_ok, vector_cuotaactual, vector_cantcuotas)

                                        banco = instancia_general_output.getBanco()
                                        nro_rendicion = instancia_general_output.generar_nro_rendicion()
                                        fecha_rendicion = instancia_general_output.getFechaRendicion()
                                        cbu_origen, cuit_origen, cbu_destino, cuit_destino = instancia_general_output.calcular_cbus_y_cuits()
                                        cant_registros = instancia_general_output.calcular_cant_registros(vector_boletas)
                                        imp_pagado = instancia_general_output.calcular_importe_determinado_y_pagado(banco_t, vector_importes_format_ok, vector_cantcuotas)
                                        imp_determinado = instancia_general_output.calcular_importe_determinado_y_pagado(banco_t, vector_importes_format_ok, vector_cantcuotas)
                                        imp_recaudado = instancia_general_output.getImpRecaudado()
                                        imp_depositado = instancia_general_output.getImpDepositado()
                                        imp_a_depositar = instancia_general_output.getImpADepositar()
                                        total_comision, total_iva = instancia_general_output.calcular_total_comision_iva(banco_t, vector_boletas, vector_fechapagos_format_ok, vector_importes_format_ok, vector_cuotaactual, vector_cantcuotas)
                                        informe_importes, informe_suma_importes, informe_comisiones, informe_suma_comisiones, informe_ivas_dp, informe_suma_ivas, informe_cant_registros, informe_iva_general = instancia_general_output.informes_general(banco_t ,vector_boletas, vector_fechapagos_format_ok, vector_importes_format_ok, vector_cuotaactual, vector_cantcuotas)


                                        sucursal_id = instancia_sucursal_output.getSucursal()
                                        cant_registros_sucursal = instancia_sucursal_output.calcular_cant_registros(vector_boletas)
                                        imp_pagado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(banco_t, vector_importes_format_ok, vector_cantcuotas)
                                        imp_determinado_sucursal = instancia_sucursal_output.calcular_importe_determinado_y_pagado(banco_t, vector_importes_format_ok, vector_cantcuotas)
                                        imp_recaudado_sucursal = instancia_sucursal_output.getImpRecaudado()
                                        imp_depositado_sucursal = instancia_sucursal_output.getImpDepositado()
                                        imp_a_depositar_sucursal = instancia_sucursal_output.getImpADepositar()
                                        total_comision_sucursal, total_iva_sucursal = instancia_sucursal_output.calcular_total_comision_iva_sucursal(banco_t, vector_boletas, vector_fechapagos_format_ok, vector_importes_format_ok, vector_cuotaactual, vector_cantcuotas)


                                        cod_registro = instancia_pagos_output.getCodRegistro()
                                        caja = instancia_pagos_output.getCaja()
                                        cajero = instancia_pagos_output.getCajero()
                                        lote = instancia_pagos_output.getLote(banco_t)
                                        cant_registros_pagos = instancia_pagos_output.calcular_cant_registros_pagos(vector_boletas)
                                        imp_pagado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(banco_t, vector_importes_format_ok, vector_cantcuotas)
                                        imp_determinado_pagos = instancia_pagos_output.calcular_importe_determinado_y_pagado(banco_t, vector_importes_format_ok, vector_cantcuotas)
                                        total_comision_pagos, total_iva_pagos = instancia_pagos_output.calcular_total_comision_iva_pagos(banco_t, vector_boletas, vector_fechapagos_format_ok, vector_importes_format_ok, vector_cuotaactual, vector_cantcuotas)


                                        cod_registro_dp = instancia_dp_output.getCodRegistro()
                                        nro_registro = instancia_dp_output.calculo_nro_registro_ycontrol()
                                        #print('cant registros', nro_registro)
                                        marca_movimiento = instancia_dp_output.getMarcaMovimiento()
                                        tipo_operacion = instancia_dp_output.getTipoOperacion()
                                        tipo_rendicion = instancia_dp_output.getTipoRendicion()
                                        moneda = instancia_dp_output.getMoneda()
                                        importe = instancia_dp_output.getImporte(banco_t, vector_cantcuotas)
                                        nro_boleta = instancia_dp_output.getNroBoletas()
                                        cuota = instancia_dp_output.getCantCuotas(banco_t)
                                        obj_imponible = instancia_dp_output.getObjImponible()
                                        obligacion = instancia_dp_output.getNroBoletas() #obligacion es el nroBoleta para gant. para psrm y otax es 0
                                        fecha_pago = instancia_dp_output.getFechaPago()
                                        nro_comercio = instancia_dp_output.getNroComercio(banco_t)
                                        comision, iva = instancia_dp_output.calculo_comision_iva_x_dp(banco_t, vector_cantcuotas)


                                        if origen == 'PSRM' or origen == 'OTAX':
                                            #generando estructura xml con los campos
                                            general = ET.Element("General",  xmlns="", banco = banco, nroTransaccion = "0", nroRendicion = str(nro_rendicion), fechaRendicion = fecha_rendicion , 
                                                                cbuOrigen = str(cbu_origen), cuitOrigen = str(cuit_origen), cbuDestino = str(cbu_destino), cuitDestino = str(cuit_destino),
                                                                registros = str(cant_registros),
                                                                totalImpDeterminado = str(imp_determinado), totalImpPagado = str(imp_pagado), totalImpRecaudado = str(imp_recaudado), totalImpDepositado = str(imp_depositado),
                                                                totalImpADepositar = str(imp_a_depositar), totalImpComision = str(total_comision), totalImpIVA = str(total_iva))


                                            
                                            sucursal_tag = ET.SubElement(general,"Sucursal", sucursal = sucursal_id, registros = str(cant_registros_sucursal),
                                                                        totalImpDeterminado = str(imp_determinado_sucursal), totalImpPagado = str(imp_pagado_sucursal),
                                                                        totalImpRecaudado = str(imp_recaudado_sucursal), totalImpDepositado = str(imp_depositado_sucursal),
                                                                        totalImpADepositar = str(imp_a_depositar_sucursal), totalImpComision = str(total_comision_sucursal), 
                                                                        totalImpIVA = str(total_iva_sucursal))                                


                                            #sucursal_tag.append(0)                 

                                            pagos = ET.SubElement(sucursal_tag,"Pagos", codigoRegistro = cod_registro, caja = caja, cajero = cajero, lote = lote,
                                                                    registros = str(cant_registros_pagos), totalImpDeterminado = str(imp_determinado_pagos),
                                                                    totalImpPagado = str(imp_pagado_pagos), totalImpComision = str(total_comision_pagos),
                                                                    totalImpIVA = str(total_iva_pagos)
                                                                    )


                                            for numero in range(len(nro_registro)):
                                                if banco == '00202' or banco == '00216':
                                                    det_pago = ET.SubElement(pagos,"DetallePago", codigoRegistro = str(cod_registro_dp), nroRegistro = str(numero + 1), nroControl = str(numero + 1),
                                                                        marcaMovimiento = str(marca_movimiento), tipoOperacion = str(tipo_operacion), tipoRendicion = str(tipo_rendicion),
                                                                        moneda = str(moneda), nroLiquidacionOriginal = nro_boleta[numero], nroLiquidacionActualizado = nro_boleta[numero], 
                                                                        fechaPago = str(fecha_pago[numero]), impDeterminado = importe[numero], impPagado = str(importe[numero]), impComision = str(comision[numero]), 
                                                                        impIVA = str(iva[numero]), nroComercio = str(nro_comercio), cantCuotas = str(cuota[numero])
                                                                      ).text = ' '
                                                else:
                                                    det_pago = ET.SubElement(pagos,"DetallePago", codRegistro = str(cod_registro_dp), nroRegistro = str(numero + 1), nroControl = str(numero + 1),
                                                                        marcaMovimiento = str(marca_movimiento), tipoOperacion = str(tipo_operacion), tipoRendicion = str(tipo_rendicion),
                                                                        moneda = str(moneda), nroLiquidacionOriginal = nro_boleta[numero], nroLiquidacionActualizado = nro_boleta[numero], 
                                                                        fechaPago = str(fecha_pago[numero]), impDeterminado = str(importe[numero]), impPagado = str(importe[numero]), impComision = str(comision[numero]), 
                                                                        impIVA = str(iva[numero]), nroComercio = str(nro_comercio), cantCuotas = str(cuota[numero]),
                                                                        idObjetoImponible = str(obj_imponible[numero]), obligacion = "0"
                                                                      ).text = ' '
                                                    


                                        elif origen == 'GANT':
                                            general = ET.Element("General",  xmlns="", banco = banco, nroTransaccion = "0", nroRendicion = str(nro_rendicion), fechaRendicion = fecha_rendicion , 
                                                                    cbuOrigen = str(cbu_origen), cuitOrigen = str(cuit_origen), cbuDestino = str(cbu_destino), cuitDestino = str(cuit_destino),
                                                                    registros = str(cant_registros),
                                                                    totalImpDeterminado = str(imp_determinado), totalImpPagado = str(imp_pagado), totalImpRecaudado = str(imp_recaudado), totalImpDepositado = str(imp_depositado),
                                                                    totalImpADepositar = str(imp_a_depositar), totalImpComision = str(total_comision), totalImpIVA = str(total_iva))



                                            sucursal_tag = ET.SubElement(general,"Sucursal", sucursal = sucursal_id, registros = str(cant_registros_sucursal),
                                                                        totalImpDeterminado = str(imp_determinado_sucursal), totalImpPagado = str(imp_pagado_sucursal),
                                                                        totalImpRecaudado = str(imp_recaudado_sucursal), totalImpDepositado = str(imp_depositado_sucursal),
                                                                        totalImpADepositar = str(imp_a_depositar_sucursal), totalImpComision = str(total_comision_sucursal), 
                                                                        totalImpIVA = str(total_iva_sucursal))                             


                                            pagos = ET.SubElement(sucursal_tag,"Pagos", codRegistro = cod_registro, caja = caja, cajero = cajero, lote = lote,
                                                                    registros = str(cant_registros_pagos), totalImpDeterminado = str(imp_determinado_pagos),
                                                                    totalImpPagado = str(imp_pagado_pagos), totalImpComision = str(total_comision_pagos),
                                                                    totalImpIVA = str(total_iva_pagos)
                                                                    )

                                            for numero in range(len(nro_registro)):
                                                if banco == '00202' or banco == '00216':
                                                    det_pago = ET.SubElement(pagos,"DetallePago", codRegistro = str(cod_registro_dp), nroRegistro = str(numero + 1), nroControl = str(numero + 1),
                                                                        marcaMovimiento = str(marca_movimiento), tipoOperacion = str(tipo_operacion), tipoRendicion = str(tipo_rendicion),
                                                                        moneda = str(moneda), nroLiquidacionOriginal = nro_boleta[numero], nroLiquidacionActualizado = nro_boleta[numero], 
                                                                        fechaPago = str(fecha_pago[numero]), impDeterminado = str(importe[numero]), impPagado = str(importe[numero]), impComision = str(comision[numero]), 
                                                                        impIVA = str(iva[numero]), nroComercio = str(nro_comercio), cantCuotas = str(cuota[numero])
                                                                      ).text = ' '
                                                else:
                                                    det_pago = ET.SubElement(pagos,"DetallePago", codRegistro = str(cod_registro_dp), nroRegistro = str(numero + 1), nroControl = str(numero + 1),
                                                                        marcaMovimiento = str(marca_movimiento), tipoOperacion = str(tipo_operacion), tipoRendicion = str(tipo_rendicion),
                                                                        moneda = str(moneda), nroLiquidacionOriginal ="0", nroLiquidacionActualizado = "0", 
                                                                        fechaPago = str(fecha_pago[numero]), impDeterminado = str(importe[numero]), impPagado = str(importe[numero]), impComision = str(comision[numero]), 
                                                                        impIVA = str(iva[numero]), nroComercio = str(nro_comercio), cantCuotas = str(cuota[numero]),
                                                                        idObjetoImponible = str(obj_imponible[numero]), obligacion = nro_boleta[numero]
                                                                      ).text = ' '
                                                

                                            

                                        #Comentarios de los calculos a nivel general
                                        comentario_cant_registros = ET.Comment(informe_cant_registros)
                                        comentario_importes = ET.Comment(informe_importes)
                                        comentario_suma_importes = ET.Comment(informe_suma_importes)  
                                        comentario_comision = ET.Comment(informe_comisiones) 
                                        comentario_suma_comisiones = ET.Comment(informe_suma_comisiones)
                                        comentario_iva_general = ET.Comment(informe_iva_general)

                                        #Comentarios de los calculos a nivel sucursal y pagos
                                        comentario_suma_ivas = ET.Comment(informe_suma_ivas)
                                        comentario_iva_pagos_sucursal = ET.Comment(informe_ivas_dp)


                                        sucursal_tag.insert(0, comentario_iva_pagos_sucursal)
                                        sucursal_tag.insert(0, comentario_suma_ivas)

                                        general.insert(0, comentario_iva_general)
                                        general.insert(0, comentario_suma_comisiones)
                                        general.insert(0, comentario_comision)
                                        general.insert(0, comentario_suma_importes)
                                        general.insert(0, comentario_importes)
                                        general.insert(0, comentario_cant_registros)

                                        nombre_archivoXML = fecha_rendicion[0:4] + fecha_rendicion[5:7] + fecha_rendicion[8:10] + '.P' + banco[2:5]
                                        tree = ET.ElementTree(general)    
                                        tree.write(nombre_archivoXML + '.xml', xml_declaration=True, encoding='utf-8')
                                        messagebox.showinfo(message=f"XML generado correctamente en carpeta dist en el archivo con nombre {nombre_archivoXML}.xml. Presiona aceptar para salir.", title="Generación exitosa")
                                        ventana.destroy()
                                        #input("El XML se generó correctamente en un archivo aparte. Presione enter para salir")
                                        #del general.attrib["sucursal"] 
                                    else:
                                        messagebox.showerror(message="Los campos de los detalles de pagos tienen que tener la misma cantidad de items", title="Error en los detalles de pagos")
                                else:
                                    messagebox.showerror(message="El formato de la fecha de rendicion debe ser DD/MM/AAAA o DD-MM-AAAA", title="Error en fecha de rendicion (General)")   
                            else:
                                messagebox.showerror(message="El numero de banco debe ser numerico", title="Error en banco")
                        else:
                            messagebox.showerror(message="El formato de la fecha de pago (detallepago) debe ser DD/MM/AAAA o DD-MM-AAAA", title="Error en las fechas de detalles de pagos")
                    else:
                        messagebox.showerror(message="Los importes deben ser numericos", title="Error en las importes")
                else:
                    messagebox.showerror(message="Para Cordobesa debe ingresar 12 o 18. Para 00202 y 00216 en cant cuotas debe ingresar C o D según si es crédito o debito(siempre será 1 pago).", title="Error en las cantidad cuotas")
            else:
                messagebox.showerror(message="Campo cuota actual deben ser todos numericos", title="Error en campo cuota actual")

        except(IndexError, AttributeError, TypeError, SystemError):
            messagebox.showerror(message="Ingrese cada detalle por fila según corresponda. Revise comas decimales. Revise valor del numero banco", title="Error")
        except(ValueError):
            messagebox.showerror(message="Revisar importes. Deben ser numerico", title="Error")
        except(UnboundLocalError):
            messagebox.showerror(message="Para Cordobesa debe ingresar 12 o 18. Para 00202 y 00216 en cant cuotas debe ingresar C o D según si es crédito o debito(siempre será 1 pago).", title="Error")
        except:
            messagebox.showerror(message="Excepcion no controlada. Revise los campos", title="Error")


    def mostrar_nombre_banco(self, event):
        banco_selec = str(self.cbbox_nrobanco.get())
        if banco_selec == "00202":
            self.label_nombrebanco = Label(self.frame,text='VISA',padx=1,pady=1 )
            self.label_nombrebanco.grid(row=3, column=2)

            self.label_cuotaactual = Label(self.frame,text='Cuota Actual:',pady=10,padx=20, state="disabled")
            self.label_cuotaactual.grid(row=5,column=8,sticky='N')

            self.input_cuotaactual = Text(self.frame, height = 15, width = 10, state="disabled")
            self.input_cuotaactual.grid(row=5, column=9)

        elif banco_selec == "00216":
            self.label_nombrebanco = Label(self.frame,text='Mastercard',padx=1,pady=1 )
            self.label_nombrebanco.grid(row=3, column=2)

            self.label_cuotaactual = Label(self.frame,text='Cuota Actual:',pady=10,padx=20, state="disabled")
            self.label_cuotaactual.grid(row=5,column=8,sticky='N')

            self.input_cuotaactual = Text(self.frame, height = 15, width = 10, state="disabled")
            self.input_cuotaactual.grid(row=5, column=9)

        elif banco_selec == "00935":
            self.label_nombrebanco = Label(self.frame,text='Cordobesa 12-18',padx=1,pady=1 )
            self.label_nombrebanco.grid(row=3, column=2)

            self.label_cuotaactual = Label(self.frame,text='Cuota Actual:',pady=10,padx=20)
            self.label_cuotaactual.grid(row=5,column=8,sticky='N')

            self.input_cuotaactual = Text(self.frame, height = 15, width = 10)
            self.input_cuotaactual.grid(row=5, column=9)
        
        

    def __init__(self, master):
        self.frame = Frame(master)
        self.label_origen = Label(self.frame, bg='grey', text='ORIGEN: ')
        self.label_origen.grid(row=0, column=0, pady=20, sticky= 'WE')

        self.cbbox_origen = ttk.Combobox(self.frame, width=17, state="readonly")
        self.cbbox_origen.place(x=163,y=20)
        opc = ["PSRM","OTAX","GANT"]
        self.cbbox_origen["values"] = opc

        #General
        self.titulo_general = Label(self.frame,bg='grey',text='GENERAL' )
        self.titulo_general.grid(row=2,column=0,sticky= 'WE')

        self.label_nrobanco = Label(self.frame,text='Número de banco:',padx=20,pady=20 )
        self.label_nrobanco.grid(row=3, column=0)
        
        self.cbbox_nrobanco = ttk.Combobox(self.frame, width=17, state="readonly")
        self.cbbox_nrobanco.place(x=163,y=100)
        opc_bancos = ["00935","00202","00216"]
        self.cbbox_nrobanco["values"] = opc_bancos

        self.cbbox_nrobanco.bind("<<ComboboxSelected>>", self.mostrar_nombre_banco)

        

        #fecha de rendicion
        self.label_fecharendicion = Label(self.frame,text='Fecha de rendición:',padx=20,pady=20 )
        self.label_fecharendicion.grid(row=3,column=3,sticky='W')

        self.input_fecharendicion = ttk.Entry(self.frame,width=20,justify=CENTER)
        self.input_fecharendicion.grid(row=3, column=4, )

        #Detalle de pago

        self.titulo_dp = Label(self.frame,text='DETALLE DE PAGO',bg='grey')
        self.titulo_dp.grid(row=4,column=0,sticky= 'WE')

        #Nro de boleta
        self.label_nroboleta = Label(self.frame,text='Número de boleta:',pady=10,padx=20)
        self.label_nroboleta.grid(row=5,column=0,sticky='N' )
  
        self.input_nroboleta = Text(self.frame, height = 15, width = 23)
        self.input_nroboleta.grid(row=5, column=1)

        #Importe
        self.label_importe = Label(self.frame,text='Importe $:',pady=10,padx=20)
        self.label_importe.grid(row=5,column=2,sticky='N')


        self.input_importe = Text(self.frame, height = 15, width = 15)
        self.input_importe.grid(row=5, column=3)
 
        #Fecha de pago
        self.label_fechapago = Label(self.frame,text='Fecha de pago:',pady=10,padx=20 )
        self.label_fechapago.grid(row=5,column=4,sticky='N')

        self.input_fechapago = Text(self.frame, height = 15, width = 20)
        self.input_fechapago.grid(row=5, column=5, sticky='N')

        #Cant cuotas
        self.label_cant_cuotas = Label(self.frame,text='Cantidad de cuotas:',pady=10,padx=20 )
        self.label_cant_cuotas.grid(row=5,column=6,sticky='N')

        self.input_cant_cuotas = Text(self.frame, height = 15, width = 10)
        self.input_cant_cuotas.grid(row=5, column=7, sticky='N')

        #Cuota Actual
        self.label_cuotaactual = Label(self.frame,text='Cuota Actual:',pady=10,padx=20, state="disabled")
        self.label_cuotaactual.grid(row=5,column=8,sticky='N')

        self.input_cuotaactual = Text(self.frame, height = 15, width = 10, state="disabled")
        self.input_cuotaactual.grid(row=5, column=9)

        
        self.btn_generarXML = Button(self.frame, text="Generar XML", command=self.tomar_datos, width=13, height=2)
        self.btn_generarXML.grid(row=8, column=3, pady=10)

        self.btn_verificar_cantregistros = Button(self.frame, text="Verif cant registros", command=self.verificar_cant_registros, width=13, height=2)
        self.btn_verificar_cantregistros.grid(row=8, column=4, pady=10)

        self.frame.pack()


    
    


ventana = Tk()
ventana.geometry('1450x520')
ventana.title('XMLGenerator')
aplicacion = Ventana(ventana)
ventana.mainloop()