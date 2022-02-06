import requests
import json
from scipy import stats

size = 100
x = stats.norm.rvs(loc=5, scale=1, size=size)
y = stats.norm.rvs(loc=5, scale=1, size=size)

headers = {"Content-Type": "application/json; charset=utf-8"}
url = "http://localhost:5000/api/v1/xy"

# print("Send data")
# for i in range(size):
#     data = {"X":x[i], "Y":y[i]}
#     response = requests.post(url, headers=headers, json=data)
# print("Saved data")
# print("Operators")
# url = "http://localhost:5000/api/v1/z_operator"
# response = requests.post(url, headers=headers)
# print("Operators done")


apis = ["xy","z_sum","z_divide","z_product","z_substract","z_operator"]
for api in apis:
    url = "http://localhost:5001/api/v1/plot/{}".format(api)
    response = requests.get(url, headers=headers)
    print(response.status_code)
