from abc import ABC, abstractmethod
import random 
class Objeto():
    
    def __init__(self, nombre, usable, descripcion, cantidad, cantidad_maxima):
        self.nombre = nombre
        self.usable = usable
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.cantidad_maxima = cantidad_maxima

    def __str__(self):
        return f"nombre: {self.nombre} - cantidad: {self.cantidad}"

    @abstractmethod
    def Utilidad(self):
        pass

    def Usar(self):
        if self.usable:
            self.Utilidad()
        else:
            print(f"{self.nombre} no se puede usar directamente")

# RECURSOS SIN UTILIDAD DIRECTA

class clase_Palo(Objeto):

    def __init__(self):
        descripcion = "de madera, capaz de usarse en distintas situaciones"
        super().__init__("Palo", False, descripcion, random.randint(1, 3), 10)

class clase_Piedra(Objeto):

    def __init__(self):
        descripcion = "son utiles en distintos objetos, son bastante resistentes y pueden afilarse"
        nombre = "Piedra"
        cantidad = random.randint(1,4)
        cant_max = 10
        super().__init__(nombre, False, descripcion, cantidad, cant_max)



class Recursos_no_Usables():
    def Palo():
        return clase_Palo()
    
    def Piedra():
        return clase_Piedra()

# RECURSOS QUE TIENEN UTILIDAD DIRECTA 

class C_Botella_agua(Objeto):

    def __init__(self):
        descripcion = "refrescante, sacia bastante la sed"
        nombre = "Botella de agua"
        cantidad = random.randint(1,3)
        cant_max = 5
        super().__init__(nombre, False, descripcion, cantidad, cant_max)

    def Utilidad(self, jugador):
        jugador.sed += 20
        self.cantidad -= 1

class Recursos_Usables():
    def Botella_agua():
        return C_Botella_agua()