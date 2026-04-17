from abc import ABC, abstractmethod
import random

class CofreAbierto():

    def __init__(self):
        self.nombre = "Cofre abierto"
        self.contenido = (1, 20)
        self.prob_vacio = 20
        self.monedas = random.randint(self.contenido[0], self.contenido[1])
        self.estado = random.randint(1, 100)
    
    def Investigar(self):
        if self.estado != "vacio":
            print(f"El cofre contiene {self.monedas} monedas")
        else:
            print("El cofre esta vacio")
        
    def Abrir(self):
        print("...")
        if self.estado != "vacio":
            print(f"El cofre contiene {self.monedas} monedas")
        else:
            print("El cofre esta vacio")

    def Recolectar(self):
        if self.estado != "vacio":
            print(f"Has recolectado {self.monedas} monedas")
            return self.monedas
        else:
            print("El cofre esta vacio!!")
            return 0

    def Patear(self):
        print("...por que? ya esta abierto")

class CofreCerrado():

    def __init__(self, prob_malo, descripcion):
        self.nombre = "Cofre cerrado"
        self.descripcion = descripcion
        self.prob_vacio = 20
        self.prob_malo = prob_malo
        self.abierto = False
        self.estado = random.randint(1, 100)
        if self.estado < self.prob_vacio:
            self.estado = "vacio"
        elif self.estado < self.prob_vacio + self.prob_malo:
            self.estado = "malo"
        else:
            self.estado = "bueno"
    
    def Investigar(self):
        if self.abierto:
            print("el cofre ya ha sido abierto")
        else:
            print(self.descripcion)
    
    @abstractmethod
    def Abrir(self):
        pass
    
    @abstractmethod
    def Recolectar(self):
        pass
    
    @abstractmethod
    def Patear(self):
        pass


class CofreMadera(CofreCerrado):
    def __init__(self):
        descripcion = "este es un cofre de madera bastante comun en las cuevas, capaz es el tesoro de un pirata."
        super().__init__(40, descripcion)
        self.contenido_bueno = (1, 10)
        self.contenido_malo = "Gnomo ladron"
        self.monedas = random.randint(self.contenido_bueno[0], self.contenido_bueno[1])
    
    def Abrir(self):
        if self.estado == "vacio":
            print("el cofre esta vacio")
            self.abierto = True
            return "vacio"
        elif self.estado == "malo":
            print(f"has abierto el cofre... y te asalta un {self.contenido_malo}")
            self.estado = "vacio"
            self.abierto = True
            return ("ladron", self.contenido_malo)
        else:
            print("el cofre tiene un tesoro!")
            self.abierto = True
            return "tesoro"
    
    def Recolectar(self):
        if self.estado == "vacio":
            print("el cofre esta vacio")
            return 0
        else:
            print(f"¡has encontrado {self.monedas} monedas!")
            return self.monedas
    
    def Patear(self):
        if self.estado == "vacio":
            print("el cofre suena medio hueco")
        elif self.estado == "malo":
            print("el cofre te parece pesado")
        else:
            if self.monedas > self.contenido_bueno[1]:
                print("el cofre te parece pesado")
            else:
                print("el cofre se mueve con facilidad")

cofres_posibles = {
    "ninguno": {
        "objeto": None,
        "probabilidad": 20
    },
    "cofre_abierto": {
        "objeto": CofreAbierto,
        "probabilidad": 30
    },
    "cofre_madera": {
        "objeto": CofreMadera,
        "probabilidad": 50
    }
}

class Juego():

    def __init__(self):
        self.profundidad = 0
        self.tesoros_acumulados = 0


    def Mostrar_Estado(self):
        print(f"\n--- Profundidad {self.profundidad} ---")
        print(f"Tesoros acumulados: {self.tesoros_acumulados}")


    def Interactuar_Cofre(self, cofre):
        while True:
            print("\n¿Que deseas hacer?")
            print("1. Abrir")
            print("2. Recolectar")
            print("3. Patear")
            print("4. Salir")
            opcion = input("\nOpcion: ")
            if opcion == "1":
                resultado = cofre.Abrir()
                if resultado[0] == "ladron":
                    print(f"al parecer el {resultado[1]} te ofrece dejar al azar de una moneda tus tesoros, elije")
                    print("1. cara")
                    print("2. cruz")
                    opcion = int(input("\nOpcion: "))
                    azar = random.randint(1, 2)
                    if azar == opcion:
                        print("has ganado!")
                        print(f"el {resultado[1]} se va a regañadientes")
                    else:
                        print("has perdido!")
                        print(f"el {resultado[1]} se queda con la mitad de tus monedas")
                        self.tesoros_acumulados -= self.tesoros_acumulados // 2

            elif opcion == "2":
                resultado = cofre.Recolectar()
                self.tesoros_acumulados += resultado

            elif opcion == "3":
                cofre.Patear()
            elif opcion == "4":
                break


    def Comienzar_Juego(self):
        print("\nBienvenido a Busqueda profunda!")
        print("el objetivo es llegar lo mas lejos posible encontrando cofres en el camino")
        print("estas profundidades tienen grandes tesoros pero tambien grandes peligros")
        print("estas listo para comenzar? (ENTER)")
        input("")
        while True:
            self.Mostrar_Estado()
            probabilidad_cofre = random.randint(1, 100)
            probabilidad_acumulada = 0
            for cofre in cofres_posibles:
                probabilidad_acumulada += cofres_posibles[cofre]["probabilidad"]
                if probabilidad_cofre <= probabilidad_acumulada:
                    if cofres_posibles[cofre]["objeto"] != None:
                        cofre_actual = cofres_posibles[cofre]["objeto"]()
                    else:
                        cofre_actual = None
            if cofre_actual != None:
                print(f"has encontrado un {cofre_actual.nombre}!")
                self.Interactuar_Cofre(cofre_actual)
            else:
                print("no has encontrado nada... sigue bajando")
                input("presiona ENTER para continuar")
            self.profundidad += 1

Partida = Juego()
Partida.Comienzar_Juego()
    