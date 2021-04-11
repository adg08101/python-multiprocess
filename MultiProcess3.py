import multiprocessing, time
from random import random

"""
def wait_for_event(e, e1):
    '''Wait for the event to be set before doing anything'''
    e.wait()
    print('wait_for_event: starting', 'ahora si')
    # e.wait()
    print('wait_for_event: e.is_set()->', e.is_set())
    e1.set()

def wait_for_event_2(e1):
    '''Wait for the event to be set before doing anything'''
    e1.wait()
    print('wait_for_event: starting', 'ahora si tambien')
    # e.wait()
    print('wait_for_event: e.is_set()->', e1.is_set())


def wait_for_event_timeout(e, t):
    '''Wait t seconds and then timeout'''
    print('wait_for_event_timeout: starting')
    e.wait(t)
    print('wait_for_event_timeout: e.is_set()->', e.is_set())


if __name__ == '__main__':
    e = multiprocessing.Event()
    e1 = multiprocessing.Event()

    w1 = multiprocessing.Process(
        name='block',
        target=wait_for_event,
        args=(e, e1),
    )
    w1.start()

    w3 = multiprocessing.Process(
        name='block',
        target=wait_for_event_2,
        args=(e1,),
    )
    w3.start()

    w2 = multiprocessing.Process(
        name='nonblock',
        target=wait_for_event_timeout,
        args=(e, 2),
    )
    w2.start()

    print('main: waiting before calling Event.set()')
    time.sleep(3)
    e.set()
    print('main: event is set')
"""

# Ejemplo con Evento
"""
def proc1(e):
    print('Proc1')
    e.set()

def proc2(e):
    e.wait(5) # 5 Sencond Timeout
    print('Proc2')

if __name__ == '__main__':
    e = multiprocessing.Event()

    p1 = multiprocessing.Process(target=proc1, args=[e])
    p2 = multiprocessing.Process(target=proc2, args=[e])

    p1.start()
    p2.start()

    p1.join()
    p2.join()
"""

# Ejemplo con Lock
"""
def proc1(l):
    l.acquire()
    print('Proc1')
    print('Proc1.1')
    print('Proc1.2')
    print('Proc1.3')
    l.release()

def proc2(l):
    with l:
        print('Proc2')
        print('Proc2.1')
        print('Proc2.2')
        print('Proc2.3')

if __name__ == '__main__':
    l = multiprocessing.Lock()

    p1 = multiprocessing.Process(target=proc1, args=[l])
    p2 = multiprocessing.Process(target=proc2, args=[l])

    p1.start()
    p2.start()

    p1.join()
    p2.join()
"""
"""
def proc1(c: multiprocessing.Condition):
    with c:
        print('Main process started')
        c.notify_all()

def proc2(c: multiprocessing.Condition):
    with c:
        c.wait()
        print(multiprocessing.process.current_process(), 'started')

def proc3(c: multiprocessing.Condition):
    with c:
        c.wait()
        print(multiprocessing.process.current_process(), 'started')

if __name__ == '__main__':
    c = multiprocessing.Condition()

    p1 = multiprocessing.Process(name='Proc1', target=proc1, args=[c])
    p2 = multiprocessing.Process(name='Proc2', target=proc2, args=[c])
    p3 = multiprocessing.Process(name='Proc3', target=proc3, args=[c])

    p2.start()
    p3.start()
    time.sleep(1)
    p1.start()

    p1.join()
    p2.join()
    p3.join()
"""

# Ejemplo con semaforo

class PiscinaActiva:
    def __init__(self):
        super(PiscinaActiva, self).__init__()
        self.manejador = multiprocessing.Manager()
        self.activo = self.manejador.list()
        self.bloqueo = multiprocessing.Lock()

    def hacerActivo(self, nombre):
        with self.bloqueo:
            self.manejador.append(nombre)

    def hacerInactivo(self, nombre):
        with self.bloqueo:
            self.manejador.remove(nombre)

    def __str__(self):
        return str(self.activo)

def trabajador(s, p):
    nombre = multiprocessing.current_process().name
    with s:
        p.hacerActivo(nombre)
        print('Iniciando {} desde {}',format(nombre, p))
        time.sleep(random.random())
        p.hacerInactivo(nombre)

if __name__ == '__main__':
    piscina = PiscinaActiva()
    semaforo = multiprocessing.Semaphore(3)

    trabajos = [
        multiprocessing.Process(
            name=str(i),
            target=trabajador,
            args=[semaforo, piscina],
        )
        for i in range(10)
    ]

    for t in trabajos:
        t.start()

    while 1 == 1:
        vivos = 0
        for t in trabajos:
            if t.is_alive():
                vivos += 1
                t.join(timeout=0.1)
                print('Ahora corriendo %s' % piscina)
            if vivos == 0:
                print('Se acabo lo que se daba')
                break
