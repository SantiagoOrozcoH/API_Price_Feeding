import requests
import json
import time
import csv

url = "https://api-osmosis.imperator.co/search/v1/price/ion"


def price_extract(url_):
    r = requests.get(url_)
    r_json = r.json()
    asset_price = r_json["price"]
    asset_price = float(asset_price) / 10
    asset_price = round(asset_price, 3)
    return asset_price

def write_csv(file_name, data_):
    f = open(file_name, 'a')
    f.write(data_)
    f.close()

def get_hour():
    date = time.localtime(time.time())
    date_str = str(date[3]).zfill(2)+":"+str(date[4]).zfill(2)+":"+str(date[5]).zfill(2)
    return date_str


last_price = price_extract(url)

while(1):
    p = price_extract(url)
    
    if (p != last_price):
        if ((p - last_price)>0):
            print("\t\t\t\t\t----------------------------SUBIO--------------------------")
        else: 
            print("\t\t\t\t\t----------------------------BAJO---------------------------")  

    print("At: ", get_hour(), " Ion Price: ", p)
    last_price = p

    data = str(time.time())+", "+str(p)+"\n"
    write_csv("ion_price.csv", data)

    time.sleep(5.00)
   