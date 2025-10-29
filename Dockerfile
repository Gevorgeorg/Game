FROM python:3.12

WORKDIR /code
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN mkdir -p data
RUN useradd --create-home --shell /bin/bash app

USER app
EXPOSE 5000
CMD ["python", "app.py"]