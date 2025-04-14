FROM python:3.12-slim AS runtime

# Install required system dependencies for diagrams + Graphviz
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    graphviz \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libfreetype6-dev \
    curl \
    git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install pip dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
        torch==2.2.2 torchvision==0.17.2 && \
    pip install --no-cache-dir -r requirements.txt

# Copy app code and assets
COPY ./src ./src
COPY README.md .
COPY .env.example .

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
