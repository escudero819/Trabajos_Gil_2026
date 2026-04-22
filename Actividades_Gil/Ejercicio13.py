#  EJERCICIO 13: DESAFIO DE DADOS

import random
import time

class Jugador():

    def __init__(self, nombre, controlador):
        self.puntos = 0
        self.multiplicador = False
        self.congelado = False
        self.nombre = nombre
        self.controlador = controlador
    
    def AumentarPuntos(self, puntos):
        if self.multiplicador:
            print(f"gracias al X2 {self.nombre} consigue {puntos*2}")
            self.puntos += puntos * 2
            self.multiplicador = False
        else:
            self.puntos += puntos
    
    def DisminuirPuntos(self, puntos):
        self.puntos -= puntos

    def TirarDados(self):
        resultado = random.randint(1, 10)
        if resultado > 6:
            if resultado == 7:
                resultado = "robar"
            if resultado == 8:
                resultado = "cambiar"
            if resultado == 9:
                resultado = "perder"
            if resultado == 10:
                resultado = "congelar"
        return resultado

    def Robar(self, jugador):
        puntos = random.randint(1, 6)
        print(f"han robado {puntos} puntos")
        if jugador.puntos - puntos < 0:
            puntos = jugador.puntos
        jugador.DisminuirPuntos(puntos)
        self.AumentarPuntos(puntos)
    
    def Congelar(self, jugador):
        if jugador.congelado:
            print("no se puede congelar a alguien congelado")
        else:
            print(f"{jugador.nombre} ha sido congelado")
            return True
    
    def Cambiar(self, jugador):
        if jugador.congelado:
            print("no se le puede cambiar a alguien congelado")
        else:
            print(f"cambiaron los puntos {self.nombre} con {jugador.nombre}")
            puntos = jugador.puntos
            jugador.puntos = self.puntos
            self.puntos = puntos
    
    def Perder(self):
        puntos = self.puntos // 6
        self.puntos -= puntos
        print(f"{self.nombre} ha perdido 1/6 de sus puntos ({puntos})")


nombres = ["pepe", "juan", "maria", "cecilia", "miranda", "diego torres", "alguien"]

class Desafio_Dados():

    def __init__(self, cantidad_jugadores, num_rondas):
        self.jugadores = []
        for i in range(cantidad_jugadores - 1): # -1 con usuario
            nombre = random.choice(nombres)
            nombres.pop(nombres.index(nombre))
            nuevo_jugador = Jugador(nombre, "maquina")
            self.jugadores.append(nuevo_jugador)
        usuario = Jugador(input("ingrese nombre:"), "usuario")
        self.jugadores.append(usuario)
        self.ronda = 1
        self.max_rondas = num_rondas + 1

    def Elegir_Maquina(self, jugador):

        def Elegir_no_Congelado():
            jugadores = self.jugadores.copy()
            jugadores.pop(jugadores.index(jugador))
            jugador_afectado = None
            while jugador_afectado == None:
                seleccionado = random.choice(jugadores)
                if not seleccionado.congelado:
                    jugador_afectado = seleccionado
                    return jugador_afectado

        resultado_dado = jugador.TirarDados()
        if isinstance(resultado_dado, str):
            if resultado_dado == "robar":
                jugador_afectado = Elegir_no_Congelado()
                jugador.Robar(jugador_afectado)
                
            if resultado_dado == "cambiar":
                jugador_afectado = Elegir_no_Congelado()
                jugador.Cambiar(jugador_afectado)
                self.Elegir_Maquina(jugador)
            
            if resultado_dado == "congelar":
                jugador_afectado = Elegir_no_Congelado()
                jugador.Congelar(jugador_afectado)            
            
            if resultado_dado == "perder":
                jugador.Perder()
        else:
            print(f"{jugador.nombre} suma {resultado_dado} puntos")
    
    def Elegir_Usuario(self, jugador):

        def Seleccionar_jugador():
            jugadores = self.jugadores.copy()
            jugadores.pop(jugadores.index(jugador))
            print("a quien seleccionas?")
            for i in range(len(jugadores)):
                print(f"{i + 1}- {jugadores[i].nombre}")
            op = int(input("-- "))
            seleccionado = jugadores[op - 1]
            return seleccionado



        resultado_dado = jugador.TirarDados()
        print("te ha salido un", resultado_dado)
        if isinstance(resultado_dado, str):
            if resultado_dado == "robar":
                print("puedes robarle lo que saquen los dados a otro jugador")
                jugador_afectado = Seleccionar_jugador()
                jugador.Robar(jugador_afectado)
                
            if resultado_dado == "cambiar":
                print("puedes cambiar tus puntos por los de alguien mas")
                jugador_afectado = Seleccionar_jugador()
                jugador.Cambiar(jugador_afectado)
                self.Elegir_Usuario(jugador)
            
            if resultado_dado == "congelar":
                print("puedes congelar a un jugador")
                jugador_afectado = Seleccionar_jugador()
                jugador.Congelar(jugador_afectado)            
            
            if resultado_dado == "perder":
                print("diablos, se te arrebatan puntos")
                jugador.Perder()
        else:
            print(f"sumas {resultado_dado} puntos")
            jugador.puntos += resultado_dado


    def Partida(self):
        print(""*20)
        print("Comenzando partida...")
        print(f"en {self.max_rondas} rondas debes conseguir la mayor cantidad de puntos")
        print(""*20)
        while self.ronda < self.max_rondas:
            print("RONDA: ", self.ronda)
            for jugador in self.jugadores:
                print("turno de: ", jugador.nombre)
                time.sleep(0.2)
                if jugador.congelado:
                    print("pierde el turno por estar congelado")
                    jugador.congelado = False
                else:
                    if jugador.controlador == "maquina":
                        self.Elegir_Maquina(jugador)
                    else:
                        self.Elegir_Usuario(jugador)
                imprimible = f"{jugador.puntos} puntos"
                if jugador.congelado:
                    imprimible += "- congelado"
                if jugador.multiplicador:
                    imprimible += "- multiplicador"
                print(imprimible)
                print("-"*10)
                time.sleep(0.4)
            print("-"*20)
            print("-"*20)
            self.ronda += 1
        ganador = Jugador("","")
        for jugador in self.jugadores:
            if jugador.puntos > ganador.puntos:
                ganador = jugador
        print("FIN DE LA PARTIDA")
        if isinstance(ganador, Jugador):
            print("GANASTE!!!")
        else:
            print("GAME OVER")
            print("el que gano fue", ganador.nombre)
        print("con", ganador.puntos, "puntos")
    

partida = Desafio_Dados(4, 10)
partida.Partida()