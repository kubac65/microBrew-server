FROM python:3.8.5-slim
WORKDIR /app
COPY ./src /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

EXPOSE 52100
CMD ["python", "program.py"]
