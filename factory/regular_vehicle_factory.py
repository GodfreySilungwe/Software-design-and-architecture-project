from domain.vehicle import Car, Motorcycle, Bus
from factory.vehicle_factory import VehicleFactory

class RegularVehicleFactory(VehicleFactory):
    def create(self, vehicle_type, regnum, make, model, color):
        if vehicle_type == "Motorcycle":
            return Motorcycle(regnum, make, model, color)
        elif vehicle_type == "Bus":
            return Bus(regnum, make, model, color)
        return Car(regnum, make, model, color)

    

