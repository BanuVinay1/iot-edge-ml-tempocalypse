FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY edge_predictor.py .


RUN mkdir -p models


COPY models/rf_model.pkl models/rf_model.pkl

CMD ["python", "edge_predictor.py"]