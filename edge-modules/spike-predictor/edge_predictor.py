from azure.iot.device.aio import IoTHubModuleClient
import asyncio
import json
from flask import Flask, request, jsonify
import joblib
import numpy as np
import threading

app = Flask(__name__)

model = joblib.load("models/rf_model.pkl")
threshold = 0.6

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array([[data['temperature'], data['humidity'], data['temp_delta'],
                          data['rolling_mean_5'], data['rolling_std_5'],
                          data['rolling_max_5'], data['temp_diff_3min']]])
    prob = model.predict_proba(features)[0][1]
    prediction = 1 if prob > threshold else 0
    return jsonify({'prediction': prediction, 'spike_probability': round(prob, 4)})

async def input_listener(client):
    while True:
        msg = await client.receive_message_on_input("input1")
        data = json.loads(msg.data)
        print(f"[spike-predictor] Received input: {data}")

        features = np.array([[data['temperature'], data['humidity'], data['temp_delta'],
                              data['rolling_mean_5'], data['rolling_std_5'],
                              data['rolling_max_5'], data['temp_diff_3min']]])
        prob = model.predict_proba(features)[0][1]
        prediction = 1 if prob > threshold else 0

        if prediction == 1:
            output_msg = json.dumps({
                'temperature': data['temperature'],
                'spike_probability': round(prob, 4),
                'spike_detected': True
            })
            await client.send_message_to_output(output_msg, "output1")
            print(f"[spike-predictor] Spike detected and sent: {output_msg}")
        else:
            print("[spike-predictor] No spike detected")

async def main_async():
    client = IoTHubModuleClient.create_from_edge_environment()
    await client.connect()
    print("[spike-predictor] Connected to Edge Hub")
    await input_listener(client)

def run_async_loop():
    asyncio.run(main_async())

if __name__ == '__main__':
    threading.Thread(target=run_async_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)