FROM python:3.12.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install dash gunicorn

COPY . .

EXPOSE 8051

CMD ["gunicorn", "app:server", "-w", "1", "-b", "0.0.0.0:8051"]