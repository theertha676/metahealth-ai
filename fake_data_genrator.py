# fake_data_generator.py - Realistic Health Simulator
import requests
import time
import random
import math
from datetime import datetime, timedelta

class RealisticHealthSimulator:
    def __init__(self, server_url="http://127.0.0.1:5000"):
        self.server_url = server_url
        self.start_time = datetime.now()
        self.reading_count = 0
        
        # Patient baseline (realistic values)
        self.baseline = {
            "glucose": 95,      # Normal fasting glucose
            "heart_rate": 72,    # Normal resting heart rate
            "temperature": 36.6,  # Normal body temperature
            "bp_sys": 118,       # Normal systolic
            "bp_dia": 76         # Normal diastolic
        }
        
        # Time of day variations
        self.last_meal_time = None
        self.last_exercise_time = None
        
        print("=" * 60)
        print("🩺 REALISTIC METAHEALTH SIMULATOR")
        print("=" * 60)
        print("📊 Simulating natural daily patterns:")
        print("   • Morning fasting: 80-100 mg/dL")
        print("   • After meals: +20-40 mg/dL (2hr peak)")
        print("   • Evening: gradual decrease")
        print("   • Exercise: temporary changes")
        print("=" * 60)
    
    def get_time_of_day_factor(self):
        """Get factor based on time of day (0-24 hours)"""
        hour = datetime.now().hour
        
        # Morning (6-9 AM): Fasting, lower glucose
        if 6 <= hour < 9:
            return "morning_fasting"
        # Breakfast time (8-9 AM): Starting to rise
        elif 8 <= hour < 10:
            return "breakfast"
        # Mid-morning (10-11 AM): Post-breakfall
        elif 10 <= hour < 12:
            return "mid_morning"
        # Lunch time (12-2 PM)
        elif 12 <= hour < 14:
            return "lunch"
        # Afternoon (2-5 PM)
        elif 14 <= hour < 17:
            return "afternoon"
        # Dinner time (7-9 PM)
        elif 19 <= hour < 21:
            return "dinner"
        # Evening/Night (9 PM - 6 AM)
        else:
            return "night"
    
    def generate_realistic_glucose(self):
        """Generate glucose with realistic patterns"""
        time_factor = self.get_time_of_day_factor()
        hour = datetime.now().hour
        
        # Base glucose varies by time of day
        if time_factor == "morning_fasting":
            # Fasting - should be lowest
            glucose = random.uniform(80, 100)
        elif time_factor == "breakfast":
            # Post-breakfast rise
            glucose = random.uniform(110, 135)
        elif time_factor == "mid_morning":
            # Coming down from breakfast
            glucose = random.uniform(95, 115)
        elif time_factor == "lunch":
            # Lunch time rise
            glucose = random.uniform(115, 140)
        elif time_factor == "afternoon":
            # Post-lunch gradual decline
            glucose = random.uniform(100, 120)
        elif time_factor == "dinner":
            # Dinner rise
            glucose = random.uniform(120, 145)
        else:  # night
            # Night time - should be lower
            glucose = random.uniform(85, 105)
        
        # Add some random variation
        glucose += random.gauss(0, 3)
        
        return round(max(70, min(180, glucose)), 1)
    
    def generate_realistic_heart_rate(self):
        """Heart rate varies by activity and time"""
        hour = datetime.now().hour
        
        # Base heart rate by time of day
        if 22 <= hour or hour < 6:  # Night/sleep
            base = random.uniform(55, 65)
        elif 6 <= hour < 9:  # Morning waking up
            base = random.uniform(65, 75)
        elif 9 <= hour < 17:  # Active day
            base = random.uniform(70, 85)
        else:  # Evening relaxing
            base = random.uniform(65, 80)
        
        # Occasionally simulate exercise (15% chance)
        if random.random() < 0.15:
            base += random.uniform(15, 30)
            activity = " (during activity)"
        else:
            activity = ""
        
        return round(base + random.gauss(0, 2)), activity
    
    def generate_realistic_temperature(self):
        """Body temperature with slight variations"""
        hour = datetime.now().hour
        
        # Body temp slightly lower in morning, higher in evening
        if 4 <= hour < 8:  # Early morning
            base = 36.2
        elif 8 <= hour < 12:  # Morning
            base = 36.4
        elif 12 <= hour < 18:  # Afternoon
            base = 36.7
        else:  # Evening
            base = 36.8
        
        # Add small variation
        temp = base + random.uniform(-0.2, 0.3)
        return round(temp, 1)
    
    def generate_health_data(self):
        """Generate complete realistic health data"""
        # Get realistic values
        glucose = self.generate_realistic_glucose()
        heart_rate, activity = self.generate_realistic_heart_rate()
        temperature = self.generate_realistic_temperature()
        
        # Blood pressure correlates with heart rate
        bp_sys = 110 + (heart_rate - 60) * 0.5 + random.randint(-5, 5)
        bp_dia = 70 + (heart_rate - 60) * 0.3 + random.randint(-3, 3)
        
        # Time context
        current_time = datetime.now()
        time_str = current_time.strftime("%H:%M:%S")
        hour = current_time.hour
        
        # Add meal/activity context for realism
        context = ""
        if 7 <= hour < 9:
            context = " (before breakfast)"
        elif 9 <= hour < 11:
            context = " (after breakfast)"
        elif 12 <= hour < 14:
            context = " (lunch time)"
        elif 18 <= hour < 20:
            context = " (dinner time)"
        elif 22 <= hour or hour < 6:
            context = " (resting)"
        
        return {
            "patient_id": "P001",
            "patient_name": "Alex",
            "age": 45,
            "bmi": round(random.uniform(22, 28), 1),
            "glucose_level": glucose,
            "heart_rate": heart_rate,
            "temperature": temperature,
            "blood_pressure_sys": int(bp_sys),
            "blood_pressure_dia": int(bp_dia),
            "context": context.strip(),
            "activity": activity.strip(),
            "timestamp": time_str,
            "reading_number": self.reading_count,
            "time_of_day": self.get_time_of_day_factor()
        }
    
    def send_data(self):
        """Send realistic data to Flask server"""
        data = self.generate_health_data()
        
        try:
            response = requests.post(
                f"{self.server_url}/api/sensor-data",
                json=data,
                timeout=2
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Beautiful output with context
                print(f"\n{'='*60}")
                print(f"📊 READING #{data['reading_number']+1} | {data['timestamp']}{data['context']}")
                print(f"{'='*60}")
                print(f"🍬 Glucose:     {data['glucose_level']} mg/dL  {self.get_glucose_status(data['glucose_level'])}")
                print(f"❤️  Heart Rate:  {data['heart_rate']} bpm{data['activity']}")
                print(f"🌡️  Temperature: {data['temperature']}°C")
                print(f"💓 Blood Press: {data['blood_pressure_sys']}/{data['blood_pressure_dia']} mmHg")
                print(f"📋 Risk Level:   {result['prediction']['risk_level']}")
                
                self.reading_count += 1
                return True
                
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def get_glucose_status(self, glucose):
        if glucose > 125:
            return "⚠️ HIGH"
        elif glucose > 100:
            return "⚡ Pre-diabetic"
        else:
            return "✅ Normal"
    
    def run(self):
        """Run continuous realistic simulation"""
        print("\n📈 Simulation started - showing realistic daily patterns")
        print("⏰ Current time affects readings (meals, activity, rest)")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.send_data()
                
                # Random interval between 2-8 minutes for realism
                # (people don't check constantly!)
                interval = random.randint(120, 480)  # 2-8 minutes in seconds
                minutes = interval // 60
                seconds = interval % 60
                
                print(f"⏱️  Next reading in ~{minutes}m {seconds}s")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n\n📊 Simulation stopped. {self.reading_count} readings taken.")
            print("👋 Thank you for using Realistic MetaHealth!")

if __name__ == "__main__":
    simulator = RealisticHealthSimulator()
    simulator.run()