# model.py - REAL Diabetes Prediction Model
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

class RealDiabetesPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = {}
        self.accuracy = 0
        self.model_file = 'real_diabetes_model.pkl'
        self.scaler_file = 'scaler.pkl'
        
    def load_real_data(self):
        """Load and prepare the PIMA dataset"""
        print("📊 Loading PIMA Indian Diabetes Dataset...")
        
        if not os.path.exists("pima-diabetes.csv"):
            print("❌ Dataset not found! Please run download_data.py first")
            return None
        
        # Load data
        df = pd.read_csv("pima-diabetes.csv")
        
        # Handle missing values (replace 0 with NaN in certain columns)
        cols_with_zeros = ['glucose', 'blood_pressure', 'skin_thickness', 
                          'insulin', 'bmi']
        
        for col in cols_with_zeros:
            df[col] = df[col].replace(0, np.nan)
            df[col].fillna(df[col].median(), inplace=True)
        
        print(f"✅ Data loaded: {len(df)} patients")
        print(f"   Features: {list(df.columns[:-1])}")
        print(f"   Target: {'Diabetic' if df['outcome'].iloc[0] else 'Non-diabetic'}")
        
        return df
    
    def train(self):
        """Train on REAL PIMA data"""
        print("\n🧠 Training REAL Diabetes Prediction Model...")
        print("=" * 50)
        
        # Load data
        df = self.load_real_data()
        if df is None:
            return None
        
        # Prepare features and target
        X = df.drop('outcome', axis=1)
        y = df['outcome']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train multiple models and pick best
        models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=200,
                max_depth=10,
                min_samples_split=5,
                random_state=42
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=150,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        }
        
        best_score = 0
        best_model_name = ""
        
        for name, model in models.items():
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            model.fit(X_train, y_train)
            test_score = model.score(X_test, y_test)
            
            print(f"\n📊 {name}:")
            print(f"   CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
            print(f"   Test Accuracy: {test_score:.3f}")
            
            if test_score > best_score:
                best_score = test_score
                best_model_name = name
                self.model = model
        
        # Use best model
        print(f"\n🏆 Best Model: {best_model_name}")
        print(f"   Test Accuracy: {best_score:.3f}")
        
        # Final evaluation
        y_pred = self.model.predict(X_test)
        print("\n📈 Classification Report:")
        print(classification_report(y_test, y_pred, 
                                  target_names=['Non-Diabetic', 'Diabetic']))
        
        # Feature importance
        feature_names = X.columns
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        print("\n🔍 Top Risk Factors:")
        for i in range(len(feature_names)):
            if i < 5:  # Top 5
                print(f"   {i+1}. {feature_names[indices[i]]}: {importances[indices[i]]:.3f}")
            self.feature_importance[feature_names[indices[i]]] = importances[indices[i]]
        
        self.accuracy = best_score
        
        # Save model and scaler
        joblib.dump(self.model, self.model_file)
        joblib.dump(self.scaler, self.scaler_file)
        print(f"\n💾 Model saved: {self.model_file}")
        
        return self.model
    
    def load_or_train(self):
        """Load existing model or train new one"""
        if os.path.exists(self.model_file) and os.path.exists(self.scaler_file):
            print("📂 Loading trained model...")
            self.model = joblib.load(self.model_file)
            self.scaler = joblib.load(self.scaler_file)
            print("✅ Model loaded!")
            
            # Load feature names from training data
            df = self.load_real_data()
            if df is not None:
                feature_names = df.drop('outcome', axis=1).columns
                importances = self.model.feature_importances_
                for name, imp in zip(feature_names, importances):
                    self.feature_importance[name] = imp
        else:
            self.train()
        
        return self.model
    
    def predict(self, features):
        """Make prediction for single patient"""
        if self.model is None:
            self.load_or_train()
        
        # Prepare features in correct order
        feature_order = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness',
                        'insulin', 'bmi', 'diabetes_pedigree', 'age']
        
        # Create feature array
        X = np.array([[features.get(f, 0) for f in feature_order]])
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Get prediction and probability
        prediction = self.model.predict(X_scaled)[0]
        probability = self.model.predict_proba(X_scaled)[0][1]
        
        return {
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': self.get_risk_level(probability),
            'risk_factors': self.get_risk_factors(features)
        }
    
    def get_risk_level(self, probability):
        if probability < 0.3:
            return "Low Risk"
        elif probability < 0.6:
            return "Moderate Risk"
        else:
            return "High Risk"
    
    def get_risk_factors(self, features):
        """Identify which factors are increasing risk"""
        risk_factors = []
        
        # Get top 3 risk factors from model
        top_factors = sorted(self.feature_importance.items(), 
                            key=lambda x: x[1], reverse=True)[:3]
        
        # Check if patient has high values in important features
        for factor, importance in top_factors:
            if factor in features:
                value = features[factor]
                
                # Thresholds based on medical guidelines
                if factor == 'glucose' and value > 125:
                    risk_factors.append(f"High glucose ({value:.0f} mg/dL)")
                elif factor == 'bmi' and value > 30:
                    risk_factors.append(f"High BMI ({value:.1f})")
                elif factor == 'age' and value > 45:
                    risk_factors.append(f"Age ({value:.0f} years)")
                elif factor == 'blood_pressure' and value > 130:
                    risk_factors.append(f"High BP ({value:.0f} mmHg)")
                elif factor == 'pregnancies' and value > 5:
                    risk_factors.append(f"Multiple pregnancies ({value:.0f})")
        
        return risk_factors[:3]  # Return top 3

# Create global instance
predictor = RealDiabetesPredictor()
predictor.load_or_train()