# Parking System - Structural (Class) Diagram

```mermaid
classDiagram
    class ParkResult {
        <<dataclass>>
        +success: bool
        +slot: int | None
        +message: str
    }

    class Vehicle {
        <<abstract>>
        -regnum: str
        -make: str
        -model: str
        -color: str
        +__init__(regnum: str, make: str, model: str, color: str) None
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
        +__init__() None
        +setCharge(charge: int) None
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
        +__init__(capacity: int, ev_capacity: int, level: int) None
        +get_empty_slot(ev: bool) Optional~int~
        +park(vehicle: Vehicle, ev: bool, level: int) Optional~int~
        +leave(slot_id: int, ev: bool) bool
        +status() List~Tuple~
        +create_lot(capacity: int, ev_capacity: int, level: int) None
        +get_slots_by_color(color: str) List~int~
        +get_slot_by_reg(regnum: str) Optional~int~
        +get_regs_by_color(color: str) List~str~
    }

    class ParkingPresenter {
        -parking_lot: ParkingLot
        -regular_factory: RegularVehicleFactory
        -electric_factory: ElectricVehicleFactory
        -charging_client: ChargingClient
        +__init__(parking_lot, regular_factory, electric_factory, charging_client) None
        +create_lot(capacity: int, ev_capacity: int, level: int) None
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
        +__init__(root: tk.Tk, presenter: ParkingPresenter) None
        -_build_ui() None
        +park_vehicle() None
        +remove_vehicle() None
        +show_status() None
    }

    class ChargingClient {
        +start_charging(regnum: str) None
        +stop_charging(regnum: str) None
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

    %% Dependency and Association relationships
    RegularVehicleFactory ..> Car : creates
    RegularVehicleFactory ..> Motorcycle : creates
    ElectricVehicleFactory ..> ElectricCar : creates
    ElectricVehicleFactory ..> ElectricMotorcycle : creates
    
    ParkingLot "1" --> "0..*" Vehicle : contains
    ParkingLot --> ParkResult : returns
    
    ParkingPresenter "1" --> "1" ParkingLot : uses
    ParkingPresenter --> RegularVehicleFactory : uses
    ParkingPresenter --> ElectricVehicleFactory : uses
    ParkingPresenter --> ChargingClient : delegates to
    ParkingUI "1" --> "1" ParkingPresenter : delegates to
```

## Symbol Legend

| Symbol | Meaning |
|--------|---------|
| `<<abstract>>` | Abstract class |
| `<<dataclass>>` | Python dataclass |
| `-` | Private attribute/method |
| `+` | Public attribute/method |
| `#` | Protected attribute/method |
| `<\|--` | Inheritance (is-a) |
| `-->` | Association (uses) |
| `..>` | Dependency |
