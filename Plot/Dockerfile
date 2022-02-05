FROM python:3.8-buster

#install requeriments
RUN pip install flask
RUN pip install requests
RUN pip install pandas
RUN pip install psycopg2==2.9.1
RUN pip install matplotlib
RUN pip install seaborn

COPY ./ /app
WORKDIR  /app
CMD [ "chmod","775","/app" ]
ENTRYPOINT [ "python3", "/app/app.py"]