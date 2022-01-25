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
from coin import Coin
import tuples
import config


class Controller(Thread):
    # 4. (add tuple to init, then new logic to run, then refactor execute), then 5. (main.py)
    def __init__(self, car: Car, coins: tuples.CoinRegistry) -> None:
        super().__init__(name='Controller')

        self.car = car
        self.coins = coins

        self.command_queue = queue.Queue()
        self.listener = Listener(self.command_queue)

        self.display_queue = queue.Queue()
        self.monitor = Monitor(
            self.car, self.display_queue, self.coins)

    def execute(self, command: str):
        try:
            assert(isinstance(command, str),
                   "'command' var is not of type 'str'")
        except AssertionError:
            command = 'invalid'

        match command.lower().split():
            case ['end']:
                print('Program will end. Until next time.')

            case ['speed', speed_str]:
                print('Velocity Change.')
                new_speed = float(speed_str)
                self.car.velocity = new_speed

            case ['dir', dir_x, dir_y]:
                print('Direction Change.')
                self.car.direction = tuples.Direction(int(dir_x), int(dir_y))

            case ['replace_tire', left_right, front_back]:
                print('Replace Tire Command.')
                self.car.replace_tire(left_right, front_back)

            case _:
                print('Invalid Command.')

    def start_threads(self):
        self.listener.start()
        self.monitor.start()

    def run(self):
        self.start_threads()
        command = ''
        init_cycle = time.time()
        last_minting_time = time.time()

        while command.lower() != 'end':
            if not self.command_queue.empty():
                command = self.command_queue.get()
                print('New command:', command)
                self.execute(command)
            elif not self.display_queue.empty():
                print(self.display_queue.get())

            if time.time() - last_minting_time >= config.CONTROLLER_SECONDS_PER_COIN_MINTING:
                self.coins.graphed.append(Coin.mint())
                last_minting_time = time.time()

            self.car.move(time.time() - init_cycle)
            init_cycle = time.time()
            time.sleep(config.CONTROLLER_SECONDS_PER_CYCLE)
