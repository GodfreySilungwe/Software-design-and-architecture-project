class ElectricMixin:
    def __init__(self):
        self.charge = 0

    def setCharge(self, charge):
        self.charge = charge

    def getCharge(self):
        return self.charge

