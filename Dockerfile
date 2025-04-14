# Use a clean, vulnerability‑free base image (Alpine with Python 3.13)
FROM python:3.13-alpine AS runtime

# Install OS dependencies needed by diagrams (Graphviz, cairo, etc.)
RUN apk update && apk add --no-cache \
    build-base \
    graphviz \
    cairo-dev \
    pango-dev \
    gdk-pixbuf-dev \
    freetype-dev

WORKDIR /app

# Copy requirements and install Python packages.
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code and auxiliary files.
COPY ./src ./src
COPY README.md .
COPY .env.example .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
