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
        self.root.geometry("650x600")
        self.root.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        self.reg = tk.StringVar()
        self.make = tk.StringVar()
        self.model = tk.StringVar()
        self.color = tk.StringVar()
        self.vehicle_category = tk.StringVar(value="Car")
        self.is_electric = tk.IntVar()

        tk.Label(self.root, text="Registration No").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.reg).grid(row=0, column=1)

        tk.Label(self.root, text="Make").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.make).grid(row=1, column=1)

        tk.Label(self.root, text="Model").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.model).grid(row=2, column=1)

        tk.Label(self.root, text="Color").grid(row=3, column=0)
        tk.Entry(self.root, textvariable=self.color).grid(row=3, column=1)
        tk.Label(self.root, text="Vehicle Type").grid(row=4, column=0)
        tk.OptionMenu(
            self.root,
            self.vehicle_category,
            "Car", "Motorcycle", "Bus"
        ).grid(row=4, column=1)

        tk.Checkbutton(
            self.root,
            text="Electric Vehicle",
            variable=self.is_electric
        ).grid(row=5, column=1)

        tk.Button(
            self.root,
            text="Park Vehicle",
            command=self.park_vehicle
        ).grid(row=6, column=1)

        tk.Button(
            self.root,
            text="Show Status",
            command=self.show_status
        ).grid(row=7, column=1)

        # Charging controls
        tk.Label(self.root, text="Charge RegNo").grid(row=9, column=0)
        self.charge_reg = tk.StringVar()
        tk.Entry(self.root, textvariable=self.charge_reg).grid(row=9, column=1)
        tk.Button(self.root, text="Start Charging", command=self.start_charging).grid(row=10, column=0)
        tk.Button(self.root, text="Stop Charging", command=self.stop_charging).grid(row=10, column=1)
        tk.Button(self.root, text="Check Charge Status", command=self.check_charge_status).grid(row=11, column=0, columnspan=2)

        self.output = tk.Text(self.root, width=70, height=15)
        self.output.grid(row=8, column=0, columnspan=2)

    def park_vehicle(self):
        factory = (
            ElectricVehicleFactory()
            if self.is_electric.get()
            else RegularVehicleFactory()
        )

        try:
            result = self.presenter.park_vehicle(
                factory,
                self.vehicle_category.get(),
                self.reg.get(),
                self.make.get(),
                self.model.get(),
                self.color.get()
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
            "Slot\tType\tRegNo\tColor\tMake\tModel\n"
        )
        for slot, level, vehicle in self.presenter.get_status():
            line = f"{slot}\t{vehicle.getType()}\t{vehicle.regnum}\t{vehicle.color}\t{vehicle.make}\t{vehicle.model}"
            self.output.insert(tk.END, line + "\n")

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