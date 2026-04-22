"""
EJERCICIO 11: BATALLA DE MAGOS
"""
descripcion = "" \
"     En esta confrontacion te encuentras ante un mago formidable, deberas utilizar sabia y estrategicamente \n" \
"tus recursos de mana, vida y la regeneracion de los mismos, tendras varios hechizos pero cada cual tiene su precio \n" \
"  ESTA SERA LA BATALLA POR LA CUAL INICIASTE TU CAMINO POR LA SENDA DE LA HECHICERIA!!! AHORA ALZATE VICTORIOSO!"

print(descripcion)

import random

nombre_enemigo = "Malefica"
nombres_hechizos_enemigo = {
    "ataque_comun": "rafaga de llamas",
    "ataque_fuerte": "llama del dragon",
    "regeneracion": "absorcion oscura",
    "escudo": "escamas de dragon",
    "esquivar": "aleteo",
    "meditacion": "concentracion del mal"
}

nombre_hechizos_jugador = {
    "ataque_comun": "haz de luz",
    "ataque_fuerte": "morado",
    "regeneracion": "curacion",
    "escudo": "infinito",
    "esquivar": "escape",
    "meditacion": "inspiracion"
}

class Hechicero():

    def __init__(self, nombres_hechizos: dict):
        self.nombres_hechizos = nombres_hechizos
        self.vida = 150
        self.mana = 50
        self.danio_comun = (5, 15)
        self.costo_comun = 5
        self.danio_fuerte = (15, 30)
        self.costo_fuerte = 15
        self.escudo_reduccion = 3
        self.escudo_costo = 5
        self.regeneracion = 10
        self.regeneracion_costo = 5
        self.meditacion_aumento = 10
        self.prob_esquivar = 70
        self.decision = None
        self.enemigo = None
    
    def Recibir_Danio(self, danio):
        if self.decision == "esquivar":
            efectivo = random.randint(1,100)
            if efectivo <= self.prob_esquivar:
                print(f" {self.nombre} logro esquivar el ataque")
            else:
                print("no logro esquivarlo!")
                self.vida -= danio
                print(f"{self.enemigo.nombre} ha pegado {danio} de danio")
        elif self.decision == "defenderse":
            danio = danio // self.escudo_reduccion
            print(f"{self.nombre} se protege, pero aun asi recibe: {danio} de danio")
            self.vida -= danio
        else:
            self.vida -= danio
            print(f"{self.enemigo.nombre} ha pegado {danio} de danio")

    def Ataque_Comun(self, enemigo):
        self.mana -= self.costo_comun
        danio_efectuado = random.randint(self.danio_comun[0], self.danio_comun[1])
        print(f"{self.nombre} utiliza {self.nombres_hechizos["ataque_comun"]}")
        enemigo.Recibir_Danio(danio_efectuado)
    
    def Ataque_Fuerte(self, enemigo):
        self.mana -= self.costo_fuerte
        danio_efectuado = random.randint(self.danio_fuerte[0], self.danio_fuerte[1])
        print(f"{self.nombre} utiliza {self.nombres_hechizos["ataque_fuerte"]}")
        enemigo.Recibir_Danio(danio_efectuado)
    
    def Seleccionar_Ataque(self):
        print("que hechizo quiere lanzar?")
        print(f"1- {self.nombres_hechizos["ataque_comun"]} - {self.costo_comun}")
        print(f"2- {self.nombres_hechizos["ataque_fuerte"]} - {self.costo_fuerte}")
        print(f"3- volver")
        op = int(input("-- "))
        if op == 1:
            self.decision = "ataque_comun"
            return True
        if op == 2:
            self.decision = "ataque_fuerte"
            return True
        if op == 3:
            return False
    
    def Enemigo(self, enemigo):
        self.enemigo = enemigo

    def Accionar(self):
        if self.decision == "ataque_comun":
            self.Ataque_Comun(self.enemigo)
        if self.decision == "ataque_fuerte":
            self.Ataque_Fuerte(self.enemigo)
        

propabilidad_100 = {
    "atacar": 70,
    "defenderse": 15,
    "esquivar": 15,
    "meditar": 0,
    "regenerar": 0,
    "fuerte": 50
}

probabilidad_60 = {
    "atacar": 30,
    "defenderse": 30,
    "esquivar": 10,
    "meditar": 15,
    "regenerar": 15,
    "fuerte": 30
}

probabilidad_40 = {
    "atacar": 15,
    "defenderse": 20,
    "esquivar": 20,
    "meditar": 15,
    "regenerar": 30,
    "fuerte": 90
}

class Sistema(Hechicero):
    def __init__(self, nombres_hechizos, nombre):
        super().__init__(nombres_hechizos)
        self.nombre = nombre
    
    def Eleccion(self):
        if self.vida > self.vida // 100 * 60:
            self.probabilidades = propabilidad_100
        elif self.vida <= self.vida // 100 * 60 and self.vida > self.vida // 100 * 40:
            self.probabilidades = probabilidad_60
        elif self.vida <= self.vida // 100 * 40:
            self.probabilidades = probabilidad_40
        
        eleccion_bot = random.randint(1, 100)
        contador = 0
        decision_actual = None
        
        for probabilidad in self.probabilidades.items():
            if probabilidad[0] != "fuerte":
                contador += probabilidad[1]
                if eleccion_bot <= contador:
                    if not decision_actual:
                        decision_actual = probabilidad[0]
                        if decision_actual == "atacar":
                            probabilidad_ataque = random.randint(1, 100)
                            if probabilidad_ataque <= self.probabilidades["fuerte"]:
                                if self.mana - self.costo_fuerte < 0:
                                    self.Eleccion()
                                    return
                                else:
                                    decision_actual = "ataque_fuerte"
                            else:
                                if self.mana - self.costo_comun < 0:
                                    self.Eleccion()
                                    return 
                                else:
                                    decision_actual = "ataque_comun"
        
        if decision_actual == "regenerar":
            if self.mana - self.regeneracion_costo < 0:
                self.Eleccion()
                return 
            else:
                self.vida += self.regeneracion
                self.mana -= self.regeneracion_costo
                print(f"{self.nombre} utilizo {self.nombres_hechizos["regeneracion"]} y se curo {self.regeneracion} de vida")
        if decision_actual == "defenderse":
            if self.mana - self.escudo_costo < 0:
                self.Eleccion()
                return 
            else:
                self.mana -= self.escudo_costo
                print(f"{self.nombre} se protege con {self.nombres_hechizos["escudo"]}")
        if decision_actual == "esquivar":
            if self.decision == "esquivar":
                self.Eleccion()
                return 
            else:
                print(f"{self.nombre} intenta esquivar con {self.nombres_hechizos["esquivar"]}")
        if decision_actual == "meditar":
            self.mana += self.meditacion_aumento
            print(f"{self.nombre} utiliza {self.nombres_hechizos["meditacion"]}")
        
        self.decision = decision_actual
        print(self.decision)
            
    def Decision(self):
        self.Eleccion()


class Jugador(Hechicero):
    def __init__(self, nombres_hechizos, nombre):
        super().__init__(nombres_hechizos)
        self.nombre = nombre

    def Menu_Eleccion(self):
        print("que vas a hacer?")
        print("1- Ataquar")
        print(f"2- {self.nombres_hechizos["escudo"]} - {self.escudo_costo}m")
        print(f"3- {self.nombres_hechizos["regeneracion"]} - {self.regeneracion_costo}m")
        print(f"4- {self.nombres_hechizos["esquivar"]} - {self.prob_esquivar}%")
        print(f"5- {self.nombres_hechizos['meditacion']} + {self.meditacion_aumento}m")
        op = input("-- ")
        while op == "":
            op = input("-- ")
        op = int(op)
        if op == 1:
            if not self.Seleccionar_Ataque():
                self.Menu_Eleccion()
            return
        if op == 2:
            self.mana -= self.escudo_costo
            self.decision = "defenderse"
            print(f"{self.nombre} se protege con {self.nombres_hechizos["escudo"]}")
        if op == 3:
            self.mana -= self.regeneracion_costo
            self.vida += self.regeneracion
            self.decision = "regenerarse"
            print(f"{self.nombre} se regenera con {self.nombres_hechizos["regeneracion"]}")
        if op == 4:
            if self.decision != "esquivar":
                print(f"{self.nombre} intenta esquivar con {self.nombres_hechizos["esquivar"]}")
                self.decision = "esquivar"
            else:
                print("no puede esquivar 2 veces seguidas")
                self.Menu_Eleccion()
        if op == 5:
            self.mana += self.meditacion_aumento
            print(f"{self.nombre} utiliza {self.nombres_hechizos["meditacion"]}")
            self.decision = "meditar"

    def Decidir(self):
        self.Menu_Eleccion()


class Juego():

    def __init__(self):
        self.jugador = Jugador(nombre_hechizos_jugador, "Gandalf")
        self.sistema = Sistema(nombres_hechizos_enemigo, nombre_enemigo)
        self.jugador.Enemigo(self.sistema)
        self.sistema.Enemigo(self.jugador)
    
    def Mostrar_Info(self):
        print(f"|{self.jugador.nombre:^15}|{self.sistema.nombre:^15}|")
        print(f"|{self.jugador.vida:^15}|{self.sistema.vida:^15}|")
        print(f"|{self.jugador.mana:^15}|{self.sistema.mana:^15}|")

    def Iniciar_Partida(self):
        while self.jugador.vida > 0 and self.sistema.vida > 0:
            self.Mostrar_Info()
            self.jugador.Decidir()
            self.sistema.Decision()
            self.jugador.Accionar()
            self.sistema.Accionar()
        
        if self.jugador.vida < 0:
            print("GAME OVER")
            print(f"{self.sistema.nombre} ha vencido")
        else:
            print("VICTORY")
            print(f"Tu, el gran {self.jugador.nombre} has derrotado a {self.sistema.nombre}")


partida = Juego()
partida.Iniciar_Partida()