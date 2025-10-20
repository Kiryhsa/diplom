import numpy as np
import pandas as pd
from datetime import datetime

class IoTTrafficSimulator:
    def __init__(self):
        self.device_types = ['Smart Camera', 'Smart Thermostat', 'Smart Lock', 'Smart Speaker', 'Smart Light']
        self.normal_profiles = {
            'Smart Camera': {'dur': (1.0, 5.0), 'spkts': (10, 50), 'dpkts': (5, 30), 'sbytes': (500, 2000), 
                           'dbytes': (300, 1500), 'rate': (10, 100), 'sttl': (64, 128), 'dttl': (64, 128)},
            'Smart Thermostat': {'dur': (0.5, 2.0), 'spkts': (5, 20), 'dpkts': (3, 15), 'sbytes': (100, 500),
                               'dbytes': (50, 300), 'rate': (5, 30), 'sttl': (64, 128), 'dttl': (64, 128)},
            'Smart Lock': {'dur': (0.1, 1.0), 'spkts': (2, 10), 'dpkts': (2, 8), 'sbytes': (50, 200),
                         'dbytes': (50, 150), 'rate': (5, 20), 'sttl': (64, 128), 'dttl': (64, 128)},
            'Smart Speaker': {'dur': (2.0, 10.0), 'spkts': (20, 100), 'dpkts': (15, 80), 'sbytes': (1000, 5000),
                            'dbytes': (800, 4000), 'rate': (20, 200), 'sttl': (64, 128), 'dttl': (64, 128)},
            'Smart Light': {'dur': (0.1, 0.5), 'spkts': (1, 5), 'dpkts': (1, 3), 'sbytes': (20, 100),
                          'dbytes': (20, 80), 'rate': (2, 10), 'sttl': (64, 128), 'dttl': (64, 128)}
        }
    
    def generate_normal_traffic(self, device_type, n_packets=1):
        profile = self.normal_profiles[device_type]
        traffic = []
        for _ in range(n_packets):
            packet = {
                'timestamp': datetime.now(), 'device': device_type,
                'dur': np.random.uniform(*profile['dur']),
                'spkts': int(np.random.uniform(*profile['spkts'])),
                'dpkts': int(np.random.uniform(*profile['dpkts'])),
                'sbytes': int(np.random.uniform(*profile['sbytes'])),
                'dbytes': int(np.random.uniform(*profile['dbytes'])),
                'rate': np.random.uniform(*profile['rate']),
                'sttl': int(np.random.uniform(*profile['sttl'])),
                'dttl': int(np.random.uniform(*profile['dttl'])),
                'label': 'Benign'
            }
            traffic.append(packet)
        return traffic
    
    def generate_ddos_attack(self, device_type, n_packets=1):
        traffic = []
        for _ in range(n_packets):
            packet = {
                'timestamp': datetime.now(), 'device': device_type,
                'dur': np.random.uniform(0.01, 0.1),
                'spkts': int(np.random.uniform(100, 500)),
                'dpkts': int(np.random.uniform(5, 20)),
                'sbytes': int(np.random.uniform(5000, 20000)),
                'dbytes': int(np.random.uniform(50, 200)),
                'rate': np.random.uniform(500, 2000),
                'sttl': int(np.random.uniform(32, 64)),
                'dttl': int(np.random.uniform(32, 64)),
                'label': 'DDoS'
            }
            traffic.append(packet)
        return traffic
    
    def generate_port_scan(self, device_type, n_packets=1):
        traffic = []
        for _ in range(n_packets):
            packet = {
                'timestamp': datetime.now(), 'device': device_type,
                'dur': np.random.uniform(0.01, 0.05),
                'spkts': int(np.random.uniform(1, 3)),
                'dpkts': int(np.random.uniform(0, 2)),
                'sbytes': int(np.random.uniform(20, 100)),
                'dbytes': int(np.random.uniform(0, 50)),
                'rate': np.random.uniform(200, 500),
                'sttl': int(np.random.uniform(64, 128)),
                'dttl': int(np.random.uniform(64, 128)),
                'label': 'PortScan'
            }
            traffic.append(packet)
        return traffic
    
    def generate_mirai_botnet(self, device_type, n_packets=1):
        traffic = []
        for _ in range(n_packets):
            packet = {
                'timestamp': datetime.now(), 'device': device_type,
                'dur': np.random.uniform(0.5, 2.0),
                'spkts': int(np.random.uniform(50, 200)),
                'dpkts': int(np.random.uniform(40, 180)),
                'sbytes': int(np.random.uniform(2000, 10000)),
                'dbytes': int(np.random.uniform(1500, 8000)),
                'rate': np.random.uniform(100, 400),
                'sttl': int(np.random.uniform(48, 64)),
                'dttl': int(np.random.uniform(48, 64)),
                'label': 'Mirai'
            }
            traffic.append(packet)
        return traffic
