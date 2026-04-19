"""
EJERCICIO 10: GRAN CARRERA

"""

import random

class Auto():
    def __init__(self, carril):
        self.aceleracion = 1
        self.limite_aceleracion = 3
        self.limite_velocidad = 10
        self.velocidad = 1
        self.turno = 1
        self.carril = carril
        self.posicion = 0
        self.ubicacion = 0
        self.distancia_meta = 100
        self.rebufo = False
        self.auto_rebufo = None
        self.carril_rebufo = None
        self.choque = False
    
    def __eq__(self, auto):
        if self.ubicacion == auto.ubicacion:
            return True
        else:
            return False
    
    def __lt__(self, auto):
        if self.carril == auto.carril:
            if self.ubicacion < auto.ubicacion:
                return True
            else:
                return False
        else:
            return False 
    
    def Datos(self):
        return (self.carril, self.ubicacion, self.velocidad)

    def Acelerar(self):
        if self.choque == True:
            self.aceleracion = 1
            self.velocidad = 0
            self.choque = False

        elif self.velocidad < self.limite_velocidad:
            self.velocidad += self.aceleracion
            if self.aceleracion < self.limite_aceleracion:
                self.aceleracion += 1
        else:
            pass
    
    def Avanzar(self):
        if self.rebufo:
            self.limite_aceleracion += 2
        else:
            self.limite_aceleracion = 3

        if self.auto_rebufo:
            if isinstance(self.auto_rebufo, Sistema):
                if self.ubicacion + self.velocidad >= self.auto_rebufo.ubicacion + self.auto_rebufo.velocidad:
                    print("no puede adelantar al auto en rebufo")
                    self.ubicacion = self.auto_rebufo.ubicacion + self.auto_rebufo.velocidad - 2
                elif self.ubicacion + self.velocidad >= self.auto_rebufo.ubicacion:
                    print("no puede adelantar al auto en rebufo")
                    self.ubicacion = self.auto_rebufo.ubicacion + self.auto_rebufo.velocidad - 2
                else:
                    self.ubicacion += self.velocidad
            else:
                self.ubicacion += self.velocidad
        else:
            self.ubicacion += self.velocidad
        
        self.turno += 1
        if self.turno % 2 == 0:
            self.Acelerar()
        else:
            pass
    
    def Rebufo(self, estado):
        if estado:
            self.rebufo = True
            self.limite_velocidad += 5
            print("limite de velocidad aumentado")
        else:
            self.rebufo = False
            self.limite_velocidad = 10
            if self.velocidad > self.limite_velocidad:
                self.velocidad = self.limite_velocidad
            print("limite de velocidad reducido")
    
    def Verificar_Meta(self):
        if self.ubicacion >= self.distancia_meta:
            return True
        else:
            return False
    
    def Verificar_Rebufo(self, autos):
        coincidencia = False
        for auto in autos:
            if self.__lt__(auto):
                coincidencia = True
                if self.rebufo == False and self.carril_rebufo != auto.carril:
                    print("te metiste en rebufo de", auto.Datos())
                    self.carril_rebufo = auto.carril
                    self.auto_rebufo = auto
                    self.Rebufo(True)
        
        if coincidencia == False:
            if self.rebufo == True:
                self.auto_rebufo = None
                print("saliste del rebufo")
                self.Rebufo(False)
                self.carril_rebufo = None
    
class Sistema(Auto):
    def __init__(self, carril):
        super().__init__(carril)
        self.aceleracion = 3

    def Decidir(self, autos):
        self.Avanzar()
        
    
class Jugador(Auto):
    def __init__(self, carril):
        super().__init__(carril)

        self.nitro = True
        self.bandera_nitro = 0
    
    def Usar_Nitro(self):
        if self.nitro == True:
            velocidad_pre_nitro = self.velocidad
            self.velocidad += self.limite_velocidad // 3
            self.nitro = False
            self.bandera_nitro = self.turno
            self.Avanzar()
            self.velocidad = velocidad_pre_nitro
            print("usaste nitro")
            return True
        else:
            print("no tienes nitro")
            return False
    
    def Verificar_Nitro(self):
        if self.turno - self.bandera_nitro == 3:
            self.nitro = True
            print("se te recargo el nitro")
        else:
            pass

    
    def Chocar(self, carril, autos):
        if self.carril - 1 == carril and carril != 0:
            for auto in autos:
                if self == auto and auto.carril == carril:
                    efectivo = random.randint(1, 10)
                    if efectivo > 7:
                        auto.choque = True
                        print("coque exitoso")
                        return True
                    else:
                        print("coque fallido")
                        self.choque = True
                        return True
            self.choque = True
            return True
        elif self.carril + 1 == carril and carril <= len(autos):
            for auto in autos:
                if self == auto and auto.carril == carril:
                    efectivo = random.randint(1, 10)
                    if efectivo > 7:
                        auto.choque = True
                        print("coque exitoso")
                        return True
                    else:
                        print("coque fallido")
                        self.choque = True
                        return True
            self.choque = True
            return True
        else:
            return False
    
    def Cambiar_Carril(self, carril, autos):
        if carril >= 0 and carril <= len(autos):
            for auto in autos:
                if self == auto and auto.carril == carril:
                    print("no puedes cambiar de carril")
                    return False
            self.carril = carril
            return True
        else:
            print("estas en el limite de carriles, no puedes cambiar")
            return False

    def Menu_Eleccion(self, autos):
        print(f"tienes {self.velocidad} de velocidad y {self.aceleracion} de aceleracion, que haras?")
        print("1 o  ENTER para avanzar")
        print("2 para usar nitro")
        print("3 para cambiar de carril")
        print("4 para chocar a un carril cercano")
        eleccion = input("ingresa tu eleccion: ")
        if eleccion == "1" or eleccion == "":
            pass
        elif eleccion == "2":
            if not self.Usar_Nitro():
                self.Menu_Eleccion(autos)
        elif eleccion == "3":
            print("a que carril quieres cambiar?")
            print("1. arriba")
            print("2. abajo")
            carril = int(input("ingresa el carril: "))
            if carril == 1:
                if self.Cambiar_Carril(self.carril - 1, autos):
                    pass
                else:
                    self.Menu_Eleccion(autos)
            elif carril == 2:
                if self.Cambiar_Carril(self.carril + 1, autos):
                    pass
                else:
                    self.Menu_Eleccion(autos)
            else:
                print("eleccion invalida")
                self.Menu_Eleccion()

        elif eleccion == "4":
            print("a que carril quieres chocar?")
            print("1. arriba")
            print("2. abajo")
            carril = int(input("ingresa el carril: "))
            if carril == 1:
                self.Chocar(self.carril - 1, autos)
            elif carril == 2:
                self.Chocar(self.carril + 1, autos)
            else:
                print("eleccion invalida")
                self.Menu_Eleccion()

    def Decidir(self, autos):
        self.Verificar_Nitro()
        self.Menu_Eleccion(autos)
        self.Avanzar()


class Juego():
    def __init__(self):
        self.autos = []
        self.turno = 0
        self.ganador = None
    
    def Agregar_Auto(self, auto):
        self.autos.append(auto)
    
    def Verificar_Ganador(self):
        for auto in self.autos:
            if auto.Verificar_Meta():
                if not self.ganador:
                    self.ganador = auto
                else:
                    if auto.ubicacion > self.ganador.ubicacion:
                        self.ganador = auto
        if self.ganador:
            return True
        return False
    
    def Mostrar_Pista(self):
        for auto in self.autos:
            print(auto.Datos())
    
    def Jugar(self):
        while not self.ganador:
            print("-"*20)
            print(f"turno {self.turno}")
            print("-"*20)
            for auto in self.autos:
                auto.Verificar_Rebufo(self.autos)
                if isinstance(auto, Jugador):
                    self.Mostrar_Pista()
                auto.Decidir(self.autos)
            self.Verificar_Ganador()
            self.turno += 1
        ganador = self.autos.index(self.ganador) + 1
        if isinstance(self.ganador, Jugador):
            print("ganaste la carrera")
            print("VICTORY")
        else:
            print(f"El ganador es el auto {ganador}")
            print("GAME OVER")

Partida = Juego()
Partida.Agregar_Auto(Jugador(1))
Partida.Agregar_Auto(Sistema(2))
Partida.Agregar_Auto(Sistema(3))
Partida.Jugar()