from time import sleep


#
# 1. Copy paste previous class, from 1-class/part_1.py. Refactor with docs and add_kid().
class Person:
    """Identifies a given person in a household
    """

    def __init__(self, name: str, age: int, job: str, kids: list) -> None:
        self.name = name
        self.age = age
        self.job = job
        self.kids = kids

    def has_kids(self) -> bool:
        return len(self.kids) > 0

    def last_name(self) -> str:
        """Infers person's last name from self.name

        Returns:
            str: person's last name
        """
        names = self.name.split(' ')
        if len(names) > 1:
            return names[-1]
        else:
            return ''

    def add_kid(self, kid_name: str):
        """Add kid to Person

        Returns:
            None
            ????? Irrelevant docs
        """
        self.kids.append(kid_name)


john = Person('john silva', 40, 'dev', ['sarah', 'peter'])
print(john.kids)
john.add_kid('james')

# instance and self. Instance variables
print(john.kids)
# print(Person.kids)  ## error -> instance variable not present! Because it is not instance
print(john.last_name())
print(Person.last_name(john))

# class vars


class Person:
    """Identifies a given person in a household
    """
    persons_created = 0

    def __init__(self, name: str, age: int, job: str, kids: list) -> None:
        self.name = name
        self.age = age
        self.job = job
        self.kids = kids

    def has_kids(self) -> bool:
        return len(self.kids) > 0

    def last_name(self) -> str:
        names = self.name.split(' ')
        if len(names) > 1:
            return names[-1]
        else:
            return ''

    def add_kid(self, kid_name: str):
        self.kids.append(kid_name)


john = Person('john adams', 40, 'dev', ['sarah', 'peter'])
print(f'Persons created (john): {john.persons_created}')
print(f'Persons created (Person): {Person.persons_created}')
Person.persons_created += 1
print(f'Persons created (john): {john.persons_created}')
john.persons_created += 1
print(f'Persons created (john): {john.persons_created}')
print(f'Persons created (Person): {Person.persons_created}')
Person.persons_created += 1
print(f'Persons created (john): {john.persons_created}')


# classmethod

class Person:
    """Identifies a given person in a household
    """
    persons_created = 0

    def __init__(self, name: str, age: int, job: str, kids: list) -> None:
        self.name = name
        self.age = age
        self.job = job
        self.kids = kids
        # Cannot change Person.persons_created here, only self.persons_created

    def has_kids(self) -> bool:
        return len(self.kids) > 0

    def last_name(self) -> str:
        names = self.name.split(' ')
        if len(names) > 1:
            return names[-1]
        else:
            return ''

    def add_kid(self, kid_name: str) -> None:
        self.kids.append(kid_name)

    @classmethod
    def create(cls, name: str, age: int, job: str, kids: list) -> Person:
        cls.persons_created += 1
        return Person(name, age, job, kids)


john = Person.create('john adams', 40, 'dev', ['sarah', 'peter'])
sarah = Person.create('sarah silva', 30, 'doc', [])
print(john.persons_created, sarah.persons_created, Person.persons_created)

# staticmethod


class Person:
    """Identifies a given person in a household
    """
    persons_created = 0

    def __init__(self, name: str, age: int, job: str, kids: list) -> None:
        self.name = name
        self.age = age
        self.job = job
        self.kids = kids

    def has_kids(self) -> bool:
        return len(self.kids) > 0

    def last_name(self) -> str:
        names = self.name.split(' ')
        if len(names) > 1:
            return names[-1]
        else:
            return ''

    def add_kid(self, kid_name: str) -> None:
        self.kids.append(kid_name)

    @staticmethod
    def name_has_surname(name: str) -> bool:
        return len(name.split(' ')) > 1

    @classmethod
    def create(cls, name: str, age: int, job: str, kids: list) -> Person:
        cls.persons_created += 1
        return Person(name, age, job, kids)


print(Person.name_has_surname('sarah lee'))
sarah = Person.create('sarah lee', 30, 'doc', [])
# print(sarah.name_has_surname('sarah lee')) # doesn't have this method

# Inheritance


class Vehicle:
    def __init__(self, wheels: int, speed_m_s: float, dist_from_origin_m: float = 0.0) -> None:
        self.wheels = wheels
        self.speed_m_s = speed_m_s
        self.dist_from_origin_m = dist_from_origin_m

    def draw_me(self):
        print(' * ')

    def move(self, seconds: int, draw_me: bool = False):
        sleep(seconds)
        self.dist_from_origin_m += self.speed_m_s * seconds
        if draw_me:
            print('\n'*10)
            self.draw_me()
        print(f'{round(self.dist_from_origin_m, 2)} meters')


v = Vehicle(2, 10)
t = 0
while t < 10:
    v.move(0.5)
    t += 1


class Car(Vehicle):
    def __init__(self, speed_m_s: float, dist_from_origin_m: float = 0) -> None:
        super().__init__(4, speed_m_s, dist_from_origin_m=dist_from_origin_m)

    def draw_me(self):
        print('__/--o\__')
        print(' O --- O ')

    def move(self, seconds: int, draw_me: bool = True):
        print('Car will move...')
        super().move(seconds, draw_me=draw_me)


car = Car(50)
t = 0
while t < 10:
    car.move(0.25)
    t += 1

print('\n'*10)
car.move(3)


class Motorcycle(Vehicle):
    def __init__(self, speed_m_s: float, dist_from_origin_m: float = 0) -> None:
        super().__init__(2, speed_m_s, dist_from_origin_m=dist_from_origin_m)

    def draw_me(self):
        print('____o__')
        print(' O - O ')

    def move(self, seconds: int, draw_me: bool = True):
        print('Bike will move...')
        super().move(seconds, draw_me=draw_me)


bike = Motorcycle(40)


def move_vehicle(vehicle: Vehicle, seconds: int):
    vehicle.move(seconds)


move_vehicle(bike, 3)
move_vehicle(car, 2)
