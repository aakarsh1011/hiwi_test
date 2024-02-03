FROM python:latest

COPY . /data_supplier
WORKDIR /data_supplier

RUN pip install -r requirements.txt
RUN apt update && apt install -y iputils-ping

CMD ["python", "./src/main.py"]