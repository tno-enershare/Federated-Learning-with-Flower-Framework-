FROM python:3.10-slim

WORKDIR /app

COPY . .

# Convert line endings and set permissions
RUN apt-get update && apt-get install -y dos2unix && dos2unix run.sh && chmod +x run.sh

RUN pip install --no-cache-dir -r requirements.txt

CMD ["./run.sh"]
