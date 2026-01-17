from abc import ABC, abstractmethod

class VehicleFactory(ABC):
    @abstractmethod
    def create(self, vehicle_type, regnum, make, model, color):
        pass

