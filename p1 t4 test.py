from random import *
from collections import deque
from datetime import *

class Cliente:
    ID=0
    def __init__(self, hora_actual):
        self.hora_llegada = hora_actual
        self.hora_salida = False
        self.id = Cliente.ID
        Cliente.ID += 1
        
class Tele:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.tiempo_actual = datetime(2018, 6, 15, 12, 0)
        self.tiempo_final = datetime(2018, 6, 18, 20, 0) #dps de 80hroas
        self.tarea_actual = None
        self.tiempo_revision = 0
        self.colaA = deque()
        self.colaB = deque()
        self.proxima_llegadaA = self.tiempo_actual + timedelta(minutes=int(expovariate(1/6)))
        self.proxima_llegadaB = self.tiempo_actual + timedelta(minutes=int(expovariate(1/4)))
        self.proxima_atencionA = datetime(2018, 6, 18, 21, 0)
        self.proxima_atencionB = datetime(2018, 6, 18, 21, 0)
        self.clientesA = []
        self.clientesB = []
        self.minutos_sin_clientesA = 0
        self.minutos_sin_clientesB = 0
        self.ocupado = False

        #estadisticas
        self.clientes_atendidosA = 0
        self.max_tiempo_esperaA = 0
        self.demanda_perdidaA = 0
        self.tiempo_sin_clientesA = 0
        self.clientes_atendidosB = 0
        self.max_tiempo_esperaB = 0
        self.demanda_perdidaB = 0
        self.tiempo_sin_clientesB = 0

        self.printeo = ""




    def promedio_tiempo_en_sistemaA(self):
            suma = 0
            for cliente in self.clientesA:
                    if not cliente.hora_salida:
                            cliente.hora_salida = self.tiempo_actual
                    espera = cliente.hora_salida - cliente.hora_llegada
                    suma += divmod(espera.days * 86400 + espera.seconds, 60)[0]
            return suma / len(self.clientesA)
    def promedio_tiempo_en_sistemaB(self):
            suma = 0
            for cliente in self.clientesB:
                    if not cliente.hora_salida:
                            cliente.hora_salida = self.tiempo_actual
                    espera = cliente.hora_salida - cliente.hora_llegada
                    suma += divmod(espera.days * 86400 + espera.seconds, 60)[0]
            return suma / len(self.clientesB)


    def run(self):
        while self.tiempo_actual < self.tiempo_final:
            if len(self.colaA) == 0:
                self.proxima_atencionA = datetime(2018, 6, 18, 21, 0)
            if len(self.colaB) == 0:
                self.proxima_atencionB = datetime(2018, 6, 18, 21, 0)
            if len(self.colaA) == 0 and len(self.colaB) == 0:
                self.ocupado = False
                self.minutos_sin_clientesA = self.tiempo_actual
                self.minutos_sin_clientesB = self.tiempo_actual
            elif (len(self.colaA) == 1 or len(self.colaB) == 1) and not self.ocupado:
                if len(self.colaA) == 1:
                        self.ocupado = True
                        tiempo = self.tiempo_actual - self.minutos_sin_clientesA
                        
                        self.tiempo_sin_clientesA += divmod(tiempo.days * 86400 + tiempo.seconds, 60) [0]
                elif len(self.colaB) == 1:
                        self.ocupado = True
                        tiempo = self.tiempo_actual - self.minutos_sin_clientesB
                        self.tiempo_sin_clientesB += divmod(tiempo.days * 86400 + tiempo.seconds, 60) [0]

            self.tiempo_actual = min(self.proxima_atencionA,self.proxima_atencionB, self.proxima_llegadaA, self.proxima_llegadaB)
            
            if self.tiempo_actual == self.proxima_llegadaA:
                    if (len(self.colaA) == self.capacidad + 1 and self.proxima_atencionA < datetime(2018, 6, 18, 21, 0)) or (len(self.colaA) == self.capacidad and self.proxima_atencionA == datetime(2018, 6, 18, 21, 0)):
                            #print("esta lleno de A")
                            self.demanda_perdidaA += 1
                    else:
                            cliente = Cliente(self.tiempo_actual)
                            self.clientesA.append(cliente)
                            self.colaA.append(cliente)
                            #print("Llego A")
                            if len(self.colaA) == 1 and not self.ocupado:
                                    self.proxima_atencionA = self.tiempo_actual + timedelta(minutes=int(uniform(1,3)))
                                    self.proxima_atencionB = datetime(2018, 6, 18, 21, 0)
                    self.proxima_llegadaA = self.tiempo_actual +  timedelta(minutes=int(expovariate(1/6)))
                    
            elif self.tiempo_actual == self.proxima_llegadaB:
                    if (len(self.colaB) == self.capacidad + 1 and self.proxima_atencionB < datetime(2018, 6, 18, 21, 0)) or (len(self.colaB) == self.capacidad and self.proxima_atencionB == datetime(2018, 6, 18, 21, 0)):
                            #print("esta lleno de B")
                            self.demanda_perdidaB += 1
                    else:
                            cliente = Cliente(self.tiempo_actual)
                            self.clientesB.append(cliente)
                            self.colaB.append(cliente)
                            #print("Llego B")
                            if len(self.colaB) == 1 and not self.ocupado:
                                    self.proxima_atencionB = self.tiempo_actual + timedelta(minutes=int(uniform(1/2,3/2)))
                                    self.proxima_atencionA = datetime(2018, 6, 18, 21, 0)
                    self.proxima_llegadaB = self.tiempo_actual +  timedelta(minutes=int(expovariate(1/4)))
                            

                    

            
            elif self.tiempo_actual == self.proxima_atencionA:
                    cliente = self.colaA.popleft()
                    cliente.hora_salida = self.tiempo_actual
                    #print("se atendio A")
                    self.clientes_atendidosA += 1
                    espera = self.tiempo_actual - cliente.hora_llegada
                    if divmod(espera.days * 86400 + espera.seconds, 60) [0] > self.max_tiempo_esperaA:
                            self.max_tiempo_esperaA = divmod(espera.days * 86400 + espera.seconds, 60) [0]
                    if len(self.colaA) > 0:
                            self.proxima_atencionA = self.tiempo_actual + timedelta(minutes=int(uniform(1,3)))
                            self.proxima_atencionB = datetime(2018, 6, 18, 21, 0)
                    elif len(self.colaA) == 0 and len(self.colaB) > 0:
                            self.proxima_atencionB = self.tiempo_actual + timedelta(minutes=int(uniform(1/2,3/2)))
                            self.proxima_atencionA = datetime(2018, 6, 18, 21, 0)
                    

            elif self.tiempo_actual == self.proxima_atencionB:
                    cliente = self.colaB.popleft()
                    cliente.hora_salida = self.tiempo_actual
                    #print("se atendio B")
                    self.clientes_atendidosB += 1
                    espera = self.tiempo_actual - cliente.hora_llegada
                    if divmod(espera.days * 86400 + espera.seconds, 60) [0] > self.max_tiempo_esperaB:
                            self.max_tiempo_esperaB = divmod(espera.days * 86400 + espera.seconds, 60) [0]
                    if len(self.colaA) > 0:
                            self.proxima_atencionA = self.tiempo_actual + timedelta(minutes=int(uniform(1,3)))
                            self.proxima_atencionB = datetime(2018, 6, 18, 21, 0)
                    elif len(self.colaA) == 0 and len(self.colaB) > 0:
                            self.proxima_atencionB = self.tiempo_actual + timedelta(minutes=int(uniform(1/2,3/2)))
                            self.proxima_atencionA = datetime(2018, 6, 18, 21, 0)

            #print(self.proxima_llegadaA,self.proxima_llegadaB)
          
def estadisticas():
	print("\nSimulación 1\n")

	simulacion1 = Tele(5)
	simulacion1.run()

	print("Cliente atendidos de tipo A: ", simulacion1.clientes_atendidosA)
	print("Clientes perdidos de tipo A: ", simulacion1.demanda_perdidaA)
	print("Maxima espera de tipo A: ", simulacion1.max_tiempo_esperaA)
	print("Promedio en sistema: ", simulacion1.promedio_tiempo_en_sistemaA())
	print("Tiempo sin clientes: {}%\n".format(simulacion1.tiempo_sin_clientesA * 100/4800))
	print("Cliente atendidos de tipo B: ", simulacion1.clientes_atendidosB)
	print("Clientes perdidos de tipo B: ", simulacion1.demanda_perdidaB)
	print("Maxima espera de tipo B: ", simulacion1.max_tiempo_esperaB)
	print("Promedio en sistema: ", simulacion1.promedio_tiempo_en_sistemaB())
	print("Tiempo sin clientes: {}%\n".format(simulacion1.tiempo_sin_clientesB * 100/4800))

estadisticas()
