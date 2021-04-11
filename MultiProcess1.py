import multiprocessing
# from datetime import datetime
from datetime import datetime

"""
names = ['me', 'you', 'he', 'she']

def greeting(n, l):
    l.acquire()
    for n in names:
        print('Hello', n, datetime.now())
    l.release()

def long_one(n):
    for n in names:
        print('Is a long one', n, datetime.now()) if len(n) > 2 else ''

if __name__ == '__main__':
    l = multiprocessing.Lock()
    p = multiprocessing.Process(target=greeting, args=(['n', l]))
    p1 = multiprocessing.Process(target=long_one, args=(['n']))
    p.start()
    p1.start()
    p1.join()
    p.join()
    print('Done')

# Ejemplo con colas
"""


import multiprocessing
from datetime import datetime

q = multiprocessing.Queue()

def is_even(numbers, q):
    for n in numbers:
        if n % 2 == 0:
            q.put(n)

if __name__ == "__main__":
    p = multiprocessing.Process(target=is_even, args=(range(20), q))

    p.start()
    p.join()

    print(q.empty(), 'at', datetime.now())

    while not q.empty():
        print(q.get())

print(q.empty(), 'at', datetime.now(), 'First line')


"""
# Ejemplo con tuberias
def f(c, q):
    print('process1 started', datetime.now())
    for i in range(11):
        q.put('hello world ' + str(i))
    c.send(q)
    print('process1 ended', datetime.now())
    c.close()

def f1(c, q):
    print('process2 started', datetime.now())
    for i in range(11, 21):
        q.put('hello world ' + str(i))
    c.send(q)
    print('process2 ended', datetime.now())
    c.close()

def g():
    parent_conn, child_conn = multiprocessing.Pipe()
    parent_conn1, child_conn1 = multiprocessing.Pipe()
    q = multiprocessing.Manager().Queue()
    q1 = multiprocessing.Manager().Queue()
    p2 = multiprocessing.Process(target=f, args=([child_conn, q]))
    p3 = multiprocessing.Process(target=f1, args=([child_conn1, q1]))

    p2.start()
    p3.start()
    p(parent_conn.recv())
    p(parent_conn1.recv())
    p2.join()
    p3.join()

def p(o):
    while not o.empty():
        print(o.get())


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=g)
    p1.start()
    p1.join()
"""
'''
class MyFancyClass:

    def __init__(self, name):
        self.name = name

    def do_something(self):
        proc_name = multiprocessing.current_process().name
        print('Doing something fancy in {} for {}!'.format(
            proc_name, self.name))


def worker(q):
    while not q.empty():
        obj = q.get()
        obj.do_something()


if __name__ == '__main__':
    queue = multiprocessing.Queue()

    p = multiprocessing.Process(target=worker, args=[queue])
    p.start()

    queue.put(MyFancyClass('Fancy dan'))
    queue.put(MyFancyClass('Fancy adg08101'))
    queue.put(MyFancyClass('Fancy kyocera'))

    # Wait for the worker to finish
    queue.close()
    queue.join_thread()
    p.join()
'''

import multiprocessing
import time

"""
class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print('{}: Exiting'.format(proc_name))
                self.task_queue.task_done()
                break
            print('{}: {}'.format(proc_name, next_task))
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)


class Task:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(0.1)  # pretend to take time to do the work
        return '{self.a} * {self.b} = {product}'.format(
            self=self, product=self.a * self.b)

    def __str__(self):
        return '{self.a} * {self.b}'.format(self=self)


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    count = 10

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * count
    print('Creating {} consumers'.format(num_consumers))
    consumers = [
        Consumer(tasks, results)
        for i in range(num_consumers)
    ]

    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = num_consumers + 1
    for i in range(num_jobs):
        tasks.put(Task(i, i))

    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Start printing results
    while not results.empty():
        print('Result:', results.get())
"""
"""
import multiprocessing

class Tarea(multiprocessing.Process):
    num1: int
    num2: int
    res: int

    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def __call__(self):
        self.res = self.num1 + self.num2

class Trabajador:
    iter: int

    def __init__(self, iter):
        tareas = [
            Tarea(i, i)
            for i in range(iter)
        ]
        print(tareas)

if __name__ == '__main__':
    t = Trabajador(10)
"""