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