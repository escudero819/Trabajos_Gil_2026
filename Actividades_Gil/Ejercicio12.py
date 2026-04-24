from Ejercicio12_objects import Recursos_no_Usables, Recursos_Usables, Recursos_Unicos
import random

class Inventario():
    """
    CASE INVENTARIO: manejara los objetos que tenga el jugador, la interaccion con ellos y su descarte
    """
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
        if not self.jugador.ambiente.Agregar_objeto_balsa(objeto):
            print("el objeto se lo lleva el mar")
            self.jugador.ambiente.Agregar_objeto_agua(objeto)

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
    """
    CLASE DE DECISIONES; sera la parte interactiva del juego con el entorno y con si mismo. Avisara a la clase partida cuando deba morir.
    y que decide hacer con los objetos que encuentra.
    """
    def __init__(self, ambiente):
        self.vida = 100
        self.sed = 100
        self.hambre = 100
        self.inventario = Inventario(self, 10)
        self.ambiente = ambiente # referencia al entorno en el que se encuentra el jugador
    
    def Aumentar_inventario(self):
        self.inventario.cantidad_maxima += 1
        print(f"ahora tienes {self.inventario.cantidad_maxima} espacios en el inventario")
    
    def Aumentar_vida(self, vida_aumentar):
        self.vida += vida_aumentar
        if self.vida > 100:
            self.vida = 100
    
    def Aumentar_sed(self, sed_aumentar):
        self.sed += sed_aumentar
        if self.sed > 100:
            self.sed = 100
    
    def Aumentar_hambre(self, hambre_aumentar):
        self.hambre += hambre_aumentar
        if self.hambre > 100:
            self.hambre = 100
    
    def Mostrar_estado(self):
        print("vida:", self.vida)
        print("sed:", self.sed)
        print("hambre:", self.hambre)
    
    def Mostrar_inventario(self):
        self.inventario.Lista()
    
    def Timelapse(self):
        # es el precio de hacer cualquier accion, es para simular el paso del tiempo
        # debido a que no hay un bucle principal que controle el tiempo y el jugador puede hacer lo que quiera 
        # ademas el programa cada vez que actualice el entorno se ejecutara este metodo
        self.sed -= 1
        self.hambre -= 1
        if self.sed <= 0 or self.hambre <= 0:
            self.vida = 0
        elif self.sed <= 30 or self.hambre <= 30:
            self.vida -= 10
        elif self.sed <= 60 or self.hambre <= 60:
            self.vida -= 5
        self.ambiente.Actualizar()
    
    def Inspeccionar_Objeto(self, objeto):
        print("nombre: ", objeto.nombre)
        print("cantidad: ", objeto.cantidad)
        print("descripcion: ", objeto.descripcion)
        if isinstance(objeto, type(Recursos_Unicos.Barril())):
            print("enter para abrir el barril")
            input()
            objeto.Abrir(self)
            return False
        else:
            print("lo quieres guardar? (si/no)")
            eleccion = input()
            if eleccion == "si":
                self.inventario.Guardar(objeto)
                return True # esto sera para avisar si hay que sacarlo del suelo
            else:
                return False

    def Tiburon(self):
        if random.randint(1, 100) <= self.ambiente.prob_tiburon:
            print("un tiburon te ataca")
            self.vida -= 10
            self.ambiente.prob_tiburon = 0
        else:
            self.ambiente.prob_tiburon += self.ambiente.prob_tiburon * 1.5
            if self.ambiente.prob_tiburon > 50:
                self.ambiente.prob_tiburon = 50

    def Buscar_objeto_agua(self, distancia, objeto, indice):
        paso = 1
        while paso < distancia:
            self.Tiburon()
            print("paso", paso, "de", distancia)
            eleccion = input("quieres seguir? (si/no)")
            if eleccion == "no":
                print("vuelves a la balsa")
                return
            paso += 1
        if self.Inspeccionar_Objeto(objeto):
            self.ambiente.Remover_objeto_agua(indice)
        print("vuelves a la balsa")

    def Inspeccionar_Agua(self, lista_objetos_agua):
        for i in range(len(lista_objetos_agua)):
            objeto = lista_objetos_agua[i]
            if objeto["distancia"] <= 5:
                print("logras reconocer un objeto cercano, es un/a:", objeto["objeto"].nombre)
                if self.ambiente.caña_pescar:
                    print("con la caña puedes alcanzarlo!")
                    print("lo quieres alcanzar? (si/no)")
                    eleccion = input()
                    if eleccion == "si":
                        self.Inspeccionar_Objeto(objeto["objeto"])
                        return True # esto sera para avisar si hay que sacarlo del suelo
                    else:
                        return False # no se saca del suelo
                else:
                    print("no puedes alcanzarlo")
                    print("quieres meterte al agua a buscarlo? (si/no)")
                    eleccion = input()
                    if eleccion == "si":
                        print(lista_objetos_agua)
                        print(i)
                        self.Buscar_objeto_agua(objeto["distancia"], objeto["objeto"], i)
            else:
                print("no logras reconocer bien el objeto")
                if objeto["distancia"] <= 10:
                    print("puedes acercarte a inspeccionarlo mejor")
                    print("quieres acercarte? (si/no)")
                    eleccion = input()
                    if eleccion == "si":
                        self.Buscar_objeto_agua(objeto["distancia"], objeto["objeto"], i)
            
            print("quieres seguir viendo el agua? (si/no)")
            eleccion = input()
            if eleccion == "no":
                return

    def Inspeccionar_Balsa(self, lista_objetos_balsa):
        if len(lista_objetos_balsa) == 0:
            print("no hay objetos en la balsa")
            return
        for i in range(len(lista_objetos_balsa)):
            objeto = lista_objetos_balsa[i]
            print("en la balsa hay un/a:", objeto["nombre"])
            print("quieres inspeccionarlo? (si/no)")
            eleccion = input()
            if eleccion == "si":
                if self.Inspeccionar_Objeto(objeto):
                    self.ambiente.Remover_objeto_balsa(i)
            print("quieres seguir viendo la balsa? (si/no)")
            eleccion = input()
            if eleccion == "no":
                return

    def Decisiones(self):
        lista_objetos_agua = self.ambiente.Buscar_agua() # son todos los objetos flotantes, tanto barriles como botellas y otros
        lista_objetos_balsa = self.ambiente.Buscar_balsa() # son todos los objetos en la balsa, tanto palos como piedras y otros

        print("que quieres hacer? ")
        print("1- Inspeccionar el agua")
        print("2- Inspeccionar la balsa")
        print("3- Inspeccionar el inventario")
        print("4- Salir")
        eleccion = input("-- ")
        if eleccion == "1":
            self.Inspeccionar_Agua(lista_objetos_agua)
        elif eleccion == "2":
            self.Inspeccionar_Balsa(lista_objetos_balsa)
        elif eleccion == "3":
            self.Mostrar_inventario()
        elif eleccion == "4":
            return
        else:
            print("opcion no valida")
            self.Decisiones()


class Ambiente():
    def __init__(self):
        self.objetos_agua = []
        self.objetos_balsa = []
        self.prob_tiburon = 10
        self.caña_pescar = False
    
    def Actualizar(self):
        print("el entorno se actualiza")
        cant_nuevos_objetos = random.randint(1, 5)
        for i in range(cant_nuevos_objetos):
            probabilidad = random.randint(1, 100)
            if probabilidad <= 30:
                objeto_nuevo = Recursos_Unicos.Barril()
            elif probabilidad <= 65:
                objeto_nuevo = Recursos_no_Usables.Palo()
            elif probabilidad <= 100:
                objeto_nuevo = Recursos_no_Usables.Piedra()
            self.objetos_agua.append({ "objeto": objeto_nuevo, "distancia": random.randint(1, 10)})
        
    def Buscar_agua(self):
        return self.objetos_agua
    
    def Buscar_balsa(self):
        return self.objetos_balsa
    
    def Remover_objeto_agua(self, indice):
        self.objetos_agua.pop(indice)
    
    def Remover_objeto_balsa(self, indice):
        self.objetos_balsa.pop(indice)
    
    def Agregar_objeto_balsa(self, objeto):
        if len(self.objetos_balsa) < 5:
            self.objetos_balsa.append(objeto)
            return True
        else:
            print("la balsa esta llena, no puedes agregar mas objetos")
            return False
    
    def Agregar_objeto_agua(self, objeto):
        self.objetos_agua.append({ "objeto": objeto, "distancia": random.randint(1, 5)})

class Partida():
    def __init__(self):
        self.ambiente = Ambiente()
        self.jugador = Jugador(self.ambiente)
    
    def Jugar(self):
        while True:
            print("\n")
            print("-"*20)
            self.jugador.Timelapse()
            self.jugador.Mostrar_estado()
            self.jugador.Decisiones()
            if self.jugador.vida <= 0:
                print("game over")
                break

partida = Partida()
partida.Jugar()