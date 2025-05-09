FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY .env .env
ENV FLASK_APP=app/views.py
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]
