import random

import simpy

numeroProcesos = 25
tiempos = []
random.seed(10)


class CPU:
    def __init__(self):
        self.cpu = simpy.Resource(env, capacity=3)
        self.ram = simpy.Container(env, init=100, capacity=100)


def proceso(name, env, cpu, tiempoEspera):
    yield env.timeout(tiempoEspera)
    tiempoInicio = env.now
    memoriaUtilizar = random.randint(1, 10)
    cantidadProcesos = random.randint(1, 10)
    s = True

    while s:
        cantidad = cpu.ram.level
        if (memoriaUtilizar <= cantidad):
            s = False

    print(name, "entro se almaceno en memoria en", tiempoInicio)

    with cpu.cpu.request() as req:
        print(name, "inicio proceso en", env.now)
        yield req
        env.timeout(cantidadProcesos)
        print(name, "sale del CPU a las ", env.now)
    cpu.ram.put(memoriaUtilizar)
    tiempoProceso = env.now - tiempoInicio
    tiempos.append(tiempoProceso)
    print(name, "se tardo", tiempoProceso)


def generarProcesos(envv, cpu):
    for i in range(numeroProcesos):
        envv.process(proceso("proceso" + str(i), env, cpu, random.expovariate(1.0 / 10)))
        yield env.timeout(5)


env = simpy.Environment()
CPU = CPU()
env.process(generarProcesos(env, CPU))
env.run(35)

print(sum(tiempos) / numeroProcesos)
