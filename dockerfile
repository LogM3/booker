FROM python:3.11

RUN mkdir /booking
WORKDIR /booking

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN alembic upgrade head

# CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
