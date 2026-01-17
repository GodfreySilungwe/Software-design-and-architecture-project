import tkinter as tk
from domain.parking_lot import ParkingLot
from factory.regular_vehicle_factory import RegularVehicleFactory
from factory.electric_vehicle_factory import ElectricVehicleFactory
from presenter.parking_presenter import ParkingPresenter
from services.charging_client import ChargingServiceClient
from ui.app import ParkingUI

def main():
    parking_lot = ParkingLot(capacity=10, ev_capacity=5, level=1)

    presenter = ParkingPresenter(
        parking_lot,
        RegularVehicleFactory(),
        ElectricVehicleFactory(),
        ChargingServiceClient()
    )

    root = tk.Tk()
    ParkingUI(root, presenter)
    root.mainloop()

if __name__ == "__main__":
    main()

