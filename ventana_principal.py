from tkinter import *
from tkinter import ttk
from tkinter.constants import CENTER, N
from tkinter import messagebox

from ventana_otros_entes import Ventana
from ventana_bpc import VentanaBPC

class VentanaPrincipal(Frame):

    
    def __init__(self, master):
        self.master = master
        self.frame_princ = Frame(self.master)
        self.titulo = Label(self.frame_princ, bg='grey', text='GENERADOR XML')
        self.titulo.grid(row=0, column=2, pady=20, sticky= 'WE')
        
        self.btn_ventana_bpc = Button(self.frame_princ, text="BPC", command=self.ventana_bpcc, width=13, height=2)
        self.btn_ventana_bpc.grid(row=1, column=1, pady=10)

        self.btn_ventana_otros_entes = Button(self.frame_princ, text="Otros entes", command=self.ventana_otros_entess, width=13, height=2)
        self.btn_ventana_otros_entes.grid(row=1, column=3, pady=10)

        self.frame_princ.pack()
    
    def ventana_bpcc(self):
        self.ventana_bpc = Toplevel()
        self.aplicacion_bpc = VentanaBPC(self.ventana_bpc)
        self.ventana_bpc.geometry('1450x700')
    
    def ventana_otros_entess(self):
        self.ventana_entes = Toplevel()
        self.aplicacion_otros_entes = Ventana(self.ventana_entes)
        self.ventana_entes.geometry('1450x520')

def main():
    ventana_principal = Tk()
    ventana_principal.geometry('700x200')
    ventana_principal.title('XMLGenerator')
    aplicacion = VentanaPrincipal(ventana_principal)
    ventana_principal.mainloop()

if __name__ == "__main__":
    main()