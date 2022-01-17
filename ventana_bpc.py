from tkinter import *
from tkinter import ttk
from tkinter.constants import CENTER, N
from tkinter import messagebox

from generador_bpc import GeneradorBPC
from validaciones_datos import validar_campo_formato_xml, validar_cant_registros_bpc, validar_codbarra1, validar_codbarra2, validar_fecha_rendicion, validar_igualdad_largo_vector, validar_tipopagos


class VentanaBPC:
    
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)

        self.label_opc = Label(self.frame, bg='grey', text='FORMATO XML: ')
        self.label_opc.grid(row=0, column=0, pady=20, sticky= 'WE')

        self.cbbox_opc = ttk.Combobox(self.frame, width=17, state="readonly")
        self.cbbox_opc.place(x=163,y=20)
        opc = ["Pagos electronicos","Pagos presenciales","Ambos pagos"]
        self.cbbox_opc["values"] = opc

        self.cbbox_opc.bind("<<ComboboxSelected>>", self.ocultar_mostrar_tipopago)

        self.label_general = Label(self.frame,text='GENERAL',bg='grey')
        self.label_general.grid(row=1,column=0,sticky= 'WE')

        self.label_fecharendicion = Label(self.frame,text='Fecha de rendición:',pady=10,padx=20)
        self.label_fecharendicion.grid(row=1,column=1)

        self.input_fecharendicion = ttk.Entry(self.frame,width=20)
        self.input_fecharendicion.grid(row=1, column=2)

        self.label_deposito = Label(self.frame,text='DEPÓSITO/PAGOS',bg='grey')
        self.label_deposito.grid(row=2,column=0,sticky= 'WE')

        self.label_fechaacreditacion = Label(self.frame,text='Fecha acreditación:',pady=10,padx=20)
        self.label_fechaacreditacion.grid(row=2,column=1)

        self.input_fechaacreditacion = ttk.Entry(self.frame,width=20)
        self.input_fechaacreditacion.grid(row=2, column=2)

        self.titulo = Label(self.frame,text='COD DE BARRAS',bg='grey')
        self.titulo.grid(row=3,column=0,sticky= 'WE')

        #Cod barra 1
        self.label_codbarra1 = Label(self.frame,text='Cod Barra 1:',pady=10,padx=20)
        self.label_codbarra1.grid(row=4,column=0,sticky='N' )
  
        self.input_codbarra1 = Text(self.frame, height = 20, width = 50)
        self.input_codbarra1.grid(row=4, column=1)

        #Cod barra 2
        self.label_codbarra2 = Label(self.frame,text='Cod Barra 2:',pady=10,padx=20)
        self.label_codbarra2.grid(row=4,column=2,sticky='N')

        self.input_codbarra2 = Text(self.frame, height = 20, width = 50)
        self.input_codbarra2.grid(row=4, column=3)

        #Tipo pago
        self.label_tipopago = Label(self.frame,text='Tipo Pago:',pady=10,padx=20, state="disabled")
        self.label_tipopago.grid(row=4,column=4,sticky='N')

        self.input_tipopago = Text(self.frame, height = 20, width = 10)
        self.input_tipopago.grid(row=4, column=5)
 
        
        self.btn_generarXML = Button(self.frame, text="Generar XML", command=self.tomar_datos, width=13, height=2)
        self.btn_generarXML.grid(row=5, column=2, pady=10)

        self.btn_calcular_registros = Button(self.frame, text="Verif cant registros", command=self.verificar_cant_registros, width=13, height=2)
        self.btn_calcular_registros.grid(row=5, column=3, pady=10)


        self.frame.pack()

    def tomar_datos(self):
        try:
            opc_pagos = self.cbbox_opc.get()


            #toma de datos codbarra
            fecha_rendicion = str(self.input_fecharendicion.get())
            fecha_acreditacion = str(self.input_fechaacreditacion.get())
            cod_barras1 = self.input_codbarra1.get("1.0","end-1c")  #estos param son tomar desde el primer caracter hasta el ultimo
            cod_barras2 = self.input_codbarra2.get("1.0","end-1c")
            tipos_pagos = self.input_tipopago.get("1.0","end-1c")


            validacion_dato_fec_rendicion, dato_fec_rendicion = validar_fecha_rendicion(fecha_rendicion)
            validacion_dato_fec_acreditacion, dato_fec_acreditacion = validar_fecha_rendicion(fecha_acreditacion) #uso la misma funcion validar porque debe tener el mismo formato
            validacion_dato_codbarra1, dato_codbarra1 = validar_codbarra1(cod_barras1)
            validacion_dato_codbarra2, dato_codbarra2 = validar_codbarra2(cod_barras2)
            validacion_dato_formato, dato_formatoxml = validar_campo_formato_xml(opc_pagos)
            validacion_largo_vectores = validar_igualdad_largo_vector(cod_barras1, cod_barras2, tipos_pagos, dato_formatoxml)
            validacion_dato_ambospagos, dato_ambospagos = validar_tipopagos(tipos_pagos, dato_formatoxml, cod_barras1) #aca se toman los valores del input de tipospagos

            if validacion_dato_codbarra1:
                if validacion_dato_codbarra2:
                    if validacion_dato_formato:
                        if validacion_dato_ambospagos:
                            if validacion_dato_fec_rendicion:
                                if validacion_dato_fec_acreditacion:
                                    if validacion_largo_vectores:
                                    
                                        generador = GeneradorBPC(dato_codbarra1, dato_codbarra2, dato_fec_rendicion, dato_fec_acreditacion, dato_formatoxml, dato_ambospagos)
                                        generador.generar_xml(dato_codbarra1, dato_codbarra2, dato_fec_rendicion, dato_fec_acreditacion, dato_formatoxml, dato_ambospagos)

                                        nombre_archivoXML = dato_fec_rendicion[0:4] + dato_fec_rendicion[5:7] + dato_fec_rendicion[8:10] + '.P1'
                                        messagebox.showinfo(message=f"XML generado correctamente en carpeta dist en el archivo con nombre {nombre_archivoXML}.xml. Presiona aceptar para salir.", title="Generación exitosa")
                                        self.cerrar_ventana()

                                    else:
                                        messagebox.showerror(message="La cantidad de datos a ingresar en cada lista deben ser iguales", title="Error")
                                else:
                                    messagebox.showerror(message="Error en la fecha de acreditación. El formato correcto es DD/MM/AAAA o DD-MM-AAAA", title="Error")
                            else:
                                messagebox.showerror(message="Error en la fecha de rendición. El formato correcto es DD/MM/AAAA o DD-MM-AAAA", title="Error")
                        else:
                            messagebox.showerror(message="Error la lista cargada en tipo de pago. Las letras deben ser E(electronico) o P(presencial)", title="Error")
                    else:
                        messagebox.showerror(message="Debe seleccionar una opcion en el campo formato xml", title="Error")
                else:
                    messagebox.showerror(message="El codigo de barra debe ser numerico y contener al menos 42 caracteres. Revise que no tenga espacios al final", title="Error")
            else:
                messagebox.showerror(message="El codigo de barra debe ser numerico y contener al menos 42 caracteres Revise que no tenga espacios al final", title="Error")
        except(UnboundLocalError):
            messagebox.showerror(message="Debe ingresar en la lista de tipo pago al menos un tipo E(electronico) y un tipo P(presencial). De lo contrario si todos los pagos son de un solo tipo, debe elegir dicha opcion en formato correspondiente", title="Error")
        except(ValueError):
            messagebox.showerror(message="El codigo de barra debe ser numerico y contener al menos 42 caracteres Revise que no tenga espacios al final", title="Error")

    def ocultar_mostrar_tipopago(self, event):
        tipo_pago_selec = str(self.cbbox_opc.get())

        if tipo_pago_selec == "Ambos pagos":
            self.label_tipopago = Label(self.frame,text='Tipo Pago:',pady=10,padx=20)
            self.label_tipopago.grid(row=4,column=4,sticky='N')

            self.input_tipopago = Text(self.frame, height = 20, width = 10)
            self.input_tipopago.grid(row=4, column=5)

            self.label_fechaacreditacion = Label(self.frame,text='Fecha acreditación:',pady=10,padx=20)
            self.label_fechaacreditacion.grid(row=2,column=1)

            self.input_fechaacreditacion = ttk.Entry(self.frame,width=20)
            self.input_fechaacreditacion.grid(row=2, column=2)
        
        
        else:
            self.label_tipopago = Label(self.frame,text='Tipo Pago:',pady=10,padx=20, state="disabled")
            self.label_tipopago.grid(row=4,column=4,sticky='N')

            self.input_tipopago = Text(self.frame, height = 20, width = 10, state="disabled")
            self.input_tipopago.grid(row=4, column=5)
    
    def verificar_cant_registros(self):
        try:
            cod_barras1 = self.input_codbarra1.get("1.0","end-1c")  #estos param son tomar desde el primer caracter hasta el ultimo
            cod_barras2 = self.input_codbarra2.get("1.0","end-1c")
            tipos_pagos = self.input_tipopago.get("1.0","end-1c")

            vector_codbarra1, vector_codbarra2, vector_tipospagos = validar_cant_registros_bpc(cod_barras1, cod_barras2, tipos_pagos)
            
            
            cant_codbarra1 = Label(self.frame, text='Cant registros: ' + str(len(vector_codbarra1)), pady=10,padx=20 )
            cant_codbarra1.grid(row=6, column=1)

            cant_codbarra2 = Label(self.frame, text='Cant registros: ' + str(len(vector_codbarra2)), pady=10,padx=20 )
            cant_codbarra2.grid(row=6, column=3)

            cant_tipospagos = Label(self.frame, text='Cant registros: ' + str(len(vector_tipospagos)), pady=10,padx=20 )
            cant_tipospagos.grid(row=6, column=5)

        except:
            messagebox.showerror(message='Error al calcular registros. Pruebe nevamente', title='Error')
    
    def cerrar_ventana(self):
        self.master.destroy()



