import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import metrics as keras_metrics
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib
import json

class IoTAnomalyDetector:
    def __init__(self, input_dim):
        self.input_dim = input_dim
        self.model = None
        self.scaler = StandardScaler()
        self.history = None
        
    def build_classifier_model(self):
        model = keras.Sequential([
            layers.Input(shape=(self.input_dim,)),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(32, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.2),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        # ВИПРАВЛЕНО: використовуємо класи метрик замість рядків
        model.compile(
            optimizer='adam', 
            loss='binary_crossentropy', 
            metrics=[
                'accuracy',
                keras_metrics.Precision(name='precision'),
                keras_metrics.Recall(name='recall')
            ]
        )
        
        self.model = model
        print("✅ Модель створено")
        return model
    
    def train(self, X, y=None, epochs=50, batch_size=128, validation_split=0.2, model_type='classifier'):
        X_scaled = self.scaler.fit_transform(X)
        if y is None:
            raise ValueError("Для classifier потрібні лейбли y")
        
        self.build_classifier_model()
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        self.history = self.model.fit(
            X_train, y_train, 
            epochs=epochs, 
            batch_size=batch_size,
            validation_data=(X_test, y_test), 
            verbose=1
        )
        
        y_pred = (self.model.predict(X_test, verbose=0) > 0.5).astype(int)
        print("\n📊 Результати:")
        print(classification_report(y_test, y_pred, target_names=['Benign', 'Malicious']))
        return self.history, (X_test, y_test)
    
    def detect_anomalies(self, X, threshold=None):
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled, verbose=0)
        anomaly_scores = predictions.flatten()
        if threshold is None:
            threshold = 0.5
        anomalies = (predictions > threshold).flatten()
        return anomalies, anomaly_scores, threshold
    
    def save_model(self, model_path='models/anomaly_detector.h5', scaler_path='models/preprocessor.pkl'):
        self.model.save(model_path)
        joblib.dump(self.scaler, scaler_path)
        if self.history:
            metrics = {
                'final_loss': float(self.history.history['loss'][-1]),
                'final_val_loss': float(self.history.history.get('val_loss', [0])[-1])
            }
            with open('models/model_metrics.json', 'w') as f:
                json.dump(metrics, f, indent=2)
        print(f"✅ Модель збережено")
    
    def load_model(self, model_path='models/anomaly_detector.h5', scaler_path='models/preprocessor.pkl'):
        self.model = keras.models.load_model(model_path)
        self.scaler = joblib.load(scaler_path)
        print(f"✅ Модель завантажено")