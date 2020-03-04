import random
import simpy
import statistics
import matplotlib.pyplot as plt

# 25 procesos, luego con 50 procesos, con 100, 150 y 200

procesosEjecutar = [25,50,100,150,200]
tiempoTotales = []

for proceso in procesosEjecutar:
    
    for _ in range(10):
        print("")
    
    # variables dinamicas
    cantidaddeProcesos = proceso
    numProcesos = 3
    numRam = 100

    # variables de simulador
    tiempos = []
    random.seed(10)  # fijar el inicio de random

    env = simpy.Environment()
    RAM = simpy.Container(env, init=numRam, capacity=numRam)
    CPU = simpy.Resource(env, capacity=numProcesos)
    CPU2 = simpy.Resource(env, capacity=numProcesos)


    # funcion que simula un proceso
    def process(name, tiempoEspera, environment, cpu, ram):
        global tiempototal
        yield environment.timeout(tiempoEspera)
        tiempoInicio = environment.now
        memoriaUtilizar = random.randint(1, 10)
        if (memoriaUtilizar > ram.level):
             yield environment.timeout(5)
        ram.get(memoriaUtilizar)
        cantidadProcesos = random.randint(1, 10)
        print(name, "se almaceno en la memoria en", tiempoInicio, "y tiene", cantidadProcesos, "procesos")

        with cpu.request() as turno:
            yield turno
            yield environment.timeout(cantidadProcesos)
            print(name, "sale del CPU a las ", environment.now)
        ram.put(memoriaUtilizar)
        tiempoProceso = env.now - tiempoInicio
        tiempos.append(tiempoProceso)
        print(name, "se tardo", tiempoProceso)

#     jj = abs(int ((proceso / 2)) - proceso / 2)
#     
#     j1 = 0
#     j2 = 0
#     
#     if jj > 0:
#         j1 = abs((proceso / 2) + 0.5)
#         j2 = abs(proceso - j1)
#     else:
#         j1 = abs(proceso / 2)
#         j2 = abs(proceso - j1)
#     
    
    for i in range(proceso):
        env.process(process("Proceso" + str(i + 1) + "-1", random.expovariate(1.0 / 10), env, CPU, RAM))
    #for ii in range(int(j2)):
        #env.process(process("Proceso" + str(ii + 1) + "-2", random.expovariate(1.0 / 10), env, CPU2, RAM))
        
    
        

    env.run(until=cantidaddeProcesos * 10)

    print("\n\n\nTiempo promedio de ejecucion de", cantidaddeProcesos, "procesos: ", sum(tiempos) / cantidaddeProcesos)
    print("La desviacion estandar es de:", statistics.stdev(tiempos))
    tiempoTotales.append(sum(tiempos) / cantidaddeProcesos)


def grafica(x,y):
    plt.plot(x,y)
    plt.xlabel('Numero de Procesos')
    plt.ylabel('Tiempo Promedio')
    plt.title('Graficas de Simulador de Procesos')
    plt.show()
    
grafica(procesosEjecutar, tiempoTotales)