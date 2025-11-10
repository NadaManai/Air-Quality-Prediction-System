FROM python:3.10-slim

WORKDIR /app

COPY app/main.py ./app/
COPY Models/xgboost_model.pkl ./Models/
COPY requirements.txt ./

ENV PIP_DEFAULT_TIMEOUT=200
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
