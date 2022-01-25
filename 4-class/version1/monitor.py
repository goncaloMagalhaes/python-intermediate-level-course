# 13. (create configs as needed). __init__, then _generate_display, then as needed

from threading import Thread
import queue
import time

from car import Car
import config


class Monitor(Thread):
    def __init__(self, car: Car, queue: queue.Queue) -> None:
        super().__init__(name='Monitor')

        self.car = car
        self.display_queue = queue

    @staticmethod
    def _generate_header():
        return '\n' * 30  # clean terminal

    def _generate_graph(self):
        graph = ''
        car_drawn = False
        for line in range(config.GRAPH_MAX_Y, config.GRAPH_MIN_Y, -1*config.Y_PER_LINE):
            for space in range(config.GRAPH_MIN_X, config.GRAPH_MAX_X, config.X_PER_SPACE):
                if 0 <= line - self.car.y < config.Y_PER_LINE and \
                        0 <= space - self.car.x < config.X_PER_SPACE and \
                        not car_drawn:
                    graph += '*'
                    car_drawn = True
                elif 0 <= line < config.Y_PER_LINE:
                    if 0 <= space < config.X_PER_SPACE:
                        graph += '+'
                    else:
                        graph += '-'
                elif 0 <= space < config.X_PER_SPACE:
                    graph += '|'
                else:
                    graph += ' '
            graph += '\n'
        return graph

    def _generate_display(self):
        return self._generate_header() + self._generate_graph() + self._generate_info()

    def _generate_info(self):
        info = ''
        info += f'v = {self.car.velocity}m/s ; '
        info += f'(x, y) = ({self.car.x}, {self.car.y})'
        info += '\n'
        return info

    def run(self):
        while True:
            self.display_queue.put(self._generate_display())
            time.sleep(0.7)

    # CONTINUE IN 14. (create controller.py)
