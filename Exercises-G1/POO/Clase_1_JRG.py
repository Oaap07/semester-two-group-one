
class Jugador_voley:
    def __init__(self):
        self.nombre = ""  #  Valores str
        self.altura = 0  #  Valores del 100 cm a 250 cm
        self.fuerza = 0  #  Valores del 1 al 10
        self.velocidad = 0  #  Valores del 1 al 10
    
    def crear_jugador(self):
        self.nombre = input("Ingrese el nombre del jugador: ")
        self.altura = int(input("Ingrese la altura: "))
        self.fuerza = int(input("Ingrese la fuerza: "))
        self.velocidad = int(input("Ingrese la velocidad: "))

    def rematar(self):
        self.remate = (self.fuerza * self.velocidad) + 50
        print(f"El jugador {self.nombre} realizó un remate a {self.remate} km/h")
    def saltar(self):
        self.salto = round(self.altura + self.fuerza/15 + self.velocidad/15, 2)
        print(f"El jugador {self.nombre} alcanzó un a altura de {self.salto} cm")
    def saque(self):
        self.presicion = round((self.fuerza + self.velocidad)*0.5, 0)
        print(f"El jugador {self.nombre} hizo un saqué a una velocidad de {(self.remate)-5} km/h")
    

class Asiatico(Jugador_voley):
    def __init__(self):
        super().__init__()
        self.velocidad += 1
        self.fuerza -= 1
        self.altura -= 0.10

class Latino(Jugador_voley):
    def __init__(self):
        super().__init__()
        self.velocidad -= 1
        self.fuerza += 2
        self.altura += 0.10

    def stats(self):
        print(f"Jugador [{self.nombre}]\n- Altura: {self.altura}\n- Fuerza: {self.fuerza}\n- Velocidad: {self.velocidad}")

jugador_1 = Latino()
jugador_1.crear_jugador()
jugador_1.rematar()
jugador_1.saltar()
jugador_1.saque()
jugador_1.stats()