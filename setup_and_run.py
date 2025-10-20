"""
Автоматичний скрипт для встановлення та запуску IoT Security AI Monitor
Виконує всі необхідні кроки для підготовки системи до демонстрації
"""

import os
import sys
import subprocess
import time

def print_header(text):
    """Красивий заголовок"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_step(step_num, text):
    """Крок виконання"""
    print(f"\n{'─'*70}")
    print(f"📍 Крок {step_num}: {text}")
    print(f"{'─'*70}\n")

def check_python_version():
    """Перевірка версії Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Потрібен Python 3.8 або вище!")
        print(f"   Поточна версія: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")

def create_directories():
    """Створення необхідних директорій"""
    dirs = ['data', 'models', 'src']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✅ Створено папку: {dir_name}/")

def check_requirements():
    """Перевірка встановлених пакетів"""
    try:
        import tensorflow
        import streamlit
        import pandas
        import numpy
        import plotly
        print("✅ Всі залежності встановлені")
        return True
    except ImportError as e:
        print(f"⚠️  Відсутні залежності: {e}")
        return False

def install_requirements():
    """Встановлення залежностей"""
    print("📦 Встановлення залежностей...")
    print("   Це може зайняти 5-10 хвилин...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "tensorflow==2.15.0",
            "streamlit==1.28.0",
            "pandas==2.1.0",
            "numpy==1.24.3",
            "plotly==5.17.0",
            "scikit-learn==1.3.0",
            "matplotlib==3.8.0",
            "seaborn==0.13.0",
            "joblib==1.3.2",
            "-q"
        ])
        print("✅ Залежності встановлені успішно!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка встановлення: {e}")
        return False

def check_files():
    """Перевірка наявності необхідних файлів"""
    required_files = [
        'src/__init__.py',
        'src/data_loader.py',
        'src/model_training.py',
        'src/simulator.py',
        'dashboard.py',
        'quick_start.py',
        'requirements.txt'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print("⚠️  Відсутні файли:")
        for file in missing:
            print(f"   ❌ {file}")
        return False
    
    print("✅ Всі необхідні файли присутні")
    return True

def generate_data_and_train():
    """Генерація даних та навчання моделі"""
    print("🤖 Генерація синтетичних даних та навчання моделі...")
    print("   Це займе 5-10 хвилин. Зачекайте...")
    
    try:
        result = subprocess.run(
            [sys.executable, "quick_start.py"],
            capture_output=True,
            text=True,
            timeout=600  # 10 хвилин timeout
        )
        
        if result.returncode == 0:
            print("✅ Модель успішно навчена!")
            print("\n📊 Результати:")
            # Виводимо останні 10 рядків виводу
            lines = result.stdout.strip().split('\n')
            for line in lines[-10:]:
                print(f"   {line}")
            return True
        else:
            print(f"❌ Помилка навчання: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️  Перевищено час очікування (10 хв)")
        return False
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

def launch_dashboard():
    """Запуск Dashboard"""
    print("🚀 Запуск Dashboard...")
    print("\n" + "="*70)
    print("  Dashboard буде доступний за адресою: http://localhost:8501")
    print("  Натисніть Ctrl+C для зупинки")
    print("="*70 + "\n")
    
    time.sleep(2)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard зупинено")

def main():
    """Головна функція"""
    print_header("🛡️ IoT Security AI Monitor - Автоматичне встановлення")
    
    # Крок 1: Перевірка Python
    print_step(1, "ПЕРЕВІРКА PYTHON")
    check_python_version()
    
    # Крок 2: Створення директорій
    print_step(2, "СТВОРЕННЯ СТРУКТУРИ ПРОЕКТУ")
    create_directories()
    
    # Крок 3: Перевірка файлів
    print_step(3, "ПЕРЕВІРКА ФАЙЛІВ")
    if not check_files():
        print("\n❌ Відсутні необхідні файли!")
        print("💡 Переконайтесь що всі файли створені згідно інструкції")
        sys.exit(1)
    
    # Крок 4: Перевірка залежностей
    print_step(4, "ПЕРЕВІРКА ЗАЛЕЖНОСТЕЙ")
    if not check_requirements():
        print("\n📦 Встановлення відсутніх залежностей...")
        response = input("   Продовжити встановлення? (y/n): ")
        if response.lower() == 'y':
            if not install_requirements():
                print("\n❌ Не вдалося встановити залежності")
                sys.exit(1)
        else:
            print("\n⚠️  Встановлення скасовано")
            sys.exit(0)
    
    # Крок 5: Генерація даних та навчання
    print_step(5, "ГЕНЕРАЦІЯ ДАНИХ ТА НАВЧАННЯ МОДЕЛІ")
    
    # Перевіряємо чи модель вже існує
    if os.path.exists('models/anomaly_detector.h5'):
        print("ℹ️  Модель вже існує")
        response = input("   Перенавчити модель? (y/n): ")
        if response.lower() == 'y':
            if not generate_data_and_train():
                print("\n⚠️  Навчання не вдалося, але можна продовжити з існуючою моделлю")
    else:
        if not generate_data_and_train():
            print("\n❌ Не вдалося навчити модель")
            print("💡 Спробуйте запустити вручну: python quick_start.py")
            sys.exit(1)
    
    # Крок 6: Запуск Dashboard
    print_step(6, "ЗАПУСК DASHBOARD")
    
    print("\n✅ Всі підготовчі кроки завершені!")
    print("\n" + "="*70)
    print("  СИСТЕМА ГОТОВА ДО ДЕМОНСТРАЦІЇ!")
    print("="*70)
    
    print("\n📋 Швидкі команди:")
    print("   • Запуск Dashboard:   streamlit run dashboard.py")
    print("   • Тестування:         python test_detection.py")
    print("   • Демо-презентація:   python demo_presentation.py")
    
    print("\n🎯 Режими Dashboard:")
    print("   1. 📊 Аналіз датасету - для роботи з реальними даними")
    print("   2. 🎬 Live Demo - для демонстрації на захисті")
    print("   3. 📈 Статистика - перегляд метрик моделі")
    
    response = input("\n🚀 Запустити Dashboard зараз? (y/n): ")
    if response.lower() == 'y':
        launch_dashboard()
    else:
        print("\n💡 Коли будете готові, запустіть: streamlit run dashboard.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Встановлення перервано користувачем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Критична помилка: {e}")
        sys.exit(1)