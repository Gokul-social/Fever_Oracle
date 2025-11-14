# Kafka Monitor Page Guide

## Overview

The Kafka Monitor page (`/kafka-monitor`) provides real-time monitoring of the Kafka data pipeline and ML model predictions. It demonstrates the effective use of Kafka for data streaming and model integration.

## Features

### 1. Kafka Data Pipeline Monitor
- **Real-time Statistics**: Shows message throughput (messages/minute) for each Kafka topic
- **Topic Status**: Displays active/idle status for each topic with visual indicators
- **Total Throughput**: Aggregated message rate across all topics
- **Auto-refresh**: Updates every 5 seconds

### 2. Real-time Data Stream
- **Live Messages**: Displays incoming messages from all Kafka topics
- **Color-coded Topics**: Each topic type has a distinct color for easy identification
- **Message History**: Shows last 50 messages with timestamps
- **Auto-update**: Refreshes every 3 seconds

### 3. Model Predictions
- **Manual Prediction**: Click "Run Prediction" to analyze latest Kafka data
- **Auto-run Mode**: Enable automatic predictions every 30 seconds
- **Risk Assessment**: Shows risk level, score, and confidence
- **Contributing Factors**: Displays wastewater and pharmacy trends
- **Blockchain Logging**: All predictions are logged to blockchain

## How It Works

1. **Kafka Producer** generates realistic healthcare data and publishes to topics
2. **Kafka Consumer** (backend) monitors topics and tracks statistics
3. **Model Endpoint** processes latest Kafka data for predictions
4. **Frontend** displays real-time updates from all components

## API Endpoints

- `GET /api/kafka/stats` - Get Kafka statistics
- `GET /api/kafka/latest-data` - Get latest messages from topics
- `POST /api/model/predict` - Run ML prediction on Kafka data

## Configuration

Kafka topics are configured in `backend/config/kafka_topics.json`:
- Topic names and descriptions
- Partition and replication settings
- Retention policies

## Troubleshooting

### No Data Showing
1. Ensure Kafka is running: `docker-compose up -d` or start Kafka manually
2. Start Kafka producer: `python scripts/kafka_data_producer.py`
3. Check backend logs for connection errors

### JSON Parsing Errors
- Backend should always return JSON (now fixed)
- Check browser console for detailed error messages
- Verify backend is running on port 5000

### Kafka Unavailable
- Install kafka-python: `pip install kafka-python`
- Check Kafka bootstrap servers configuration
- Verify Kafka is accessible on configured port

