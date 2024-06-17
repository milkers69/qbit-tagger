FROM alpine:latest

RUN  apk add --no-cache --upgrade python3 py3-pip python3-dev

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "app.py"]