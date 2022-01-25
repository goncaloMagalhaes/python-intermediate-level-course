# 9.

from threading import Thread
import queue
import time

import config


class Listener(Thread):
    def __init__(self, queue: queue.Queue) -> None:
        super().__init__(name='Listener')
        self.command_queue = queue

    def get_command_from_file(self) -> str:
        # STOP HERE, create config.py --> go to 10.
        # 11.
        line = ""
        with open(config.COMMAND_FILE, 'r+') as file:
            line = file.readline()
            file.truncate(0)
        return line

    def transmit(self, command: str):
        self.command_queue.put(command)

    def run(self):
        while True:
            command = self.get_command_from_file()
            if command != '':
                self.transmit(command)
            time.sleep(config.SECONDS_PER_FILE_READ)  # Add to configs

    # CONTINUE TO 12. (refactor tire configs to be in config.py)
