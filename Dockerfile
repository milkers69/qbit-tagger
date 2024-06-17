FROM alpine:latest

RUN  apk add --no-cache --upgrade python3 py3-pip python3-dev

COPY . .

RUN ls -la
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]