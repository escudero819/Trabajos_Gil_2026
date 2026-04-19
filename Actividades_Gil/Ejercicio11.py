"""
EJERCICIO 11: BATALLA DE MAGOS
"""
descripcion = "" \
"     En esta confrontacion te encuentras ante un mago formidable, deberas utilizar sabia y estrategicamente \n" \
"tus recursos de mana, vida y la regeneracion de los mismos, tendras varios hechizos pero cada cual tiene su precio \n" \
"  ESTA SERA LA BATALLA POR LA CUAL INICIASTE TU CAMINO POR LA SENDA DE LA HECHICERIA!!! AHORA ALZATE VICTORIOSO!"

print(descripcion)

import random

class Hechicero():

    def __init__(self, nombres_hechizos: dict):
        self.nombres_hechizos = nombres_hechizos
        self.vida = 100
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
        if self.decision == "defenderse":
            self.vida -= danio // self.escudo_reduccion
        else:
            self.vida -= danio

    def Ataque_Comun(self, enemigo):
        self.mana -= self.costo_comun
        danio_efectuado = random.randint(self.danio_comun)
        enemigo.Recibir_Danio(danio_efectuado)
    
    def Ataque_Fuerte(self, enemigo):
        self.mana -= self.costo_fuerte
        danio_efectuado = random.randint(self.danio_fuerte)
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

    def Accionar(self, decision):
        if decision == "ataque_comun":
            self.Ataque_Comun(self.enemigo)
        if decision == "ataque_fuerte":
            self.Ataque_Fuerte(self.enemigo)
        

propabilidad_100 = {
    "atacar": 40,
    "defender": 20,
    "esquivar": 30,
    "meditar": 10,
    "regenerar": 0,
    "fuerte": 50
}

probabilidad_60 = {
    "atacar": 30,
    "defender": 30,
    "esquivar": 10,
    "meditar": 15,
    "regenerar": 15,
    "fuerte": 30
}

probabilidad_40 = {
    "atacar": 15,
    "defender": 20,
    "esquivar": 20,
    "meditar": 15,
    "regenerar": 30,
    "fuerte": 90
}

class Sistema(Hechicero):
    def __init__(self, nombres_hechizos):
        super().__init__(nombres_hechizos)
    
    def Eleccion(self):
        if self.vida > 60:
            self.probabilidades = propabilidad_100
        elif self.vida <= 60 and self.vida > 40:
            self.probabilidades = probabilidad_60
        elif self.vida <= 40:
            self.probabilidades = probabilidad_40
        
        eleccion_bot = random.randint(1, 100)
        contador = 0
        
        for probabilidad in self.probabilidades.tems():
            contador += probabilidad[1]
            if eleccion_bot <= contador:
                self.decision = probabilidad[0]
                if self.decision == "atacar":
                    probabilidad_ataque = random.randint(1, 100)
                    if probabilidad_ataque <= self.probabilidades["fuerte"]:
                        self.decision = "ataque_fuerte"
                    else:
                        self.decision = "ataque_comun"
    
    def Decision(self):
        self.Eleccion()






class Jugador(Hechicero):
    def __init__(self, nombres_hechizos):
        super().__init__(nombres_hechizos)

    def Menu_Eleccion(self):
        print("que vas a hacer?")
        print("1- Ataquar")
        print(f"2- {self.nombres_hechizos["escudo"]} - {self.escudo_costo}m")
        print(f"3- {self.nombres_hechizos["regeneracion"]} - {self.regeneracion_costo}m")
        print(f"4- {self.nombres_hechizos["esquivar"]} - {self.prob_esquivar}%")
        print(f"5- {self.nombres_hechizos['meditacion']} + {self.meditacion_aumento}m")
        op = int(input("-- "))
        if op == 1:
            if not self.Seleccionar_Ataque():
                self.Menu_Eleccion()
            return
        if op == 2:
            self.mana -= self.escudo_costo
            self.decision = "protegerse"
        if op == 3:
            self.mana -= self.regeneracion_costo
            self.decision = "regenerarse"
        if op == 4:
            if self.decision != "esquivar":
                self.decision = "esquivar"
            else:
                self.Menu_Eleccion()
        if op == 5:
            self.mana += self.meditacion_aumento
            self.decision = "meditar"

    def Decidir(self):
        self.Menu_Eleccion()


