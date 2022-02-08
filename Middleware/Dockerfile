FROM python:3.8-slim-buster
#install requeriments
RUN pip install flask
RUN pip install requests

COPY ./ /app
WORKDIR  /app
CMD [ "chmod","775","/app" ]
ENTRYPOINT [ "python3", "/app/app.py"]
