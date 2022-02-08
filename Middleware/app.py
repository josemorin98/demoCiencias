import requests as R
from flask import Flask, request, g
import os

# _________________________________________________
PORT  = os.environ.get("NODE_PORT",3000)
HOST  = os.environ.get("NODE_HOST","0.0.0.0")
DEBUG = bool(os.environ.get("DEBUG",True))
MODE  = os.environ.get("MODE","LOCAL")
# _________________________________________________
app = Flask(__name__)
app.debug = DEBUG
app.config['PROPAGATE_EXCEPTIONS'] = True
# __________________________________________________
@app.route('/api/v1/processing/<path:path>',defaults = {"path":""} ,methods = ['GET','POST'])
def middleware(path):
    hostname = "localhost" if(MODE == "LOCAL") else "processing"
    port     = 5000 if(MODE == "LOCAL") else 5000
    url      = "http://{}:{}{}".format(hostname,port,request.path)
    app.logger.debug("URL "+url)
    if (request.method == 'POST'):
        data     = request.get_json()
        response = R.post(url,headers = {"Content-Type":"application/json"},json = data)
        return (response.content, response.status_code,response.headers.items())
    else:
        
        #response = R.post()
        return "GET"

@app.route('/api/v1/plot/<path:path>',defaults = {"path":""} ,methods = ['GET','POST'])
def middlewarePlot(path):
    hostname = "localhost" if(MODE == "LOCAL") else "plot"
    port     = 5001 if(MODE == "LOCAL") else 5000
    # ___________________________________________________________
    url      = "http://{}:{}{}".format(hostname,port,request.path)
    app.logger.debug("URL "+url)
    if (request.method == 'POST'):
        return "POST :)"
    else:
        response = R.get(url)
        return (response.content, response.status_code,response.headers.items())

@app.route("/test",methods=["GET","POST"])
def test():
    return "TEST"



if __name__ == '__main__':
    app.run(host= HOST,port=PORT,debug=DEBUG)
