import multiprocessing, time

class Consumidor(multiprocessing.Process):
    def __init__(self, tareas, respuestas):
        multiprocessing.Process.__init__(self)
        self.tareas = tareas
        self.respuestas = respuestas

    def run(self):
        nombre_proceso = self.name
        while 1 == 1:
            proxima_tarea = self.tareas.get()
            if proxima_tarea is None:
                print('Me voy del aire', '{}'.format(nombre_proceso))
                self.tareas.task_done()
                break
            print('{}: {}'.format(nombre_proceso, proxima_tarea))
            respuesta = proxima_tarea()
            self.tareas.task_done()
            self.respuestas.put(respuesta)

class Tarea:
    def __init__(self, a, b, operador):
        self.a = a
        self.b = b
        self.operador = operador
        self.operacion = str(self.a) + str(self.operador) + str(self.b)

    def __call__(self):
        time.sleep(0.1)
        return '{self.a} {self.operador} {self.b} = {res}'.format(self=self, res=eval(self.operacion))

    def __str__(self):
        return '{self.a} {self.operador} {self.b}'.format(self=self)

if __name__ == '__main__':
    tareas = multiprocessing.JoinableQueue()
    respuestas = multiprocessing.Queue()

    cantidad = 4
    total_consumidores = multiprocessing.cpu_count() * cantidad

    print('Se correran {} procesos concurrentes'.format(total_consumidores))

    consumidores = [
        Consumidor(tareas, respuestas)
        for i in range(total_consumidores)
    ]

    for c in consumidores:
        c.start()

    for t in range(total_consumidores + 1):
        tareas.put(Tarea(t, t, '<<'))

    for t in range(total_consumidores):
        tareas.put(None)

    tareas.join()

    while not respuestas.empty():
        print('Respuesta:', respuestas.get())
