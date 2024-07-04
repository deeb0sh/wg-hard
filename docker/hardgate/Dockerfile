FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apk add wireguard-tools curl
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
