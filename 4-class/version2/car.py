import math
from typing import List

from tuples import Direction
from coin import Coin
import config


class Tire:
    def __init__(self) -> None:
        self.__life_percentage = config.TIRE_INITIAL_LIFE_PERCENTAGE
        self.__radius_meters = config.TIRE_RADIUS_METERS
        self.__cycles_per_1percent_discount = config.TIRE_CYCLES_PER_1PERCENT_DISCOUNT

    @property
    def life_percentage(self) -> float:
        return self.__life_percentage

    @property
    def radius_meters(self) -> float:
        return self.__radius_meters

    @property
    def perimeter_meters(self) -> float:
        return 2 * math.pi * self.radius_meters

    def life_discount_from_distance(self, distance_meters: float) -> float:
        """Formula explanation:
        meters_per_1percent_discount  -  1
        distance_travelled_meters     - (X)

        ==> (X) = distance_travelled_meters / meters_per_1percent_discount
        """
        return distance_meters / (self.__cycles_per_1percent_discount * self.perimeter_meters)

    def discount_life_from_usage(self, distance_meters: float) -> None:
        self.__life_percentage -= self.life_discount_from_distance(
            distance_meters)
        if self.__life_percentage < 0:
            self.__life_percentage = 0


class Car:
    # 2. (Add coins and self.__coins, then money property), then 3. (monitor.py)
    def __init__(self, coins: List[Coin], x: float = 0, y: float = 0, velocity: float = 0) -> None:
        self.__x = x
        self.__y = y
        self.__velocity_meters_second = velocity
        self.__tires = self._initialize_tires()
        self.__direction = Direction(0, 1)
        self.__coins: List[Coin] = coins

    def _initialize_tires(self):
        return {
            'left': {
                'front': Tire(),
                'back': Tire()
            },
            'right': {
                'front': Tire(),
                'back': Tire()
            }
        }

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def velocity(self) -> float:
        return self.__velocity_meters_second

    @velocity.setter
    def velocity(self, value: float):
        if value >= 0:
            self.__velocity_meters_second = value

    @property
    def direction(self) -> Direction:
        return self.__direction

    @direction.setter
    def direction(self, direction: Direction) -> None:
        if not (direction.x == 0 and direction.y == 0):
            self.__direction = direction

    @property
    def direction_angle_radians(self) -> float:
        if self.direction.x == 0:
            sign = 1 if self.direction.y > 0 else -1
            return math.pi / 2 * sign
        return math.atan2(self.direction.y, self.direction.x)

    @property
    def velocity_x(self) -> float:
        return self.velocity * math.cos(self.direction_angle_radians)

    @property
    def velocity_y(self) -> float:
        return self.velocity * math.sin(self.direction_angle_radians)

    @property
    def money(self) -> int:
        return sum((coin.value for coin in self.__coins))

    def _discount_tire_usage(self, distance: float):
        self.__tires['left']['front'].discount_life_from_usage(distance)
        self.__tires['left']['back'].discount_life_from_usage(distance)
        self.__tires['right']['front'].discount_life_from_usage(distance)
        self.__tires['right']['back'].discount_life_from_usage(distance)

    def _tire_life_percentage_tuple(self) -> tuple:
        percentages = []
        percentages.append(self.__tires['left']['front'].life_percentage)
        percentages.append(self.__tires['left']['back'].life_percentage)
        percentages.append(self.__tires['right']['front'].life_percentage)
        percentages.append(self.__tires['right']['back'].life_percentage)
        return tuple(percentages)

    def _move_x(self, seconds: float) -> float:
        x_shift = self.velocity_x * seconds
        self.__x += x_shift
        return x_shift

    def _move_y(self, seconds: float) -> float:
        y_shift = self.velocity_y * seconds
        self.__y += y_shift
        return y_shift

    def _any_tire_is_dead(self):
        life_percentages = self._tire_life_percentage_tuple()
        for percentage in life_percentages:
            if percentage == 0:
                return True
        return False

    def replace_tire(self, left_right: str, front_back: str):
        self.__tires[left_right][front_back] = Tire()

    def move(self, seconds: float):
        if self._any_tire_is_dead():
            self.velocity = 0
            return
        elif self.velocity == 0:
            return
        x_shift = self._move_x(seconds)
        y_shift = self._move_y(seconds)
        self._discount_tire_usage(math.sqrt(x_shift**2 + y_shift**2))
