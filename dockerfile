FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["bash", "-c", "python -m parser.main && uvicorn parser.api:app --host 0.0.0.0 --port 8000"]
