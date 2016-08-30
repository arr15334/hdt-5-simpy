import simpy
import random
import math

# simula el funcionamiento de un sistema operativo

# name: identificacion del programa
# cpu:  cargador de bateria
# arrival_time: tiempo en el que llega cada proceso, es aleatorio
# tiempo_cpu: tiempo que toma hacer un proceso

def proceso(env, name, cpu, arrival_time, tiempo_cpu):
    global tiempoCargaTotal
    global lista_tiempos
    velocidad_cpu = 3
    yield env.timeout(arrival_time) #simula llegada aleatoria de procesos
    llegada = env.now #registrar hora llegada a ready
    # new proceso, debe esperar a que haya memoria ram
    ocupacionRam = random.randint(1,10)
    with ram.get(ocupacionRam) as req:  #pedimos crear un nuevo proceso
        yield req
        #print('%s pide a %s' % (name, env.now))
        yield env.timeout(tiempo_cpu)
        #print('%s se crea at %s' % (name, env.now))
    
    #estado ready, esperar a que lo atienda el cpu
    operaciones = random.randint(1,10)
    while operaciones > 0:      
      with cpu.request() as req:  #pedimos conectarnos al cpu
          yield req
          #print('%s proceso inicia a %s' % (name, env.now))
          yield env.timeout(tiempo_cpu)
          operaciones = operaciones - velocidad_cpu
          #print('%s leaving the bcs at %s' % (name, env.now))
          # se sale del cpu
      entra_io = random.randint(1,2)
      if entra_io == 1:
        with io.request() as req:
          yield req
          yield env.timeout(1)
          #print ('%s sale de io at %s'%(name, env.now))

    ram.put(ocupacionRam) #terminated, devuelve lo utilizado
    
    tiempoCarga = env.now - llegada
    lista_tiempos.append(tiempoCarga)
    #print('%s tiempo total espera + carga %s' % (name, tiempoCarga))
    tiempoCargaTotal = tiempoCargaTotal + tiempoCarga
    
#
env = simpy.Environment()  #crear ambiente de simulacion
memoriaRam = 100
cpu = simpy.Resource(env, capacity=1) #solo hay un cpu
ram = simpy.Container(env, init=memoriaRam, capacity=memoriaRam) #capacidad de memoria es 100
io = simpy.Resource(env, capacity=1) #espacio para i/o
tiempoCargaTotal = 0.0
nprocesos = 100 #numero de procesos
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
interval = 10
lista_tiempos=[]
# crear los procesos
for i in range(nprocesos):
    t = random.expovariate(1.0 / interval)
    env.process(proceso(env, 'Proceso %d' % i, cpu, t, 1))
# correr la simulacion
env.run()
#calcular promedio
promedio = tiempoCargaTotal/nprocesos
#calcular dev estandar
var = 0
for i in range(nprocesos):
    temp = (promedio-lista_tiempos[i])*(promedio-lista_tiempos[i])
    var = var + temp
varianza = var/nprocesos
devstand = math.sqrt(varianza)
#imprimir resultados finales
print ('La desviacion estandar es %f' %devstand)
print ('En promedio se tardan %d' %promedio)
print ('Tiempo total %d' %tiempoCargaTotal)
