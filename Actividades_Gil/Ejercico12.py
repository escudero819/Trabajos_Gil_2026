from Ejercicio12_objects import Recursos_no_Usables, Recursos_Usables

class Inventario():

    def __init__(self, jugador, cant_maxima):
        self.cantidad_maxima = cant_maxima
        self.inventario = []
        self.jugador = jugador
    
    def Guardar(self, objeto):
        nuevo = True
        for objeto_espacio in self.inventario:
            if objeto_espacio.nombre == objeto.nombre:
                objeto_espacio.cantidad += objeto.cantidad
                nuevo = False
        
        if nuevo:
            if len(self.inventario) < self.cantidad_maxima:
                self.inventario.append(objeto)
            else:
                print("no hay mas espacio")

    def Descartar(self, indice):
        objeto = self.inventario.pop(indice)
        return objeto

    def Usar(self, indice):
        print("usando:", indice)
        objeto = self.inventario[indice]
        if objeto.usable:
            objeto.Usar(self.jugador)
            if objeto.cantidad <= 0:
                self.inventario.pop(indice)
            self.Lista()
        else:
            print("este objeto no se puede usar")
            self.Lista()

    def Inspeccionar(self, objeto, indice):
        print("nombre:", objeto.nombre)
        print("cantidad:", objeto.cantidad)
        print("descripcion:", objeto.descripcion)
        print("que desea hacer? ")
        print("1- Usar")
        print("2- Descartar")
        print("3 o enter- salir")
        eleccion = input("-- ")
        if eleccion != "":
            eleccion = int(eleccion)
            if eleccion != 3:
                if eleccion == 1:
                    self.Usar(indice)
                elif eleccion == 2:
                    objeto = self.Descartar(indice)
                    self.Lista()
                else:
                    self.Lista()
            else:
                self.Lista()
        else:
            self.Lista()


    def Lista(self):
        for i in range(len(self.inventario)):
            print(f"espacio {i + 1}- {self.inventario[i].nombre}")
        print("enter para salir o ingrese el numero de espacio para inspeccionar")
        eleccion = input()
        if eleccion != "":
            indice_eleccion = int(eleccion) - 1
            objeto = self.inventario[indice_eleccion]
            self.Inspeccionar(objeto, indice_eleccion)
        else:
            return


class Jugador():

    def __init__(self):
        self.vida = 100
        self.sed = 100
        self.hambre = 100

prueba = Inventario(Jugador(), 10)
coso = Recursos_no_Usables.Palo()
print(coso)
prueba.Guardar(coso)
coso = Recursos_no_Usables.Piedra()
print(coso)
prueba.Guardar(coso)
coso = Recursos_no_Usables.Palo()
print(coso)
prueba.Guardar(coso)
prueba.Lista()