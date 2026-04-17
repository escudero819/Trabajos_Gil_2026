import random, colorama

ataque_global = 15
defensa_global = 7

class Personaje():

    def __init__(self, nombre):
        self.name = nombre
        self.vida = 100
        self.danio = ataque_global
        self.defensa = defensa_global
        self.estado = "comienzo"
    
    def Atacar(self, objetivo):
        if objetivo.estado == "mareado":
            objetivo.vida -= self.danio
            print(objetivo.name, "recibio un golpe critico!!!")
            objetivo.estado = "normal"
        else:
            if objetivo.estado == "atacando":
                objetivo.vida -= self.danio - objetivo.defensa
                print("danio mutuo")
            elif objetivo.estado == "esquivando":
                self.estado = "mareado"
                print(objetivo.name, "esquivo el ataque")
                print(self.name, "esta mareado!")
            elif objetivo.estado == "defendiendo":
                print(objetivo.name, "repelio el ataque")
            
    

class Jugador(Personaje):

    def __init__(self, nombre):
        super().__init__(nombre)   

    def Decidir(self):
        if self.estado != "mareado":
            print("Tu turno")
            print("1- Atacar")
            print("2- Defender")
            print("3- Esquivar")
            op = int(input("-- "))
            if op == 1:
                self.estado = "atacando"
            if op == 2:
                self.estado = "defendiendo"
            if op == 3:
                if self.estado == "esquivando":
                    print("no puede esquivar 2 veces seguidas")
                    print("1- Atacar")
                    print("2- Defender")
                    op = int(input("-- "))
                    if op == 1:
                        self.estado = "atacando"
                    else:
                        self.estado = "defendiendo"
                else:
                    self.estado = "esquivando"
        else:
            input("estas mareado, estad a merced del enemigo!")
    
class Sistema(Personaje):

    def __init__(self, nombre):
        super().__init__(nombre)
    
    def Decidir(self):
        if self.estado != "mareado":
            op = random.randint(1, 3)
            if op == 1:
                self.estado = "atacando"
            if op == 2:
                self.estado = "defendiendo"
            if op == 3:
                if self.estado == "esquivando":
                    op = random.randint(1,2)
                    if op == 1:
                        self.estado = "atacando"
                    else:
                        self.estado = "defendiendo"
                else:
                    self.estado = "esquivando"

def Juego():
    nombre = input("ingrese su nombre: ")
    jugador = Jugador(nombre)
    bot = Sistema("orco")
    while jugador.vida > 0 and bot.vida > 0:
        print(colorama.Fore.CYAN + "-"*20, colorama.Fore.WHITE)
        jugador.Decidir()
        bot.Decidir()

        if bot.estado == "atacando":
            bot.Atacar(jugador)
        elif bot.estado == "defendiendo":
            print(bot.name, "decidio defenderse")
        elif bot.estado == "esquivando":
            print(bot.name, "hizo una maniobra de esquive")
        
        if jugador.estado == "atacando":
            jugador.Atacar(bot)
        
        print(f"| {jugador.name}: {jugador.vida}HP")
        print(f"| {bot.name}: {bot.vida}HP")
    if jugador.vida <= 0:
        print(colorama.Fore.LIGHTMAGENTA_EX + "GAME OVER")
    else:
        print(colorama.Fore.LIGHTGREEN_EX + "VICTORY!!!!")

Juego()