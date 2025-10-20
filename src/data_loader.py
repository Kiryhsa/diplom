import pandas as pd
import numpy as np
from pathlib import Path

class IoTDataLoader:
    def __init__(self, data_path='data/iot23_dataset.csv'):
        self.data_path = data_path
        self.data = None
        
    def load_data(self, sample_size=None):
        print(f"📥 Завантаження даних з {self.data_path}...")
        try:
            self.data = pd.read_csv(self.data_path)
            if sample_size:
                self.data = self.data.sample(n=sample_size, random_state=42)
            print(f"✅ Завантажено {len(self.data)} записів")
            return self.data
        except FileNotFoundError:
            print("❌ Файл не знайдено!")
            return None
    
    def get_basic_stats(self):
        if self.data is None:
            return None
        stats = {
            'total_records': len(self.data),
            'features': list(self.data.columns),
            'missing_values': self.data.isnull().sum().to_dict(),
            'label_distribution': self.data['label'].value_counts().to_dict() if 'label' in self.data.columns else None
        }
        return stats
    
    def prepare_features(self):
        numeric_features = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl']
        available_features = [f for f in numeric_features if f in self.data.columns]
        X = self.data[available_features]
        y = None
        if 'label' in self.data.columns:
            y = (self.data['label'] != 'Benign').astype(int)
        return X, y, available_features
