import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import datetime

print("[*] Initializing AI Defender Engine...")

normal_traffic = {
    'packet_size': np.random.normal(loc=500, scale=50, size=200),
    'request_frequency': np.random.normal(loc=2, scale=0.5, size=200)
}
df_normal = pd.DataFrame(normal_traffic)

ai_model = IsolationForest(contamination=0.02, random_state=42)
ai_model.fit(df_normal)
print("[+] AI Engine trained successfully on baseline system patterns.")

test_activities = [
    {"name": "Standard Web Browsing", "packet_size": 520, "request_frequency": 1.8},
    {"name": "Automated Nmap Scan / Directory Busting", "packet_size": 64, "request_frequency": 45.0},
    {"name": "Database Exfiltration Attempt", "packet_size": 6500, "request_frequency": 3.2}
]

print("\n[*] Monitoring incoming system logs...")
print("-" * 65)

for activity in test_activities:
    features = pd.DataFrame(
        [[activity['packet_size'], activity['request_frequency']]],
        columns=['packet_size', 'request_frequency']
    )
    prediction = ai_model.predict(features)[0]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if prediction == -1:
        print(f"[{timestamp}] [ALERT - ANOMALY DETECTED] Target: {activity['name']}")
        print(f"    ↳ Metrics: Size {activity['packet_size']}b | Freq {activity['request_frequency']}/sec")
        print("    ↳ Action: Automated trigger sent to block traffic.\n")
    else:
        print(f"[{timestamp}] [INFO - PASS] Target: {activity['name']} behaves normally.\n")
