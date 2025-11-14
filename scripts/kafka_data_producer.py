#!/usr/bin/env python3
"""
Kafka Data Producer
Generates realistic raw data streams for Fever Oracle system
Produces data to Kafka topics for real-time processing
"""

import json
import time
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import os

try:
    from kafka import KafkaProducer
    from kafka.errors import KafkaError
except ImportError:
    print("kafka-python not installed. Install with: pip install kafka-python")
    sys.exit(1)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Topics
TOPICS = {
    'wastewater': 'fever-oracle-wastewater',
    'pharmacy': 'fever-oracle-pharmacy',
    'patients': 'fever-oracle-patients',
    'vitals': 'fever-oracle-vitals',
    'alerts': 'fever-oracle-alerts',
    'outbreak': 'fever-oracle-outbreak'
}

class RealisticDataGenerator:
    """Generate realistic healthcare data"""
    
    def __init__(self):
        self.regions = ["Northeast", "Central", "West", "South", "Northwest"]
        self.patient_names = [
            "Sarah Johnson", "Michael Chen", "Emily Rodriguez", "David Kim",
            "Lisa Anderson", "Robert Taylor", "Jennifer Martinez", "James Wilson",
            "Maria Garcia", "William Brown", "Patricia Davis", "Richard Miller"
        ]
        self.comorbidities_list = [
            "Diabetes Type 2", "Hypertension", "COPD", "Autoimmune disorder",
            "Asthma", "Heart Disease", "Obesity", "Chronic Kidney Disease"
        ]
        self.symptoms_list = [
            "Fever", "Fatigue", "Cough", "Headache", "Shortness of breath",
            "Body aches", "Chills", "Sore throat", "Runny nose"
        ]
    
    def generate_wastewater_data(self) -> Dict:
        """Generate realistic wastewater viral load data"""
        region = random.choice(self.regions)
        base_load = 45 + random.uniform(-10, 10)
        
        # Add realistic trends (morning/evening variations, weekly patterns)
        hour = datetime.now().hour
        time_factor = 1.0
        if 6 <= hour <= 10:  # Morning peak
            time_factor = 1.15
        elif 18 <= hour <= 22:  # Evening peak
            time_factor = 1.10
        
        # Weekly pattern (higher on weekdays)
        day_of_week = datetime.now().weekday()
        if day_of_week < 5:  # Weekday
            time_factor *= 1.05
        
        viral_load = max(20, min(100, base_load * time_factor + random.uniform(-5, 5)))
        
        return {
            'timestamp': datetime.now().isoformat(),
            'region': region,
            'viral_load': round(viral_load, 2),
            'threshold': 70.0,
            'sample_location': f"{region}_Treatment_Plant_{random.randint(1, 3)}",
            'collection_method': random.choice(['Composite', 'Grab', '24h Composite']),
            'temperature_c': round(20 + random.uniform(-2, 2), 1),
            'ph_level': round(7.0 + random.uniform(-0.5, 0.5), 2)
        }
    
    def generate_pharmacy_data(self) -> Dict:
        """Generate realistic pharmacy OTC sales data"""
        region = random.choice(self.regions)
        base_sales = 75 + random.uniform(-15, 15)
        
        # Day of week effect (higher sales on weekends)
        day_of_week = datetime.now().weekday()
        if day_of_week >= 5:  # Weekend
            base_sales *= 1.2
        
        # Time of day effect (higher in afternoon/evening)
        hour = datetime.now().hour
        if 14 <= hour <= 20:
            base_sales *= 1.15
        
        sales_index = max(50, min(150, base_sales + random.uniform(-10, 10)))
        
        # Product categories
        categories = {
            'fever_reducers': round(sales_index * 0.35, 2),
            'cough_suppressants': round(sales_index * 0.25, 2),
            'antihistamines': round(sales_index * 0.20, 2),
            'vitamins': round(sales_index * 0.20, 2)
        }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'region': region,
            'sales_index': round(sales_index, 2),
            'baseline': 85.0,
            'pharmacy_chain': random.choice(['CVS', 'Walgreens', 'Rite Aid', 'Independent']),
            'store_id': f"PHARM-{region[:3].upper()}-{random.randint(100, 999)}",
            'categories': categories,
            'total_transactions': random.randint(150, 400)
        }
    
    def generate_patient_vitals(self, patient_id: str, base_temp: float = 36.5) -> Dict:
        """Generate realistic patient vital signs"""
        # Realistic temperature variations
        temp_variation = random.uniform(-0.3, 0.3)
        if random.random() < 0.05:  # 5% chance of fever spike
            temp_variation += random.uniform(1.0, 2.5)
        
        temperature = max(35.0, min(40.0, base_temp + temp_variation))
        
        # Correlated vitals (fever affects other vitals)
        heart_rate_base = 70
        if temperature >= 38.0:
            heart_rate_base += 15 + (temperature - 38.0) * 5
        
        return {
            'patient_id': patient_id,
            'timestamp': datetime.now().isoformat(),
            'temperature': round(temperature, 1),
            'heart_rate': max(50, min(120, heart_rate_base + random.randint(-5, 5))),
            'blood_pressure_systolic': max(90, min(160, 120 + random.randint(-10, 10))),
            'blood_pressure_diastolic': max(60, min(100, 80 + random.randint(-5, 5))),
            'respiratory_rate': random.randint(12, 20),
            'oxygen_saturation': round(95 + random.uniform(-2, 2), 1),
            'device_id': f"VITAL-{random.randint(1000, 9999)}",
            'measurement_location': random.choice(['Home', 'Clinic', 'Hospital', 'Remote'])
        }
    
    def generate_patient_data(self) -> Dict:
        """Generate realistic patient record"""
        patient_id = f"PT-{random.randint(2000, 9999)}"
        name = random.choice(self.patient_names)
        age = random.randint(18, 85)
        
        # Age-based risk factors
        comorbidities = []
        if age > 65:
            if random.random() < 0.6:
                comorbidities.append(random.choice(["Diabetes Type 2", "Hypertension", "Heart Disease"]))
        if age > 50:
            if random.random() < 0.3:
                comorbidities.append(random.choice(["COPD", "Asthma"]))
        
        # Temperature based on symptoms
        base_temp = 36.5
        symptoms = []
        if random.random() < 0.3:  # 30% chance of symptoms
            num_symptoms = random.randint(1, 3)
            symptoms = random.sample(self.symptoms_list, num_symptoms)
            if "Fever" in symptoms:
                base_temp = 37.5 + random.uniform(0.3, 1.5)
        
        # Risk calculation
        risk_score = 0
        if age > 65:
            risk_score += 30
        if len(comorbidities) > 0:
            risk_score += len(comorbidities) * 10
        if base_temp >= 38.0:
            risk_score += 25
        if len(symptoms) > 0:
            risk_score += len(symptoms) * 8
        
        risk_score = min(100, risk_score + random.randint(-5, 5))
        
        if risk_score >= 70:
            risk_level = "high"
        elif risk_score >= 40:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            'id': patient_id,
            'name': name,
            'age': age,
            'riskScore': risk_score,
            'riskLevel': risk_level,
            'lastTemperature': round(base_temp, 1),
            'symptoms': symptoms,
            'comorbidities': comorbidities,
            'lastUpdate': datetime.now().isoformat(),
            'region': random.choice(self.regions),
            'gender': random.choice(['M', 'F', 'Other']),
            'admission_date': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat().split('T')[0]
        }
    
    def generate_alert_data(self) -> Dict:
        """Generate realistic alert data"""
        alert_types = [
            {'type': 'wastewater_threshold', 'severity': 'high', 'source': 'Wastewater Analysis'},
            {'type': 'pharmacy_spike', 'severity': 'medium', 'source': 'Pharmacy Data'},
            {'type': 'patient_cluster', 'severity': 'high', 'source': 'Federated Learning'},
            {'type': 'climate_conditions', 'severity': 'low', 'source': 'Climate Monitoring'},
            {'type': 'outbreak_prediction', 'severity': 'high', 'source': 'Federated Learning'}
        ]
        
        alert_type = random.choice(alert_types)
        region = random.choice(self.regions)
        
        messages = {
            'wastewater_threshold': f"Wastewater viral load threshold exceeded in {region} sector",
            'pharmacy_spike': f"OTC fever medication sales spike detected in {region}",
            'patient_cluster': f"Fever outbreak similarity detected across institutions in {region}",
            'climate_conditions': f"Temperature and humidity conditions favorable for transmission in {region}",
            'outbreak_prediction': f"Elevated fever cases predicted - 10 day forecast for {region}"
        }
        
        return {
            'id': f"{alert_type['type'][:2].upper()}-{random.randint(1, 999):03d}",
            'severity': alert_type['severity'],
            'region': f"{region} District",
            'message': messages[alert_type['type']],
            'timestamp': datetime.now().isoformat(),
            'source': alert_type['source'],
            'confidence': random.randint(65, 95),
            'affectedPopulation': random.randint(200, 2000),
            'trend': random.choice(['increasing', 'stable', 'decreasing'])
        }
    
    def generate_outbreak_prediction(self) -> Dict:
        """Generate realistic outbreak prediction"""
        region = random.choice(self.regions)
        days_ahead = random.randint(1, 14)
        prediction_date = (datetime.now() + timedelta(days=days_ahead)).isoformat().split('T')[0]
        
        # Base prediction with realistic variance
        base_cases = 20 + random.uniform(-5, 15)
        trend_factor = 1.0 + (days_ahead / 14) * 0.3  # Increasing trend
        predicted = max(0, int(base_cases * trend_factor + random.uniform(-3, 3)))
        
        return {
            'date': prediction_date,
            'predicted_cases': predicted,
            'confidence': max(60, 95 - days_ahead * 2),
            'region': region,
            'model_version': 'outbreak_v1.0',
            'factors': {
                'wastewater_trend': round(random.uniform(0.8, 1.2), 2),
                'pharmacy_trend': round(random.uniform(0.9, 1.15), 2),
                'historical_cases': random.randint(15, 35),
                'seasonal_factor': round(random.uniform(0.95, 1.1), 2)
            }
        }


class KafkaDataProducer:
    """Kafka producer for realistic data streams"""
    
    def __init__(self, bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',
            retries=3
        )
        self.generator = RealisticDataGenerator()
        self.running = True
    
    def produce_wastewater_data(self, interval: int = 3600):
        """Produce wastewater data every interval seconds"""
        print(f"Starting wastewater data producer (interval: {interval}s)")
        while self.running:
            try:
                data = self.generator.generate_wastewater_data()
                key = data['region']
                self.producer.send(TOPICS['wastewater'], key=key, value=data)
                print(f"Produced wastewater data: {data['region']} - {data['viral_load']:.2f}")
                time.sleep(interval)
            except Exception as e:
                print(f"Error producing wastewater data: {e}")
                time.sleep(5)
    
    def produce_pharmacy_data(self, interval: int = 1800):
        """Produce pharmacy data every interval seconds"""
        print(f"Starting pharmacy data producer (interval: {interval}s)")
        while self.running:
            try:
                data = self.generator.generate_pharmacy_data()
                key = data['region']
                self.producer.send(TOPICS['pharmacy'], key=key, value=data)
                print(f"Produced pharmacy data: {data['region']} - {data['sales_index']:.2f}")
                time.sleep(interval)
            except Exception as e:
                print(f"Error producing pharmacy data: {e}")
                time.sleep(5)
    
    def produce_patient_data(self, interval: int = 300):
        """Produce patient vital signs data every interval seconds"""
        print(f"Starting patient vitals producer (interval: {interval}s)")
        patient_ids = [f"PT-{2847+i}" for i in range(10)]
        
        while self.running:
            try:
                # Produce vitals for random patient
                patient_id = random.choice(patient_ids)
                vitals = self.generator.generate_patient_vitals(patient_id)
                self.producer.send(TOPICS['vitals'], key=patient_id, value=vitals)
                print(f"Produced vitals for {patient_id}: {vitals['temperature']}°C")
                time.sleep(interval)
            except Exception as e:
                print(f"Error producing patient vitals: {e}")
                time.sleep(5)
    
    def produce_patient_records(self, interval: int = 600):
        """Produce new patient records every interval seconds"""
        print(f"Starting patient records producer (interval: {interval}s)")
        while self.running:
            try:
                patient = self.generator.generate_patient_data()
                self.producer.send(TOPICS['patients'], key=patient['id'], value=patient)
                print(f"Produced patient record: {patient['id']} - {patient['name']}")
                time.sleep(interval)
            except Exception as e:
                print(f"Error producing patient record: {e}")
                time.sleep(5)
    
    def produce_alert_data(self, interval: int = 7200):
        """Produce alert data every interval seconds"""
        print(f"Starting alert data producer (interval: {interval}s)")
        while self.running:
            try:
                alert = self.generator.generate_alert_data()
                self.producer.send(TOPICS['alerts'], key=alert['id'], value=alert)
                print(f"Produced alert: {alert['id']} - {alert['severity']}")
                time.sleep(interval)
            except Exception as e:
                print(f"Error producing alert: {e}")
                time.sleep(5)
    
    def produce_outbreak_predictions(self, interval: int = 86400):
        """Produce outbreak predictions every interval seconds"""
        print(f"Starting outbreak predictions producer (interval: {interval}s)")
        while self.running:
            try:
                prediction = self.generator.generate_outbreak_prediction()
                key = prediction['region']
                self.producer.send(TOPICS['outbreak'], key=key, value=prediction)
                print(f"Produced outbreak prediction: {prediction['region']} - {prediction['predicted_cases']} cases")
                time.sleep(interval)
            except Exception as e:
                print(f"Error producing outbreak prediction: {e}")
                time.sleep(5)
    
    def run_all_producers(self):
        """Run all data producers in separate threads"""
        import threading
        
        producers = [
            threading.Thread(target=self.produce_wastewater_data, daemon=True),
            threading.Thread(target=self.produce_pharmacy_data, daemon=True),
            threading.Thread(target=self.produce_patient_data, daemon=True),
            threading.Thread(target=self.produce_patient_records, daemon=True),
            threading.Thread(target=self.produce_alert_data, daemon=True),
            threading.Thread(target=self.produce_outbreak_predictions, daemon=True),
        ]
        
        for producer in producers:
            producer.start()
        
        print("All Kafka producers started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping producers...")
            self.running = False
            self.producer.close()


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Kafka Data Producer for Fever Oracle')
    parser.add_argument('--bootstrap-servers', default=KAFKA_BOOTSTRAP_SERVERS,
                       help='Kafka bootstrap servers')
    parser.add_argument('--topic', choices=list(TOPICS.keys()) + ['all'],
                       default='all', help='Topic to produce to')
    parser.add_argument('--interval', type=int, default=60,
                       help='Production interval in seconds')
    
    args = parser.parse_args()
    
    producer = KafkaDataProducer(bootstrap_servers=args.bootstrap_servers)
    
    if args.topic == 'all':
        producer.run_all_producers()
    elif args.topic == 'wastewater':
        producer.produce_wastewater_data(args.interval)
    elif args.topic == 'pharmacy':
        producer.produce_pharmacy_data(args.interval)
    elif args.topic == 'patients':
        producer.produce_patient_records(args.interval)
    elif args.topic == 'vitals':
        producer.produce_patient_data(args.interval)
    elif args.topic == 'alerts':
        producer.produce_alert_data(args.interval)
    elif args.topic == 'outbreak':
        producer.produce_outbreak_predictions(args.interval)


if __name__ == "__main__":
    main()

