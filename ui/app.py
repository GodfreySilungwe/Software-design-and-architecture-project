# ======================================================
# TKINTER UI
# ======================================================
import tkinter as tk
from tkinter import messagebox
from factory.regular_vehicle_factory import RegularVehicleFactory
from factory.electric_vehicle_factory import ElectricVehicleFactory


class ParkingUI:
    def __init__(self, root, presenter):
        self.root = root
        self.presenter = presenter
        self.root.title("Vehicle Parking Manager")
        self.root.geometry("800x850")
        self.root.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        # ===== PARKING LOT CREATION SECTION =====
        tk.Label(self.root, text="=== Create Parking Lot ===", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        
        tk.Label(self.root, text="Capacity (Regular Slots)").grid(row=1, column=0)
        self.capacity = tk.StringVar(value="10")
        tk.Entry(self.root, textvariable=self.capacity).grid(row=1, column=1)
        
        tk.Label(self.root, text="EV Capacity").grid(row=2, column=0)
        self.ev_capacity = tk.StringVar(value="5")
        tk.Entry(self.root, textvariable=self.ev_capacity).grid(row=2, column=1)
        
        tk.Label(self.root, text="Level").grid(row=3, column=0)
        self.level = tk.StringVar(value="1")
        tk.Entry(self.root, textvariable=self.level).grid(row=3, column=1)
        
        tk.Button(
            self.root,
            text="Create Parking Lot",
            command=self.create_parking_lot
        ).grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Separator
        tk.Label(self.root, text="=" * 40).grid(row=5, column=0, columnspan=2)
        
        # ===== VEHICLE PARKING SECTION =====
        tk.Label(self.root, text="=== Park Vehicle ===", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=2, pady=5)
        
        self.reg = tk.StringVar()
        self.make = tk.StringVar()
        self.model = tk.StringVar()
        self.color = tk.StringVar()
        self.vehicle_category = tk.StringVar(value="Car")
        self.is_electric = tk.IntVar()
        self.park_level = tk.StringVar(value=self.level.get())

        tk.Label(self.root, text="Registration No").grid(row=7, column=0)
        tk.Entry(self.root, textvariable=self.reg).grid(row=7, column=1)

        tk.Label(self.root, text="Make").grid(row=8, column=0)
        tk.Entry(self.root, textvariable=self.make).grid(row=8, column=1)

        tk.Label(self.root, text="Model").grid(row=9, column=0)
        tk.Entry(self.root, textvariable=self.model).grid(row=9, column=1)

        tk.Label(self.root, text="Color").grid(row=10, column=0)
        tk.Entry(self.root, textvariable=self.color).grid(row=10, column=1)
        tk.Label(self.root, text="Vehicle Type").grid(row=11, column=0)
        tk.OptionMenu(
            self.root,
            self.vehicle_category,
            "Car", "Motorcycle"
        ).grid(row=11, column=1)

        # Park level moved into the main form (keeps two-column layout)
        tk.Label(self.root, text="Park Level").grid(row=12, column=0)
        tk.Entry(self.root, textvariable=self.park_level, width=10).grid(row=12, column=1)

        tk.Checkbutton(
            self.root,
            text="Electric Vehicle",
            variable=self.is_electric
        ).grid(row=13, column=1)

        tk.Button(
            self.root,
            text="Park Vehicle",
            command=self.park_vehicle
        ).grid(row=14, column=1)

        tk.Button(
            self.root,
            text="Show Status",
            command=self.show_status
        ).grid(row=15, column=1)

        # Separator
        tk.Label(self.root, text="=" * 40).grid(row=15, column=0, columnspan=2)

        # ===== REMOVE VEHICLE SECTION =====
        tk.Label(self.root, text="=== Remove Vehicle ===", font=("Arial", 10, "bold")).grid(row=17, column=0, columnspan=2, pady=5)
        
        tk.Label(self.root, text="Slot Number").grid(row=18, column=0)
        self.remove_slot = tk.StringVar()
        tk.Entry(self.root, textvariable=self.remove_slot).grid(row=18, column=1)
        
        tk.Button(
            self.root,
            text="Remove Vehicle",
            command=self.remove_vehicle
        ).grid(row=19, column=0, columnspan=2, sticky="ew")

        # ===== QUERY SECTION =====
        tk.Label(self.root, text="=== Query Vehicles ===", font=("Arial", 10, "bold")).grid(row=20, column=0, columnspan=2, pady=5)
        
        tk.Label(self.root, text="Search by Color").grid(row=21, column=0)
        self.query_color = tk.StringVar()
        tk.Entry(self.root, textvariable=self.query_color).grid(row=21, column=1)
        
        tk.Button(
            self.root,
            text="Get Slots by Color",
            command=self.get_slots_by_color
        ).grid(row=22, column=0)
        
        tk.Button(
            self.root,
            text="Get Registration by Color",
            command=self.get_regs_by_color
        ).grid(row=22, column=1)
        
        tk.Label(self.root, text="Search by Registration").grid(row=23, column=0)
        self.query_reg = tk.StringVar()
        tk.Entry(self.root, textvariable=self.query_reg).grid(row=23, column=1)
        
        tk.Button(
            self.root,
            text="Get Slot by Registration",
            command=self.get_slot_by_reg
        ).grid(row=24, column=0, columnspan=2, sticky="ew")

        # Separator
        tk.Label(self.root, text="=" * 40).grid(row=24, column=0, columnspan=2)

        # ===== CHARGING SECTION =====
        tk.Label(self.root, text="=== Vehicle Charging ===", font=("Arial", 10, "bold")).grid(row=25, column=0, columnspan=2, pady=5)
        
        tk.Label(self.root, text="Charge RegNo").grid(row=26, column=0)
        self.charge_reg = tk.StringVar()
        tk.Entry(self.root, textvariable=self.charge_reg).grid(row=26, column=1)
        tk.Button(self.root, text="Start Charging", command=self.start_charging).grid(row=28, column=0)
        tk.Button(self.root, text="Stop Charging", command=self.stop_charging).grid(row=28, column=1)
        tk.Button(self.root, text="Check Charge Status", command=self.check_charge_status).grid(row=29, column=0, columnspan=2, sticky="ew")

        self.output = tk.Text(self.root, width=90, height=15)
        self.output.grid(row=30, column=0, columnspan=2, pady=5)

    def create_parking_lot(self):
        try:
            capacity = int(self.capacity.get())
            ev_capacity = int(self.ev_capacity.get())
            level = int(self.level.get())
            
            if capacity <= 0 or ev_capacity < 0 or level <= 0:
                messagebox.showerror("Error", "Capacity and Level must be positive numbers")
                return
            
            self.presenter.create_lot(capacity, ev_capacity, level)
            messagebox.showinfo("Success", f"Parking lot created:\n- Regular Slots: {capacity}\n- EV Slots: {ev_capacity}\n- Level: {level}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for capacity and level")

    def park_vehicle(self):
        factory = (
            ElectricVehicleFactory()
            if self.is_electric.get()
            else RegularVehicleFactory()
        )

        try:
            # parse park level input
            level = None
            park_level_val = self.park_level.get()
            if park_level_val:
                level = int(park_level_val)

            result = self.presenter.park_vehicle(
                factory,
                self.vehicle_category.get(),
                self.reg.get(),
                self.make.get(),
                self.model.get(),
                self.color.get(),
                level
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        if result.success:
            messagebox.showinfo("Success", f"Vehicle parked at slot {result.slot}")
        else:
            messagebox.showerror("Error", result.message)

    def show_status(self):
        self.output.delete("1.0", tk.END)
        self.output.insert(
            tk.END,
            "Slot\tLevel\tType\tRegNo\tColor\tMake\tModel\n"
        )
        for slot, lvl, vehicle in self.presenter.get_status():
            line = f"{slot}\t{lvl}\t{vehicle.getType()}\t{vehicle.regnum}\t{vehicle.color}\t{vehicle.make}\t{vehicle.model}"
            self.output.insert(tk.END, line + "\n")

    def remove_vehicle(self):
        try:
            slot_number = int(self.remove_slot.get())
            if slot_number <= 0:
                messagebox.showerror("Error", "Slot number must be positive")
                return
            
            success = self.presenter.remove_vehicle(slot_number)
            if success:
                messagebox.showinfo("Success", f"Vehicle removed from slot {slot_number}")
                self.show_status()
            else:
                messagebox.showerror("Error", "Slot is empty or invalid")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid slot number")

    def get_slots_by_color(self):
        color = self.query_color.get()
        if not color:
            messagebox.showerror("Error", "Please enter a color")
            return
        
        slots = self.presenter.get_slots_by_color(color)
        self.output.delete("1.0", tk.END)
        if slots:
            self.output.insert(tk.END, f"Slots with {color} vehicles:\n")
            for slot in slots:
                self.output.insert(tk.END, f"  Slot {slot}\n")
        else:
            self.output.insert(tk.END, f"No vehicles found with color: {color}")

    def get_regs_by_color(self):
        color = self.query_color.get()
        if not color:
            messagebox.showerror("Error", "Please enter a color")
            return
        
        regs = self.presenter.get_regs_by_color(color)
        self.output.delete("1.0", tk.END)
        if regs:
            self.output.insert(tk.END, f"Registration numbers with {color} vehicles:\n")
            for reg in regs:
                self.output.insert(tk.END, f"  {reg}\n")
        else:
            self.output.insert(tk.END, f"No vehicles found with color: {color}")

    def get_slot_by_reg(self):
        regnum = self.query_reg.get()
        if not regnum:
            messagebox.showerror("Error", "Please enter a registration number")
            return
        
        slot = self.presenter.get_slot_by_reg(regnum)
        self.output.delete("1.0", tk.END)
        if slot is not None:
            self.output.insert(tk.END, f"Vehicle Registration: {regnum}\nParked at Slot: {slot}")
        else:
            self.output.insert(tk.END, f"Vehicle with registration {regnum} not found")

    def start_charging(self):
        reg = self.charge_reg.get()
        if not reg:
            messagebox.showerror("Error", "Please enter registration number")
            return
        ok = self.presenter.start_charging(reg)
        if ok:
            messagebox.showinfo("Charging", f"Started charging for {reg}")
        else:
            messagebox.showerror("Error", "Failed to start charging")

    def stop_charging(self):
        reg = self.charge_reg.get()
        if not reg:
            messagebox.showerror("Error", "Please enter registration number")
            return
        ok = self.presenter.stop_charging(reg)
        if ok:
            messagebox.showinfo("Charging", f"Stopped charging for {reg}")
        else:
            messagebox.showerror("Error", "Failed to stop charging")

    def check_charge_status(self):
        reg = self.charge_reg.get()
        if not reg:
            messagebox.showerror("Error", "Please enter registration number")
            return
        status = self.presenter.get_charge_status(reg)
        if status is None:
            messagebox.showerror("Charging", "Charging service unavailable or vehicle not found")
            return
        messagebox.showinfo("Charging Status", str(status))