# recommendation_engine.py - AI-Powered Recommendations
import numpy as np
import pandas as pd
from datetime import datetime

class AIRecommendationEngine:
    def __init__(self):
        self.recommendation_database = self.build_recommendation_db()
        
    def build_recommendation_db(self):
        """Build knowledge base of medical recommendations"""
        return {
            'glucose': {
                'very_high': [
                    "🔴 EMERGENCY: Blood glucose >180 mg/dL - Seek immediate medical attention!",
                    "💉 Check if you've taken your medication today",
                    "🚫 Avoid all carbohydrates until glucose normalizes",
                    "💧 Drink water to help flush excess sugar"
                ],
                'high': [
                    "⚠️ High glucose detected (>{threshold} mg/dL)",
                    "🍚 Reduce carbohydrate intake in next meal",
                    "🚶 Take a 15-minute walk to lower blood sugar",
                    "📊 Monitor glucose again in 2 hours"
                ],
                'pre_diabetic': [
                    "⚡ Pre-diabetic range ({min}-{max} mg/dL)",
                    "🥗 Choose low-glycemic index foods",
                    "🏃 Exercise 30 minutes today",
                    "🍎 Replace sugary snacks with fruits"
                ],
                'normal': [
                    "✅ Glucose in normal range ({min}-{max} mg/dL)",
                    "👍 Maintain your healthy eating habits",
                    "💪 Keep up the good work!"
                ],
                'low': [
                    "⚠️ Low blood sugar detected (<70 mg/dL)",
                    "🧃 Eat or drink 15g of fast-acting carbs",
                    "📊 Recheck glucose in 15 minutes"
                ]
            },
            'bmi': {
                'obese': [
                    "⚖️ BMI indicates obesity (>30)",
                    "🥗 Consult a dietitian for meal planning",
                    "🏃 Start with 20-minute daily walks",
                    "📝 Keep a food diary"
                ],
                'overweight': [
                    "⚖️ Overweight BMI (25-30)",
                    "🥗 Reduce portion sizes by 25%",
                    "🚶 Aim for 8,000 steps daily",
                    "💧 Replace sugary drinks with water"
                ],
                'normal': [
                    "⚖️ Healthy BMI range (18.5-24.9)",
                    "🏋️ Maintain with regular exercise",
                    "🥗 Continue balanced diet"
                ]
            },
            'age': {
                'senior': [
                    "👴 Age >60: Regular checkups important",
                    "🦴 Ensure adequate calcium and vitamin D",
                    "🧠 Keep mind active with puzzles/reading"
                ],
                'middle': [
                    "👨 Age 45-60: Monitor health markers",
                    "💪 Strength training 2x per week",
                    "❤️ Annual heart health checkup"
                ],
                'young': [
                    "👦 Young adult: Build healthy habits now",
                    "🏃 Establish regular exercise routine",
                    "🥗 Learn healthy cooking skills"
                ]
            }
        }
    
    def generate_recommendations(self, features, prediction):
        """Generate AI-powered recommendations based on actual risk factors"""
        recommendations = []
        risk_level = prediction['risk_level']
        probability = prediction['probability']
        
        # 1. URGENT recommendations based on critical values
        glucose = features.get('glucose', 100)
        
        if glucose > 180:
            recommendations.extend(self.recommendation_database['glucose']['very_high'])
        elif glucose > 140:
            recs = self.recommendation_database['glucose']['high']
            threshold = 140
            recommendations.append(recs[0].replace('{threshold}', str(threshold)))
            recommendations.extend(recs[1:])
        elif glucose > 125:
            recs = self.recommendation_database['glucose']['pre_diabetic']
            recommendations.append(recs[0].replace('{min}', '126').replace('{max}', '140'))
            recommendations.extend(recs[1:])
        elif glucose < 70:
            recommendations.extend(self.recommendation_database['glucose']['low'])
        else:
            recs = self.recommendation_database['glucose']['normal']
            recommendations.append(recs[0].replace('{min}', '70').replace('{max}', '99'))
            recommendations.extend(recs[1:])
        
        # 2. BMI-based recommendations
        bmi = features.get('bmi', 25)
        if bmi > 30:
            recommendations.extend(self.recommendation_database['bmi']['obese'])
        elif bmi > 25:
            recommendations.extend(self.recommendation_database['bmi']['overweight'])
        else:
            recommendations.extend(self.recommendation_database['bmi']['normal'])
        
        # 3. Age-based recommendations
        age = features.get('age', 40)
        if age > 60:
            recommendations.extend(self.recommendation_database['age']['senior'])
        elif age > 45:
            recommendations.extend(self.recommendation_database['age']['middle'])
        else:
            recommendations.extend(self.recommendation_database['age']['young'])
        
        # 4. Risk-based personalized recommendations
        if risk_level == "High Risk":
            recommendations.append("🏥 Schedule comprehensive diabetes screening THIS WEEK")
            recommendations.append("📊 Monitor blood glucose at least 3 times daily")
            recommendations.append("💊 Discuss metformin or other medications with doctor")
        elif risk_level == "Moderate Risk":
            recommendations.append("📅 Get A1C test within next 3 months")
            recommendations.append("🥗 Follow Mediterranean-style diet")
            recommendations.append("🏃 Exercise 150 minutes per week")
        
        # 5. Add lifestyle recommendations based on multiple factors
        if features.get('blood_pressure', 120) > 130:
            recommendations.append("🧂 Reduce sodium intake to <1500mg daily")
            recommendations.append("🥑 Increase potassium-rich foods")
        
        if features.get('bmi', 25) > 25 and features.get('age', 40) > 40:
            recommendations.append("💪 Join a structured weight loss program")
        
        # Remove duplicates and return top 6
        seen = set()
        unique_recs = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recs.append(rec)
        
        return unique_recs[:6]
    
    def get_explanation(self, features, prediction):
        """Explain WHY the AI made this prediction"""
        risk_factors = prediction.get('risk_factors', [])
        probability = prediction['probability']
        
        explanation = f"Based on analysis of {len(risk_factors)} key factors"
        
        if risk_factors:
            explanation += f": {', '.join(risk_factors)}"
        
        if probability > 0.7:
            explanation += ". The model shows strong confidence in this prediction."
        elif probability > 0.5:
            explanation += ". Multiple indicators suggest elevated risk."
        else:
            explanation += ". Most health markers are within normal range."
        
        return explanation

# Create global instance
recommendation_engine = AIRecommendationEngine()