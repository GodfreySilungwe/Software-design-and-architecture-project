# Electric Vehicle Parking System - Microservices Architecture Diagram

## Proposed Microservices Architecture

```mermaid
graph TB
    Client["Client Applications"]
    
    subgraph APIGateway["API Gateway & Load Balancer"]
        Gateway["API Gateway"]
    end
    
    subgraph ParkingService["Parking Management Service"]
        ParkingAPI["REST API<br/>POST /parking/reserve<br/>GET /parking/status<br/>DELETE /parking/release"]
        ParkingBiz["Parking Business Logic"]
        ParkingDB[(Parking Database)]
    end
    
    subgraph ChargingService["EV Charging Service"]
        ChargingAPI["REST API<br/>POST /charging/start<br/>POST /charging/stop<br/>GET /charging/status"]
        ChargingBiz["Charging Business Logic"]
        ChargingDB[(Charging Database)]
    end
    
    subgraph NotificationService["Notification Service"]
        NotificationAPI["Event Listeners<br/>charging.started<br/>charging.completed<br/>parking.reserved"]
        NotificationBiz["Notification Logic<br/>Email/SMS/Push"]
        NotificationDB[(Notification Database)]
    end
    
    subgraph Analytics["Analytics & Monitoring Service"]
        AnalyticsAPI["REST API<br/>GET /analytics/usage<br/>GET /analytics/revenue<br/>GET /metrics/health"]
        AnalyticsBiz["Analytics Logic"]
        AnalyticsDB[(Analytics Database)]
    end
    
    subgraph MessageBus["Message Bus / Event Stream"]
        MessageQueue["Event Streaming Platform<br/>Event Topics:<br/>parking.events<br/>charging.events"]
    end
    
    subgraph Cache["Cache Layer"]
        CacheStore["Distributed Cache<br/>Parking Slots<br/>Charging Rates"]
    end
    
    Client --> Gateway
    
    Gateway --> ParkingAPI
    Gateway --> ChargingAPI
    Gateway --> AnalyticsAPI
    
    ParkingAPI --> ParkingBiz
    ParkingBiz --> ParkingDB
    ParkingBiz --> CacheStore
    ParkingBiz --> MessageQueue
    
    ChargingAPI --> ChargingBiz
    ChargingBiz --> ChargingDB
    ChargingBiz --> CacheStore
    ChargingBiz --> MessageQueue
    
    MessageQueue --> NotificationAPI
    MessageQueue --> AnalyticsAPI
    
    NotificationAPI --> NotificationBiz
    NotificationBiz --> NotificationDB
    
    AnalyticsAPI --> AnalyticsBiz
    AnalyticsBiz --> AnalyticsDB
    
    style APIGateway fill:#ff9999
    style ParkingService fill:#99ccff
    style ChargingService fill:#99ff99
    style NotificationService fill:#ff99ff
    style Analytics fill:#99ffff
    style MessageBus fill:#ffcccc
    style Cache fill:#ccffcc
```

## Service Details & Database Schema

### 1. **Parking Management Service**
- **Base URL**: `http://parking-service:3001`
- **Endpoints**:
  - `POST /parking/reserve` - Reserve a parking slot
  - `GET /parking/status` - Get all parking slots status
  - `GET /parking/slots/:id` - Get specific slot details
  - `DELETE /parking/release` - Release a parked vehicle
  - `GET /parking/history/:vehicleId` - Get parking history

- **Database**: Parking Database
  - Tables: `parking_slots`, `parking_reservations`, `parking_history`, `lot_configuration`

---

### 2. **EV Charging Service**
- **Base URL**: `http://charging-service:3002`
- **Endpoints**:
  - `POST /charging/start` - Start charging session
  - `POST /charging/stop` - Stop charging session
  - `GET /charging/status/:vehicleId` - Get current charging status
  - `GET /charging/history/:vehicleId` - Get charging history
  - `GET /charging/rates` - Get current charging rates

- **Database**: Charging Database
  - Tables: `charging_sessions`, `charging_history`, `charging_rates`, `charger_stations`

---

### 3. **Notification Service**
- **Base URL**: `http://notification-service:3003`
- **Event-Driven Architecture**
- **Listens to**:
  - `parking.reserved`
  - `parking.released`
  - `charging.started`
  - `charging.completed`
  - `charging.failed`

- **Database**: Notification Database
  - Tables: `notifications`, `notification_queue`, `notification_templates`, `user_preferences`

---

### 4. **Analytics & Monitoring Service**
- **Base URL**: `http://analytics-service:3004`
- **Endpoints**:
  - `GET /analytics/usage` - Get usage statistics
  - `GET /analytics/revenue` - Get revenue metrics
  - `GET /metrics/health` - Get system health metrics
  - `GET /analytics/peak-hours` - Get peak usage hours
  - `GET /analytics/vehicle-types` - Get vehicle type distribution

- **Database**: Analytics Database
  - Tables: `usage_metrics`, `revenue_metrics`, `system_health`, `event_logs`

---

## Infrastructure Components

### **API Gateway**
- Acts as single entry point for all clients
- Handles authentication, rate limiting, request routing
- Implements cross-cutting concerns (logging, security)

### **Message Bus (Event-Driven)**
- **Event Topics**:
  - `parking.events` - Parking reservation/release events
  - `charging.events` - Charging start/stop events

### **Cache Layer**
- **Cached Data**:
  - Active parking slots status
  - Charging rates

### **Databases**
- Separate instances for data isolation
- Each service owns its data schema
- Cross-service queries go through APIs only

---

## Communication Patterns

### Synchronous (Request-Response)
- Client → API Gateway → Service APIs
- Service-to-service communication for immediate responses
- REST/gRPC protocols

### Asynchronous (Event-Driven)
- Services publish events to Message Bus
- Notification and Analytics services consume events
- Decouples services, improves scalability

---

## Deployment Architecture

```mermaid
graph TB
    subgraph Kubernetes["Kubernetes Cluster"]
        subgraph NS["Namespace: production"]
            ParkingSvc["Parking Service<br/>Pod Replicas: 2"]
            ChargingSvc["Charging Service<br/>Pod Replicas: 2"]
            NotificationSvc["Notification Service<br/>Pod Replicas: 2"]
            AnalyticsSvc["Analytics Service<br/>Pod Replicas: 1"]
        end
        
        subgraph Infra["Infrastructure Services"]
            MessageBusCluster["Message Bus<br/>2 Nodes"]
            CacheCluster["Cache Cluster<br/>2 Nodes"]
            APIGw["API Gateway<br/>Ingress Controller"]
        end
    end
    
    subgraph DBCluster["Database Cluster"]
        ParkingDB["Parking Database"]
        ChargingDB["Charging Database"]
        NotificationDB["Notification Database"]
        AnalyticsDB["Analytics Database"]
    end
    
    ParkingSvc --> ParkingDB
    ChargingSvc --> ChargingDB
    NotificationSvc --> NotificationDB
    AnalyticsSvc --> AnalyticsDB
    
    ParkingSvc --> MessageBusCluster
    ChargingSvc --> MessageBusCluster
    NotificationSvc --> MessageBusCluster
    AnalyticsSvc --> MessageBusCluster
    
    ParkingSvc --> CacheCluster
    ChargingSvc --> CacheCluster
    
    APIGw --> ParkingSvc
    APIGw --> ChargingSvc
    APIGw --> AnalyticsSvc
    
    style Kubernetes fill:#e1f5ff
    style Infra fill:#fff3e0
    style DBCluster fill:#f3e5f5
    style NS fill:#e0f2f1
```

---

## Key Design Principles

1. **Single Responsibility**: Each service handles one business domain
2. **Database Per Service**: Data isolation and independence
3. **Event-Driven**: Async communication via message bus
4. **API-First**: All inter-service communication through APIs
5. **Scalability**: Services can be scaled independently
6. **Resilience**: Circuit breakers, retries, fallbacks
7. **Monitoring**: Centralized logging and metrics collection



