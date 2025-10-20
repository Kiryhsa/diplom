import numpy as np
import pandas as pd
from src.model_training import IoTAnomalyDetector
from src.simulator import IoTTrafficSimulator
import os
from datetime import datetime

def print_progress(message, progress=None):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if progress:
        print(f"[{timestamp}] {message} ({progress}%)")
    else:
        print(f"[{timestamp}] {message}")

print("="*70)
print("🚀 IoT Security AI - Швидкий старт")
print("="*70)

# Створення папок
print_progress("Створення директорій...")
os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)
print_progress("✅ Директорії створено")

# Генерація даних
print_progress("📊 Початок генерації даних...")
simulator = IoTTrafficSimulator()
all_traffic = []

total_packets = 0
target_packets = 7750

print_progress(f"Генерація даних для {len(simulator.device_types)} пристроїв...")

for i, device in enumerate(simulator.device_types, 1):
    print_progress(f"  Пристрій {i}/5: {device}")
    
    # Нормальний трафік
    print_progress(f"    → Генерація нормального трафіку (1000 пакетів)...")
    normal = simulator.generate_normal_traffic(device, n_packets=1000)
    all_traffic.extend(normal)
    total_packets += 1000
    progress = int((total_packets / target_packets) * 100)
    print_progress(f"    ✓ Згенеровано {total_packets}/{target_packets}", progress)
    
    # DDoS
    print_progress(f"    → Генерація DDoS атак (200 пакетів)...")
    ddos = simulator.generate_ddos_attack(device, n_packets=200)
    all_traffic.extend(ddos)
    total_packets += 200
    progress = int((total_packets / target_packets) * 100)
    print_progress(f"    ✓ Згенеровано {total_packets}/{target_packets}", progress)
    
    # Port Scan
    print_progress(f"    → Генерація Port Scan (150 пакетів)...")
    port_scan = simulator.generate_port_scan(device, n_packets=150)
    all_traffic.extend(port_scan)
    total_packets += 150
    progress = int((total_packets / target_packets) * 100)
    print_progress(f"    ✓ Згенеровано {total_packets}/{target_packets}", progress)
    
    # Mirai
    print_progress(f"    → Генерація Mirai Botnet (100 пакетів)...")
    mirai = simulator.generate_mirai_botnet(device, n_packets=100)
    all_traffic.extend(mirai)
    total_packets += 100
    progress = int((total_packets / target_packets) * 100)
    print_progress(f"    ✓ Згенеровано {total_packets}/{target_packets}", progress)

df = pd.DataFrame(all_traffic)
print_progress(f"✅ Всього згенеровано: {len(df):,} записів")

# Збереження
print_progress("💾 Збереження датасету...")
df.to_csv('data/synthetic_iot_dataset.csv', index=False)
print_progress("✅ Датасет збережено: data/synthetic_iot_dataset.csv")

# Статистика
print("\n" + "="*70)
print("📊 СТАТИСТИКА ДАТАСЕТУ")
print("="*70)
for label, count in df['label'].value_counts().items():
    pct = (count / len(df)) * 100
    print(f"  {label:15s}: {count:5d} ({pct:5.1f}%)")

# Підготовка до навчання
print("\n" + "="*70)
print("🔧 ПІДГОТОВКА ДО НАВЧАННЯ")
print("="*70)
feature_columns = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl']
X = df[feature_columns]
y = (df['label'] != 'Benign').astype(int)
print_progress(f"Розмір матриці ознак: {X.shape}")
print_progress(f"Benign: {sum(y==0)} | Malicious: {sum(y==1)}")

# Навчання
print("\n" + "="*70)
print("🤖 НАВЧАННЯ TENSORFLOW МОДЕЛІ")
print("="*70)
detector = IoTAnomalyDetector(input_dim=X.shape[1])

print_progress("Початок навчання (30 епох)...")
print_progress("Це займе 5-10 хвилин. Зачекайте...\n")

history, (X_test, y_test) = detector.train(X, y, epochs=30, batch_size=128, model_type='classifier')

# Збереження моделі
print("\n" + "="*70)
print_progress("💾 Збереження моделі...")
detector.save_model()

# Результати
print("\n" + "="*70)
print("✅ СИСТЕМА ГОТОВА ДО РОБОТИ!")
print("="*70)
print(f"📊 Training Accuracy:    {history.history['accuracy'][-1]*100:.2f}%")
print(f"📊 Validation Accuracy:  {history.history['val_accuracy'][-1]*100:.2f}%")
print(f"📊 Final Loss:           {history.history['loss'][-1]:.4f}")
print("="*70)

print("\n💡 Наступні кроки:")
print("   1. Запустіть Dashboard:  streamlit run dashboard.py")
print("   2. Оберіть режим 'Live Demo'")
print("   3. Натисніть 'Завантажити модель'")
print("   4. Насолоджуйтесь демонстрацією! 🎉")