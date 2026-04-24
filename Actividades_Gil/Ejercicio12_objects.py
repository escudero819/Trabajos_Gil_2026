from abc import ABC, abstractmethod
import random 

# CLASE PADRE DE TODOS LOS OBJETOS

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

class C_Palo(Objeto):

    def __init__(self):
        descripcion = "de madera, capaz de usarse en distintas situaciones"
        super().__init__("Palo", False, descripcion, random.randint(1, 3), 10)

class C_Piedra(Objeto):

    def __init__(self):
        descripcion = "son utiles en distintos objetos, son bastante resistentes y pueden afilarse"
        nombre = "Piedra"
        cantidad = random.randint(1,4)
        cant_max = 10
        super().__init__(nombre, False, descripcion, cantidad, cant_max)



class Recursos_no_Usables():
    def Palo():
        return C_Palo()
    
    def Piedra():
        return C_Piedra()

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

class C_Barra_Cereal(Objeto):
    def __init__(self):
        descripcion = "deliciosa, sacia bastante el hambre"
        nombre = "Barra de Cereal"
        cantidad = random.randint(1,3)
        cant_max = 5
        super().__init__(nombre, True, descripcion, cantidad, cant_max)

    def Utilidad(self, jugador):
        jugador.hambre += 20
        self.cantidad -= 1

class C_Kit_Primeros_Auxilios(Objeto):
    def __init__(self):
        descripcion = "curativo, cura heridas leves"
        nombre = "Kit de Primeros Auxilios"
        cantidad = random.randint(1,3)
        cant_max = 5
        super().__init__(nombre, True, descripcion, cantidad, cant_max)

    def Utilidad(self, jugador):
        jugador.vida += 20
        self.cantidad -= 1


class Recursos_Usables():
    def Botella_agua():
        return C_Botella_agua()
    def Barra_Cereal():
        return C_Barra_Cereal()
    def Kit_Primeros_Auxilios():
        return C_Kit_Primeros_Auxilios()

# Objetos que requieren combinacion de recursos o son herramientas

class C_Caña_Pescar(Objeto):
    def __init__(self):
        descripcion = "permite pescar"  
        nombre = "Caña de Pescar"
        cantidad = 1
        cant_max = 1
        super().__init__(nombre, True, descripcion, cantidad, cant_max)

    def Utilidad(self, jugador):
        jugador.pescar()
        self.cantidad -= 1



class C_Barril(Objeto):
    def __init__(self):
        descripcion = "un barril de madera, puede contener objetos dentro"
        nombre = "Barril"
        cantidad = 1
        cant_max = 1
        super().__init__(nombre, True, descripcion, cantidad, cant_max)
        self.objetos = []
        probabilidad = random.randint(1, 100)
        if probabilidad <= 15:
            self.objetos.append(C_Caña_Pescar())
        elif probabilidad <= 30:
            self.objetos.append(Recursos_Usables.Barra_Cereal())
        elif probabilidad <= 45:
            self.objetos.append(Recursos_Usables.Botella_agua())
        elif probabilidad <= 60:
            self.objetos.append(Recursos_Usables.Kit_Primeros_Auxilios())
        else:
            probabilidad = random.randint(1, 100)
            if probabilidad <= 50:
                self.objetos.append(Recursos_no_Usables.Palo())
            else:
                self.objetos.append(Recursos_no_Usables.Piedra())
    
    def Abrir(self, jugador):
        for objeto in self.objetos:
            jugador.Inspeccionar_Objeto(objeto)
            if objeto.cantidad <= 0:
                if objeto.nombre == "Caña de Pescar":
                    jugador.ambiente.caña_pescar = True
                self.objetos.remove(objeto)
        print("has terminado de revisar el barril")
        self.cantidad -= 1

class Recursos_Unicos():

    def Barril():
        return C_Barril()
    
    def Caña_Pescar():
        return C_Caña_Pescar()