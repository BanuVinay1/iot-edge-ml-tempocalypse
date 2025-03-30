FROM mcr.microsoft.com/devcontainers/python:0-3.9

WORKDIR /app

COPY temp_simulator.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN echo "build-$(date +%s)" > /build_id.txt

CMD ["python", "temp_simulator.py"]