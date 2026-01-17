from domain.vehicle import Car, Motorcycle
from domain.electric_mixin import ElectricMixin
from factory.vehicle_factory import VehicleFactory

class ElectricCar(Car, ElectricMixin):
    def __init__(self, regnum, make, model, color):
        Car.__init__(self, regnum, make, model, color)
        ElectricMixin.__init__(self)

class ElectricBike(Motorcycle, ElectricMixin):
    def __init__(self, regnum, make, model, color):
        Motorcycle.__init__(self, regnum, make, model, color)
        ElectricMixin.__init__(self)

class ElectricVehicleFactory(VehicleFactory):
    def create(self, vehicle_type, regnum, make, model, color):
        if vehicle_type == "Motorcycle":
            return ElectricBike(regnum, make, model, color)
        return ElectricCar(regnum, make, model, color)

