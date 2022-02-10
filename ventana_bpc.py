from tkinter import *
from tkinter import ttk
from tkinter.constants import CENTER, N
from tkinter import messagebox

from generador_bpc import GeneradorBPC
from validaciones_datos import validar_campo_formato_xml, validar_cant_registros_bpc, validar_codbarra1, validar_codbarra2, validar_fecha_rendicion, validar_igualdad_largo_vector, validar_tipopagos


class VentanaBPC(Frame):
    
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)

        self.label_opc = Label(self.frame, bg='grey', text='FORMATO XML: ')
        self.label_opc.grid(row=0, column=0, pady=20, sticky= 'WE')

        self.cbbox_opc = ttk.Combobox(self.frame, width=17, state="readonly")
        self.cbbox_opc.place(x=300,y=20)
        opc = ["Pagos electronicos","Pagos presenciales","Ambos pagos"]
        self.cbbox_opc["values"] = opc

        self.cbbox_opc.bind("<<ComboboxSelected>>", self.ocultar_mostrar_codbarra_segun_formato)

        self.label_general = Label(self.frame,text='GENERAL',bg='grey')
        self.label_general.grid(row=1,column=0,sticky= 'WE')

        self.label_fecharendicion = Label(self.frame,text='Fecha de rendición:',pady=10,padx=20)
        self.label_fecharendicion.grid(row=1,column=1)

        self.input_fecharendicion = ttk.Entry(self.frame,width=20)
        self.input_fecharendicion.grid(row=1, column=2)

        #self.label_deposito = Label(self.frame,text='DEPÓSITO/PAGOS',bg='grey')
        #self.label_deposito.grid(row=2,column=0,sticky= 'WE')

        #self.label_fechaacreditacion = Label(self.frame,text='Fecha acreditación:',pady=10,padx=20)
        #self.label_fechaacreditacion.grid(row=2,column=1)
#
        #self.input_fechaacreditacion = ttk.Entry(self.frame,width=20)
        #self.input_fechaacreditacion.grid(row=2, column=2)

        self.titulo = Label(self.frame,text='COD DE BARRAS P/ PAGOS PRESENCIALES',bg='grey')
        self.titulo.grid(row=2,column=0,sticky= 'WE')

        #Cod barra 1 presencial
        self.label_codbarra1_p = Label(self.frame,text='Cod Barra 1:',pady=10,padx=20, state="disabled")
        self.label_codbarra1_p.grid(row=3,column=0,sticky='N', pady=10)
  
        self.input_codbarra1_p = Text(self.frame, height = 10, width = 50, state="disabled")
        self.input_codbarra1_p.grid(row=3, column=1, pady=10)

        #Cod barra 2 presencial
        self.label_codbarra2_p = Label(self.frame,text='Cod Barra 2:',pady=10,padx=20, state="disabled")
        self.label_codbarra2_p.grid(row=3,column=2,sticky='N', pady=10)

        self.input_codbarra2_p = Text(self.frame, height = 10, width = 50, state="disabled")
        self.input_codbarra2_p.grid(row=3, column=3, pady=10)

        self.titulo1 = Label(self.frame,text='COD DE BARRAS P/ PAGOS ELECTRONICOS',bg='grey')
        self.titulo1.grid(row=4,column=0,sticky= 'WE')

        #Cod barra 1 electronico
        self.label_codbarra1_e = Label(self.frame,text='Cod Barra 1:',pady=10,padx=20, state="disabled")
        self.label_codbarra1_e.grid(row=5,column=0,sticky='N', pady=10)
  
        self.input_codbarra1_e = Text(self.frame, height = 10, width = 50, state="disabled")
        self.input_codbarra1_e.grid(row=5, column=1, pady=10)

        #Cod barra 2 electronico
        self.label_codbarra2_e = Label(self.frame,text='Cod Barra 2:',pady=10,padx=20, state="disabled")
        self.label_codbarra2_e.grid(row=5,column=2,sticky='N', pady=10)

        self.input_codbarra2_e = Text(self.frame, height = 10, width = 50, state="disabled")
        self.input_codbarra2_e.grid(row=5, column=3, pady=10)

        #Tipo pago
        #self.label_tipopago = Label(self.frame,text='Tipo Pago:',pady=10,padx=20, state="disabled")
        #self.label_tipopago.grid(row=6,column=4,sticky='N')
#
        #self.input_tipopago = Text(self.frame, height = 10, width = 10)
        #self.input_tipopago.grid(row=6, column=5)
 
        
        self.btn_generarXML = Button(self.frame, text="Generar XML", command=self.tomar_datos, width=13, height=2)
        self.btn_generarXML.grid(row=7, column=1, pady=10)

        self.btn_calcular_registros = Button(self.frame, text="Verif cant registros", command=self.verificar_cant_registros, width=13, height=2)
        self.btn_calcular_registros.grid(row=7, column=2, pady=10)


        self.frame.pack()

    def tomar_datos(self):
        try:
            opc_pagos = self.cbbox_opc.get()


            #toma de datos codbarra
            fecha_rendicion = str(self.input_fecharendicion.get())
            #fecha_acreditacion = str(self.input_fechaacreditacion.get())
            cod_barras1_p = self.input_codbarra1_p.get("1.0","end-1c")  #estos param son tomar desde el primer caracter hasta el ultimo
            cod_barras2_p = self.input_codbarra2_p.get("1.0","end-1c")
            cod_barras1_e = self.input_codbarra1_e.get("1.0","end-1c")
            cod_barras2_e = self.input_codbarra2_e.get("1.0","end-1c")
            #tipos_pagos = self.input_tipopago.get("1.0","end-1c")


            validacion_dato_fec_rendicion, dato_fec_rendicion = validar_fecha_rendicion(fecha_rendicion)
            #validacion_dato_fec_acreditacion, dato_fec_acreditacion = validar_fecha_rendicion(fecha_acreditacion) #uso la misma funcion validar porque debe tener el mismo formato
            validacion_dato_codbarra1_p, validacion_dato_codbarra1_e, dato_codbarra1_p, dato_codbarra1_e = validar_codbarra1(cod_barras1_p, cod_barras1_e)
            validacion_dato_codbarra2_p, validacion_dato_codbarra2_e, dato_codbarra2_p, dato_codbarra2_e = validar_codbarra2(cod_barras2_p, cod_barras2_e)
            validacion_dato_formato, dato_formatoxml = validar_campo_formato_xml(opc_pagos)
            validacion_largo_vectores = validar_igualdad_largo_vector(cod_barras1_p, cod_barras2_p, cod_barras1_e, cod_barras2_e, dato_formatoxml)
            dato_contador_barras_e, dato_contador_barras_p = validar_tipopagos(cod_barras1_p, cod_barras2_p, cod_barras1_e, cod_barras2_e, dato_formatoxml) #aca se toman los valores del input de tipospagos

            if dato_formatoxml == "Pagos presenciales":
                if validacion_dato_codbarra1_p:
                    if validacion_dato_codbarra2_p:
                        if validacion_dato_formato:
                            if validacion_dato_fec_rendicion:
                                if validacion_largo_vectores:
                        
                                    generador = GeneradorBPC(dato_codbarra1_p, dato_codbarra2_p, dato_codbarra1_e, dato_codbarra2_e, dato_fec_rendicion, dato_formatoxml, dato_contador_barras_p, dato_contador_barras_e)
                                    generador.generar_xml(dato_codbarra1_p, dato_codbarra2_p, dato_codbarra1_e, dato_codbarra2_e, dato_fec_rendicion, dato_formatoxml, dato_contador_barras_p, dato_contador_barras_e)

                                    nombre_archivoXML = dato_fec_rendicion[0:4] + dato_fec_rendicion[5:7] + dato_fec_rendicion[8:10] + '.P1'
                                    messagebox.showinfo(message=f"XML generado correctamente en carpeta dist en el archivo con nombre {nombre_archivoXML}.xml. Presiona aceptar para salir.", title="Generación exitosa")
                                    #self.cerrar_ventana()

                                else:
                                    messagebox.showerror(message="La cantidad de datos a ingresar en cada lista deben ser iguales", title="Error")
                            else:
                                messagebox.showerror(message="Error en la fecha de rendición. El formato correcto es DD/MM/AAAA o DD-MM-AAAA", title="Error")
                        else:
                            messagebox.showerror(message="Debe seleccionar una opcion en el campo formato xml", title="Error")
                    else:
                        messagebox.showerror(message="El codigo de barra 2 debe ser numerico y contener al menos 42 caracteres. Revise que no tenga espacios al final ni un enter demas", title="Error")
                else:
                    messagebox.showerror(message="El codigo de barra 1 debe ser numerico, empezar con 04 y contener al menos 42 caracteres Revise que no tenga espacios al final ni en un enter demas", title="Error")
            
            elif dato_formatoxml == "Pagos electronicos":
                if validacion_dato_codbarra1_e:
                    if validacion_dato_codbarra2_e:
                        if validacion_dato_formato:
                            if validacion_dato_fec_rendicion:
                                if validacion_largo_vectores:

                                    generador = GeneradorBPC(dato_codbarra1_p, dato_codbarra2_p, dato_codbarra1_e, dato_codbarra2_e, dato_fec_rendicion, dato_formatoxml, dato_contador_barras_p, dato_contador_barras_e)
                                    generador.generar_xml(dato_codbarra1_p, dato_codbarra2_p, dato_codbarra1_e, dato_codbarra2_e, dato_fec_rendicion, dato_formatoxml, dato_contador_barras_p, dato_contador_barras_e)

                                    nombre_archivoXML = dato_fec_rendicion[0:4] + dato_fec_rendicion[5:7] + dato_fec_rendicion[8:10] + '.P1'
                                    messagebox.showinfo(message=f"XML generado correctamente en carpeta dist en el archivo con nombre {nombre_archivoXML}.xml. Presiona aceptar para salir.", title="Generación exitosa")
                                    #self.cerrar_ventana()

                                else:
                                   messagebox.showerror(message="La cantidad de datos a ingresar en cada lista deben ser iguales", title="Error")
                            else:
                                messagebox.showerror(message="Error en la fecha de rendición. El formato correcto es DD/MM/AAAA o DD-MM-AAAA", title="Error")
                        else:
                            messagebox.showerror(message="Debe seleccionar una opcion en el campo formato xml", title="Error")
                    else:
                        messagebox.showerror(message="El codigo de barra 2 debe ser numerico y contener al menos 42 caracteres. Revise que no tenga espacios al final ni un enter demas", title="Error")
                else:
                    messagebox.showerror(message="El codigo de barra 1 debe ser numerico, empezar con 04 y contener al menos 42 caracteres Revise que no tenga espacios al final ni en un enter demas", title="Error")

            else:
                if validacion_dato_codbarra1_p and validacion_dato_codbarra1_e:
                    if validacion_dato_codbarra2_p and validacion_dato_codbarra2_e:
                        if validacion_dato_formato:
                            if validacion_dato_fec_rendicion:
                                if validacion_largo_vectores:

                                    generador = GeneradorBPC(dato_codbarra1_p, dato_codbarra2_p, dato_codbarra1_e, dato_codbarra2_e, dato_fec_rendicion, dato_formatoxml, dato_contador_barras_p, dato_contador_barras_e)
                                    generador.generar_xml(dato_codbarra1_p, dato_codbarra2_p, dato_codbarra1_e, dato_codbarra2_e, dato_fec_rendicion, dato_formatoxml, dato_contador_barras_p, dato_contador_barras_e)

                                    nombre_archivoXML = dato_fec_rendicion[0:4] + dato_fec_rendicion[5:7] + dato_fec_rendicion[8:10] + '.P1'
                                    messagebox.showinfo(message=f"XML generado correctamente en carpeta dist en el archivo con nombre {nombre_archivoXML}.xml. Presiona aceptar para salir.", title="Generación exitosa")
                                    #self.cerrar_ventana()

                                else:
                                    messagebox.showerror(message="La cantidad de datos a ingresar en cada lista deben ser iguales", title="Error")
                            else:
                                messagebox.showerror(message="Error en la fecha de rendición. El formato correcto es DD/MM/AAAA o DD-MM-AAAA", title="Error")
                        else:
                            messagebox.showerror(message="Debe seleccionar una opcion en el campo formato xml", title="Error")
                    else:
                        messagebox.showerror(message="El codigo de barra 2 debe ser numerico y contener al menos 42 caracteres. Revise que no tenga espacios al final ni un enter demas", title="Error")
                else:
                    messagebox.showerror(message="El codigo de barra 1 debe ser numerico, empezar con 04 y contener al menos 42 caracteres Revise que no tenga espacios al final ni un enter demas", title="Error")

        
        except:
            messagebox.showerror(message="Excepcion no controlada", title="Error")

    def ocultar_mostrar_codbarra_segun_formato(self, event):
        tipo_pago_selec = str(self.cbbox_opc.get())

        if tipo_pago_selec == "Ambos pagos":
            #Cod barra 1 presencial
            self.label_codbarra1_p = Label(self.frame,text='Cod Barra 1:',pady=10,padx=20)
            self.label_codbarra1_p.grid(row=3,column=0,sticky='N', pady=10)
    
            self.input_codbarra1_p = Text(self.frame, height = 10, width = 50)
            self.input_codbarra1_p.grid(row=3, column=1, pady=10)

            #Cod barra 2 presencial
            self.label_codbarra2_p = Label(self.frame,text='Cod Barra 2:',pady=10,padx=20)
            self.label_codbarra2_p.grid(row=3,column=2,sticky='N', pady=10)

            self.input_codbarra2_p = Text(self.frame, height = 10, width = 50)
            self.input_codbarra2_p.grid(row=3, column=3, pady=10)

            #Cod barra 1 electronico
            self.label_codbarra1_e = Label(self.frame,text='Cod Barra 1:',pady=10,padx=20)
            self.label_codbarra1_e.grid(row=5,column=0,sticky='N', pady=10)
    
            self.input_codbarra1_e = Text(self.frame, height = 10, width = 50)
            self.input_codbarra1_e.grid(row=5, column=1, pady=10)

            #Cod barra 2 electronico
            self.label_codbarra2_e = Label(self.frame,text='Cod Barra 2:',pady=10,padx=20)
            self.label_codbarra2_e.grid(row=5,column=2,sticky='N', pady=10)

            self.input_codbarra2_e = Text(self.frame, height = 10, width = 50)
            self.input_codbarra2_e.grid(row=5, column=3, pady=10)
        
        
        elif tipo_pago_selec == "Pagos presenciales":
            #Cod barra 1 presencial
            self.label_codbarra1_p = Label(self.frame,text='Cod Barra 1:',pady=10,padx=20)
            self.label_codbarra1_p.grid(row=3,column=0,sticky='N', pady=10)
    
            self.input_codbarra1_p = Text(self.frame, height = 10, width = 50)
            self.input_codbarra1_p.grid(row=3, column=1, pady=10)

            #Cod barra 2 presencial
            self.label_codbarra2_p = Label(self.frame,text='Cod Barra 2:',pady=10,padx=20)
            self.label_codbarra2_p.grid(row=3,column=2,sticky='N', pady=10)

            self.input_codbarra2_p = Text(self.frame, height = 10, width = 50)
            self.input_codbarra2_p.grid(row=3, column=3, pady=10)

            #Cod barra 1 electronico
            self.label_codbarra1_e = Label(self.frame,text='Cod Barra 1:',pady=10,padx=20, state="disabled")
            self.label_codbarra1_e.grid(row=5,column=0,sticky='N', pady=10)
    
            self.input_codbarra1_e = Text(self.frame, height = 10, width = 50, state="disabled")
            self.input_codbarra1_e.grid(row=5, column=1, pady=10)

            #Cod barra 2 electronico
            self.label_codbarra2_e = Label(self.frame,text='Cod Barra 2:',pady=10,padx=20, state="disabled")
            self.label_codbarra2_e.grid(row=5,column=2,sticky='N', pady=10)

            self.input_codbarra2 = Text(self.frame, height = 10, width = 50, state="disabled")
            self.input_codbarra2.grid(row=5, column=3, pady=10)
        
        else:
            #Cod barra 1 presencial
            self.label_codbarra1_p = Label(self.frame,text='Cod Barra 1:',pady=10,padx=20, state="disabled")
            self.label_codbarra1_p.grid(row=3,column=0,sticky='N', pady=10)
    
            self.input_codbarra1_p = Text(self.frame, height = 10, width = 50, state="disabled")
            self.input_codbarra1_p.grid(row=3, column=1, pady=10)

            #Cod barra 2 presencial
            self.label_codbarra2_p = Label(self.frame,text='Cod Barra 2:',pady=10,padx=20, state="disabled")
            self.label_codbarra2_p.grid(row=3,column=2,sticky='N', pady=10)

            self.input_codbarra2_p = Text(self.frame, height = 10, width = 50, state="disabled")
            self.input_codbarra2_p.grid(row=3, column=3, pady=10)

            #Cod barra 1 electronico
            self.label_codbarra1_e = Label(self.frame,text='Cod Barra 1:',pady=10,padx=20)
            self.label_codbarra1_e.grid(row=5,column=0,sticky='N', pady=10)
    
            self.input_codbarra1_e = Text(self.frame, height = 10, width = 50)
            self.input_codbarra1_e.grid(row=5, column=1, pady=10)

            #Cod barra 2 electronico
            self.label_codbarra2_e = Label(self.frame,text='Cod Barra 2:',pady=10,padx=20)
            self.label_codbarra2_e.grid(row=5,column=2,sticky='N', pady=10)

            self.input_codbarra2_e = Text(self.frame, height = 10, width = 50)
            self.input_codbarra2_e.grid(row=5, column=3, pady=10)
            

    
    def verificar_cant_registros(self):
        try:
            cod_barras1_p = self.input_codbarra1_p.get("1.0","end-1c")  #estos param son tomar desde el primer caracter hasta el ultimo
            cod_barras2_p = self.input_codbarra2_p.get("1.0","end-1c")
            cod_barras1_e = self.input_codbarra1_e.get("1.0","end-1c")
            cod_barras2_e = self.input_codbarra2_e.get("1.0","end-1c")

            vector_codbarra1_p, vector_codbarra2_p, vector_codbarra1_e, vector_codbarra2_e = validar_cant_registros_bpc(cod_barras1_p, cod_barras2_p, cod_barras1_e, cod_barras2_e)
            
            
            cant_codbarra1_p = Label(self.frame, text='Cant registros: ' + str(len(vector_codbarra1_p)), pady=10,padx=20 )
            cant_codbarra1_p.grid(row=4, column=1)

            cant_codbarra2_p = Label(self.frame, text='Cant registros: ' + str(len(vector_codbarra2_p)), pady=10,padx=20 )
            cant_codbarra2_p.grid(row=4, column=3)

            cant_codbarra1_e = Label(self.frame, text='Cant registros: ' + str(len(vector_codbarra1_e)), pady=10,padx=20 )
            cant_codbarra1_e.grid(row=6, column=1)

            cant_codbarra2_e = Label(self.frame, text='Cant registros: ' + str(len(vector_codbarra2_e)), pady=10,padx=20 )
            cant_codbarra2_e.grid(row=6, column=3)

        except:
            messagebox.showerror(message='Error al calcular registros. Pruebe nevamente', title='Error')
    
    def cerrar_ventana(self):
        self.master.destroy()



