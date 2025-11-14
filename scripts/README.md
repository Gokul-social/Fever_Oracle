# Scripts

Utility scripts for data processing, ingestion, and real-time data generation using Kafka.

## Kafka Data Pipeline

### kafka_data_producer.py

Generates realistic raw data streams and publishes them to Kafka topics. This is the primary data generation system.

**Usage:**
```bash
# Run all producers (default)
python scripts/kafka_data_producer.py

# Run specific producer
python scripts/kafka_data_producer.py --topic wastewater --interval 60

# With custom Kafka server
python scripts/kafka_data_producer.py --bootstrap-servers localhost:9092
```

**Topics:**
- `fever-oracle-wastewater` - Wastewater viral load data
- `fever-oracle-pharmacy` - Pharmacy OTC sales data
- `fever-oracle-patients` - Patient records
- `fever-oracle-vitals` - Patient vital signs
- `fever-oracle-alerts` - System alerts
- `fever-oracle-outbreak` - Outbreak predictions

**Features:**
- Realistic data generation with temporal patterns
- Time-of-day and day-of-week effects
- Correlated data (e.g., fever affects heart rate)
- Configurable production intervals
- Multi-threaded production for all data types

### kafka_data_consumer.py

Consumes data from Kafka topics and stores in data files.

**Usage:**
```bash
python scripts/kafka_data_consumer.py
```

**Output Files:**
- `data/wastewater_demo.csv` - Wastewater data
- `data/otc_demo.csv` - Pharmacy data
- `data/patients_demo.jsonl` - Patient records
- `data/patient_vitals.jsonl` - Patient vitals
- `data/alerts_demo.jsonl` - Alert data
- `data/outbreak_predictions.jsonl` - Outbreak predictions

## Data Ingestion Scripts

### ingest_wastewater.py

Processes and ingests wastewater viral load data from CSV files.

**Usage:**
```bash
python scripts/ingest_wastewater.py
```

**Input:** `data/wastewater_demo.csv`
**Output:** `data/wastewater_processed.json`

### generate_synthetic_vitals.py

Generates synthetic patient vital signs data for testing and development.

**Usage:**
```bash
python scripts/generate_synthetic_vitals.py
```

**Output:** `data/patient_vitals.jsonl`

This script creates realistic patient vital sign records including:
- Temperature
- Heart rate
- Blood pressure
- Respiratory rate
- Oxygen saturation

## Kafka Setup

### Using Docker Compose

Kafka is automatically started with:
```bash
docker-compose up -d
```

This starts:
- Zookeeper (port 2181)
- Kafka (port 9092)
- Kafka Producer (generates data automatically)

### Manual Setup

1. **Start Kafka Producer:**
   ```bash
   python scripts/kafka_data_producer.py --topic all
   ```

2. **Start Kafka Consumer:**
   ```bash
   python scripts/kafka_data_consumer.py
   ```

### Data Generation Patterns

The Kafka producer generates realistic data with:
- **Temporal Patterns**: Morning/evening peaks, weekday/weekend variations
- **Correlated Data**: Fever affects heart rate, symptoms affect risk scores
- **Realistic Distributions**: Age-based comorbidities, region-based variations
- **Event-Based**: Random fever spikes, alert generation based on thresholds

