import numpy as np
import pandas as pd
import json
import subprocess


def sector_prediction():
    companylist = pd.read_csv('companylist.csv')
    userstock = pd.read_csv('users.csv')
    id = int(input())
    useridstocks = userstock.loc[userstock['User id'] == id]
    sectorarray = useridstocks['Sector']
    print(sectorarray)
    symbols = []
    for x in sectorarray:
        stocks = companylist.loc[companylist['Sector'] == x]
        symbols.append(stocks['Symbol'])
    print(symbols)


def get_weights(arr):
    summ = np.sum(arr)
    for i in range(0,len(arr)):
        arr[i] = arr[i]/summ
    arr = np.array(arr)
    mydata = pd.read_csv('adjclose2.csv')
    returns = (mydata/mydata.shift(1)) - 1
    port_var = np.dot(arr.T, np.dot(returns.cov()*250, arr))
    port_var = port_var ** 0.5
    return port_var


def get_stock_weights(current_price, dmatbal, std_array, port_var):
    dev = []
    for i in range(0, len(current_price)):
        cutie2 = [100, 360, 100, 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        price = dmatbal // current_price[i]
        amount = price*current_price[i]
        cutie2[i] = cutie2[i] + amount
        port_var2 = get_weights(cutie2)
        dev.append(port_var2 - port_var)
    mini = min(dev)
    maxi = max(dev)
    for i in range(0, len(dev)):
        dev[i] = (dev[i] + abs(mini))/ (maxi - mini)
        dev[i] = round(dev[i] * 10, 2)
    json_data = json.dumps({'results': dev})
    print(json_data)



current_price = [178.02, 95.61, 330.47, 156.46, 45.01, 115.40, 102.87, 67.96, 14.31, 267.60, 178.96, 160.26, 51.17,
                 133.68, 115.44, 43.46, 162.36, 237.22, 55.67, 94.6, 65.91, 36.78, 78.97, 141.32, 227.86, 128.33,
                 124.53, 48.56, 89.16, 75.12]
std_array = [100, 360, 100, 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
std_arr2 = std_array
port_var = get_weights(std_arr2)
dmatbal = 1000
dmatbal = dmatbal - (port_var*100)
cutie = [100, 360, 100, 150, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
get_stock_weights(current_price, 1000, cutie, port_var)








