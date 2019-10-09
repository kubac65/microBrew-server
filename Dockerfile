FROM python:slim-stretch
WORKDIR /app
COPY ./src /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

EXPOSE 52100
CMD ["python", "program.py"]