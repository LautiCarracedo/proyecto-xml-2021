from abc import ABC, abstractmethod

class FormaPago(ABC):
    @abstractmethod
    def tipo_pago_selec(self) -> str:
        pass

class PagoPresencial(FormaPago):
    def __init__(self) -> str:
        super().__init__()
        self.forma_pago = "Pagos presenciales"
    
    def tipo_pago_selec(self):
        return self.forma_pago

class PagoElectronico(FormaPago):
    def __init__(self) -> str:
        super().__init__()
        self.forma_pago = "Pagos electronicos"
    
    def tipo_pago_selec(self):
        return self.forma_pago

class AmbosPagos(FormaPago):
    def __init__(self) -> str:
        super().__init__()
        self.forma_pago = "Ambos pagos"
    
    def tipo_pago_selec(self):
        return self.forma_pago

def tipo_pago_selec(forma_pago : FormaPago):
    print(forma_pago.tipo_pago_selec())



#valor = PagoPresencial()
#tipo_pago_selec(valor)