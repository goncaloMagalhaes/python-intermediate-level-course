from threading import Thread
from typing import List
import queue
import time

from car import Car
from coin import Coin
import config
import tuples

# 3. (Add CoinRegistry to tuples.py, then add in init, then go
# to _generate_graph and refactor to have _generate_graph_position, then add coin methods as needed,
# then add money info to _generate_info), then go to 4. (controller.py)


class Monitor(Thread):
    def __init__(self, car: Car, display_queue: queue.Queue, coins: tuples.CoinRegistry) -> None:
        super().__init__(name='Monitor')

        self.car = car
        self.display_queue = display_queue
        self.coins = coins

    @staticmethod
    def _generate_header():
        return '\n' * 30  # clean terminal

    def _fetch_coin_from_coords(self, x: int, y: int) -> Coin | None:
        for coin in self.coins.graphed:
            if coin.x == x and coin.y == y:
                return coin
        return None

    def _collect(self, coin: Coin):
        assert(coin in self.coins.graphed, 'Coin not in graphed list')
        self.coins.collected.append(coin)
        self.coins.graphed.remove(coin)

    def _generate_graph_position(self, space: int, line: int, car_drawn: bool):
        if 0 <= line - self.car.y < config.Y_PER_LINE and \
                0 <= space - self.car.x < config.X_PER_SPACE and \
                not car_drawn:
            if (coin := self._fetch_coin_from_coords(space, line)) is not None:
                self._collect(coin)
            return '*'
        elif (coin := self._fetch_coin_from_coords(space, line)) is not None:
            if coin.coin_is_collectable():
                return 'B'
            else:
                self.coins.graphed.remove(coin)
        if 0 <= line < config.Y_PER_LINE:
            if 0 <= space < config.X_PER_SPACE:
                return '+'
            else:
                return '-'
        elif 0 <= space < config.X_PER_SPACE:
            return '|'
        else:
            return ' '

    def _generate_graph(self):
        graph = ''
        car_drawn = False
        for line in range(config.GRAPH_MAX_Y, config.GRAPH_MIN_Y, -1*config.Y_PER_LINE):
            for space in range(config.GRAPH_MIN_X, config.GRAPH_MAX_X, config.X_PER_SPACE):
                new_position_graph = self._generate_graph_position(
                    space, line, car_drawn)
                if new_position_graph == '*':
                    car_drawn = True
                graph += new_position_graph
            graph += '\n'
        return graph

    def _generate_display(self):
        return self._generate_header() + self._generate_graph() + self._generate_info()

    def _generate_info(self):
        info = ''
        info += f'v = {self.car.velocity}m/s ; '
        info += f'(x, y) = ({self.car.x}, {self.car.y}) ; '
        info += f'money = {self.car.money}'
        info += '\n'
        return info

    def run(self):
        while True:
            self.display_queue.put(self._generate_display())
            time.sleep(0.7)
