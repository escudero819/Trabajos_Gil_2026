class Cliente():
    def __init__(self, nombre, contrasena):
        self.nombre = nombre.capitalize()
        self._contrasena = contrasena
        self.capital = 0
    
    def Depositar(self, monto):
        self.capital += monto
    
    def Extraer(self, monto):
        self.capital -= monto
    
    def MostrarCapital(self):
        print("capital del cliente:", self.capital)

class Banco():

    def __init__(self):
        self.lista_clientes = []
        for i in range(3):
            nombre = input("ingrese el nombre: ")
            contrasena = input("ingrese contrasena: ")
            cliente = Cliente(nombre, contrasena)
            self.lista_clientes.append(cliente)
    
    def Operar(self, cliente: Cliente):
        print("Que desea realizar?")
        print("1- Depositar")
        print("2- Extraer")
        print("3- Ver Capital")
        print("4- Salir")
        op = int(input("-- "))
        while op != 4:
            if op == 1:
                print("cuanto va a depositar?")
                monto = int(input("-- "))
                cliente.Depositar(monto)
            if op == 2:
                print("Cuanto va a extraer?")
                monto = int(input("--"))
                if cliente.capital - monto < 0:
                    print("no tiene suficiente capital")
                else:
                    cliente.Extraer(monto)
            if op == 3:
                cliente.MostrarCapital()
                print("Que desea realizar?")
            print("1- Depositar")
            print("2- Extraer")
            print("3- Ver Capital")
            print("4- Salir")
            op = int(input("-- "))

    def Ingresar(self):
        print("nombre de la cuenta")
        nombre_cuenta = input("--").capitalize()
        for cuenta in self.lista_clientes:
            if cuenta.nombre == nombre_cuenta:
                cliente = cuenta
        if cliente:
            print("ingrese la contrasena")
            contrasena = input("-- ")
            if cliente._contrasena == contrasena:
                self.Operar(cliente)
            else:
                print("contrasena incorrecta")
        else:
            print("usuario no encontrado")

    def Deposito_total(self):
        total = 0
        for cliente in self.lista_clientes:
            total += cliente.capital
        print("el Deposito total es de:", total)

    def iniciar(self):
        print("-"*10)
        print("MENU")
        print("1- ingresar")
        print("2- total depositado en el banco")
        print("3- salir")
        op = int(input("--"))
        while op != 3:
            if op == 1:
                self.Ingresar()
            if op == 2:
                self.Deposito_total()
            print("-"*10)
            print("MENU")
            print("1- ingresar")
            print("2- total depositado en el banco")
            print("3- salir")
            op = int(input("--"))

banco = Banco()
banco.iniciar()