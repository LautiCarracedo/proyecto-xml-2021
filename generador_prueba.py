from os import name
import clases




def main():
    generador = clases.Generador()
    generador.generar_xml()

    try:
        #instance_objeto_general_input = clases.GeneralInput()
        instance_objeto_general = clases.GeneralOutput()
        instance_objeto_sucursal = clases.SucursalOutput()
        instance_objeto_pagos = clases.PagosOutput()
        instance_objeto_detallepago = clases.DetallePagoOutput()
        #no es necesario, es para ver la salida x consola mediante un vector
        vector_general = []
        vector_sucursal = []
        vector_pagos = []
        vector_detalle_pago = []

        vector_general = [instance_objeto_general.banco, 0,
                          instance_objeto_general.transformar_fecha(), 
                          instance_objeto_general.cbu_origen, instance_objeto_general.cuit_origen, instance_objeto_general.cbu_destino, instance_objeto_general.cuit_destino, 
                          instance_objeto_general.calcular_cant_registros(), instance_objeto_general.calcular_importe_determinado_y_pagado(),
                          instance_objeto_general.calcular_importe_determinado_y_pagado(), instance_objeto_general.imp_recaudado,
                          instance_objeto_general.imp_depositado, instance_objeto_general.imp_a_depositar,
                          instance_objeto_general.calcular_total_comision_iva()[0], instance_objeto_general.calcular_total_comision_iva()[1]]
        
        vector_sucursal = [instance_objeto_sucursal.getSucursal(),  
                          instance_objeto_sucursal.calcular_cant_registros(), instance_objeto_sucursal.calcular_importe_determinado_y_pagado(),
                          instance_objeto_sucursal.calcular_importe_determinado_y_pagado(), instance_objeto_sucursal.getImpRecaudado(),
                          instance_objeto_sucursal.getImpDepositado(), instance_objeto_sucursal.getImpADepositar(),
                          instance_objeto_sucursal.calcular_total_comision_iva_sucursal()[0], instance_objeto_sucursal.calcular_total_comision_iva_sucursal()[1]]
        
        vector_pagos = [instance_objeto_pagos.getCodRegistro(), instance_objeto_pagos.getCaja(), instance_objeto_pagos.getCajero(), instance_objeto_pagos.getLote(),  
                        instance_objeto_pagos.calcular_cant_registros_pagos(), instance_objeto_pagos.calcular_importe_determinado_y_pagado(),
                        instance_objeto_pagos.calcular_importe_determinado_y_pagado(),
                        instance_objeto_pagos.calcular_total_comision_iva_pagos()[0], instance_objeto_pagos.calcular_total_comision_iva_pagos()[1]]
        
        vector_detalle_pago = [instance_objeto_detallepago.calculo_comision_iva_x_dp()
                                #instance_objeto_detallepago.getFechaPago(),
                               #instance_objeto_detallepago.getImporte(), instance_objeto_detallepago.getCantCuotas(),  
                                #instance_objeto_detallepago.getIdObjImponible(), instance_objeto_detallepago.getObligacion()
                                ]

        print("Datos tag general: ", vector_general)
        print("Datos tag sucursal: ", vector_sucursal)
        print("Datos tag pagos: ", vector_pagos)
        print("Datos tag detallepago: ", vector_detalle_pago)
    except (AttributeError):
            print("ERROR")



if __name__ == "__main__":
    main()




