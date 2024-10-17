FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir numpy pandas

CMD ["python", "collect_predictions.py"]
