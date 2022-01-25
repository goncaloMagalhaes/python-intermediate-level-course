from controller import Controller
from car import Car
from tuples import CoinRegistry

# 5. (add CoinRegistry init and pass it)
coin_registry = CoinRegistry([], [])

my_car = Car(coin_registry.collected, 100, 200)
controller = Controller(my_car, coin_registry)

controller.start()
controller.join()


# Test it out
