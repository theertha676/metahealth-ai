# app.py - Main Flask Application
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
from datetime import datetime
import pytz
import json
from model import predictor
import random
from ai_recommendation_engine import ai_recommender

IST = pytz.timezone('Asia/Kolkata')
app = Flask(__name__)
CORS(app)

# Store data
latest_data = {}
health_history = []
recommendations_history = []

# Health tips and recommendations database
HEALTH_TIPS = [
    "🥗 Eat fiber-rich foods like vegetables and whole grains",
    "💧 Drink at least 8 glasses of water daily",
    "🚶 Take a 15-minute walk after meals",
    "😴 Get 7-8 hours of quality sleep",
    "🧘 Practice stress management techniques",
    "🍎 Choose fruits over sugary snacks",
    "🏋️ Exercise for 30 minutes daily",
    "📝 Monitor your blood sugar regularly",
    "🥑 Include healthy fats in your diet",
    "🚫 Avoid processed and sugary foods"
]

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    global latest_data
    
    data = request.json
    print(f"📥 Received: {data}")
    
    # Add timestamp
    data['timestamp'] = datetime.now().strftime("%H:%M:%S")
    data['datetime'] = datetime.now().isoformat()
    
    # Store latest
    latest_data = data
    
    # Add to history (keep last 50)
    health_history.append(data)
    if len(health_history) > 50:
        health_history.pop(0)
    
    # Get prediction
    prediction = get_diabetes_prediction(data)
    
    # Generate recommendations
    recommendations = generate_recommendations(data, prediction)
    
    return jsonify({
        'status': 'success',
        'prediction': prediction,
        'recommendations': recommendations
    })

@app.route('/api/latest-data', methods=['GET'])
def get_latest():
    if latest_data:
        return jsonify(latest_data)
    return jsonify({'message': 'No data yet'})

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify(health_history)

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Get prediction from model
    prediction = get_diabetes_prediction(data)
    
    # Generate recommendations
    recommendations = generate_recommendations(data, prediction)
    
    return jsonify({
        'prediction': prediction,
        'recommendations': recommendations,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health-tip', methods=['GET'])
def random_health_tip():
    tip = random.choice(HEALTH_TIPS)
    return jsonify({'tip': tip})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about the data"""
    if not health_history:
        return jsonify({'message': 'No data available'})
    
    glucose_values = [d.get('glucose_level', 0) for d in health_history]
    
    stats = {
        'avg_glucose': sum(glucose_values) / len(glucose_values),
        'max_glucose': max(glucose_values),
        'min_glucose': min(glucose_values),
        'readings_count': len(health_history),
        'high_glucose_count': sum(1 for g in glucose_values if g > 126)
    }
    
    return jsonify(stats)

def get_diabetes_prediction(data):
    """Get prediction from ML model"""
    
    # Prepare features for model
    features = {
        'glucose': data.get('glucose_level', 100),
        'bmi': data.get('bmi', 25),
        'age': data.get('age', 40),
        'blood_pressure': data.get('blood_pressure', 120),
        'insulin': data.get('insulin', 100),
        'skin_thickness': data.get('skin_thickness', 20),
        'pregnancies': data.get('pregnancies', 0),
        'diabetes_pedigree': data.get('diabetes_pedigree', 0.5)
    }
    
    # Get prediction from model
    result = predictor.predict(features)
    
    return result

def generate_recommendations(data, prediction):
    """Generate personalized health recommendations"""
    recommendations = []
    risk_level = prediction['risk_level']
    glucose = data.get('glucose_level', 100)
    
    # Urgent recommendations based on glucose
    if glucose > 180:
        recommendations.append("🔴 URGENT: Very high glucose! Seek medical attention immediately")
    elif glucose > 140:
        recommendations.append("⚠️ High glucose detected. Contact your doctor today")
    elif glucose > 126:
        recommendations.append("⚠️ Elevated glucose levels. Monitor closely and consult doctor")
    elif glucose > 100:
        recommendations.append("⚠️ Pre-diabetic range. Lifestyle changes recommended")
    
    # Risk-based recommendations
    if risk_level == "High Risk":
        recommendations.append("🏥 Schedule a comprehensive diabetes screening")
        recommendations.append("📊 Monitor blood glucose 3-4 times daily")
        recommendations.append("💊 Discuss medication options with your doctor")
    elif risk_level == "Moderate Risk":
        recommendations.append("✅ Get tested for diabetes every 3 months")
        recommendations.append("🥗 Follow a low-glycemic diet")
        recommendations.append("🏃 Exercise 30-45 minutes daily")
    else:
        recommendations.append("👍 Maintain your healthy lifestyle")
        recommendations.append("📅 Annual checkups recommended")
    
    # General health tips
    if glucose > 100:
        recommendations.append("🍚 Choose complex carbs over simple sugars")
        recommendations.append("🥩 Include lean protein in every meal")
    
    recommendations.append("💧 Stay hydrated - drink water instead of sugary drinks")
    recommendations.append("👣 Check your feet daily for any cuts or sores")
    
    # Remove duplicates and return top 5
    unique_recs = []
    for rec in recommendations:
        if rec not in unique_recs:
            unique_recs.append(rec)
    
    return unique_recs[:6]  # Return top 6 recommendations

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 METAHEALTH AI SYSTEM")
    print("=" * 50)
    print("📊 Diabetes Prediction Model: Ready")
    print("🌐 Dashboard: http://127.0.0.1:5000")
    print("📡 API Endpoint: http://127.0.0.1:5000/api/sensor-data")
    print("=" * 50)
    app.run()
@app.route('/api/generate-data', methods=['GET'])
def generate_data_endpoint():
    """Public endpoint that generates and stores a data point"""
    import random
    from datetime import datetime
    
    hour = datetime.now().hour
    
    # Generate realistic data
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
        "patient_name": "Auto Patient",
        "age": 45,
        "bmi": round(random.uniform(22, 28), 1),
        "glucose_level": round(glucose, 1),
        "heart_rate": random.randint(65, 85),
        "temperature": round(36.5 + random.uniform(-0.3, 0.5), 1),
        "blood_pressure_sys": random.randint(110, 130),
        "blood_pressure_dia": random.randint(70, 85),
        "timestamp": datetime.now(IST).strftime("%H:%M:%S"),
        "source": "cron-job"
    }
    
    # Store in your existing data structure
    global latest_data, health_history
    latest_data = data
    health_history.append(data)
    if len(health_history) > 50:
        health_history.pop(0)
    
    # Also send to prediction endpoint
    prediction = get_diabetes_prediction(data)
    
    return jsonify({"status": "success", "data": data})
