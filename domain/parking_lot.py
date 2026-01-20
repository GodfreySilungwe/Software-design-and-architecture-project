class ParkingLot:
    def __init__(self, capacity, ev_capacity, level):
        self.capacity = capacity
        self.ev_capacity = ev_capacity
        self.level = level

        self.slots = [None] * capacity
        self.ev_slots = [None] * ev_capacity

    def get_empty_slot(self, ev=False):
        slots = self.ev_slots if ev else self.slots
        for i, slot in enumerate(slots):
            if slot is None:
                return i
        return None

    def park(self, vehicle, ev=False, level=None):
        # allow caller to specify level for this parking action
        if level is not None:
            self.level = level

        slot = self.get_empty_slot(ev)
        if slot is None:
            return None

        if ev:
            self.ev_slots[slot] = vehicle
        else:
            self.slots[slot] = vehicle

        return slot + 1

    def leave(self, slot_id, ev=False):
        slots = self.ev_slots if ev else self.slots
        index = slot_id - 1
        if 0 <= index < len(slots) and slots[index] is not None:
            slots[index] = None
            return True
        return False
    
    def status(self):
        vehicles = []
        # Regular slots
        for i, vehicle in enumerate(self.slots):
            if vehicle:
                vehicles.append((i + 1, self.level, vehicle))
        # EV slots (prefix with EV- to distinguish)
        for i, vehicle in enumerate(self.ev_slots):
            if vehicle:
                vehicles.append((f"EV-{i + 1}", self.level, vehicle))
        return vehicles

    def create_lot(self, capacity, ev_capacity, level):
        self.capacity = capacity
        self.ev_capacity = ev_capacity
        self.level = level
        self.slots = [None] * capacity
        self.ev_slots = [None] * ev_capacity

    def get_slots_by_color(self, color):
        results = []
        for i, v in enumerate(self.slots):
            if v and v.color.lower() == color.lower():
                results.append(i + 1)
        for i, v in enumerate(self.ev_slots):
            if v and v.color.lower() == color.lower():
                results.append(f"EV-{i + 1}")
        return results

    def get_slot_by_reg(self, regnum):
        for i, v in enumerate(self.slots):
            if v and v.regnum == regnum:
                return i + 1
        for i, v in enumerate(self.ev_slots):
            if v and v.regnum == regnum:
                return f"EV-{i + 1}"
        return None

    def get_regs_by_color(self, color):
        regs = []
        for v in self.slots + self.ev_slots:
            if v and v.color.lower() == color.lower():
                regs.append(v.regnum)
        return regs




