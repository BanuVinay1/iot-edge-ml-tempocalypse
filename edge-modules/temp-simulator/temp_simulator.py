import time
import json
import random
import pandas as pd
from collections import deque
from datetime import datetime
from azure.iot.device import IoTHubModuleClient, Message

# Create IoT Edge client
client = IoTHubModuleClient.create_from_edge_environment()
client.connect()

# Rolling history for calculations
history = deque(maxlen=5)
prev_temps = deque(maxlen=5)

def generate_sensor_data():
    base_temp = 25 + random.normalvariate(0, 0.5)
    spike = random.random() < 0.01  # 1% chance of spike
    temperature = base_temp + random.uniform(20, 30) if spike else base_temp
    humidity = 50 + random.normalvariate(0, 2)
    return round(temperature, 2), round(humidity, 2)

while True:
    temp, hum = generate_sensor_data()
    history.append(temp)
    prev_temps.append(temp)

    # 7 features for the ML model
    temp_delta = temp - prev_temps[-2] if len(prev_temps) >= 2 else 0
    rolling_mean_5 = pd.Series(list(history)).mean() if len(history) >= 1 else temp
    rolling_std_5 = pd.Series(list(history)).std() if len(history) >= 2 else 0
    rolling_max_5 = max(history) if history else temp
    temp_diff_3min = temp - prev_temps[-4] if len(prev_temps) >= 4 else 0

    payload = {
        "temperature": temp,
        "humidity": hum,
        "temp_delta": round(temp_delta, 2),
        "rolling_mean_5": round(rolling_mean_5, 2),
        "rolling_std_5": round(rolling_std_5, 2),
        "rolling_max_5": round(rolling_max_5, 2),
        "temp_diff_3min": round(temp_diff_3min, 2)
    }

    message = Message(json.dumps(payload))
    client.send_message_to_output(message, "output1")
    print(f"[temp-simulator] Sent: {payload}")

    time.sleep(5)