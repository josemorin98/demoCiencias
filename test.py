import requests
import json
from scipy import stats

size = 500
x    = stats.expon.rvs(loc=100, scale=10, size=size)
y    = stats.expon.rvs(loc=100, scale=10, size=size)

def loadData():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = "http://localhost:3000/api/v1/processing/xy"
    print("Send data")
    for i in range(size):
        data = {"X":x[i], "Y":y[i]}
        response = requests.post(url, headers=headers, json=data)
        print("Saved data {}".format(response.status_code))

def calculateOperations():
    print("Operators")
    url = "http://localhost:3000/api/v1/processing/z_operator"
    #headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.post(url)
    print("Operators done {}".format(response.status_code))

if __name__ == "__main__":
    loadData()
    print("_"*100)
    calculateOperations()
