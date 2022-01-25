from threading import Thread, Timer, Lock
from time import sleep, time
from typing import List
import concurrent.futures
import os


def print_after_sleeping(seconds: int):
    sleep(seconds)
    print(f'I slept for {seconds}s.')


threads = [Thread(target=print_after_sleeping, args=(i,)) for i in range(5)]
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
    print(f'thread {thread.native_id} joined.')

threads = [Thread(target=print_after_sleeping, args=(i,)) for i in range(5)]
for thread in threads:
    thread.start()

for thread in reversed(threads):  # don't use reversed first
    thread.join()
    print(f'thread {thread.native_id} joined.')

# este exemplo não mostra muito a utilidade. Mas se pensarmos em trabalhadores numa empresa, num café p.ex, é evidente
# que ajuda ter várias pessoas a trabalhar em paralelo.

# Create ThreadPoolExecutor

with concurrent.futures.ThreadPoolExecutor(5) as executor:
    executor.map(print_after_sleeping, range(5))


# Mostrar que threading para compute intensive process não vale a pena (mais vale multiprocessing), por fazer as ações
# no mesmo processo, mais as transições de thread para thread


def multiply_numbers(start: int, end: int, register: List[int]):
    total = 1
    for i in range(start, end):
        total *= i
    register.append(total)


def multiply_numbers_in_threads(threads: int, numbers: int):
    my_threads: List[Thread] = []
    register: List[int] = []
    for start in range(1, numbers, numbers // threads):
        end = start + (numbers // threads)
        t = Thread(target=multiply_numbers, args=(start, end, register))
        t.start()
        my_threads.append(t)
    for t in my_threads:
        t.join()
    total = 1
    for i in register:
        total *= i
    print(f'{total = }')


print('Non threads')
s = time()
register = []
multiply_numbers(1, 100, register)
total = register[0]
print(f'{total = }')
print(time() - s)

print('threads')
s = time()
multiply_numbers_in_threads(10, 100)
print(time() - s)  # pior até


# I/O intense
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def write_file(number: int):
    print('Writing number', number)
    with open(f'{SCRIPT_DIR}/files/f{number}.txt', 'w+') as f:
        f.write(str(number**40000))


# Note: first refactor filepath because compatibility with all OS -> os.path.join(SCRIPT_DIR, 'files', f'f{self.number}.txt')


print('Non threads')
s = time()
for i in range(100):
    write_file(i)
print(time() - s)

print('threads')
s = time()
with concurrent.futures.ThreadPoolExecutor(100) as executor:
    executor.map(write_file, range(100))
print(time() - s)  # whatever

# Thread Class

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class FileWriter(Thread):
    def __init__(self, number: int) -> None:
        super().__init__()
        self.number = number

    def run(self):
        n = 0
        while n < 10:
            print(n)
            file_name = os.path.join(
                SCRIPT_DIR, 'files', f'f{self.number}.txt')
            with open(file_name, 'w+') as f:
                f.write(str(self.number**40000))
            n += 1


writer = FileWriter(10)
writer.start()
print('Something while files are being written.')
writer.join()


# Timer


t1 = Timer(2, function=print, args=('I am t1 running.', ))
t2 = Timer(4, function=print, args=('I am t2 running.', ))
t3 = Timer(0, function=print, args=('I am t3 running.', ))
t4 = Timer(1, function=print, args=('I am t4 running.', ))


t1.start()
t2.start()
t3.start()
t4.start()
# joins not needed, unless we want everything to stop
t1.join()
t2.join()
t3.join()
t4.join()

# Lock


def waiter(lock: Lock):
    sleep(1)
    print('Waiter trying to pass lock')
    lock.acquire()
    print('OK lock passed. Time to do my things.')
    print('Waiter pid:', os.getpid())
    lock.release()


def locker(lock: Lock):
    print('Locker will lock')
    with lock:
        print('Locked')
        print('Locker pid:', os.getpid())
        sleep(5)
    print('Unlocked by locker.')


shared_lock = Lock()
w = Thread(target=waiter, args=(shared_lock,))
l = Thread(target=locker, args=(shared_lock,))
w.start()
l.start()
# no need
w.join()
l.join()

# Deadlock example


def access_something(lock):
    lock.acquire()
    print('access done.')
    lock.release()


def waiter(lock: Lock):
    sleep(1)
    print('Waiter trying to pass lock')
    lock.acquire()
    print('OK lock passed. Time to do my things.')
    access_something(lock)
    lock.release()


def locker(lock: Lock):
    print('Locker will lock')
    with lock:
        print('Locked')
        sleep(5)
    print('Unlocked by locker.')


# this will provoke deadlock
# shared_lock = Lock()
# w = Thread(target=waiter, args=(shared_lock,))
# l = Thread(target=locker, args=(shared_lock,))
# w.start()
# l.start()


# Another deadlock example, and its fix

def make_division(p: int, q: int):
    return p / q


def waiter(lock: Lock):
    sleep(1)
    print('Waiter trying to pass lock')
    lock.acquire()
    print('OK lock passed. Time to do my things.')
    lock.release()


def locker(lock: Lock):
    print('Locker will lock')
    lock.acquire()
    print('Locked')

    make_division(10, 0)

    lock.release()
    print('Unlocked by locker.')


# this gives deadlock of waiter
# shared_lock = Lock()
# w = Thread(target=waiter, args=(shared_lock,))
# l = Thread(target=locker, args=(shared_lock,))
# w.start()
# l.start()

# fix

def waiter(lock: Lock):
    sleep(1)
    print('Waiter trying to pass lock')
    lock.acquire()
    print('OK lock passed. Time to do my things.')
    lock.release()


def locker(lock: Lock):
    print('Locker will lock')
    lock.acquire()
    print('Locked')

    # make this test with 'with' --> same thing (make sure to remove all acquire and release)
    try:
        make_division(10, 0)
    except Exception:
        print('Err')
    finally:
        lock.release()

    print('Unlocked by locker.')


shared_lock = Lock()
w = Thread(target=waiter, args=(shared_lock,))
l = Thread(target=locker, args=(shared_lock,))
w.start()
l.start()
# no need
w.join()
l.join()
