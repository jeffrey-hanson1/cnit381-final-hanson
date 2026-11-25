FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

COPY devices.yml .
COPY template.j2 .
COPY generate.py .

CMD ["python3", "generate.py"]
