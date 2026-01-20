# Parking System - Class Diagram

```mermaid
classDiagram
    class Vehicle {
        <<abstract>>
        -regnum: str
        -make: str
        -model: str
        -color: str
        +__init__(regnum: str, make: str, model: str, color: str)
        +getType()* str
    }

    class Car {
        +getType() str
    }

    class Motorcycle {
        +getType() str
    }

    class ElectricMixin {
        -charge: int
        +__init__()
        +setCharge(charge: int)
        +getCharge() int
    }

    class ElectricCar {
        +getType() str
    }

    class ElectricMotorcycle {
        +getType() str
    }

    class VehicleFactory {
        <<abstract>>
        +create(vehicle_type: str, regnum: str, make: str, model: str, color: str)* Vehicle
    }

    class RegularVehicleFactory {
        +create(vehicle_type: str, regnum: str, make: str, model: str, color: str) Vehicle
    }

    class ElectricVehicleFactory {
        +create(vehicle_type: str, regnum: str, make: str, model: str, color: str) Vehicle
    }

    class ParkingLot {
        -capacity: int
        -ev_capacity: int
        -level: int
        -slots: list
        -ev_slots: list
        +__init__(capacity: int, ev_capacity: int, level: int)
        +get_empty_slot(ev: bool) Optional~int~
        +park(vehicle: Vehicle, ev: bool, level: int) Optional~int~
        +leave(slot_id: int, ev: bool) bool
        +status() List~Tuple~
        +create_lot(capacity: int, ev_capacity: int, level: int)
        +get_slots_by_color(color: str) List~int~
        +get_slot_by_reg(regnum: str) Optional~int~
        +get_regs_by_color(color: str) List~str~
    }

    class ParkResult {
        <<dataclass>>
        +success: bool
        +slot: int | None
        +message: str
    }

    class ParkingPresenter {
        -parking_lot: ParkingLot
        -regular_factory: RegularVehicleFactory
        -electric_factory: ElectricVehicleFactory
        -charging_client: ChargingClient
        +__init__(parking_lot, regular_factory, electric_factory, charging_client)
        +create_lot(capacity: int, ev_capacity: int, level: int)
        +park_vehicle(factory, vehicle_type: str, regnum, make, model, color, level: int) ParkResult
        +remove_vehicle(slot_number: int) bool
        +get_status() List~Tuple~
        +get_slots_by_color(color: str) List~int~
        +get_slot_by_reg(regnum: str) Optional~int~
        +get_regs_by_color(color: str) List~str~
        +start_charging(regnum: str) bool
        +stop_charging(regnum: str) bool
        +get_charge_status(regnum: str) dict
    }

    class ParkingUI {
        -root: tk.Tk
        -presenter: ParkingPresenter
        -capacity: tk.StringVar
        -ev_capacity: tk.StringVar
        -level: tk.StringVar
        -reg: tk.StringVar
        -make: tk.StringVar
        -model: tk.StringVar
        -color: tk.StringVar
        -vehicle_category: tk.StringVar
        -is_electric: tk.IntVar
        -park_level: tk.StringVar
        -remove_slot: tk.StringVar
        -query_color: tk.StringVar
        -query_reg: tk.StringVar
        -charge_reg: tk.StringVar
        -output: tk.Text
        +__init__(root: tk.Tk, presenter: ParkingPresenter)
        -_build_ui()
        +create_parking_lot()
        +park_vehicle()
        +remove_vehicle()
        +show_status()
        +get_slots_by_color()
        +get_regs_by_color()
        +get_slot_by_reg()
        +start_charging()
        +stop_charging()
        +check_charge_status()
    }

    class ChargingClient {
        +start_charging(regnum: str)
        +stop_charging(regnum: str)
        +get_status(regnum: str) dict
    }

    class EVChargingService {
        -clients: dict
        +start_charging(regnum: str)
        +stop_charging(regnum: str)
        +get_status(regnum: str) dict
    }

    %% Inheritance relationships
    Vehicle <|-- Car
    Vehicle <|-- Motorcycle
    Car <|-- ElectricCar
    Motorcycle <|-- ElectricMotorcycle
    ElectricMixin <|-- ElectricCar
    ElectricMixin <|-- ElectricMotorcycle

    VehicleFactory <|-- RegularVehicleFactory
    VehicleFactory <|-- ElectricVehicleFactory

    %% Association relationships
    ParkingLot "1" --> "0..*" Vehicle : contains
    ParkingLot --> ParkResult : returns

    ParkingPresenter "1" --> "1" ParkingLot : uses
    ParkingPresenter --> "1" RegularVehicleFactory : uses
    ParkingPresenter --> "1" ElectricVehicleFactory : uses
    ParkingPresenter --> "1" ChargingClient : delegates to

    ParkingUI "1" --> "1" ParkingPresenter : delegates to
    ParkingUI --> RegularVehicleFactory : instantiates
    ParkingUI --> ElectricVehicleFactory : instantiates

    ChargingClient --> EVChargingService : communicates
```

## Legend

| Symbol | Meaning |
|--------|---------|
| `<<abstract>>` | Abstract class |
| `<<dataclass>>` | Python dataclass |
| `-` | Private attribute/method |
| `+` | Public attribute/method |
| `<\|--` | Inheritance (is-a) |
| `-->` | Association (uses) |
| `"1" --> "0..*"` | One-to-many relationship |
