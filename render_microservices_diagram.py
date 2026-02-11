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
    style Cache fill:#ccffcc'''

# Deployment Architecture Diagram
DEPLOYMENT_DIAGRAM = '''graph TB
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
    style NS fill:#e0f2f1'''

# Multi-Facility Architecture Diagram
MULTI_FACILITY_DIAGRAM = '''graph TB
    Clients["Client Applications<br/>(Mobile, Web, Desktop)"]
    
    subgraph APIGateway["API Gateway & Service Discovery"]
        Gateway["API Gateway<br/>(Kong/Nginx)<br/>Routes by facility_id"]
        ServiceReg["Service Registry<br/>(Consul/Eureka)"]
    end
    
    subgraph FacilityCluster["Facility Management Layer"]
        FacilityService["Facility Service<br/>Manages metadata<br/>locations, configs"]
        FacilityDB["Facility Registry DB<br/>facilities_postgres"]
    end
    
    subgraph ParkingServices["Parking Services - Multi-Facility"]
        ParkingAPI["Parking API<br/>facility-aware<br/>/v2/facilities/:id/..."]
        ParkingBiz["Business Logic<br/>per-facility ops"]
        ParkingDBCluster["DB Shard Cluster<br/>parking_shard_1,2,3..."]
    end
    
    subgraph ChargingServices["Charging Services - Multi-Facility"]
        ChargingAPI["Charging API<br/>facility-aware<br/>/v2/facilities/:id/..."]
        ChargingBiz["Business Logic<br/>per-facility ops"]
        ChargingDBCluster["DB Shard Cluster<br/>charging_shard_1,2,3..."]
    end
    
    subgraph MessageBus["Message Bus / Event Streaming"]
        MessageQueue["RabbitMQ / Kafka<br/>Partitioned by facility_id<br/>parking.events.X<br/>charging.events.Y"]
    end
    
    subgraph CachingLayer["Distributed Cache Layer"]
        Redis["Redis Cluster<br/>Facility cache keys<br/>facility:downtown:slots"]
    end
    
    Clients --> Gateway
    Gateway --> ServiceReg
    ServiceReg --> ParkingAPI
    ServiceReg --> ChargingAPI
    ServiceReg --> FacilityService
    
    Gateway --> FacilityService
    FacilityService --> FacilityDB
    
    Gateway --> ParkingAPI
    ParkingAPI --> ParkingBiz
    ParkingBiz --> ParkingDBCluster
    ParkingBiz --> Redis
    ParkingBiz --> MessageQueue
    
    Gateway --> ChargingAPI
    ChargingAPI --> ChargingBiz
    ChargingBiz --> ChargingDBCluster
    ChargingBiz --> Redis
    ChargingBiz --> MessageQueue
    
    MessageQueue --> MessageQueue
    
    style APIGateway fill:#ff6b6b
    style FacilityCluster fill:#ffd43b
    style ParkingServices fill:#74c0fc
    style ChargingServices fill:#69db7c
    style MessageBus fill:#ffa94d
    style CachingLayer fill:#90ee90'''

# Multi-Facility Deployment Architecture Diagram
MULTI_FACILITY_DEPLOYMENT_DIAGRAM = '''graph TB
    subgraph K8S["Kubernetes Multi-Cluster"]
        subgraph Region1["Region 1: US-West"]
            subgraph NS1["Namespace: us-west"]
                ParkingDC1["Parking Service<br/>Replicas: 3<br/>facility filter"]
                ChargingDC1["Charging Service<br/>Replicas: 3<br/>facility filter"]
            end
            DBR1["Database Shard 1<br/>parking_shard_1<br/>charging_shard_1"]
        end
        
        subgraph Region2["Region 2: US-East"]
            subgraph NS2["Namespace: us-east"]
                ParkingDC2["Parking Service<br/>Replicas: 3<br/>facility filter"]
                ChargingDC2["Charging Service<br/>Replicas: 3<br/>facility filter"]
            end
            DBR2["Database Shard 2<br/>parking_shard_2<br/>charging_shard_2"]
        end
        
        subgraph Central["Central Services"]
            APIGw["API Gateway<br/>Global"]
            MsgBus["RabbitMQ Cluster<br/>Partitioned"]
            RedisGlobal["Redis Cluster<br/>Global"]
            FacilityDB["Facility Registry<br/>Replicated"]
        end
    end
    
    ParkingDC1 --> DBR1
    ChargingDC1 --> DBR1
    
    ParkingDC2 --> DBR2
    ChargingDC2 --> DBR2
    
    ParkingDC1 --> RedisGlobal
    ParkingDC2 --> RedisGlobal
    
    ParkingDC1 --> MsgBus
    ChargingDC1 --> MsgBus
    ParkingDC2 --> MsgBus
    ChargingDC2 --> MsgBus
    
    APIGw --> ParkingDC1
    APIGw --> ChargingDC1
    APIGw --> ParkingDC2
    APIGw --> ChargingDC2
    
    MsgBus --> FacilityDB
    APIGw --> FacilityDB
    
    style Region1 fill:#e3f2fd
    style Region2 fill:#f3e5f5
    style Central fill:#fff3e0
    style K8S fill:#f0f0f0'''

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
        ("Multi-Facility Architecture Overview", MULTI_FACILITY_DIAGRAM),
        ("Multi-Facility Deployment Architecture", MULTI_FACILITY_DEPLOYMENT_DIAGRAM),
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
