#!/usr/bin/env python3
"""
Render Microservices Architecture diagrams to PNG
"""

import requests
import base64
from pathlib import Path

# Microservices Architecture Diagram
MICROSERVICES_DIAGRAM = '''graph TB
    Client["Client Applications"]
    
    subgraph APIGateway["API Gateway & Load Balancer"]
        Gateway["API Gateway"]
    end
    
    subgraph ParkingService["Parking Management Service"]
        ParkingAPI["REST API<br/>POST /parking/reserve<br/>GET /parking/status<br/>DELETE /parking/release"]
        ParkingBiz["Parking Business Logic"]
        ParkingDB[(Parking DB<br/>parking_postgres)]
    end
    
    subgraph ChargingService["EV Charging Service"]
        ChargingAPI["REST API<br/>POST /charging/start<br/>POST /charging/stop<br/>GET /charging/status"]
        ChargingBiz["Charging Business Logic"]
        ChargingDB[(Charging DB<br/>charging_postgres)]
    end
    
    subgraph VehicleService["Vehicle Registry Service"]
        VehicleAPI["REST API<br/>POST /vehicles/register<br/>GET /vehicles/:id<br/>PUT /vehicles/:id"]
        VehicleBiz["Vehicle Business Logic"]
        VehicleDB[(Vehicle DB<br/>vehicle_postgres)]
    end
    
    subgraph NotificationService["Notification Service"]
        NotificationAPI["Event Listeners<br/>charging.started<br/>charging.completed<br/>parking.reserved"]
        NotificationBiz["Notification Logic<br/>Email/SMS/Push"]
        NotificationDB[(Notification DB<br/>notification_postgres)]
    end
    
    subgraph PaymentService["Payment & Billing Service"]
        PaymentAPI["REST API<br/>POST /payments/charge<br/>GET /payments/history<br/>POST /invoices/generate"]
        PaymentBiz["Payment Business Logic"]
        PaymentDB[(Payment DB<br/>payment_postgres)]
    end
    
    subgraph Analytics["Analytics & Monitoring Service"]
        AnalyticsAPI["REST API<br/>GET /analytics/usage<br/>GET /analytics/revenue<br/>GET /metrics/health"]
        AnalyticsBiz["Analytics Logic"]
        AnalyticsDB[(Analytics DB<br/>analytics_postgres)]
    end
    
    subgraph MessageBus["Message Bus / Event Stream"]
        MessageQueue["RabbitMQ / Kafka<br/>Event Topics:<br/>parking.events<br/>charging.events<br/>vehicle.events<br/>payment.events"]
    end
    
    subgraph Cache["Cache Layer"]
        Redis["Redis Cache<br/>Vehicle Status<br/>Parking Slots<br/>Charging Rates"]
    end
    
    Client --> Gateway
    
    Gateway --> ParkingAPI
    Gateway --> ChargingAPI
    Gateway --> VehicleAPI
    Gateway --> PaymentAPI
    Gateway --> AnalyticsAPI
    
    ParkingAPI --> ParkingBiz
    ParkingBiz --> ParkingDB
    ParkingBiz --> Redis
    ParkingBiz --> MessageQueue
    
    ChargingAPI --> ChargingBiz
    ChargingBiz --> ChargingDB
    ChargingBiz --> Redis
    ChargingBiz --> MessageQueue
    
    VehicleAPI --> VehicleBiz
    VehicleBiz --> VehicleDB
    VehicleBiz --> Redis
    VehicleBiz --> MessageQueue
    
    PaymentAPI --> PaymentBiz
    PaymentBiz --> PaymentDB
    PaymentBiz --> MessageQueue
    
    MessageQueue --> NotificationAPI
    MessageQueue --> AnalyticsAPI
    
    NotificationAPI --> NotificationBiz
    NotificationBiz --> NotificationDB
    
    AnalyticsAPI --> AnalyticsBiz
    AnalyticsBiz --> AnalyticsDB
    
    style APIGateway fill:#ff9999
    style ParkingService fill:#99ccff
    style ChargingService fill:#99ff99
    style VehicleService fill:#ffcc99
    style NotificationService fill:#ff99ff
    style PaymentService fill:#ffff99
    style Analytics fill:#99ffff
    style MessageBus fill:#ffcccc
    style Cache fill:#ccffcc'''

# Deployment Architecture Diagram
DEPLOYMENT_DIAGRAM = '''graph TB
    subgraph Kubernetes["Kubernetes Cluster"]
        subgraph NS["Namespace: production"]
            ParkingSvc["Parking Service<br/>Pod Replicas: 3"]
            ChargingSvc["Charging Service<br/>Pod Replicas: 3"]
            VehicleSvc["Vehicle Service<br/>Pod Replicas: 2"]
            PaymentSvc["Payment Service<br/>Pod Replicas: 2"]
            NotificationSvc["Notification Service<br/>Pod Replicas: 2"]
            AnalyticsSvc["Analytics Service<br/>Pod Replicas: 1"]
        end
        
        subgraph Infra["Infrastructure Services"]
            RabbitMQ["RabbitMQ Cluster<br/>3 Nodes"]
            Redis["Redis Cluster<br/>3 Nodes"]
            APIGw["API Gateway<br/>Ingress Controller"]
        end
    end
    
    subgraph DBCluster["Database Cluster"]
        ParkingDB["parking_postgres"]
        ChargingDB["charging_postgres"]
        VehicleDB["vehicle_postgres"]
        PaymentDB["payment_postgres"]
        NotificationDB["notification_postgres"]
        AnalyticsDB["analytics_postgres"]
    end
    
    ParkingSvc --> ParkingDB
    ChargingSvc --> ChargingDB
    VehicleSvc --> VehicleDB
    PaymentSvc --> PaymentDB
    NotificationSvc --> NotificationDB
    AnalyticsSvc --> AnalyticsDB
    
    ParkingSvc --> RabbitMQ
    ChargingSvc --> RabbitMQ
    VehicleSvc --> RabbitMQ
    PaymentSvc --> RabbitMQ
    NotificationSvc --> RabbitMQ
    AnalyticsSvc --> RabbitMQ
    
    ParkingSvc --> Redis
    ChargingSvc --> Redis
    VehicleSvc --> Redis
    
    APIGw --> ParkingSvc
    APIGw --> ChargingSvc
    APIGw --> VehicleSvc
    APIGw --> PaymentSvc
    APIGw --> AnalyticsSvc
    
    style Kubernetes fill:#e1f5ff
    style Infra fill:#fff3e0
    style DBCluster fill:#f3e5f5
    style NS fill:#e0f2f1'''

def render_diagram(mermaid_code, output_path):
    """Render diagram using mermaid.ink service."""
    try:
        encoded = base64.b64encode(mermaid_code.encode()).decode()
        url = f"https://mermaid.ink/img/{encoded}"
        
        print(f"  Downloading...", end=" ", flush=True)
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_bytes(response.content)
            print(f"✓ Saved to {output_path}")
            return True
        else:
            print(f"✗ (HTTP {response.status_code})")
            return False
    except requests.exceptions.Timeout:
        print(f"✗ (Timeout)")
        return False
    except Exception as e:
        print(f"✗ ({e})")
        return False

def main():
    diagrams = [
        ("Microservices Architecture Overview", MICROSERVICES_DIAGRAM),
        ("Kubernetes Deployment Architecture", DEPLOYMENT_DIAGRAM),
    ]
    
    print("Rendering Microservices Architecture Diagrams...\n")
    
    output_dir = Path("diagrams")
    success_count = 0
    
    for i, (title, code) in enumerate(diagrams, 6):  # Start from 06 to continue numbering
        output_file = output_dir / f"{i:02d}_{title.replace(' ', '_')}.png"
        
        print(f"[{i-5}/{len(diagrams)}] {title}")
        print(f"  → {output_file}... ", end="", flush=True)
        
        if render_diagram(code, str(output_file)):
            success_count += 1
    
    print(f"\nResult: {success_count}/{len(diagrams)} diagrams rendered successfully")
    if success_count > 0:
        print(f"PNG files saved to ./{output_dir}/ directory")

if __name__ == "__main__":
    main()
