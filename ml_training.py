"""
DOCWIPING Machine Learning Module
Train ML models for wipe duration prediction and optimization
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class WipeDurationPredictor:
    """
    Machine Learning model to predict data wipe duration
    based on device type, size, and wipe method
    """
    
    def __init__(self):
        self.model = None
        self.device_encoder = LabelEncoder()
        self.method_encoder = LabelEncoder()
        self.is_trained = False
        
    def generate_training_data(self, n_samples=1000):
        """Generate synthetic training data based on real-world patterns"""
        
        device_types = ['NVMe SSD', 'SATA SSD', 'SATA HDD', 'Android', 'USB Flash']
        wipe_methods = [
            'NVMe Format (Crypto Erase)',
            'ATA Secure Erase',
            'DoD 5220.22-M (3-pass)',
            'DoD 5220.22-M (7-pass)',
            'Gutmann (35-pass)',
            'NIST SP 800-88',
            'Crypto Erase'
        ]
        
        # Speed characteristics (MB/s)
        speed_map = {
            'NVMe SSD': {'base': 3000, 'variance': 500},
            'SATA SSD': {'base': 500, 'variance': 100},
            'SATA HDD': {'base': 150, 'variance': 30},
            'Android': {'base': 100, 'variance': 20},
            'USB Flash': {'base': 50, 'variance': 15}
        }
        
        # Method complexity multipliers
        method_multiplier = {
            'NVMe Format (Crypto Erase)': 0.1,
            'Crypto Erase': 0.1,
            'ATA Secure Erase': 0.5,
            'NIST SP 800-88': 1.0,
            'DoD 5220.22-M (3-pass)': 3.0,
            'DoD 5220.22-M (7-pass)': 7.0,
            'Gutmann (35-pass)': 35.0
        }
        
        data = []
        
        for _ in range(n_samples):
            device_type = np.random.choice(device_types)
            wipe_method = np.random.choice(wipe_methods)
            
            # Generate realistic size based on device type
            if device_type == 'NVMe SSD':
                size_gb = np.random.choice([512, 1000, 2000, 4000])
            elif device_type == 'SATA SSD':
                size_gb = np.random.choice([256, 512, 960, 1000])
            elif device_type == 'SATA HDD':
                size_gb = np.random.choice([1000, 2000, 4000, 8000, 10000])
            elif device_type == 'Android':
                size_gb = np.random.choice([64, 128, 256, 512])
            else:  # USB Flash
                size_gb = np.random.choice([16, 32, 64, 128])
            
            # Calculate duration
            speed_info = speed_map[device_type]
            actual_speed = np.random.normal(speed_info['base'], speed_info['variance'])
            multiplier = method_multiplier[wipe_method]
            
            # Duration in seconds
            total_mb = size_gb * 1024
            duration = (total_mb / actual_speed) * multiplier
            
            # Add some realistic variance
            duration *= np.random.uniform(0.9, 1.1)
            
            data.append({
                'device_type': device_type,
                'size_gb': size_gb,
                'wipe_method': wipe_method,
                'duration_seconds': int(duration)
            })
        
        return pd.DataFrame(data)
    
    def train(self, df=None):
        """Train the ML model"""
        
        if df is None:
            print("Generating training data...")
            df = self.generate_training_data(1000)
        
        print(f"Training on {len(df)} samples...")
        
        # Encode categorical variables
        df['device_encoded'] = self.device_encoder.fit_transform(df['device_type'])
        df['method_encoded'] = self.method_encoder.fit_transform(df['wipe_method'])
        
        # Prepare features and target
        X = df[['device_encoded', 'size_gb', 'method_encoded']]
        y = df['duration_seconds']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"✓ Model trained successfully")
        print(f"  Training R² score: {train_score:.4f}")
        print(f"  Testing R² score: {test_score:.4f}")
        
        self.is_trained = True
        
        return train_score, test_score
    
    def predict(self, device_type, size_gb, wipe_method):
        """Predict wipe duration"""
        
        if not self.is_trained:
            raise Exception("Model not trained yet. Call train() first.")
        
        try:
            device_encoded = self.device_encoder.transform([device_type])[0]
            method_encoded = self.method_encoder.transform([wipe_method])[0]
        except ValueError as e:
            # Fallback for unknown categories
            return self._fallback_prediction(device_type, size_gb, wipe_method)
        
        features = np.array([[device_encoded, size_gb, method_encoded]])
        duration = self.model.predict(features)[0]
        
        return {
            'duration_seconds': int(duration),
            'duration_minutes': round(duration / 60, 1),
            'duration_hours': round(duration / 3600, 2),
            'confidence': 0.85
        }
    
    def _fallback_prediction(self, device_type, size_gb, wipe_method):
        """Fallback prediction for unknown categories"""
        
        # Simple heuristic
        base_speeds = {
            'NVMe SSD': 3000,
            'SATA SSD': 500,
            'SATA HDD': 150,
            'Android': 100
        }
        
        method_multipliers = {
            'NVMe Format (Crypto Erase)': 0.1,
            'Crypto Erase': 0.1,
            'ATA Secure Erase': 0.5,
            'NIST SP 800-88': 1.0,
            'DoD 5220.22-M (3-pass)': 3.0,
            'DoD 5220.22-M (7-pass)': 7.0,
            'Gutmann (35-pass)': 35.0
        }
        
        speed = base_speeds.get(device_type, 200)
        multiplier = method_multipliers.get(wipe_method, 1.0)
        
        total_mb = size_gb * 1024
        duration = (total_mb / speed) * multiplier
        
        return {
            'duration_seconds': int(duration),
            'duration_minutes': round(duration / 60, 1),
            'duration_hours': round(duration / 3600, 2),
            'confidence': 0.65
        }
    
    def save_model(self, filepath='ml_models/wipe_predictor.pkl'):
        """Save trained model to disk"""
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'device_encoder': self.device_encoder,
            'method_encoder': self.method_encoder,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
        print(f"✓ Model saved to {filepath}")
    
    def load_model(self, filepath='ml_models/wipe_predictor.pkl'):
        """Load trained model from disk"""
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.device_encoder = model_data['device_encoder']
        self.method_encoder = model_data['method_encoder']
        self.is_trained = model_data['is_trained']
        
        print(f"✓ Model loaded from {filepath}")


def train_and_save_model():
    """Main function to train and save the model"""
    
    print("=" * 60)
    print("DOCWIPING ML Model Training")
    print("=" * 60)
    
    predictor = WipeDurationPredictor()
    
    # Generate and train
    predictor.train()
    
    # Test predictions
    print("\nTest Predictions:")
    print("-" * 60)
    
    test_cases = [
        ('NVMe SSD', 1600, 'NVMe Format (Crypto Erase)'),
        ('SATA SSD', 960, 'ATA Secure Erase'),
        ('SATA HDD', 4000, 'DoD 5220.22-M (3-pass)'),
        ('Android', 128, 'Crypto Erase'),
    ]
    
    for device, size, method in test_cases:
        result = predictor.predict(device, size, method)
        print(f"{device} ({size}GB) - {method}")
        print(f"  Estimated: {result['duration_minutes']} min ({result['duration_hours']} hrs)")
        print(f"  Confidence: {result['confidence']:.0%}\n")
    
    # Save model
    predictor.save_model()
    
    print("=" * 60)
    print("✓ Training complete!")
    print("=" * 60)


if __name__ == '__main__':
    train_and_save_model()
