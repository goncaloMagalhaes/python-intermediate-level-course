from dataclasses import dataclass
from functools import total_ordering
import math
from typing import List

# first add __repr__, then __str__. Add unit test to see object str. Then remove them and add dataclass. Rerun tests.
# then change last_name to use if else pythonically. Rerun tests. Then introduce walrus operator. Rerun tests.


@dataclass
class Person:
    name: str
    age: int
    job: str
    kids: list

    def has_kids(self) -> bool:
        return len(self.kids) > 0

    def last_name(self) -> str:
        return names[-1] if len(names := self.name.split(' ')) > 1 else ''


# Vector

@dataclass
@total_ordering
class Vector:
    x: float
    y: float

    def __len__(self):
        return round(math.sqrt(self.x**2 + self.y**2))

    def __eq__(self, other):
        return len(self) == len(other)

    def __lt__(self, other):
        return len(self) < len(other)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other.x, self.y * other.y)


v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(v1, f'{len(v1) = }')
print(v2, f'{len(v2) = }')
print(f'{v1+v2 = }')
print(f'{v1-v2 = }')
print(f'{v1*v2 = }')

# Add Point object and interactions with Vector


@dataclass
class Point:
    x: float
    y: float

    def __add__(self, other):
        if isinstance(other, Vector):
            return Point(self.x + other.x, self.y + other.y)
        raise TypeError(
            f'unsupported operand type(s) for +: \'Point\' and \'{type(other)}\'')

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)


v1 = Vector(2, 2)
p1 = Point(1, 0)
print(f'{p1 + v1 = }')
p2 = Point(3, 1)
print(f'{p2 - p1 = }')


# Repaste Person but smaller for simplification, and do PersonList

@dataclass
class Person:
    name: str
    age: int
    job: str

    def last_name(self) -> str:
        return names[-1] if len(names := self.name.split(' ')) > 1 else ''


class PersonList:
    def __init__(self) -> None:
        self._persons: List[Person] = []

    def append(self, person: Person):
        # Custom list gives me possibility to do this kind of stuff
        if not isinstance(person, Person):
            raise TypeError(
                f'Object to append \'{person}\' is not of type \'Person\'')
        return self._persons.append(person)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f'PersonList{self._persons})'

    def __len__(self) -> int:
        return len(self._persons)

    def __getitem__(self, index: int) -> Person:
        return self._persons[index]

    def __reversed__(self):
        return self._persons[::-1]

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self):
        if self._n < len(self):
            result = self[self._n]
            self._n += 1
            return result
        else:
            raise StopIteration


person1 = Person('g', 25, 'dev')
person2 = Person('j', 10, 'none')
person3 = Person('m', 50, 'doc')

personList = PersonList()
personList.append(person1)
personList.append(person2)
personList.append(person3)

print(personList)
print(f'{len(personList) = }')
print(f'{personList[0] = }')
print(f'{list(reversed(personList)) = }')
for person in personList:
    print(person)

# personList.append(1) # will raise exception
