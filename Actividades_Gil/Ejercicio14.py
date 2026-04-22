
import time

def Mostrar_estado_juego(lista_ataque_enemigo, torre):
    tropas_en_camino = list(map(lambda tropa: tropa if tropa == "-"  else tropa.dibujo if tropa.dibujo != "" else "-", lista_ataque_enemigo))
    tropas_visibles = "".join(tropas_en_camino)
    #print(tropas_en_camino) # TEST

    #print("visibles", tropas_visibles) # TEST
    lineas_torre = []
    cant_arqueros = len(torre.arqueros)
    for i in range(1, 6):
        linea = "H"
        if i <= cant_arqueros:
            arquero = torre.arqueros[i-1].dibujo
            linea += arquero
        else:
            linea += " "
        
        if torre.vida > 100 - i*20:
            linea += " |"
        else:
            linea += "  "
        
        lineas_torre.append(linea)

    print(f"{f"{lineas_torre[0]} T":>26}")
    print(f"{f"{lineas_torre[1]} O":>26}")
    print(f"{tropas_visibles:}{lineas_torre[2]} R") 
    print(f"{f"{lineas_torre[3]} R":>26}")
    print(f"{f"{lineas_torre[4]} E":>26}")



class Tropa():

    def __init__(self, vida, velocidad, lista_dibujos, danio, bando):
        self.vida = vida
        self.velocidad = velocidad
        self.lista_dibujos = lista_dibujos
        self.danio = danio
        self.bando = bando
        self.dibujo_actual = 0
        self.dibujo = lista_dibujos[self.dibujo_actual]
    
    def RecibirGolpe(self, danio):
        self.vida -= danio
        if self.vida:
            #print("recibio golpe")
            self.dibujo_actual += 1
            self.dibujo = self.lista_dibujos[self.dibujo_actual]
        else:
            self.dibujo = "-"

    def Atacar(self, enemigo):
        if isinstance(enemigo, Tropa):
            enemigo.RecibirGolpe(1)
        else:
            enemigo.RecibirGolpe(self.danio)

    def Avanzar(self, tropa_proxima):
        # retorna True si la tropa puede avanzar evitando una superposicion de tropas y sea printeable el juego
        if tropa_proxima != "-":
            if tropa_proxima.dibujo != "-":
                if tropa_proxima.bando == self.bando:
                    return False
                else:
                    self.Atacar(tropa_proxima)
                    return False
            else:
                #print("se puede avanzar")
                return True
        else:
            #print("se puede avanzar")
            return True


class Barbaro(Tropa):
    def __init__(self, bando):
        super().__init__(2, 1, ["o", "x"], 2, bando)
    


class Arquero():
    def __init__(self, distancia):
        self.velocidad = 2
        self.distancia = distancia
        self.lista_dibujos = ["<", "@"]
        self.danio = 1
        self.bando = 1
        self.recargando = False
        self.bandera_recarga = 0
        self.dibujo = self.lista_dibujos[0]
    
    def Defender(self, lista_camino):

        def Disparar(enemigo):
            enemigo.RecibirGolpe(self.danio)

        enemigo = None
        for casilla in range(len(lista_camino) - 1, len(lista_camino) - self.distancia, -1):
            objetivo = lista_camino[casilla]
            if not enemigo:
                if objetivo != "-":
                    if objetivo.dibujo != "-":
                        if objetivo.bando != self.bando:
                            enemigo = objetivo
        
        if enemigo:
            if not self.recargando:
                Disparar(enemigo)
                self.recargando = True
                self.bandera_recarga += 1
                self.dibujo = self.lista_dibujos[1]
            else:
                if self.bandera_recarga - self.velocidad <= 0:
                    self.recargando = False
                    self.bandera_recarga = 0
                    self.dibujo = self.lista_dibujos[0]

class Torre():
    def __init__(self):
        self.vida = 100
        self.defensa = 0
        self.arqueros = [Arquero(10)]
        self.lim_arqueros = 5
        self.coste_defensa = 2
        self.coste_reparacion = 5
        self.coste_arquero = 1
        self.coste_arquero_nv2 = 3
        self.monedas = 0
    
    def Nuevo_Arquero(self):
        if self.monedas - self.coste_arquero < 0:
            print("no tienes suficiente dinero")
            return False
        elif len(self.arqueros) == self.lim_arqueros:
            print("ya tienes el maximo de arqueros")
            return False
        else:
            self.arqueros.append(Arquero(10))
            self.monedas -= self.coste_arquero
            return True
    
    def Mejorar_Defensa(self):
        if self.monedas - self.coste_defensa < 0:
            print("no tienes suficiente dinero")
            return False
        else:
            self.monedas -= self.coste_defensa
            self.defensa += 1
            return False
    
    def Reparar(self):
        if self.vida == 100:
            print("estas al tope de vida")
            return False
        elif self.monedas - self.coste_reparacion:
            print("no tienes suficiente dinero")
            return False
        else:
            self.monedas -= self.coste_reparacion
            self.vida += 20
            if self.vida > 100:
                self.vida = 100

    def RecibirGolpe(self, danio):
        self.vida -= danio - self.defensa

    def Arqueros_Atacar(self, lista_camino):
        for arquero in self.arqueros:
            arquero.Defender(lista_camino)


tropa1 = Barbaro(2)
tropa2 = Barbaro(2)
tropa3 = Barbaro(2)

lista_camino = []
for i in range(1, 21):
    lista_camino.append("-")

lista = [tropa1, tropa2, tropa3]

class Horda():
    def __init__(self, cantidad, lista_camino, torre, remuneracion):
        self.lista_tropas = []
        for i in range(cantidad):
            self.lista_tropas.append(Barbaro(2))
        self.torre = torre
        self.lista_camino = lista_camino
        self.remuneracion = remuneracion

    def Atacar(self):
        if not isinstance(self.lista_camino[-1], str):
            self.lista_camino[-1].Atacar(self.torre)

    def Avanzar(self):
        print("-"*30)
        self.torre.Arqueros_Atacar(self.lista_camino)
        self.Atacar()
        for i in range(len(self.lista_camino) - 1, -1, -1):
            #print(f"casilla {i}")
            casilla_actual = self.lista_camino[i]
            if i == 0:
                if self.lista_tropas:
                    casilla_anterior = self.lista_tropas[-1]
                    if not isinstance(casilla_anterior, str):
                        if casilla_anterior.Avanzar(casilla_actual):
                            self.lista_camino[i] = casilla_anterior
                            self.lista_tropas.pop(-1)
                    else:
                        casilla_actual = casilla_anterior
                        casilla_anterior = "-"
            else:
                casilla_anterior = self.lista_camino[i - 1]
                if not isinstance(casilla_anterior, str):
                    if casilla_anterior.Avanzar(casilla_actual):
                        self.lista_camino[i] = casilla_anterior
                        self.lista_camino[i - 1] = "-"
                else:
                    casilla_actual = casilla_anterior
                    casilla_anterior = "-"
            #print(f"{casilla_actual} | {casilla_anterior}")
            #time.sleep(0.1)
        #print(self.lista_tropas)
        
        for tropa in self.lista_tropas:
            if tropa.vida <= 0:
                self.lista_tropas.remove(tropa)
                self.lista_camino[i] = "-"
        #print(self.lista_tropas)
        Mostrar_estado_juego(self.lista_camino, self.torre)
        print("-"*30)
        time.sleep(0.7)

    def Iniciar_Horda(self):
        while True:
            self.Avanzar()
            finalizo = True
            for tropa in self.lista_camino:
                if not isinstance(tropa, str):
                    if tropa.vida > 0:
                        finalizo = False
            if finalizo: 
                break
        print("sobreviviste a la ronda!")
        self.torre.monedas += self.remuneracion
        print(f"recibiste {self.remuneracion} monedas")
        print(f"tienes {self.torre.vida} puntos de vida")
        print(f"tienes {self.torre.monedas} monedas")
    
torre = Torre()
remuneracion = 5
horda = Horda(4, lista_camino, torre, remuneracion)
horda.Iniciar_Horda()
    
