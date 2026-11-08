# ML Training and Inference Worker Image
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY models/requirements.txt* ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; \
    else pip install --no-cache-dir numpy pandas scikit-learn lightgbm joblib torch; fi

COPY models /app/models
COPY scripts/ml /app/scripts/ml

ENV PYTHONUNBUFFERED=1

CMD ["python", "scripts/ml/evaluate_models.py"]
