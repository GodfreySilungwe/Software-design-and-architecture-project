# Parking System - Behavioral (Sequence) Diagrams

## Sequence Diagram 1: Park a Regular Vehicle

```mermaid
sequenceDiagram
    participant User
    participant ParkingUI
    participant Factory as RegularVehicleFactory
    participant Presenter as ParkingPresenter
    participant ParkingLot
    participant Vehicle as Car

    User->>ParkingUI: park_vehicle()
    activate ParkingUI
    
    ParkingUI->>ParkingUI: Get input: regnum, make,<br/>model, color, vehicle_type
    
    ParkingUI->>Factory: create(vehicle_type, regnum, make, model, color)
    activate Factory
    Factory->>Vehicle: __init__(regnum, make, model, color)
    activate Vehicle
    Vehicle->>Vehicle: Set attributes
    deactivate Vehicle
    Factory-->>ParkingUI: Car instance
    deactivate Factory
    
    ParkingUI->>Presenter: park_vehicle(factory, vehicle_type,<br/>regnum, make, model, color)
    activate Presenter
    
    Presenter->>Factory: create(vehicle_type, regnum, make, model, color)
    activate Factory
    Factory-->>Presenter: Vehicle instance
    deactivate Factory
    
    Presenter->>ParkingLot: park(vehicle, ev=False)
    activate ParkingLot
    
    ParkingLot->>ParkingLot: get_empty_slot(ev=False)
    alt Slot Available
        ParkingLot->>ParkingLot: slots[slot] = vehicle
        ParkingLot-->>Presenter: slot + 1
    else No Available Slot
        ParkingLot-->>Presenter: None
    end
    deactivate ParkingLot
    
    alt Success
        Presenter-->>ParkingUI: ParkResult(True, slot, "")
    else Full
        Presenter-->>ParkingUI: ParkResult(False, None, "Parking is full")
    end
    deactivate Presenter
    
    alt Success
        ParkingUI->>User: "Vehicle parked at slot X"
    else Full
        ParkingUI->>User: "Parking lot is full"
    end
    deactivate ParkingUI
```

## Sequence Diagram 2: View Parking Status

```mermaid
sequenceDiagram
    participant User
    participant ParkingUI
    participant Presenter as ParkingPresenter
    participant ParkingLot
    participant Vehicle

    User->>ParkingUI: show_status()
    activate ParkingUI
    
    ParkingUI->>Presenter: get_status()
    activate Presenter
    
    Presenter->>ParkingLot: status()
    activate ParkingLot
    
    loop For each occupied slot (regular and EV)
        ParkingLot->>Vehicle: getType()
        Vehicle-->>ParkingLot: type
        
        ParkingLot->>Vehicle: regnum
        ParkingLot->>Vehicle: make
        ParkingLot->>Vehicle: model
        ParkingLot->>Vehicle: color
    end
    
    ParkingLot-->>Presenter: List[Tuple(slot, level, vehicle)]
    deactivate ParkingLot
    
    Presenter-->>ParkingUI: status data
    deactivate Presenter
    
    ParkingUI->>User: Display vehicle details
    deactivate ParkingUI
```

## Sequence Diagram 3: Remove Vehicle from Parking

```mermaid
sequenceDiagram
    participant User
    participant ParkingUI
    participant Presenter as ParkingPresenter
    participant ParkingLot

    User->>ParkingUI: remove_vehicle(slot_number)
    activate ParkingUI
    
    ParkingUI->>Presenter: remove_vehicle(slot_number)
    activate Presenter
    
    Presenter->>ParkingLot: leave(slot_id, ev=False)
    activate ParkingLot
    
    alt Slot number is invalid or out of range
        ParkingLot-->>Presenter: False
    else Slot is empty
        ParkingLot-->>Presenter: False
    else Vehicle exists
        ParkingLot->>ParkingLot: slots[index] = None
        ParkingLot-->>Presenter: True
    end
    deactivate ParkingLot
    
    Presenter-->>ParkingUI: success status
    deactivate Presenter
    
    alt Success
        ParkingUI->>User: "Vehicle removed successfully"
    else Failure
        ParkingUI->>User: "Slot is empty or invalid"
    end
    deactivate ParkingUI
```

## Sequence Diagram 4: Park an Electric Vehicle

```mermaid
sequenceDiagram
    participant User
    participant ParkingUI
    participant Factory as ElectricVehicleFactory
    participant Presenter as ParkingPresenter
    participant ParkingLot
    participant Vehicle as ElectricCar
    participant Mixin as ElectricMixin

    User->>ParkingUI: park_vehicle(is_electric=True)
    activate ParkingUI
    
    ParkingUI->>ParkingUI: Get input: regnum, make,<br/>model, color, vehicle_type
    
    ParkingUI->>Factory: create(vehicle_type, regnum, make, model, color)
    activate Factory
    
    Factory->>Vehicle: __init__(regnum, make, model, color)
    activate Vehicle
    
    Vehicle->>Vehicle: Car.__init__()
    Vehicle->>Mixin: ElectricMixin.__init__()
    activate Mixin
    Mixin->>Mixin: charge = 0
    deactivate Mixin
    deactivate Vehicle
    
    Factory-->>ParkingUI: ElectricCar instance
    deactivate Factory
    
    ParkingUI->>Presenter: park_vehicle(factory, vehicle_type,<br/>regnum, make, model, color)
    activate Presenter
    
    Presenter->>Factory: create(vehicle_type, regnum, make, model, color)
    activate Factory
    Factory-->>Presenter: ElectricCar instance
    deactivate Factory
    
    Presenter->>Presenter: hasattr(vehicle, "getCharge") → True
    
    Presenter->>ParkingLot: park(vehicle, ev=True)
    activate ParkingLot
    ParkingLot->>ParkingLot: get_empty_slot(ev=True)
    ParkingLot->>ParkingLot: ev_slots[slot] = vehicle
    ParkingLot-->>Presenter: slot + 1
    deactivate ParkingLot
    
    Presenter-->>ParkingUI: ParkResult(True, slot, "")
    deactivate Presenter
    
    ParkingUI->>User: "Electric vehicle parked at slot X"
    deactivate ParkingUI
```
