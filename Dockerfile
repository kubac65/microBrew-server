FROM python:slim-stretch
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

EXPOSE 52100
CMD ["python", "program.py"]