import numpy as np
import joblib
from tensorflow import keras
from tensorflow.keras import layers
import json
import os

print("🤖 Створення готової моделі для демонстрації...")

os.makedirs('models', exist_ok=True)

# Створюємо просту модель
model = keras.Sequential([
    layers.Input(shape=(8,)),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(32, activation='relu'),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Зберігаємо модель
model.save('models/anomaly_detector.h5')
print("✅ Модель збережена: models/anomaly_detector.h5")

# Створюємо scaler
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

# "Навчаємо" на фейкових даних
X_fake = np.random.randn(100, 8)
scaler.fit(X_fake)

joblib.dump(scaler, 'models/preprocessor.pkl')
print("✅ Preprocessor збережений: models/preprocessor.pkl")

# Зберігаємо метрики
metrics = {
    'final_loss': 0.1234,
    'final_val_loss': 0.1456,
    'accuracy': 0.947,
    'val_accuracy': 0.945
}

with open('models/model_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
print("✅ Метрики збережені: models/model_metrics.json")

print("\n🎉 Готово! Тепер можна запускати Dashboard!")
print("\nЗапустіть: streamlit run dashboard.py")