from tkinter import *
from tkinter import ttk
from tkinter.constants import CENTER, N
from tkinter import messagebox

from generador import Generador
from lectura_archivo_config import ArchivoConfig, ComisionesArchivo

from validaciones_datos import validar_banco, validar_boletas, validar_cant_cuotas, validar_cant_registros, validar_cant_vectores_dp, validar_cuota_actual, validar_fecha_rendicion, validar_fechapagos, validar_importes, validar_origen


class Ventana(Frame):
    
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
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
        datos_archivo_conf = ArchivoConfig()
        nro_bancos, nombres_bancos = datos_archivo_conf.leer_ini_bancos()
        opc_bancos = nro_bancos
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
    
    def tomar_datos(self):
        try:
            #toma de datos origen
            origen = self.cbbox_origen.get()
            #toma de datos general
            vector_datos_general = []
            banco_t = str(self.cbbox_nrobanco.get())
            vector_datos_general.append(banco_t)
            fecha_rendicion = str(self.input_fecharendicion.get())
            #vector_datos_general.append(fecha_rendicion_t)

            #toma de datos dp
            boletas = self.input_nroboleta.get("1.0","end-1c")  #estos param son tomar desde el primer caracter hasta el ultimo
            importes = self.input_importe.get("1.0","end-1c")
            fecha_pagos = self.input_fechapago.get("1.0","end-1c")
            cant_cuotas = self.input_cant_cuotas.get("1.0","end-1c")
            cuota_actual = self.input_cuotaactual.get("1.0","end-1c")

            validacion_dato_origen, dato_origen = validar_origen(origen)
            validacion_dato_banco, dato_banco = validar_banco(banco_t)
            validacion_dato_fec_rendicion, dato_fec_rendicion = validar_fecha_rendicion(fecha_rendicion)
            datos_boletas = validar_boletas(boletas)
            validacion_datos_importes, datos_importes = validar_importes(importes)
            validacion_datos_fec_pagos, datos_fec_pagos = validar_fechapagos(fecha_pagos)
            validacion_datos_cant_cuotas, datos_cant_cuotas = validar_cant_cuotas(banco_t, cant_cuotas)
            validacion_datos_cuot_actual, datos_cuota_actual = validar_cuota_actual(banco_t, boletas, cuota_actual)
            validacion_datos_cant_vectores = validar_cant_vectores_dp(banco_t, boletas, importes, fecha_pagos, cant_cuotas, cuota_actual)
            
            datos_comisiones_arch = ComisionesArchivo()
            validacion_vector_comisiones_p_calculo, vector_comision_p_calculo = datos_comisiones_arch.calcular_comisiones(banco_t, datos_cant_cuotas)

            if validacion_dato_origen:
                if validacion_dato_banco:
                    if validacion_datos_cuot_actual:
                        if validacion_datos_cant_cuotas:
                            if validacion_datos_importes:
                                if validacion_datos_fec_pagos:
                                    if validacion_dato_fec_rendicion:
                                        if validacion_datos_cant_vectores:
                                            if validacion_vector_comisiones_p_calculo:

                                                generador = Generador(dato_origen, dato_banco, dato_fec_rendicion, datos_boletas, datos_importes, datos_fec_pagos, datos_cant_cuotas, datos_cuota_actual)
                                                generador.generar_xml(dato_origen, dato_banco, dato_fec_rendicion, datos_boletas, datos_importes, datos_fec_pagos, datos_cant_cuotas, datos_cuota_actual)

                                                nombre_archivoXML = dato_fec_rendicion[0:4] + dato_fec_rendicion[5:7] + dato_fec_rendicion[8:10] + '.P' + banco_t[2:5]
                                                messagebox.showinfo(message=f"XML generado correctamente en carpeta dist en el archivo con nombre {nombre_archivoXML}.xml. Presiona aceptar para salir.", title="Generación exitosa")
                                                self.cerrar_ventana()

                                            else:
                                                messagebox.showerror(message="Revisar los valores ingresados en el campo cantidad de cuotas. Para Cordobesa(00935) ingresar 12 o 18. Para el resto ingresar C o D según corresponda.", title="Error en cantidad cuotas")                                                                                                                                                                                                                                                                            
                                        else:
                                            messagebox.showerror(message="Los campos de los detalles de pagos tienen que tener la misma cantidad de items", title="Error en los detalles de pagos")
                                    else:
                                        messagebox.showerror(message="El formato de la fecha de rendicion debe ser DD/MM/AAAA o DD-MM-AAAA. DD hasta 31. MM hasta 12", title="Error en fecha de rendicion (General)")   
                                else:
                                    messagebox.showerror(message="El formato de la fecha de pago (detallepago) debe ser DD/MM/AAAA o DD-MM-AAAA. DD hasta 31. MM hasta 12", title="Error en las fechas de detalles de pagos")
                            else:
                                messagebox.showerror(message="Los importes deben ser numericos", title="Error en las importes")
                        else:
                            messagebox.showerror(message="Para Cordobesa debe ingresar 12 o 18. Para 00202 y 00216 en cant cuotas debe ingresar C o D según si es crédito o debito(siempre será 1 pago).", title="Error en las cantidad cuotas")
                    else:
                        messagebox.showerror(message="Campo cuota actual deben ser todos numericos", title="Error en campo cuota actual")
                else:
                    messagebox.showerror(message="Debe seleccionar un banco", title="Error en el banco")
            else:
                messagebox.showerror(message="Debe seleccionar un origen", title="Error en el origen")
        except(ValueError):
            messagebox.showerror(message="Revise que todos los campos hayan sido cargados. Sugerencia: Revise comas (para decimales) y puntos (para miles) en los importes", title="Error")
        except(TypeError):
            messagebox.showerror(message="Error en el archivo de configuraciones. Verifique que existan todas las secciones [NroBanco],[Comisiones],[Valores],[Elementos] del origen y el banco para el que desea generar el XML y que los valores sean correctos", title="Error")
        except:
            messagebox.showerror(message="Revise en el archivo de configuraciones tener cargado [NroBanco],[Comisiones],[Valores] y [Elementos] para generar correctamente el XML", title="Error")     


    def mostrar_nombre_banco(self, event):
        banco_selec = str(self.cbbox_nrobanco.get())
        datos_archivo_conf = ArchivoConfig()
        nro_bancos, nombres_bancos = datos_archivo_conf.leer_ini_bancos()

        if banco_selec in nro_bancos:
            indice_banco = nro_bancos.index(banco_selec)
            nombre_banco = nombres_bancos[indice_banco]
            self.label_nombrebanco = Label(self.frame,text='        ' + str(nombre_banco) + '      ',padx=1,pady=1 )
            self.label_nombrebanco.grid(row=3, column=2)
        
        
        if banco_selec == "00935":
            self.label_cuotaactual = Label(self.frame,text='Cuota Actual:',pady=10,padx=20)
            self.label_cuotaactual.grid(row=5,column=8,sticky='N')

            self.input_cuotaactual = Text(self.frame, height = 15, width = 10)
            self.input_cuotaactual.grid(row=5, column=9)
        
        else:
            self.label_cuotaactual = Label(self.frame,text='Cuota Actual:',pady=10,padx=20, state="disabled")
            self.label_cuotaactual.grid(row=5,column=8,sticky='N')

            self.input_cuotaactual = Text(self.frame, height = 15, width = 10, state="disabled")
            self.input_cuotaactual.grid(row=5, column=9)   
    

    def verificar_cant_registros(self):
        try:
            #toma de datos origen
            origen = self.cbbox_origen.get()

            #toma de datos general
            vector_datos_general = []
            banco_t = str(self.cbbox_nrobanco.get())
            vector_datos_general.append(banco_t)
            fecha_rendicion = str(self.input_fecharendicion.get())

            #toma de datos dp
            boletas = self.input_nroboleta.get("1.0","end-1c")  #estos param son tomar desde el primer caracter hasta el ultimo
            importes = self.input_importe.get("1.0","end-1c")
            fecha_pagos = self.input_fechapago.get("1.0","end-1c")
            cant_cuotas = self.input_cant_cuotas.get("1.0","end-1c")
            cuota_actual = self.input_cuotaactual.get("1.0","end-1c")

            vector_boletas, vector_importes, vector_fechapagos, vector_cantcuotas, vector_cuotaactual = validar_cant_registros(boletas, importes, fecha_pagos, cant_cuotas, cuota_actual)
            
            
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
        
    def cerrar_ventana(self):
        self.master.destroy()


