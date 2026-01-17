from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, regnum, make, model, color):
        self.regnum = regnum
        self.make = make
        self.model = model
        self.color = color

    @abstractmethod
    def getType(self):
        pass


class Car(Vehicle):
    def getType(self):
        return "Car"


class Motorcycle(Vehicle):
    def getType(self):
        return "Motorcycle"


class Bus(Vehicle):
    def getType(self):
        return "Bus"
