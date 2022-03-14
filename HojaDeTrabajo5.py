import simpy
import random

def process(name, environment, ram, cpu, admitted_time, number_of_instructions, ram_req):
    #Tiempo de llegada del proceso
    yield environment.timeout(admitted_time)

    #Se guarda el tiempo de llegada
    tiempo_llegada = environment.now

    #Se establece un intento de ejecución del proceso por defecto, si I/O
    wait = 2

    #Se imprime el estado del proceso que acaba de llegar
    print("---------------NEW Incomme---------------")
    print('%s in queue ADMITTED in time: %d, RAM required: %d, Available: %d' % (name, environment.now, ram_req, ram.level))
    print("-----------------------------------------")

    #Se solicita la memoria al contenedor de RAM o se queda en espera
    yield ram.get(ram_req)

    #Avisa que ya consiguió la RAM necesaria
    print("----------------RAM INFO-----------------")
    print('%s  got memory, RAM acquired: %d' % (name, ram_req))
    print("-----------------------------------------")

    #Una vez obtenida la memoria se colocará en las colas READY y WAITING hasta que finalice sus instrucciones (I/O's incluidos)
    while number_of_instructions > 0:

        #Colocar en WAITING si necesita realizar una instruccion de I/O
        if(wait != 2):
            print("-----------------WAITING-----------------")
            print('%s in queue WAITING, Instructions remaining: %d' % (name, number_of_instructions))
            print("-----------------------------------------")

            #Simula una ejecución de instrucción I/O
            yield environment.timeout(1)

        print("------------------READY------------------")
        print('%s in queue READY in time: %d, Instructions remaining: %d' % (name, environment.now, number_of_instructions))
        print("-----------------------------------------")

        #Solicitud del procesador como recurso
        with cpu.request() as req:
            yield req

            #Se ejecutan 3 instrucciones en un ciclo de reloj
            number_of_instructions = number_of_instructions - 3
            yield environment.timeout(1)

            #Se imprime la ejecucion del proceso
            if(number_of_instructions == 0):
                print("-----------------RUNNING-----------------")
                print('%s in queue RUNNING in time: %d, Instructions remaining: %d' % (name, environment.now, number_of_instructions))
                print("-----------------------------------------")
            else:
                print("-----------------RUNNING-----------------")
                print('%s in queue RUNNING in time: %d, Instructions remaining: 0' % (name, environment.now))
                print("-----------------------------------------")
        
        #Se genera un estado aleatorio para las instrucciones I/O
        wait = random.randint(1,2)

    #Imprime el estado de memoria junto con la RAM devuelta
    yield ram.put(ram_req)
    print("---------------TERMINATED----------------")
    print('%s in queue TERMINATED in total time: %d, RAM returned: %d, Available: %d' % (name, (environment.now-tiempo_llegada), ram_req, ram.level))
    print("-----------------------------------------")
    
    global tiempo_total
    tiempo_total += environment.now - tiempo_llegada
    array_tiempo.append(environment.now-tiempo_llegada)

#Creación de atributos y entorno de simulacion
random.seed(15401)
environment = simpy.Environment()  # crear ambiente de simulacion
initial_ram = simpy.Container(environment, 30, init=30)  # crea el container de la ram
initial_cpu = simpy.Resource(environment, capacity=1)  # se crea el procesador con capacidad establecida
initial_procesos = 200  # cantidad de procesos a generar
tiempo_total = 0
array_tiempo = []

for i in range(initial_procesos):
    llegada = random.expovariate(1/10) #Todos los procesos llegan al mismo tiempo
    cantidad_instrucciones = random.randint(1, 10)  # cantidad de operaciones por proceso
    UsoRam = random.randint(1, 10)  # cantidad de ram que requiere cada proceso
    environment.process(process('Process #%d' % i, environment, initial_ram, initial_cpu, llegada, cantidad_instrucciones, UsoRam))

# correr la simulacion
environment.run()
print('Tiempo de ejecución promedio: %f ' % (tiempo_total / initial_procesos))
print('Desviación estándar de tiempo de ejecución: %f' %())