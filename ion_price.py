import requests
import json
import time
import csv

url_ion_price = "https://api-osmosis.imperator.co/search/v1/price/ion"
url_osmo_price = "https://api-osmosis.imperator.co/search/v1/price/osmo"

url_pool_ion_osmo_amount= "https://api-osmosis.imperator.co/search/v1/pools/2"   #80%-20%
url_pool_ion_osmo_amount= "https://api-osmosis.imperator.co/search/v1/pools/11"  #50%-50%
url_pool_atom_ion_amount= "https://api-osmosis.imperator.co/search/v1/pools/14"  #50%-50%

def price_extract(url_):
    r = requests.get(url_)
    r_json = r.json()
    # asset_price = r_json["price"]
    # asset_price = float(asset_price)                #for some reason there is a x10 in the value
    asset_price = round(float(r_json["price"]) , 3) / 10
    return asset_price

def write_csv(file_name, data_):
    f = open(file_name, 'a')
    f.write(data_)
    f.close()

def get_hour():
    date = time.localtime(time.time())
    date_str = str(date[3]).zfill(2)+":"+str(date[4]).zfill(2)+":"+str(date[5]).zfill(2)
    return date_str


last_price = price_extract(url_ion_price)

time_div = 30       #Seconds

while(1):
    p = price_extract(url_ion_price)
    
    if (p != last_price):
        if ((p - last_price)>0):
            print("\t\t\t\t\t----------------------------SUBIO--------------------------")
        else: 
            print("\t\t\t\t\t----------------------------BAJO---------------------------")  

    print("At: ", get_hour(), " Ion Price: ", p)
    last_price = p

    data = str(time.time())+", "+str(p)+"\n"
    f_name = "ion_price_"+str(time_div)+"s.csv"
    write_csv(f_name, data)

    time.sleep(time_div)
   