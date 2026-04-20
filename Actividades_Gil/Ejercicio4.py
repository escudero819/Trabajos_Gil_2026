class Calculadora():
    def __init__(self):
        num1 = int(input("numero 1:"))
        num2 = int(input("numero 2:"))
        if num1 > num2:
            self.num1 = num1
            self.num2 = num2
        else:
            self.num1 = num2
            self.num2 = num1
        print("mayor:", self.num1)
        print("menor:", self.num2)
    
    def Suma(self):
        print(self.num1 + self.num2)
    
    def Resta(self):
        print(self.num1 - self.num2)
    
    def Multiplicacion(self):
        print(self.num1 * self.num2)
    
    def Division(self):
        print(self.num1 / self.num2)


calcu = Calculadora()
calcu.Suma()
calcu.Resta()
calcu.Multiplicacion()
calcu.Division()