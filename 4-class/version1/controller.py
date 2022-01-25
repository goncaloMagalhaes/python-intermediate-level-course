# 14. (create configs as needed. __init__, then run)
# Controller receives commands through writing in a commands.txt file.
# Controller acts over Car.
# Monitor reads all Car info and displays it nicely, with alerts as well.
# All Threads.

from threading import Thread
import queue
import time

from car import Car
from listener import Listener
from monitor import Monitor
import tuples
import config


class Controller(Thread):
    def __init__(self, car: Car) -> None:
        super().__init__(name='Controller')

        self.car = car

        self.command_queue = queue.Queue()
        self.listener = Listener(self.command_queue)

        self.display_queue = queue.Queue()
        self.monitor = Monitor(self.car, self.display_queue)

    def execute(self, command: str):
        # all try except come in refactor after working properly
        command_lower: str = ''

        try:
            command_lower = command.lower()
        except AttributeError:
            command_lower = 'invalid'

        if command_lower == 'end':
            print('Program will end. Until next time.')

        elif command_lower.startswith('speed'):
            print('Velocity Change.')
            new_speed = float(command_lower.split(' ')[1])
            self.car.velocity = new_speed

        elif command_lower.startswith('dir'):
            print('Direction Change.')
            dir_x = int(command_lower.split(' ')[1])
            dir_y = int(command_lower.split(' ')[2])
            self.car.direction = tuples.Direction(dir_x, dir_y)

        elif command_lower.startswith('replace_tire'):
            print('Replace Tire Command.')
            left_right = command_lower.split(' ')[1]
            front_back = command_lower.split(' ')[2]
            self.car.replace_tire(left_right, front_back)
        else:
            print('Invalid Command.')

    def start_threads(self):
        self.listener.start()
        self.monitor.start()

    def run(self):
        self.start_threads()
        command = ''
        init_cycle = time.time()

        while command.lower() != 'end':
            if not self.command_queue.empty():
                command = self.command_queue.get()
                print('New command:', command)
                self.execute(command)
            elif not self.display_queue.empty():
                print(self.display_queue.get())

            self.car.move(time.time() - init_cycle)
            init_cycle = time.time()
            time.sleep(config.CONTROLLER_SECONDS_PER_CYCLE)

    # CONTINUE IN 15. (create main.py)
