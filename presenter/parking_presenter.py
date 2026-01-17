from dataclasses import dataclass


@dataclass
class ParkResult:
    success: bool
    slot: int | None = None
    message: str = ""


class ParkingPresenter:
    def __init__(self, parking_lot, regular_factory, electric_factory, charging_client):
        self.parking_lot = parking_lot
        self.regular_factory = regular_factory
        self.electric_factory = electric_factory
        self.charging_client = charging_client

    # Lot creation
    def create_lot(self, capacity, ev_capacity, level):
        self.parking_lot.create_lot(capacity, ev_capacity, level)

    # Park
    def park_vehicle(self, factory, vehicle_type, regnum, make, model, color):
        vehicle = factory.create(vehicle_type, regnum, make, model, color)
        ev = hasattr(vehicle, "getCharge")
        slot = self.parking_lot.park(vehicle, ev=ev)
        if slot:
            return ParkResult(True, slot, "")
        return ParkResult(False, None, "Parking is full")

    # Remove
    def remove_vehicle(self, slot_number):
        success = self.parking_lot.leave(slot_number)
        return success

    # Status
    def get_status(self):
        return self.parking_lot.status()

    # Queries
    def get_slots_by_color(self, color):
        return self.parking_lot.get_slots_by_color(color)

    def get_slot_by_reg(self, regnum):
        return self.parking_lot.get_slot_by_reg(regnum)

    def get_regs_by_color(self, color):
        return self.parking_lot.get_regs_by_color(color)

    # EV / Charging service integration
    def start_charging(self, regnum):
        try:
            self.charging_client.start_charging(regnum)
            return True
        except Exception:
            return False

    def stop_charging(self, regnum):
        try:
            self.charging_client.stop_charging(regnum)
            return True
        except Exception:
            return False

    def get_charge_status(self, regnum):
        return self.charging_client.get_status(regnum)
