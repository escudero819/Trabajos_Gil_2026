class Contacto():
    def __init__(self, nombre, telefono, email):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def __str__(self):
        return f"Nombre: {self.nombre}, Telefono: {self.telefono}, Email: {self.email}"

class Agenda():
    def __init__(self):
        self.contactos = []

    def agregar_contacto(self, contacto):
        self.contactos.append(contacto)

    def mostrar_contactos(self):
        for contacto in self.contactos:
            print(contacto)

    def buscar_contacto(self, nombre):
        for contacto in self.contactos:
            if contacto.nombre == nombre:
                print(contacto)
                return
        print("Contacto no encontrado")

    def eliminar_contacto(self, nombre):
        for contacto in self.contactos:
            if contacto.nombre == nombre:
                self.contactos.remove(contacto)
                print("Contacto eliminado")
                return
        print("Contacto no encontrado")

    def modificar_contacto(self, nombre, telefono, email):
        for contacto in self.contactos:
            if contacto.nombre == nombre:
                contacto.telefono = telefono
                contacto.email = email
                print("Contacto modificado")
                return
        print("Contacto no encontrado")

    def menu(self):
        while True:
            print("\n1. Agregar contacto")
            print("2. Mostrar contactos")
            print("3. Buscar contacto")
            print("4. Eliminar contacto")
            print("5. Modificar contacto")
            print("6. Salir")
            opcion = int(input("Seleccione una opcion: "))
            if opcion == 1:
                nombre = input("Ingrese el nombre: ")
                telefono = input("Ingrese el telefono: ")
                email = input("Ingrese el email: ")
                self.agregar_contacto(Contacto(nombre, telefono, email))
            elif opcion == 2:
                self.mostrar_contactos()
            elif opcion == 3:
                nombre = input("Ingrese el nombre: ")
                self.buscar_contacto(nombre)
            elif opcion == 4:
                nombre = input("Ingrese el nombre: ")
                self.eliminar_contacto(nombre)
            elif opcion == 5:
                nombre = input("Ingrese el nombre: ")
                telefono = input("Ingrese el telefono: ")
                email = input("Ingrese el email: ")
                self.modificar_contacto(nombre, telefono, email)
            elif opcion == 6:
                break
            else:
                print("Opcion no valida")

agenda = Agenda()
agenda.menu()
