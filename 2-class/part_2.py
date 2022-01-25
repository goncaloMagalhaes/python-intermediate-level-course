# Create file and add Person

class Person:
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

# Create file for unit testing --> part_2_test.py

# Now on to refactor in part 3
