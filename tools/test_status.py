import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from domain.parking_lot import ParkingLot
from presenter.parking_presenter import ParkingPresenter
from factory.regular_vehicle_factory import RegularVehicleFactory
from factory.electric_vehicle_factory import ElectricVehicleFactory
from services.charging_client import ChargingServiceClient

lot = ParkingLot(3, 2, 1)
presenter = ParkingPresenter(lot, RegularVehicleFactory(), ElectricVehicleFactory(), ChargingServiceClient())

factory = RegularVehicleFactory()
res = presenter.park_vehicle(factory, 'Car', 'ABC123', 'Toyota', 'Corolla', 'Blue')
print('Park result:', res)
print('Status:', presenter.get_status())

# Park an EV
efac = ElectricVehicleFactory()
res2 = presenter.park_vehicle(efac, 'Car', 'EV001', 'Tesla', 'Model3', 'Red')
print('Park EV result:', res2)
print('Status after EV:', presenter.get_status())
