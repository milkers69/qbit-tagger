FROM alpine:3.22.1

# make and move into "app" folder
WORKDIR /app

# copy files to app folder
COPY ["app.py", "requirements.txt", "./"]

# print contents of app folder for debug purposes
RUN ls -la && \
  # install system packages
  apk add --no-cache --upgrade python3 py3-pip python3-dev && \
  # install requirements
  pip3 install --upgrade pip --break-system-packages && \
  pip3 install -r requirements.txt --break-system-packages

# run app.py
ENTRYPOINT ["python3", "/app/app.py"]
