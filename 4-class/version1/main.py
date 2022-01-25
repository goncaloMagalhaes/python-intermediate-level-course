# 15.

from controller import Controller
from car import Car


my_car = Car(100, 200)
controller = Controller(my_car)

controller.start()
controller.join()

# Now let's try it, and we'll be done with version 1 (version 2 starts at coin.py)
