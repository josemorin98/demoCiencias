FROM python:3.8-buster

#install requeriments
# RUN pip install --upgrade pip
RUN pip install flask
RUN pip install requests
RUN pip install pandas
RUN pip install psycopg2==2.9.1

COPY ./ /app
WORKDIR  /app
CMD [ "chmod","775","/app" ]
ENTRYPOINT [ "python3", "/app/app.py"]