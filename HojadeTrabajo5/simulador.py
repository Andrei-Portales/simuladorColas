import random
import simpy

# variables dinamicas
cantidaddeProcesos = 5
numProcesos = 3
numRam = 100

# variables de simulador
random.seed(10)  # fijar el inicio de random
tiempototal = 0
env = simpy.Environment()
RAM = simpy.Container(env, init=numRam, capacity=numRam)
CPU = simpy.Resource(env, capacity=numProcesos)


# funcion que simula un proceso
def process(name, tiempoEspera, environment, cpu, ram):
    global tiempototal
    yield environment.timeout(tiempoEspera)
    tiempoInicio = environment.now
    memoriaUtilizar = random.randint(1, 10)
    ram.get(memoriaUtilizar)
    print(ram.level)
    cantidadProcesos = random.randint(1, 10)
    print(name, "se almaceno en la memoria en", tiempoInicio, "y tiene", cantidadProcesos, "procesos")

    with cpu.request() as turno:
        yield turno
        yield environment.timeout(cantidadProcesos)
        print(name, "sale del CPU a las ", environment.now)
    ram.put(memoriaUtilizar)
    tiempoProceso = env.now - tiempoInicio
    print(name, "se tardo", tiempoProceso)
    tiempototal += tiempoProceso


for i in range(cantidaddeProcesos):
    env.process(process("Proceso" + str(i + 1), random.expovariate(1.0/10), env, CPU, RAM))

env.run(until=cantidaddeProcesos*10)

print("\n\n\nTiempo promedio de ejecucion de", cantidaddeProcesos, "procesos: ", tiempototal / cantidaddeProcesos)