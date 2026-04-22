
import time

def Mostrar_estado_juego(lista_ataque_enemigo, torre):
    tropas_en_camino = list(map(lambda tropa: tropa if tropa == "-"  else tropa.dibujo if tropa.dibujo != "" else "-", lista_ataque_enemigo))
    tropas_visibles = "".join(tropas_en_camino)
    print(tropas_en_camino) # TEST

    print("visibles", tropas_visibles) # TEST
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
            self.dibujo_actual += 1
            self.dibujo = self.lista_dibujos[self.dibujo_actual]
        else:
            self.dibujo = ""

    def Atacar(self, enemigo):
        if isinstance(enemigo, Tropa):
            enemigo.RecibirGolpe(1)
        else:
            enemigo.RecibirGolpe(self.danio)

    def Avanzar(self, tropa_proxima):
        # retorna True si la tropa puede avanzar evitando una superposicion de tropas y sea printeable el juego
        if tropa_proxima != "-":
            if tropa_proxima.dibujo != "":
                if tropa_proxima.bando == self.bando:
                    return False
                else:
                    self.Atacar(tropa_proxima)
                    return False
            else:
                print("se puede avanzar")
                return True
        else:
            print("se puede avanzar")
            return True

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
                    if objetivo.bando != self.bando:
                        enemigo = objetivo
        
        if enemigo:
            if not self.recargando:
                Disparar(enemigo)
                self.recargando = True
                self.bandera_recarga += 1
            else:
                if self.bandera_recarga - self.velocidad <= 0:
                    self.recargando = False
                    self.bandera_recarga = 0

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
        self.vida -= danio - self.defenza


tropa1 = Tropa(0, 2, ["o", "x"], 1, 0)
tropa2 = Tropa(0, 2, ["o", "x"], 1, 0)
tropa3 = Tropa(0, 2, ["o", "x"], 1, 0)

lista_camino = []
for i in range(1, 21):
    lista_camino.append("-")

lista = [tropa1, tropa2, tropa3]

def Avanzar(lista_camino, lista, torre):
    for i in range(len(lista_camino) - 1, -1, -1):
        #print(f"casilla {i}")
        casilla_actual = lista_camino[i]
        if i == 0:
            if lista:
                casilla_anterior = lista[-1]
                if not isinstance(casilla_anterior, str):
                    if casilla_anterior.Avanzar(casilla_actual):
                        lista_camino[i] = casilla_anterior
                        lista.pop(-1)
                else:
                    casilla_actual = casilla_anterior
                    casilla_anterior = "-"
        else:
            casilla_anterior = lista_camino[i - 1]
            if not isinstance(casilla_anterior, str):
                if casilla_anterior.Avanzar(casilla_actual):
                    lista_camino[i] = casilla_anterior
                    lista_camino[i - 1] = "-"
            else:
                casilla_actual = casilla_anterior
                casilla_anterior = "-"
        #print(f"{casilla_actual} | {casilla_anterior}")
        time.sleep(0.1)
    print(lista)
    Mostrar_estado_juego(lista_camino, torre)
    time.sleep(0.7)

torre = Torre()
for i in range(1, 21):
    Avanzar(lista_camino, lista, torre)
    
