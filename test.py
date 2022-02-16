import requests
import json
from scipy import stats

size = 100
x    = stats.norm.rvs(loc=100, scale=10, size=size)
y    = stats.norm.rvs(loc=100, scale=10, size=size)

MIDDLEWARE_PORT = 5002

def loadData():

    headers = {"Content-Type": "application/json; charset=utf-8"}
w
    url     = "http://localhost:{}/api/v1/processing/xy".format(MIDDLEWARE_PORT)

    print("Send data")
    for i in range(size):
        data = {"X":x[i], "Y":y[i]}
        response = requests.post(url, headers=headers, json=data)
        print("SAVE_DATA[{}] STAUTS_CODE={}".format(i,response.status_code))

def calculateOperations():
    print("Operators")
    url = "http://localhost:{}/api/v1/processing/z_operator".format(MIDDLEWARE_PORT)
    #headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.post(url)
    print("Operations done {}".format(response.status_code))

if __name__ == "__main__":
    loadData()
    print("_"*100)
    calculateOperations()
