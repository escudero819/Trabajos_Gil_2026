class Triangulo():
    def __init__(self, *kwargs):
        self.lados = [*kwargs]
    
    def MostrarMayor(self):
        mayor = 0
        for indice in range(len(self.lados)):
            if self.lados[indice] > mayor:
                mayor = self.lados[indice]
                indice_mayor = indice
        print("el lado mas grande es el lado:", indice_mayor + 1, "con", self.lados[indice_mayor], "cm")

    def MostrarTipo(self):
        coincidencias = 0
        if self.lados[0] == self.lados[1] and self.lados[1] == self.lados[2] and self.lados[2] == self.lados[0]:
            print("equilatero")
        elif self.lados[0] == self.lados[1] or self.lados[1] == self.lados[2] or self.lados[2] == self.lados[0]:
            print("isoseles")
        else:
            print("escaleno")
            
print("ingrese lado 1:")
l1 = int(input("--"))
print("ingrese lado 2:")
l2 = int(input("--"))
print("ingrese lado 3:")
l3 = int(input("--"))
triangulo = Triangulo(l1, l2, l3)
triangulo.MostrarMayor()
triangulo.MostrarTipo()