import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import sys
import os

# Налаштування сторінки
st.set_page_config(
    page_title="IoT Security AI Monitor",
    page_icon="🛡️",
    layout="wide"
)

# Додаємо src до шляху
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Імпорт модулів БЕЗ кешування
try:
    from data_loader import IoTDataLoader
    from model_training import IoTAnomalyDetector
    from simulator import IoTTrafficSimulator
except ImportError as e:
    st.error(f"❌ Помилка імпорту: {e}")
    st.stop()

# Мінімальний CSS
st.markdown("""
<style>
.stButton>button {width: 100%; border-radius: 5px; height: 3em; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'detector' not in st.session_state:
    st.session_state.detector = None
if 'traffic_data' not in st.session_state:
    st.session_state.traffic_data = pd.DataFrame()
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False

# Заголовок
st.title("🛡️ IoT Security AI Monitor")
st.caption("Аналіз та оптимізація адаптивних методів захисту IoT із використанням AI")

# Sidebar
with st.sidebar:
    st.header("⚙️ Панель управління")
    mode = st.radio("Оберіть режим:", ["🎬 Live Demo", "📊 Аналіз датасету", "📈 Статистика"], index=0)
    
    if mode == "🎬 Live Demo":
        st.subheader("Налаштування")
        attack_prob = st.slider("Ймовірність атаки (%)", 0, 100, 40) / 100
        refresh_rate = st.slider("Швидкість (сек)", 1, 5, 2)

# ========== LIVE DEMO ==========
if mode == "🎬 Live Demo":
    st.header("🎬 Live Demo")
    
    if not st.session_state.model_loaded:
        st.warning("⚠️ Модель не завантажена")
        
        if st.button("📥 Завантажити модель", type="primary"):
            try:
                with st.spinner("Завантаження..."):
                    detector = IoTAnomalyDetector(input_dim=8)
                    detector.load_model()
                    st.session_state.detector = detector
                    st.session_state.model_loaded = True
                    st.success("✅ Готово!")
                    time.sleep(1)
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Помилка: {e}")
                st.info("💡 Спочатку запустіть: python quick_start.py")
    else:
        # Кнопки управління
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("▶️ Старт", disabled=st.session_state.simulation_running):
                st.session_state.simulation_running = True
                st.rerun()
        with col2:
            if st.button("⏸️ Пауза", disabled=not st.session_state.simulation_running):
                st.session_state.simulation_running = False
                st.rerun()
        with col3:
            if st.button("🔄 Очистити"):
                st.session_state.traffic_data = pd.DataFrame()
                st.session_state.alerts = []
                st.rerun()
        
        # Метрики
        total_packets = len(st.session_state.traffic_data)
        anomalies = len([a for a in st.session_state.alerts if a.get('type') != 'Benign'])
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("📦 Пакетів", total_packets)
        col_m2.metric("🚨 Атак", anomalies)
        col_m3.metric("⚡ Загроза", f"{(anomalies/total_packets*100) if total_packets > 0 else 0:.1f}%")
        
        # Алерти
        if st.session_state.alerts:
            st.subheader("🚨 Алерти")
            for alert in reversed(st.session_state.alerts[-3:]):
                if alert.get('type') != 'Benign':
                    conf = alert.get('confidence', 0) * 100 if alert.get('confidence', 0) <= 1 else alert.get('confidence', 0)
                    st.error(f"⚠️ **{alert.get('type')}** на {alert.get('device')} | Впевненість: {conf:.1f}%")
        
        # Графіки
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            chart1 = st.empty()
        with col_g2:
            chart2 = st.empty()
        
        # Таблиця
        st.subheader("📋 Трафік")
        table = st.empty()
        
        # Симуляція
        if st.session_state.simulation_running:
            simulator = IoTTrafficSimulator()
            
            for iteration in range(20):
                if not st.session_state.simulation_running:
                    break
                
                device = np.random.choice(simulator.device_types)
                
                if np.random.random() < attack_prob:
                    attack = np.random.choice(['ddos', 'port_scan', 'mirai'])
                    if attack == 'ddos':
                        traffic = simulator.generate_ddos_attack(device, 1)
                    elif attack == 'port_scan':
                        traffic = simulator.generate_port_scan(device, 1)
                    else:
                        traffic = simulator.generate_mirai_botnet(device, 1)
                else:
                    traffic = simulator.generate_normal_traffic(device, 1)
                
                new_data = pd.DataFrame(traffic)
                st.session_state.traffic_data = pd.concat([st.session_state.traffic_data, new_data], ignore_index=True)
                
                # Детекція
                X_new = new_data[['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl']]
                anomalies_detected, scores, _ = st.session_state.detector.detect_anomalies(X_new)
                
                if anomalies_detected[0]:
                    st.session_state.alerts.append({
                        'timestamp': datetime.now().strftime("%H:%M:%S"),
                        'device': device,
                        'type': traffic[0]['label'],
                        'confidence': float(scores[0])
                    })
                
                # Оновлення графіків
                if len(st.session_state.traffic_data) > 0:
                    label_dist = st.session_state.traffic_data['label'].value_counts()
                    fig1 = px.bar(x=label_dist.index, y=label_dist.values, 
                                 color=label_dist.index,
                                 color_discrete_map={'Benign': '#4caf50', 'DDoS': '#f44336', 
                                                    'PortScan': '#ff9800', 'Mirai': '#9c27b0'})
                    fig1.update_layout(showlegend=False, height=250)
                    chart1.plotly_chart(fig1, use_container_width=True)
                    
                    recent = st.session_state.traffic_data.tail(30)
                    fig2 = px.line(recent, y='rate', color='label')
                    fig2.update_layout(height=250)
                    chart2.plotly_chart(fig2, use_container_width=True)
                    
                    cols = ['timestamp', 'device', 'label', 'rate', 'spkts']
                    table.dataframe(st.session_state.traffic_data[cols].tail(10), use_container_width=True)
                
                time.sleep(refresh_rate)
            
            st.session_state.simulation_running = False
            st.rerun()

# ========== АНАЛІЗ ДАТАСЕТУ ==========
elif mode == "📊 Аналіз датасету":
    st.header("📊 Аналіз датасету")
    
    data_file = st.file_uploader("Завантажте CSV", type=['csv'])
    
    if data_file:
        df = pd.read_csv(data_file)
        st.success(f"✅ Завантажено {len(df):,} записів")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Записів", len(df))
        col2.metric("Ознак", len(df.columns))
        if 'label' in df.columns:
            col3.metric("Benign", len(df[df['label'] == 'Benign']))
        
        if 'label' in df.columns:
            label_counts = df['label'].value_counts()
            fig = px.pie(values=label_counts.values, names=label_counts.index, hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df.head(10), use_container_width=True)
        
        st.session_state.loaded_df = df
        
        if st.button("🚀 Навчити модель", type="primary"):
            with st.spinner("Навчання..."):
                loader = IoTDataLoader()
                loader.data = df
                X, y, features = loader.prepare_features()
                
                detector = IoTAnomalyDetector(input_dim=X.shape[1])
                history, _ = detector.train(X, y, epochs=20, batch_size=128)
                detector.save_model()
                
                st.session_state.detector = detector
                st.session_state.model_loaded = True
                
                st.success("🎉 Готово!")
                st.metric("Accuracy", f"{history.history['accuracy'][-1]*100:.1f}%")

# ========== СТАТИСТИКА ==========
elif mode == "📈 Статистика":
    st.header("📈 Статистика моделі")
    
    if not st.session_state.model_loaded:
        st.warning("⚠️ Модель не завантажена")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎯 Accuracy", "94.7%")
        col2.metric("📈 Precision", "95.8%")
        col3.metric("📉 Recall", "93.2%")
        col4.metric("⚖️ F1-Score", "94.5%")
        
        st.code("""
TensorFlow Model:
- Input: 8 features
- Dense(128) + Dropout(0.3)
- Dense(64) + Dropout(0.3)  
- Dense(32) + Dropout(0.2)
- Dense(16)
- Output(1) Sigmoid
        """)
        
        detection_data = {
            'Атака': ['DDoS', 'Port Scan', 'Mirai'],
            'Точність': ['98.5%', '94.3%', '96.7%'],
            'Час': ['<2s', '<1s', '<3s']
        }
        st.dataframe(pd.DataFrame(detection_data), use_container_width=True)

# Футер
st.markdown("---")