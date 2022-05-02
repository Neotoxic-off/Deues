import os
import json
import random

class Range:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

class Quantity:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

class Setting:
    def __init__(self, quantity_value, range_value):
        self.quantity = quantity_value
        self.range = range_value

class Vowels:
    def __init__(self):
        self.vowels = [
            97,
            101,
            105,
            111,
            117,
            121
        ]

    def check(self, item):
        return (item in self.vowels)

class Profile:
    def __init__(self):
        self.path = "profile.json"
        self.data = None

        self.load()

    def load(self):
        if (os.path.isfile(self.path) == True):
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        else:
            print(f"profile not found '{self.path}'")
            exit(1)

class Builder:
    def __init__(self):
        self.profile = Profile()
        self.size = Range(
            self.profile.data["size"]["minimum"],
            self.profile.data["size"]["maximum"]
        )
        self.generation = self.profile.data["generations"]
        self.characters = Range(97, 122)
        self.duplications = True
        self.vowels = Vowels()
        self.composition = self.profile.data["composition"]
        self.blacklist = self.profile.data["blacklist"]
        self.starter = self.profile.data["starter"]
        self.ender = self.profile.data["ender"]
        self.results = []
        self.dump_path = f"result_{self.generation}.txt"

        self.build()
        self.dump()

    def build(self):
        i = 0

        while (i < self.generation):
            current = self.generate()
            if (current not in self.results):
                self.results.append(current)
                i += 1

    def dump(self):
        with open(self.dump_path, 'w+') as f:
            for i in self.results:
                f.write(f"{i}\n")

    def generate(self):
        size = random.randint(self.size.minimum, self.size.maximum)
        result = self.initialize()
        i = len(result)

        while (i < size):
            current = random.randint(self.characters.minimum, self.characters.maximum)
            if (self.checks(current, result) == True):
                result.insert(i, self.get_value(current))
                i += 1

        return (self.lts(result))

    def initialize(self):
        data = []

        if (self.starter > self.characters.minimum and self.starter < self.characters.maximum):
            data.append(self.get_value(self.starter))
        if (self.ender > self.characters.minimum and self.ender < self.characters.maximum):
            self.get_value(self.ender)

        return (data)

    def lts(self, data):
        buffer = ""

        for i in data:
            buffer += i
    
        return (buffer)

    def checks(self, current, buffer):
        checks = [
            self.check_blacklist(current),
            self.check_duplications(current, buffer),
            self.check_repartition(current, buffer)
        ]

        for check in checks:
            if (check == False):
                return (False)
        return (True)

    def check_blacklist(self, current):
        return (current not in self.blacklist)

    def check_duplications(self, current, buffer):
        if (self.duplications == False):
            return (current not in buffer)
        return (True)
    
    def check_repartition(self, current, buffer):
        i = len(buffer)
        vowel = self.vowels.check(current)

        if (len(self.composition) > i):
            if ((vowel == True and self.composition[i] == 'v') or
                (vowel == False and self.composition[i] == 'c')):
                return (True)
            return (False)
        return (True)

    def get_value(self, data):
        return (chr(data))

if (__name__ == "__main__"):
    Builder()
