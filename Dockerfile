FROM python:3.9
ENV PYTHONUNBUFFERED 13
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

CMD uvicorn fastService:app --port 8000 --host 0.0.0.0
