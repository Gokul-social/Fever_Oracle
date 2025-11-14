#!/usr/bin/env python3
"""
Kafka Data Consumer
Consumes data from Kafka topics and stores in data files
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import os

try:
    from kafka import KafkaConsumer
    from kafka.errors import KafkaError
except ImportError:
    print("kafka-python not installed. Install with: pip install kafka-python")
    sys.exit(1)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Topics
TOPICS = {
    'wastewater': 'fever-oracle-wastewater',
    'pharmacy': 'fever-oracle-pharmacy',
    'patients': 'fever-oracle-patients',
    'vitals': 'fever-oracle-vitals',
    'alerts': 'fever-oracle-alerts',
    'outbreak': 'fever-oracle-outbreak'
}


class KafkaDataConsumer:
    """Kafka consumer for processing data streams"""
    
    def __init__(self, bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS):
        self.consumer = KafkaConsumer(
            *list(TOPICS.values()),
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='fever-oracle-consumers'
        )
        self.data_dir = DATA_DIR
    
    def consume_wastewater(self, message):
        """Process wastewater data"""
        data = message.value
        # Append to CSV file
        csv_file = self.data_dir / "wastewater_demo.csv"
        
        # Check if file exists and has header
        file_exists = csv_file.exists()
        
        with open(csv_file, 'a') as f:
            if not file_exists:
                f.write("date,viral_load,threshold,region\n")
            f.write(f"{data['timestamp'].split('T')[0]},{data['viral_load']},{data['threshold']},{data['region']}\n")
    
    def consume_pharmacy(self, message):
        """Process pharmacy data"""
        data = message.value
        csv_file = self.data_dir / "otc_demo.csv"
        
        file_exists = csv_file.exists()
        
        with open(csv_file, 'a') as f:
            if not file_exists:
                f.write("date,sales_index,baseline,region\n")
            f.write(f"{data['timestamp'].split('T')[0]},{data['sales_index']},{data['baseline']},{data['region']}\n")
    
    def consume_patients(self, message):
        """Process patient data"""
        data = message.value
        jsonl_file = self.data_dir / "patients_demo.jsonl"
        
        with open(jsonl_file, 'a') as f:
            f.write(json.dumps(data) + '\n')
    
    def consume_vitals(self, message):
        """Process patient vitals"""
        data = message.value
        jsonl_file = self.data_dir / "patient_vitals.jsonl"
        
        with open(jsonl_file, 'a') as f:
            f.write(json.dumps(data) + '\n')
    
    def consume_alerts(self, message):
        """Process alert data"""
        data = message.value
        jsonl_file = self.data_dir / "alerts_demo.jsonl"
        
        with open(jsonl_file, 'a') as f:
            f.write(json.dumps(data) + '\n')
    
    def consume_outbreak(self, message):
        """Process outbreak predictions"""
        data = message.value
        jsonl_file = self.data_dir / "outbreak_predictions.jsonl"
        
        with open(jsonl_file, 'a') as f:
            f.write(json.dumps(data) + '\n')
    
    def start_consuming(self):
        """Start consuming messages from all topics"""
        print(f"Starting Kafka consumer. Listening to topics: {list(TOPICS.values())}")
        print(f"Data will be saved to: {self.data_dir}")
        
        topic_handlers = {
            TOPICS['wastewater']: self.consume_wastewater,
            TOPICS['pharmacy']: self.consume_pharmacy,
            TOPICS['patients']: self.consume_patients,
            TOPICS['vitals']: self.consume_vitals,
            TOPICS['alerts']: self.consume_alerts,
            TOPICS['outbreak']: self.consume_outbreak,
        }
        
        try:
            for message in self.consumer:
                topic = message.topic
                handler = topic_handlers.get(topic)
                if handler:
                    handler(message)
                    print(f"Processed message from {topic}")
        except KeyboardInterrupt:
            print("\nStopping consumer...")
        finally:
            self.consumer.close()


def main():
    """Main function"""
    consumer = KafkaDataConsumer()
    consumer.start_consuming()


if __name__ == "__main__":
    main()

