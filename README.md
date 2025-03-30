# 🌡️ IOT-EDGE-SPIKE-DETECTOR

An AI-powered IoT Edge solution that detects **real-time temperature spikes** with zero internet dependency. Built with **Azure IoT Edge**, this project runs a trained **Random Forest** ML model directly at the edge using Docker containers.

> 💥 Model inference runs **entirely at the Edge** – enabling ultra-low-latency, offline predictions without cloud calls.  
> 🚀 Designed for industrial safety, smart factories, and edge-enabled anomaly detection.

---

## 🧠 How It Works

### 🔁 End-to-End Flow:
Synthetic Sensor → Edge ML Prediction → Azure IoT Hub (if spike) → Cloud

### 🔌 Pipeline

1. **temp-simulator**  
   - Simulates live temperature, humidity, and rolling stats.
   - Sends enriched data to the spike detector module.

2. **spike-predictor**  
   - Loads pre-trained ML model (`RandomForest`) inside a Docker container.
   - Makes predictions locally on incoming data.
   - Sends only spike alerts to the cloud.

3. **Azure IoT Hub**  
   - Collects only spike events, reducing bandwidth and noise.

   ---

## 🧱 Project Structure

```bash
IOT-EDGE-SPIKE-DETECTOR
│
├── edge-modules/
│   ├── spike-predictor/
│   │   ├── edge_predictor.py        # Edge ML inference logic
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── models/
│   │       └── tempocalypse_model.pkl
│   │
│   └── temp-simulator/
│       ├── temp_simulator.py        # Synthetic data generator
│       ├── Dockerfile
│       └── requirements.txt
│
├── model-training/
│   ├── trainingpipeline.py          # Model training script
│   ├── data/
│   │   └── temperature_data.parquet
│   └── models/
│       └── tempocalypse_model.pkl
│
├── Deployment.json                  # Azure IoT Edge deployment config
└── README.md


🔍 Key Features
✅ Runs Offline: No internet required for inference.

✅ Real-Time ML: Predicts temperature spikes using edge-local ML model.

✅ IoT Edge Optimized: Fully Dockerized and Azure IoT Edge compatible.

✅ Event-Driven: Only spike alerts are sent upstream, saving bandwidth.

✅ Custom Simulated Data: Uses synthetic, labeled data with rolling stats.



🚀 Setup & Deployment
Prerequisites: Azure IoT Hub, Azure VM / Raspberry Pi, Azure CLI, IoT Edge runtime installed.

🧪 1. Train the Model
cd model-training
python trainingpipeline.py

This will output tempocalypse_model.pkl

🧱 2. Build Docker Modules
cd edge-modules/spike-predictor
docker build -t <acr-name>.azurecr.io/spike-predictor:latest .

cd ../temp-simulator
docker build -t <acr-name>.azurecr.io/temp-simulator:latest .

Push both images to your Azure Container Registry.


📦 3. Deploy to IoT Edge
az iot edge set-modules --device-id <device-id> \
  --hub-name <iot-hub-name> \
  --content Deployment.json

📈 Sample Spike Detection
{
  "temperature": 26.5,
  "spike_probability": 0.67,
  "spike_detected": true
}

🌱 Future Enhancements
📊 Grafana real-time dashboards using ADX.

⚠️ Edge-to-Cloud alerting via Azure Functions.

🧠 Convert model to ONNX for true TinyML compatibility.

🤖 Switch to XGBoost + auto retraining pipeline.

⏱️ Edge buffering module for network outages.



🙌 Acknowledgements
Built with ❤️ by BanuVinay1
Edge ML. Real-Time. Reliable. 💡
