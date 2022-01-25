# 1. (add configs as needed)

import dataclasses
import time
import random

import config


@dataclasses.dataclass
class Coin:
    value: int
    x: int
    y: int
    ttl_seconds: int
    created_at_timestamp: int = dataclasses.field(init=False)

    def __post_init__(self):
        self.created_at_timestamp = int(time.time())

    @classmethod
    def mint(cls):
        x = random.randrange(config.GRAPH_MIN_X,
                             config.GRAPH_MAX_X, config.X_PER_SPACE)
        y = random.randrange(config.GRAPH_MAX_Y,
                             config.GRAPH_MIN_Y, -1*config.Y_PER_LINE)
        value = random.randint(1, config.COIN_MAX_VALUE)
        ttl = random.randint(config.COIN_MIN_TTL, config.COIN_MAX_TTL)
        return cls(value, x, y, ttl)

    def coin_is_collectable(self):
        return time.time() - self.created_at_timestamp < self.ttl_seconds

    # CONTINUE IN 2. (car.py __init__)
