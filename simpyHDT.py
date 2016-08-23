import simpy
import random
#
# el carro se conduce un tiempo y tiene que llegar a cargarse de energia
# luego puede continuar conduciendo
# Debe hacer cola (FIFO) en el cargador

# name: identificacion del programa
# cpu:  cargador de bateria
# driving_time: tiempo que conduce antes de necesitar carga
# charge_duration: tiempo que toma cargar la bateria

def proceso(env, name, cpu, driving_time, charge_duration):
    global tiempoCargaTotal
    #global memoriaRam
    # Simulate driving to the BCS
    yield env.timeout(driving_time)

    # new proceso, debe esperar a que haya memoria ram
    ocupacionRam = random.randint(1,10)
    if ram.level > ocupacionRam:
        print('%s se crea a %s' % (name, env.now))
        ram.get(ocupacionRam)
        print('%s ready at %s' % (name, env.now))
    else :
        print ('No hay memoria ram, espere')
    yield env.timeout(1)
    
    # estado ready, esperar a que lo atienda el cpu
    print('%s arriving at %d' % (name, env.now))
    llegada = env.now #registrar hora llegada
    with cpu.request() as req:  #pedimos conectarnos al cpu
        yield req
        # Charge the battery
        print('%s proceso inicia a %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s leaving the bcs at %s' % (name, env.now))
        # se hizo release automatico del cargador bcs
    tiempoCarga = env.now - llegada
    print('%s tiempo total espera + carga %s' % (name, tiempoCarga))
    tiempoCargaTotal = tiempoCargaTotal + tiempoCarga
    
#
env = simpy.Environment()  #crear ambiente de simulacion
memoriaRam = 100
cpu = simpy.Resource(env, capacity=1) #solo hay un cpu
ram = simpy.Container(env, init=100, capacity=memoriaRam) #capacidad de memoria es 100                                  
tiempoCargaTotal=0.0
nprocesos = 100
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
interval = 10

# crear los procesos
for i in range(nprocesos):
    t = random.expovariate(1.0 / interval)
    env.process(proceso(env, 'Proceso %d' % i, cpu, t, 5))

# correr la simulacion
env.run()
    
promedio = tiempoCargaTotal/nprocesos
print ('En promedio se tardan %d' %promedio)
print ('Tiempo total %d' %tiempoCargaTotal)
