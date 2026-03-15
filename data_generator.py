# data_generator.py
import requests
import time
import random
from datetime import datetime

# Your main app URL
MAIN_APP_URL = "https://metahealth-ai.onrender.com/api/sensor-data"

def generate_data():
    while True:
        hour = datetime.now().hour
        
        # Realistic glucose based on time
        if 6 <= hour < 9:  # Morning fasting
            glucose = random.uniform(80, 100)
        elif 9 <= hour < 11:  # After breakfast
            glucose = random.uniform(110, 135)
        elif 12 <= hour < 14:  # Lunch
            glucose = random.uniform(115, 140)
        elif 19 <= hour < 21:  # Dinner
            glucose = random.uniform(120, 145)
        else:  # Night
            glucose = random.uniform(85, 105)
        
        data = {
            "patient_id": "P001",
            "patient_name": "Demo Patient",
            "age": 45,
            "bmi": round(random.uniform(22, 28), 1),
            "glucose_level": round(glucose, 1),
            "heart_rate": random.randint(65, 85),
            "temperature": round(36.5 + random.uniform(-0.3, 0.5), 1),
            "blood_pressure_sys": random.randint(110, 130),
            "blood_pressure_dia": random.randint(70, 85)
        }
        
        try:
            response = requests.post(MAIN_APP_URL, json=data, timeout=5)
            print(f"✅ Sent: Glucose={data['glucose_level']}")
        except:
            print("❌ Failed to send")
        
        time.sleep(30)  # Send every 30 seconds

if __name__ == "__main__":
    generate_data()
