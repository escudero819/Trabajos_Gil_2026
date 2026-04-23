
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

    def __init__(self, vida, lista_dibujos, danio, bando):
        self.vida = vida
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
        super().__init__(2, ["o", "x"], 2, bando)
    


class Arquero():
    def __init__(self, distancia):
        self.velocidad = 4
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
                if self.velocidad - self.bandera_recarga <= 0:
                    self.recargando = False
                    self.bandera_recarga = 0
                    self.dibujo = self.lista_dibujos[0]
                self.bandera_recarga += 1

class Torre():
    def __init__(self):
        self.vida = 100
        self.defensa = 0
        self.defensa_max = 0
        self.distancia_arqueros = 10
        self.arqueros = [Arquero(self.distancia_arqueros)]
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
            self.arqueros.append(Arquero(self.distancia_arqueros))
            self.monedas -= self.coste_arquero
            self.coste_arquero += 1
            return True
    
    def Mejorar_Defensa(self):
        if self.monedas - self.coste_defensa < 0:
            print("no tienes suficiente dinero")
            return False
        else:
            self.monedas -= self.coste_defensa
            self.defensa += 4
            self.coste_defensa += 2
            print(f"ahora tienes {self.defensa} de defensa")
            return False
    
    def Reparar(self):
        if self.vida == 100:
            print("estas al tope de vida")
            return False
        elif self.monedas - self.coste_reparacion < 0:
            print("no tienes suficiente dinero")
            return False
        else:
            self.monedas -= self.coste_reparacion
            self.vida += 20
            if self.vida > 100:
                self.vida = 100
            print(f"ahora la torre tiene {self.vida} de vida")

    def RecibirGolpe(self, danio):
        if self.defensa:
            self.defensa -= danio
        else:
            self.vida -= danio
        

    def Arqueros_Atacar(self, lista_camino):
        for arquero in self.arqueros:
            arquero.Defender(lista_camino)

class Horda():
    def __init__(self, cantidad, lista_camino, torre, remuneracion):
        self.lista_tropas = []
        for i in range(cantidad):
            self.lista_tropas.append(Barbaro(2))
        self.torre = torre
        self.lista_camino = lista_camino
        self.remuneracion = remuneracion
        for arquero in self.torre.arqueros:
            arquero.recargando = False
            arquero.dibujo = arquero.lista_dibujos[0]

    def Atacar(self):
        if not isinstance(self.lista_camino[-1], str):
            if self.lista_camino[-1].vida > 0:
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


class Partida():
    def __init__(self):
        self.torre = Torre()
        self.cantidad_barbaros = 3
        self.ronda = 1
        self.recompensa = 2
        self.lista_camino = []
        for i in range(1, 21):
            self.lista_camino.append("-")
        
        print("bienvenido a la frontera Capitan")
        print("tu encomienda sera defender la torre de los barbaros")
        print("tendras que mejorar tu defensa, reclutar arqueros y reparar la torre")
        print("cada ronda vendran mas barbaros pero con ellos vendran sus tesoros")
        print("si logras sobrevivir a 10 rondas habras ganado")
        print("si la torre llega a 0 puntos de vida habras perdido")
        print("")
    
    def Subir_Nivel_Horda(self):
        if self.ronda % 2 == 0:
            barbaros = self.cantidad_barbaros // 3
            if barbaros < 4:
                barbaros = 4
            self.cantidad_barbaros += barbaros
            aumento = self.recompensa // 5
            if aumento < 3:
                aumento = 3
            self.recompensa += aumento
        self.ronda += 1

    def Menu(self):
        print(f"tenes {self.torre.monedas} monedas, que haras?")
        print("1. reclutar 1 arquero mas (max 5) -", self.torre.coste_arquero)
        print("2. mejorar defensas -", self.torre.coste_defensa)
        print("3. reparar la Torre (max 20) -", self.torre.coste_reparacion)
        #print("4. subir de nivel un arquero -", self.torre.coste_arquero_nv2)
        print("4. avanzar a la siguiente horda")
        op = int(input("-- "))
        return op


    def Entre_Tiempo(self):
        eleccion = self.Menu()
        if eleccion == 1:
            self.torre.Nuevo_Arquero()
        if eleccion == 2:
            self.torre.Mejorar_Defensa()
        if eleccion == 3:
            self.torre.Reparar()
        if eleccion == 4:
            return
        self.Entre_Tiempo()

            

    def Iniciar_Partida(self):
        while self.torre.vida > 0:
            self.Entre_Tiempo()
            print(f"HORDA NUMERO:", self.ronda)
            self.horda = Horda(self.cantidad_barbaros, self.lista_camino, self.torre, self.recompensa)
            self.horda.Iniciar_Horda()
            self.Subir_Nivel_Horda()



partida = Partida()
partida.Iniciar_Partida()
    
