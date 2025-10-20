"""
Швидкий старт з детальним відображенням прогресу
"""

import numpy as np
import pandas as pd
from src.model_training import IoTAnomalyDetector
from src.simulator import IoTTrafficSimulator
import os
from datetime import datetime
from tqdm import tqdm
import sys

def print_header(text):
    print("\n" + "="*70)
    print(f"{text:^70}")
    print("="*70)

def print_step(text):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {text}")

# Початок
print_header("🛡️ IoT Security AI Monitor - Швидкий старт")
print_step(f"Початок роботи")

# Крок 1: Створення директорій
print_step("📁 Створення директорій...")
os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)
print_step("✅ Директорії створено")

# Крок 2: Ініціалізація симулятора
print_step("🔧 Ініціалізація симулятора...")
simulator = IoTTrafficSimulator()
print_step(f"✅ Симулятор готовий. Пристроїв: {len(simulator.device_types)}")

# Крок 3: Генерація даних
print_header("📊 ГЕНЕРАЦІЯ ДАТАСЕТУ")

all_traffic = []
device_stats = {}

# Progress bar для пристроїв
for device in tqdm(simulator.device_types, desc="🔄 Пристрої", ncols=80, file=sys.stdout):
    device_traffic = []
    
    # Нормальний трафік
    for _ in tqdm(range(1000), desc=f"  ✓ {device[:15]:15s} (Normal)", 
                  leave=False, ncols=80, file=sys.stdout):
        traffic = simulator.generate_normal_traffic(device, 1)
        device_traffic.extend(traffic)
    
    # DDoS атаки
    for _ in tqdm(range(200), desc=f"  ⚠️  {device[:15]:15s} (DDoS)  ", 
                  leave=False, ncols=80, file=sys.stdout):
        traffic = simulator.generate_ddos_attack(device, 1)
        device_traffic.extend(traffic)
    
    # Port Scan
    for _ in tqdm(range(150), desc=f"  🔍 {device[:15]:15s} (Scan)  ", 
                  leave=False, ncols=80, file=sys.stdout):
        traffic = simulator.generate_port_scan(device, 1)
        device_traffic.extend(traffic)
    
    # Mirai
    for _ in tqdm(range(100), desc=f"  🦠 {device[:15]:15s} (Mirai) ", 
                  leave=False, ncols=80, file=sys.stdout):
        traffic = simulator.generate_mirai_botnet(device, 1)
        device_traffic.extend(traffic)
    
    all_traffic.extend(device_traffic)
    device_stats[device] = len(device_traffic)

# Створення DataFrame
print_step("📦 Створення DataFrame...")
df = pd.DataFrame(all_traffic)

# Статистика
print_header("📊 СТАТИСТИКА ДАТАСЕТУ")
print(f"{'Параметр':<20} {'Значення':>15}")
print("-" * 70)
print(f"{'Всього записів:':<20} {len(df):>15,}")
print(f"{'Ознак:':<20} {len(df.columns):>15}")
print()

print("Розподіл по типах:")
print("-" * 70)
for label, count in df['label'].value_counts().items():
    pct = (count / len(df)) * 100
    print(f"  {label:<17} {count:>6,}  ({pct:>5.1f}%)")

print()
print("Розподіл по пристроях:")
print("-" * 70)
for device, count in device_stats.items():
    pct = (count / len(df)) * 100
    print(f"  {device:<17} {count:>6,}  ({pct:>5.1f}%)")

# Збереження
print_step("💾 Збереження датасету...")
df.to_csv('data/synthetic_iot_dataset.csv', index=False)
print_step("✅ Збережено: data/synthetic_iot_dataset.csv")

# Крок 4: Підготовка даних
print_header("🔧 ПІДГОТОВКА ДО НАВЧАННЯ")

feature_columns = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl']
X = df[feature_columns]
y = (df['label'] != 'Benign').astype(int)

print(f"{'Параметр':<25} {'Значення':>15}")
print("-" * 70)
print(f"{'Розмір матриці ознак:':<25} {str(X.shape):>15}")
print(f"{'Benign трафік:':<25} {sum(y==0):>15,}")
print(f"{'Malicious трафік:':<25} {sum(y==1):>15,}")
print(f"{'Співвідношення:':<25} {f'{sum(y==0)/sum(y==1):.2f}:1':>15}")

# Крок 5: Навчання моделі
print_header("🤖 НАВЧАННЯ TENSORFLOW МОДЕЛІ")

print_step("Створення моделі...")
detector = IoTAnomalyDetector(input_dim=X.shape[1])

print_step("Початок навчання (30 епох)")
print_step("Це займе 5-10 хвилин. Зачекайте...")
print()

# Навчання з progress
try:
    history, (X_test, y_test) = detector.train(
        X, y, 
        epochs=30, 
        batch_size=128, 
        model_type='classifier'
    )
    
    print()
    print_step("✅ Навчання завершено!")
    
except Exception as e:
    print()
    print_step(f"❌ Помилка: {str(e)}")
    sys.exit(1)

# Крок 6: Збереження моделі
print_header("💾 ЗБЕРЕЖЕННЯ МОДЕЛІ")

print_step("Збереження моделі та preprocessor...")
detector.save_model()
print_step("✅ Модель збережено:")
print_step("   • models/anomaly_detector.h5")
print_step("   • models/preprocessor.pkl")
print_step("   • models/model_metrics.json")

# Результати
print_header("✅ СИСТЕМА ГОТОВА!")

print("\n📊 Фінальні метрики:")
print("-" * 70)
print(f"  Training Accuracy:     {history.history['accuracy'][-1]*100:6.2f}%")
print(f"  Validation Accuracy:   {history.history['val_accuracy'][-1]*100:6.2f}%")
print(f"  Training Loss:         {history.history['loss'][-1]:6.4f}")
print(f"  Validation Loss:       {history.history['val_loss'][-1]:6.4f}")

if 'precision' in history.history:
    print(f"  Precision:             {history.history['precision'][-1]*100:6.2f}%")
if 'recall' in history.history:
    print(f"  Recall:                {history.history['recall'][-1]*100:6.2f}%")

# Час виконання
print_header("⏱️ ЧАС ВИКОНАННЯ")
print_step(f"Завершено: {datetime.now().strftime('%H:%M:%S')}")

# Інструкції
print_header("💡 НАСТУПНІ КРОКИ")
print("""
1. Запустіть Dashboard:
   streamlit run dashboard.py

2. Оберіть режим "🎬 Live Demo"

3. Натисніть "📥 Завантажити модель"

4. Налаштуйте параметри:
   • Ймовірність атаки: 40%
   • Швидкість: 2 сек

5. Натисніть "▶️ Старт"

6. Насолоджуйтесь демонстрацією! 🎉
""")

print("="*70)
print("🎓 Готово до захисту магістерської роботи!")
print("="*70 + "\n")