class Cuenta():

    def __init__(self, titular, cantidad):
        self.titular = titular
        self._cantidad = cantidad
    
    def MostrarDatos(self):
        print(f"el titular '{self.titular}' tiene ${self._cantidad}")

class CajaAhorro(Cuenta):

    def __init__(self, *kwargs):
        super().__init__(*kwargs)

class PlazoFijo(Cuenta):

    def __init__(self, titular, cantidad, plazo, interes):
        super().__init__(titular, cantidad)
        self.plazo = plazo
        self.interes = interes
    
    def ImporteInteres(self):
        interes = self.interes * self.cantidad / 100
        return interes
    
    def MostrarDatos(self):
        super().MostrarDatos()
        print(f"con un plazo fijo de {self.plazo} meses con un interes del {self.interes}%")

cuenta_ahorro = CajaAhorro("pepito", 9000)
plazo_fijo = PlazoFijo("juancito", 2000, 12, 5)