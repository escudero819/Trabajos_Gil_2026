
class Alumno():
    nota_aprovatoria = 7
    def __init__(self, nombre, nota):
        self.nombre = nombre
        self.nota = nota
    
    def MostrarAtributos(self):
        print(f"Alumno: {self.nombre} - ha sacado: {self.nota}")
    
    def Aprobado(self):
        if self.nota >= self.nota_aprovatoria:
            print("saco:",self.nota," Ha aprovado")
        else:
            print("saco:",self.nota," No ha aprovado")
print("ingrese el nombre del alumno")
nombre_alumno = input("--")
print("ingrese la nota:")
nota_alumno = int(input("--"))
alumno = Alumno(nombre_alumno, nota_alumno)
alumno.MostrarAtributos()
alumno.Aprobado()