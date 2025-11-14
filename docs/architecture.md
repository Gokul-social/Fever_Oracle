# Fever Oracle Architecture

## Overview

Fever Oracle is a comprehensive healthcare monitoring system that uses machine learning to predict fever outbreaks and assess individual patient risk. The system integrates multiple data sources including wastewater monitoring, pharmacy sales, and patient vital signs.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  React + TypeScript + Vite + Tailwind CSS + shadcn/ui      │
│  - Dashboard                                                 │
│  - Patient Risk Assessment                                   │
│  - Alert Management                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP/REST API
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                      Backend Layer                           │
│  Flask REST API                                              │
│  - /api/patients                                             │
│  - /api/wastewater                                           │
│  - /api/pharmacy                                             │
│  - /api/outbreak/predictions                                 │
│  - /api/alerts                                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌─────▼──────┐ ┌────▼──────┐
│   Models     │ │   Data     │ │ Database  │
│              │ │            │ │           │
│ - Outbreak   │ │ - CSV      │ │ PostgreSQL│
│ - Patient    │ │ - JSONL    │ │           │
│   Twin       │ │            │ │           │
└──────────────┘ └────────────┘ └───────────┘
```

## Components

### Frontend (`frontend/`)

- **Technology Stack**: React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui
- **Key Features**:
  - Real-time dashboard with charts and metrics
  - Patient risk assessment interface
  - Alert management system
  - Responsive design for mobile and desktop

### Backend (`backend/`)

- **Technology Stack**: Flask, Python 3.11+, Blockchain
- **API Endpoints**:
  - `GET /api/health` - Health check
  - `GET /api/patients` - List all patients
  - `GET /api/patients/<id>` - Get specific patient
  - `GET /api/wastewater` - Wastewater viral load data
  - `GET /api/pharmacy` - Pharmacy OTC sales data
  - `GET /api/outbreak/predictions` - Outbreak predictions
  - `GET /api/alerts` - System alerts
  - `GET /api/dashboard/metrics` - Dashboard metrics
  - **Blockchain Endpoints**:
    - `GET /api/blockchain/info` - Blockchain information
    - `POST /api/blockchain/audit` - Add audit log
    - `GET /api/blockchain/audit-trail` - Get audit trail
    - `GET /api/blockchain/verify` - Verify blockchain integrity
    - `POST /api/blockchain/data-hash` - Store data integrity hash
    - `POST /api/blockchain/zk-proof` - Create zero-knowledge proof

### Models (`models/`)

#### Outbreak Prediction Model (`models/outbreak/`)
- Time series analysis for outbreak forecasting
- Multi-feature risk assessment
- Regional outbreak detection

#### Patient Digital Twin (`models/twin/`)
- Individual patient risk modeling
- Sequential ML for personalized risk assessment
- Real-time risk score calculation

### Data (`data/`)

- **wastewater_demo.csv**: Wastewater viral load monitoring data
- **otc_demo.csv**: Over-the-counter medication sales data
- **patients_demo.jsonl**: Patient records with vital signs and risk factors

### Scripts (`scripts/`)

- **ingest_wastewater.py**: Process and ingest wastewater data
- **generate_synthetic_vitals.py**: Generate synthetic patient vital signs for testing

## Data Flow

1. **Data Ingestion**: Scripts process raw data from various sources
2. **Model Processing**: ML models analyze data and generate predictions
3. **API Layer**: Backend exposes processed data via REST API
4. **Frontend Display**: React frontend visualizes data and predictions
5. **Alert Generation**: System generates alerts based on risk thresholds

## Deployment

### Docker Compose

The system can be deployed using Docker Compose:

```bash
docker-compose up -d
```

This starts:
- Backend API on port 5000
- Frontend on port 8080
- PostgreSQL database on port 5432

### Development Setup

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Security Considerations

- **Blockchain Technology**: Immutable audit logging and data integrity verification
- **Zero-Knowledge Proofs**: Privacy-preserving data verification without exposing sensitive information
- **CORS enabled** for frontend-backend communication
- **Environment variables** for sensitive configuration
- **Input validation** on API endpoints
- **HIPAA/GDPR compliant** with blockchain-based audit trails
- **Encrypted communications** with end-to-end encryption
- **Decentralized identity** management for enhanced privacy

## Blockchain Integration

The system uses blockchain technology for:

1. **Immutable Audit Logging**: All data access and modifications are logged on the blockchain, creating an unalterable audit trail
2. **Data Integrity Verification**: Data hashes are stored on-chain to verify data hasn't been tampered with
3. **Zero-Knowledge Proofs**: Privacy-preserving verification without exposing sensitive patient data
4. **Decentralized Trust**: No single point of failure for audit logs
5. **Compliance**: Meets HIPAA/GDPR requirements for audit logging and data integrity

### Blockchain Features

- **Proof of Work**: Blocks are mined with configurable difficulty
- **Chain Verification**: Automatic integrity checking
- **Privacy-Preserving**: Zero-knowledge proofs for sensitive operations
- **Audit Trail**: Complete history of all data access and modifications

## Future Enhancements

- Real-time WebSocket connections for live updates
- Authentication and authorization with blockchain-based identity
- Database integration for persistent storage
- Advanced ML models (LSTM, Transformer-based)
- Federated learning for cross-institutional collaboration
- GraphQL API for flexible data queries
- Smart contracts for automated access control
- Interoperable blockchain networks for multi-institutional trust

