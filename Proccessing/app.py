from flask import Flask, request, g
import psycopg2
import numpy as np
import os

app = Flask(__name__)
app.debug = True
app.config['PROPAGATE_EXCEPTIONS'] = True
con = None


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
                          host = os.environ.get("POSTGRES_HOST","postgres_db"),
                          port = os.environ.get("POSTGRES_PORT","5432"),
                          db   = os.environ.get("POSTGRES_DB","demo"))
    return g.db

@app.route('/api/v1/xy', methods = ['GET', 'POST'])
def xOperations():
    if (request.method == 'POST'):
        # guardamos los valores de x e y
        db = get_db()
        # obtenemos los valroes recibidos por el usuario
        message = request.get_json()
        xValue = message["X"]
        yValue = message["Y"]
        # insertamos los valores
        insertSql = db.insert(x = xValue, y = yValue)
        app.logger.info(insertSql)
        return insertSql
    else:
        # get values in x
        db = get_db()
        selectInfo, rows = db.select(columns = "x,y")
        app.logger.info(selectInfo)
        x = list(zip(*rows))[0]
        y = list(zip(*rows))[1]
        return {"X":x,"Y":y}


# SUMARA LA COLUMNA X E Y
@app.route('/api/v1/z_sum', methods = ['GET','POST'])
def zSum():
    if (request.method == 'POST'):
        # guardamos los valores de x e y
        db = get_db()
        operationSql = db.operation(column='z_sum',operator='+')
        app.logger.info(operationSql)
        return operationSql
    else:
        # get values in x
        db = get_db()
        selectInfo, rows = db.select(columns = "x,y,z_sum")
        app.logger.info(selectInfo)
        x = list(zip(*rows))[0]
        y = list(zip(*rows))[1]
        z = list(zip(*rows))[2]
        return {"X":x,"Y":y, "Z_SUM":z}

# MULTIPLICARA LA COLUMNA X E Y
@app.route('/api/v1/z_product', methods = ['GET','POST'])
def zPro():
    if (request.method == 'POST'):
        # guardamos los valores de x e y
        db = get_db()
        operationSql = db.operation(column='z_product',operator='*')
        app.logger.info(operationSql)
        return operationSql
    else:
        # get values in x
        db = get_db()
        selectInfo, rows = db.select(columns = "x,y,z_product")
        app.logger.info(selectInfo)
        x = list(zip(*rows))[0]
        y = list(zip(*rows))[1]
        z = list(zip(*rows))[2]
        return {"X":x,"Y":y, "Z_PRODUCT":z} 


# DIVIDE LA COLUMNA X E Y
@app.route('/api/v1/z_divide', methods = ['GET','POST'])
def zDiv():
    if (request.method == 'POST'):
        # guardamos los valores de x e y
        db = get_db()
        operationSql = db.operation(column='z_divide',operator='/')
        app.logger.info(operationSql)
        return operationSql
    else:
        # get values in x
        db = get_db()
        selectInfo, rows = db.select(columns = "x,y,z_divide")
        app.logger.info(selectInfo)
        x = list(zip(*rows))[0]
        y = list(zip(*rows))[1]
        z = list(zip(*rows))[2]
        return {"X":x,"Y":y, "Z_SUM":z}


# RESTA LA COLUMNA X E Y
@app.route('/api/v1/z_substract', methods = ['GET','POST'])
def zSub():
    if (request.method == 'POST'):
        # guardamos los valores de x e y
        db = get_db()
        operationSql = db.operation(column='z_substract',operator='-')
        app.logger.info(operationSql)
        return operationSql
    else:
        # get values in x
        db = get_db()
        selectInfo, rows = db.select(columns = "x,y,z_substract")
        app.logger.info(selectInfo)
        x = list(zip(*rows))[0]
        y = list(zip(*rows))[1]
        z = list(zip(*rows))[2]
        return {"X":x,"Y":y, "Z_SUBSTRACT":z}

# RESTA LA COLUMNA X E Y
@app.route('/api/v1/z_operator', methods = ['GET','POST'])
def zOperators():
    if (request.method == 'POST'):
        # guardamos los valores de x e y
        db = get_db()
        operationSql = db.operation(column='z_sum',operator='+')
        operationSql = db.operation(column='z_product',operator='*')
        operationSql = db.operation(column='z_divide',operator='/')
        operationSql = db.operation(column='z_substract',operator='-')
        app.logger.info('ALL OPERATORS DONE')
        return 'ALL OPERATORS DONE'
    else:
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
        return resultJson


@app.route('/', methods = ['GET'])
def ok():
    return "OK :)"

if __name__ == '__main__':
    app.run(host= '0.0.0.0',port=5000,debug=True)