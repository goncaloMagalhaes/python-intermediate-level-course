import concurrent.futures
from time import time, sleep
import functools
import os
from typing import Iterable, Callable
from multiprocessing import Process, Pipe, Queue, Value, Array
from multiprocessing.connection import Connection


# Process Pool
# same function as in threading, i/o intensive. Use time() and prints instead of decorator


def register_time(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        s = time()
        func(*args, **kwargs)
        print(time() - s)
    return wrapper


def write_file(number: int):
    print(f'Process {os.getpid()} writing number {number}')
    with open(f'files/f{number}.txt', 'w+') as f:
        f.write(str(number**40000))


@register_time
def run_process_pool(func: Callable, workers: int, iterable: Iterable):
    with concurrent.futures.ProcessPoolExecutor(workers) as executor:
        executor.map(func, iterable)


run_process_pool(write_file, 100, range(100))

# Show that we can give less workers (we actually could on threads as well) and see the result
run_process_pool(write_file, 10, range(100))

# show that a same process writes multiple numbers
# then, explain what the hell is a decorator (syntactic sugar for decorator(func))

# decorator example from functools


def fib(n: int) -> int:
    if n < 1:
        raise ValueError('Cannot be < 1')
    if n <= 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


@functools.lru_cache
def fib_with_cache(n: int) -> int:
    if n < 1:
        raise ValueError('Cannot be < 1')
    if n <= 2:
        return 1
    else:
        return fib_with_cache(n - 1) + fib_with_cache(n - 2)


def time_fib(n: int, cache: bool = False):
    s = time()
    if cache:
        print(f'{n = }:{fib_with_cache(n) = }')
    else:
        print(f'{n = }:{fib(n) = }')
    print(round(time() - s, 8))


print('fib start')
time_fib(5)
time_fib(5, cache=True)
time_fib(20)
time_fib(20, cache=True)
time_fib(30)
time_fib(30, cache=True)
time_fib(35)
time_fib(35, cache=True)
time_fib(37)
time_fib(37, cache=True)
time_fib(100, cache=True)

# explain this cache thing in detail, (e.g., with cache, f(20) only runs 20 times the func). Then go see lru_cache code

# Process


def hello_world():
    print('Hello world!')


process = Process(target=hello_world)
process.start()
process.join()


# process queue communication

def fetch_info_from_mars(info_queue: Queue):
    sleep(3)
    info_queue.put({
        'temperature': 5,
        'clouds': 0,
        'humidity': 0,
        'wind': 100
    })


queue = Queue(maxsize=10)
process = Process(target=fetch_info_from_mars, args=(queue,))
process.start()
print(queue.get())  # will wait
process.join()


# using pipes

def snipper(radio: Connection):
    sleep(2)
    radio.send({'target_spotted': True})
    msg = radio.recv()
    if msg['kill'] is True:
        print('*Snipper* Received kill permission.')
        sleep(2)
        print('*Shot*')
        sleep(2)
        radio.send('Done. Over.')


parent_conn, child_conn = Pipe()
snipper_process = Process(target=snipper, args=(child_conn,))
snipper_process.start()
msg = parent_conn.recv()
if msg['target_spotted'] is True:
    print('*General* Received msg target was spotted. Send kill msg.')
    sleep(2)
    parent_conn.send({'kill': True})
    print(f'*General* Received: "{parent_conn.recv()}"')

snipper_process.join()


# show why it's harder to share memory


def dictionary_value_changer(dictionary: dict):
    dictionary['value'] = 10
    dictionary['list'].append(30)


d = {'value': 20, 'list': [10, 20]}
print(d)
process = Process(target=dictionary_value_changer, args=(d,))
process.start()
process.join()
print(d)


# The hard way to have shared memory between processes


def changer(number: Value, my_list: Array):
    number.value = 10
    my_list[2] = 30


num = Value('i', 20)
arr = Array('i', [10, 20, 0])
print(num.value, arr[:])
process = Process(target=changer, args=(num, arr))
process.start()
process.join()
print(num.value, arr[:])
