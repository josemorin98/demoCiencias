from flask import Flask, request, g, send_file
import psycopg2
import numpy as np
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)
app.debug = True
app.config['PROPAGATE_EXCEPTIONS'] = True
con = None

sinkPath = os.environ.get('SINK_PATH','/test/demo_ciencias/plots')

class ConectorBD:
    def __init__(self,user,db,psw,port,host):
        self.user = user
        self.psw = psw
        self.db = db
        self.host = host
        self.port = port
        self.conn = psycopg2.connect(   user = self.user,
                                    password = self.psw,
                                        host = self.host,
                                        port = self.port,
                                    database = self.db)
    
    def cursor(self):
        return self.conn.cursor()
    
    def select(self,columns):
        try:
            selectSql = """SELECT {} FROM ciencias;""".format(columns)
            cursor = self.cursor()
            cursor.execute(selectSql)
            rows = cursor.fetchall()
            return "SELECT DONE", rows
        except (Exception, psycopg2.DatabaseError) as error:
            app.logger.error(error)
            return "SELECT FAILED", np.array()
    
    def insert(self,x,y):
        try:
            insertSql = """INSERT INTO ciencias (x,y) VALUES(%(X)s,%(Y)s);"""
            cursor = self.cursor()
            cursor.execute(insertSql, {'X':str(x),'Y':str(y)})
            self.conn.commit()
            return "INSERT DONE"
        except (Exception, psycopg2.DatabaseError) as error:
            app.logger.error(error)
            return "INSERT FAILED"
    
    def operation(self,column,operator):
        try:
            updateSql = """UPDATE ciencias SET {} = x {} y;""".format(column,operator)
            cursor = self.cursor()
            cursor.execute(updateSql)
            self.conn.commit()
            return "OPERATOR {} DONE".format(operator)
        except (Exception, psycopg2.DatabaseError) as error:
            app.logger.error(error)
            return "OPERATOR {} FAILED".format(operator)
    
def get_db():
    if 'db' not in g:
        # g.db = ConectorBD(user = "postgres",
        #                   psw  = "postgres",
        #                   host = "127.0.0.1",
        #                   port = "5432",
        #                   db   = 'demo')
        g.db = ConectorBD(user = os.environ.get("POSTGRES_USER","postgres"),
                          psw  = os.environ.get("POSTGRES_PASSWORD","postgres"),
                          host = os.environ.get("POSTGRES_HOST","127.0.0.1"),
                          port = os.environ.get("POSTGRES_PORT","5432"),
                          db   = os.environ.get("POSTGRES_DB","demo"))
    return g.db

def plotBoxplot(resultJson,name):
    xyDf = pd.DataFrame(resultJson)
    df_melt = pd.melt(xyDf)
    plt.figure(figsize=(13,7))
    ax = sns.boxplot(x="variable", y="value", data=df_melt)
    nameFile = '{}/{}.png'.format(sinkPath,name)
    plt.savefig('{}'.format(nameFile))
    plt.cla()
    return nameFile

@app.route('/api/v1/xy', methods = ['GET'])
def xOperations():
    if (request.method == 'GET'):
        # get values in x
        db = get_db()
        selectInfo, rows = db.select(columns = "x,y")
        app.logger.info(selectInfo)
        x = list(zip(*rows))[0]
        y = list(zip(*rows))[1]
        resultJson = {"X":x,"Y":y}

        nameFile = plotBoxplot(resultJson=resultJson,
                    name='xy')
        return send_file(nameFile, mimetype='image/png')

    else:
        return 'Select method GET'
        


# SUMARA LA COLUMNA X E Y
@app.route('/api/v1/z_sum', methods = ['GET','POST'])
def zSum():
    if (request.method == 'GET'):
        db = get_db()
        selectInfo, rows = db.select(columns = "z_sum")
        app.logger.info(selectInfo)
        z = list(zip(*rows))[0]
        resultJson = {"Z_SUM":z}
        nameFile = plotBoxplot(resultJson=resultJson,
                    name='z_sum')
        return send_file(nameFile, mimetype='image/png')
    else:
        return 'Select method GET'

# MULTIPLICARA LA COLUMNA X E Y
@app.route('/api/v1/z_product', methods = ['GET','POST'])
def zPro():
    if (request.method == 'GET'):
        db = get_db()
        selectInfo, rows = db.select(columns = "z_product")
        app.logger.info(selectInfo)
        z = list(zip(*rows))[0]
        resultJson = {"Z_PRODUCT":z}
        nameFile = plotBoxplot(resultJson=resultJson,
                    name='z_product')
        return send_file(nameFile, mimetype='image/png')
    else:
        return 'Select method GET'


# DIVIDE LA COLUMNA X E Y
@app.route('/api/v1/z_divide', methods = ['GET','POST'])
def zDiv():
    if (request.method == 'GET'):
        db = get_db()
        selectInfo, rows = db.select(columns = "z_divide")
        app.logger.info(selectInfo)
        z = list(zip(*rows))[0]
        resultJson = {"Z_DIVIDE":z}
        nameFile = plotBoxplot(resultJson=resultJson,
                    name='z_divide')
        return send_file(nameFile, mimetype='image/png')


# RESTA LA COLUMNA X E Y
@app.route('/api/v1/z_substract', methods = ['GET','POST'])
def zSub():
    if (request.method == 'GET'):
        db = get_db()
        selectInfo, rows = db.select(columns = "z_substract")
        app.logger.info(selectInfo)
        z = list(zip(*rows))[0]
        resultJson = {"Z_SUBSTRACT":z}
        nameFile = plotBoxplot(resultJson=resultJson,
                    name='z_substract')
        return send_file(nameFile, mimetype='image/png')

# RESTA LA COLUMNA X E Y
@app.route('/api/v1/z_operator', methods = ['GET','POST'])
def zOperators():
    if (request.method == 'GET'):
        # get values in x
        db = get_db()
        selectInfo, rows = db.select(columns = "*")
        app.logger.info(selectInfo)
        resultJson = {"X":list(zip(*rows))[0],
                      "Y":list(zip(*rows))[1],
                  "Z_SUM":list(zip(*rows))[2],
            "Z_SUBSTRACT":list(zip(*rows))[3],
              "Z_PRODUCT":list(zip(*rows))[4],
               "Z_DIVIDE":list(zip(*rows))[5]}
        nameFile = plotBoxplot(resultJson=resultJson,name='operations')
        return send_file(nameFile, mimetype='image/png')


@app.route('/prueba', methods = ['GET'])
def ok():
    return "OK :)"

if __name__ == '__main__':
    app.run(host= '0.0.0.0',port=5000,debug=True)