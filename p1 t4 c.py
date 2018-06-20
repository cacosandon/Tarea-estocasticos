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
        
        #PARAMETROS
        self.capacidad = capacidad
        self.tiempo_actual = datetime(2018, 6, 15, 12, 0)
        self.tiempo_final = datetime(2018, 6, 18, 20, 0) #despues de 80 horas
        self.tarea_actual = None
        self.tiempo_revision = 0
        self.colaA = deque()
        self.colaB = deque()
        self.proxima_llegadaA = self.tiempo_actual + timedelta(minutes=int(uniform(2,10)))
        self.proxima_llegadaB = self.tiempo_actual + timedelta(minutes=int(expovariate(1/4)))
        self.proxima_atencionA = datetime(2018, 6, 18, 21, 0)
        self.proxima_atencionB = datetime(2018, 6, 18, 21, 0)
        self.clientesA = []
        self.clientesB = []
        self.minutos_sin_clientesS = 0
        self.ocupado = False
        
        #ESTADISTICAS
        self.clientes_atendidosA = 0
        self.max_tiempo_esperaA = 0
        self.demanda_perdidaA = 0

        self.clientes_atendidosB = 0
        self.max_tiempo_esperaB = 0
        self.demanda_perdidaB = 0

        self.tiempo_sin_clientesS = 0
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
                self.minutos_sin_clientesS = self.tiempo_actual
            elif (len(self.colaA) == 1 or len(self.colaB) == 1) and not self.ocupado:
                self.ocupado = True
                tiempo = self.tiempo_actual - self.minutos_sin_clientesS
                self.tiempo_sin_clientesS += divmod(tiempo.days * 86400 + tiempo.seconds, 60) [0]

            self.tiempo_actual = min(self.proxima_atencionA,self.proxima_atencionB, self.proxima_llegadaA, self.proxima_llegadaB)
            
            if self.tiempo_actual == self.proxima_llegadaA:
                    if (len(self.colaA) == self.capacidad + 1 and self.proxima_atencionA < datetime(2018, 6, 18, 21, 0))    or (len(self.colaA) == self.capacidad and self.proxima_atencionA == datetime(2018, 6, 18, 21, 0)):
                            self.demanda_perdidaA += 1
                            #print("Se fue A porque estaba lleno")
                    else:
                            cliente = Cliente(self.tiempo_actual)
                            self.clientesA.append(cliente)
                            self.colaA.append(cliente)
                            #print("Llego A")
                            if len(self.colaA) == 1 and not self.ocupado:
                                    self.proxima_atencionA = self.tiempo_actual + timedelta(minutes=int(uniform(1,3)))
                                    self.proxima_atencionB = datetime(2018, 6, 18, 21, 0)
                    self.proxima_llegadaA = self.tiempo_actual +  timedelta(minutes=int(uniform(2,10)))
                    
            elif self.tiempo_actual == self.proxima_llegadaB:
                    if (len(self.colaB) == self.capacidad + 1 and self.proxima_atencionB < datetime(2018, 6, 18, 21, 0)) or (len(self.colaB) == self.capacidad and self.proxima_atencionB == datetime(2018, 6, 18, 21, 0)):
                            self.demanda_perdidaB += 1
                            #print("Se fue B porque estaba lleno")
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

            
          
def estadisticas():
	print("\nSimulación 1\n")

	simulacion1 = Tele(5)
	simulacion1.run()

   
	print("Clientes atendidos de tipo A: ", simulacion1.clientes_atendidosA)
	print("Proporción de clientes perdidos de tipo A: {}%".format(simulacion1.demanda_perdidaA/(simulacion1.demanda_perdidaA+len(simulacion1.clientesA))))
	print("Maximo tiempo en sistema de tipo A: ", simulacion1.max_tiempo_esperaA,"minutos.")
	print("Tiempo promedio de clientes tipo A en el sistema: ", simulacion1.promedio_tiempo_en_sistemaA(),"minutos.")
	
	print("\n")
	
	print("Clientes atendidos de tipo B: ", simulacion1.clientes_atendidosB)
	print("Proporción de clientes perdidos de tipo B: {}%".format(simulacion1.demanda_perdidaB/(simulacion1.demanda_perdidaB+len(simulacion1.clientesB))))
	print("Maximo tiempo en sistema de tipo B: ", simulacion1.max_tiempo_esperaB,"minutos.")
	print("Tiempo promedio de clientes tipo B en el sistema: ", simulacion1.promedio_tiempo_en_sistemaB(),"minutos.\n")
	
	print("Probabilidad de que el sistema se quede vacio en el largo plazo: {}%\n".format(simulacion1.tiempo_sin_clientesS * 100/4800))

estadisticas()
