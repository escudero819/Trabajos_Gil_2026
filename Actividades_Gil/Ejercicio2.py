class Persona():
    mayoria_edad = 18
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
    
    def Mostrar(self):
        if self.edad >= self.mayoria_edad:
            print(f"{self.nombre} es mayor de edad con {self.edad} años")
        else:
            print(f"{self.nombre} no es mayor de edad, tiene {self.edad} años")

print("ingrese el nombre:")
nombre_persona = input("--")
print("ingrese la edad:")
edad_persona = int(input("--"))
persona = Persona(nombre_persona, edad_persona)
persona.Mostrar()