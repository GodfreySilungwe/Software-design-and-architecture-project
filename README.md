# Electric Vehicle Parking Management System

A comprehensive software design and architecture project demonstrating enterprise-level design patterns, UML diagrams, and a proposed microservices architecture for an electric vehicle parking management system.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database Design](#database-design)
- [Design Patterns](#design-patterns)
- [UML Diagrams](#uml-diagrams)
- [Contributing](#contributing)

## 🎯 Overview

This project implements a complete parking management system with specialized support for electric vehicles (EVs). It showcases software design best practices including:

- **Design Patterns**: Factory Pattern, Mixin Pattern, Presenter Pattern
- **UML Documentation**: Structural, Behavioral, and Microservices Architecture diagrams
- **Service-Oriented Architecture**: Proposed microservices design with independent services, databases, and APIs
- **Clean Architecture**: Separation of concerns across domain, factory, services, and UI layers

The project includes both a current monolithic implementation and a proposed microservices architecture diagram for scalability and maintainability.

## ✨ Features

### Core Functionality
- 🅿️ **Parking Slot Management**: Reserve and release parking slots
- 🔌 **EV Charging Support**: Dedicated charging management for electric vehicles
- 🚗 **Vehicle Registration**: Support for regular and electric vehicles (cars and motorcycles)
- 📊 **Parking Status Monitoring**: Real-time availability tracking
- 🎨 **User Interface**: Tkinter-based GUI for easy interaction

### Vehicle Types Supported
- Regular Cars
- Regular Motorcycles
- Electric Cars (with charging capability)
- Electric Motorcycles (with charging capability)

### Advanced Capabilities
- Multi-level parking lot support
- Separate capacity tracking for EV slots
- Charging status monitoring
- Vehicle history tracking
- Extensible factory pattern for new vehicle types

## 🏗️ Architecture

### Current Monolithic Architecture

```
┌─────────────────────────────────────────┐
│         User Interface (Tkinter)        │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│    Parking Presenter (MVC Pattern)      │
├──────────────────────────────────────────┤
│  • Vehicle Factory                       │
│  • Parking Lot Management                │
│  • Charging Service Client               │
└────────────────────┬────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼─────────┐    ┌─────────▼────────┐
│  Domain Models  │    │  Services Layer  │
│  • Vehicle      │    │  • EV Charging   │
│  • Parking Lot  │    │  • Charging      │
│  • ElectricMixin│    │    Simulation    │
└─────────────────┘    └──────────────────┘
```

### Proposed Microservices Architecture

```
Client Applications
         │
         ▼
    API Gateway
         │
    ┌────┼────┬────┬────┐
    │    │    │    │    │
┌───▼──┐ ┌──▼──┐ ┌──▼──┐ ... (6 services)
│Parking│ │EV   │ │Vehicle
│Service│ │Charge│ │Service
└───┬──┘ └──┬──┘ └──┬──┘
    │       │       │
┌───▼──┐ ┌──▼──┐ ┌──▼──┐
│Park  │ │Charge│ │Vehicle
│DB    │ │DB    │ │DB
└──────┘ └──────┘ └──────┘
         │
    ┌────▼────┐
    │Message  │
    │Bus/Kafka│
    └─────────┘
```

See [UML_Microservices_Architecture.md](UML_Microservices_Architecture.md) for detailed microservices design.

## 📁 Project Structure

```
.
├── README.md                              # This file
├── main.py                                # Application entry point
├── UML_Structural_Diagram.md              # Class diagram documentation
├── UML_Behavioral_Diagram.md              # Sequence diagrams
├── UML_Microservices_Architecture.md      # Proposed microservices design
├── render_diagrams.py                     # Diagram rendering utility
├── render_microservices_diagram.py        # Microservices diagram renderer
├── export_diagrams.py                     # Export utility
│
├── domain/                                # Core domain models
│   ├── vehicle.py                         # Vehicle base class
│   ├── parking_lot.py                     # Parking lot management
│   └── electric_mixin.py                  # Electric vehicle mixin
│
├── factory/                               # Factory pattern implementation
│   ├── vehicle_factory.py                 # Abstract factory
│   ├── regular_vehicle_factory.py         # Regular vehicle factory
│   └── electric_vehicle_factory.py        # Electric vehicle factory
│
├── services/                              # Business services
│   ├── charging_client.py                 # EV charging client
│   ├── ev_charging_service.py             # Charging service implementation
│   └── __pycache__/
│
├── presenter/                             # MVC presenter layer
│   ├── parking_presenter.py               # Main presenter
│   └── __pycache__/
│
├── ui/                                    # User interface
│   ├── app.py                             # Tkinter GUI
│   └── __pycache__/
│
├── tools/                                 # Utility tools
│   └── test_status.py                     # Testing utilities
│
└── diagrams/                              # Generated UML diagrams
    ├── 00_Structural_Diagram.png
    ├── 01_Sequence_Diagram_1_Park_a_Regular_Vehicle.png
    ├── 02_Sequence_Diagram_2_View_Parking_Status.png
    ├── 03_Sequence_Diagram_3_Remove_Vehicle_from_Parking.png
    ├── 04_Sequence_Diagram_4_Park_an_Electric_Vehicle.png
    ├── 05_Class_Diagram.png
    ├── 06_Microservices_Architecture_Overview.png
    └── 07_Kubernetes_Deployment_Architecture.png
```

## 🛠️ Technologies Used

### Current Implementation
- **Language**: Python 3.x
- **GUI Framework**: Tkinter
- **Architecture Pattern**: MVC (Model-View-Controller) with Presenter
- **Design Patterns**: Factory, Mixin, Abstract Base Classes

### Proposed Microservices Stack
- **Services**: Python, FastAPI/Flask
- **API Gateway**: Kong or Nginx Ingress
- **Databases**: PostgreSQL (per-service)
- **Message Bus**: RabbitMQ or Apache Kafka
- **Cache**: Redis
- **Container Orchestration**: Kubernetes
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **CI/CD**: GitLab CI / GitHub Actions

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/GodfreySilungwe/Software-design-and-architecture-project.git
   cd Software-design-and-architecture-project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` doesn't exist, install necessary packages:
   ```bash
   pip install requests
   ```

## 🚀 Usage

### Running the Application

```bash
python main.py
```

This will launch the Tkinter GUI for the parking management system.

### Running Diagram Generation

Generate PNG diagrams from the Mermaid markdown files:

```bash
# Generate behavioral diagrams
python render_diagrams.py

# Generate microservices architecture diagrams
python render_microservices_diagram.py
```

## 📡 API Documentation

### Proposed Microservices APIs

#### Parking Management Service
- **Base URL**: `http://parking-service:3001`
- **Endpoints**:
  - `POST /parking/reserve` - Reserve a parking slot
  - `GET /parking/status` - Get all parking slots status
  - `GET /parking/slots/:id` - Get specific slot details
  - `DELETE /parking/release` - Release a parked vehicle
  - `GET /parking/history/:vehicleId` - Get parking history

#### EV Charging Service
- **Base URL**: `http://charging-service:3002`
- **Endpoints**:
  - `POST /charging/start` - Start charging session
  - `POST /charging/stop` - Stop charging session
  - `GET /charging/status/:vehicleId` - Get current charging status
  - `GET /charging/history/:vehicleId` - Get charging history
  - `GET /charging/rates` - Get current charging rates

#### Vehicle Registry Service
- **Base URL**: `http://vehicle-service:3003`
- **Endpoints**:
  - `POST /vehicles/register` - Register a new vehicle
  - `GET /vehicles/:vehicleId` - Get vehicle details
  - `PUT /vehicles/:vehicleId` - Update vehicle information
  - `GET /vehicles/search?type=electric` - Search vehicles by type
  - `GET /vehicles/:vehicleId/status` - Get vehicle operational status

#### Payment & Billing Service
- **Base URL**: `http://payment-service:3004`
- **Endpoints**:
  - `POST /payments/charge` - Charge customer account
  - `GET /payments/history/:customerId` - Get payment history
  - `POST /invoices/generate` - Generate invoice
  - `GET /billing/estimate` - Calculate billing estimate
  - `POST /payments/refund` - Process refund

#### Notification Service
- **Base URL**: `http://notification-service:3005`
- **Event-Driven** architecture subscribing to:
  - `parking.reserved`
  - `parking.released`
  - `charging.started`
  - `charging.completed`

#### Analytics Service
- **Base URL**: `http://analytics-service:3006`
- **Endpoints**:
  - `GET /analytics/usage` - Get usage statistics
  - `GET /analytics/revenue` - Get revenue metrics
  - `GET /metrics/health` - Get system health metrics

## 🗄️ Database Design

### Current Implementation
Single database with tables:
- `vehicles` - Vehicle records
- `parking_lots` - Parking lot configurations
- `parking_slots` - Individual parking slots
- `charging_sessions` - EV charging logs

### Proposed Microservices Databases

Each service has its own PostgreSQL database:

| Service | Database | Key Tables |
|---------|----------|-----------|
| Parking | `parking_postgres` | parking_slots, parking_reservations, parking_history |
| Charging | `charging_postgres` | charging_sessions, charging_history, charging_rates |
| Vehicle | `vehicle_postgres` | vehicles, vehicle_types, vehicle_registration |
| Payment | `payment_postgres` | payments, invoices, billing_rates, transactions |
| Notification | `notification_postgres` | notifications, notification_queue, templates |
| Analytics | `analytics_postgres` | usage_metrics, revenue_metrics, event_logs |

## 🏛️ Design Patterns

### 1. **Factory Pattern**
- **Location**: `factory/` directory
- **Purpose**: Create different vehicle types (Regular, Electric) and subtypes (Car, Motorcycle)
- **Benefit**: Encapsulates object creation logic, easy to extend for new vehicle types

### 2. **Mixin Pattern**
- **Location**: `domain/electric_mixin.py`
- **Purpose**: Add electric vehicle capabilities (charge, discharge) without inheritance
- **Benefit**: Flexible composition, avoid multiple inheritance complexities

### 3. **Presenter Pattern (MVP)**
- **Location**: `presenter/parking_presenter.py`
- **Purpose**: Separate UI logic from business logic
- **Benefit**: Testability, reusability, clear separation of concerns

### 4. **Strategy Pattern**
- **Implicit usage**: Vehicle factory selection based on vehicle type
- **Benefit**: Runtime algorithm selection

### 5. **Repository Pattern (Proposed)**
- **Usage in microservices**: Per-service data access layer
- **Benefit**: Database abstraction, easier to switch databases

## 📊 UML Diagrams

### Available Diagrams

1. **Structural (Class) Diagram**
   - Shows class hierarchies, relationships, and attributes
   - Generated: `diagrams/05_Class_Diagram.png`

2. **Behavioral (Sequence) Diagrams**
   - Diagram 1: Park a Regular Vehicle
   - Diagram 2: View Parking Status
   - Diagram 3: Remove Vehicle from Parking
   - Diagram 4: Park an Electric Vehicle

3. **Microservices Architecture**
   - Overview diagram with all 6 services, APIs, and databases
   - Kubernetes deployment architecture
   - Generated: `diagrams/06_Microservices_Architecture_Overview.png`
   - Generated: `diagrams/07_Kubernetes_Deployment_Architecture.png`

### Viewing Diagrams

All PNG diagrams are in the `diagrams/` folder. View in:
- Web browser
- Image viewer
- Markdown preview (in VS Code or GitHub)

See [UML_Structural_Diagram.md](UML_Structural_Diagram.md), [UML_Behavioral_Diagram.md](UML_Behavioral_Diagram.md), and [UML_Microservices_Architecture.md](UML_Microservices_Architecture.md) for source code.

## 🔄 Architecture Evolution

### Phase 1: Monolithic (Current)
- Single application
- All logic in one codebase
- Good for learning and prototyping

### Phase 2: Microservices (Proposed)
- 6 independent services
- Each service owns its database
- Event-driven communication
- Kubernetes deployment
- See [UML_Microservices_Architecture.md](UML_Microservices_Architecture.md)

### Migration Path
1. Extract charging logic → Charging Service
2. Extract vehicle management → Vehicle Service
3. Add Payment Service
4. Add Notification Service
5. Add Analytics Service
6. Deploy with API Gateway and Message Bus

## 🧪 Testing

```bash
# Run tests (if available)
python -m pytest tests/

# Or use provided test utility
python tools/test_status.py
```

## 📝 Key Classes and Interfaces

### Domain Models
- `Vehicle` (Abstract) - Base class for all vehicles
- `Car`, `Motorcycle` - Regular vehicles
- `ElectricCar`, `ElectricMotorcycle` - Electric vehicles
- `ElectricMixin` - Adds charging capabilities
- `ParkingLot` - Manages parking slots

### Factories
- `VehicleFactory` (Abstract) - Factory interface
- `RegularVehicleFactory` - Creates regular vehicles
- `ElectricVehicleFactory` - Creates electric vehicles

### Services
- `ChargingServiceClient` - EV charging interface
- `EVChargingService` - Charging implementation
- `ParkingPresenter` - Business logic orchestrator

### UI
- `ParkingUI` - Tkinter interface

## 📚 Documentation Files

- **UML_Structural_Diagram.md** - Class relationships and structure
- **UML_Behavioral_Diagram.md** - Sequence diagrams for key operations
- **UML_Microservices_Architecture.md** - Proposed microservices design with:
  - Architecture overview
  - Service endpoints
  - Database schemas
  - Deployment architecture
  - Technology stack

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Enhancement

- [ ] Implement REST API endpoints
- [ ] Add database layer
- [ ] Integrate actual EV charging service
- [ ] Implement payment processing
- [ ] Add comprehensive unit tests
- [ ] Migrate to microservices architecture
- [ ] Set up Kubernetes deployment configs
- [ ] Add monitoring and logging
- [ ] Implement authentication/authorization
- [ ] Add admin dashboard

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Godfrey Silungwe**

- GitHub: [@GodfreySilungwe](https://github.com/GodfreySilungwe)
- Project: [Software-design-and-architecture-project](https://github.com/GodfreySilungwe/Software-design-and-architecture-project)

## 📧 Contact & Support

For questions or issues:
- Open an issue on GitHub
- Check existing documentation in markdown files
- Review UML diagrams for architecture insights

## 🎓 Learning Outcomes

This project demonstrates:
- Software architecture and design patterns
- UML diagram creation and documentation
- Object-oriented programming principles
- Factory and Mixin patterns
- MVC/MVP architectural patterns
- Microservices architecture concepts
- Database design (per-service)
- Event-driven communication
- Kubernetes deployment concepts
- Python best practices

---

**Last Updated**: February 2026

**Project Status**: Active Development

For the latest changes and upcoming features, see the [GitHub repository](https://github.com/GodfreySilungwe/Software-design-and-architecture-project).
