import requests
import json
import sys
import threading
import csv
import numpy as np
from sender_email_config import *

def price_extract(url_):
    r = requests.get(url_)
    r_json = r.json()
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

def reset_offset(n=3600):       #default 1h
    global hour_min_ion_price
    global hour_max_ion_price
    global offset_ion_price
    global ion_price_alerts

    while True:
        min_max_lock.acquire()
        offset_ion_price = (hour_max_ion_price + hour_min_ion_price)/2
        hour_max_ion_price = offset_ion_price
        hour_min_ion_price = offset_ion_price
        ion_price_alerts = np.array([0.05, 0.1, 0.2, 0.3, 0.4])*offset_ion_price
        min_max_lock.release()
        time.sleep(n)

def max_min_setter(price):
    global hour_min_ion_price
    global hour_max_ion_price

    min_max_lock.acquire()
    if(price > hour_max_ion_price):
        hour_max_ion_price = price
    elif(price < hour_min_ion_price):
        hour_min_ion_price = price
    min_max_lock.release()

def check_alerts(price):
    global ion_price_alerts_nflags
    global ion_price_alerts_pflags

    for i in range(len(ion_price_alerts)):
        if((price > (offset_ion_price+ion_price_alerts[i])) & ion_price_alerts_pflags[i]):
            ion_price_alerts_nflags = np.array([True,True,True,True,True])
            price_relation = price / offset_ion_price
            percent = (price_relation-1)*100
            body = "$"+str(round(price,2))+" ATOMS\n\nToday's Offset: "+str(offset_ion_price)+" ATOMS ---> +"+str(round(percent,2))+"%"
            send_msg("Ion Price", body)
            ion_price_alerts_pflags[i] = False
            print("+",str(round(percent,2)),"% msg sent")
        elif((price < (offset_ion_price-ion_price_alerts[i])) & ion_price_alerts_nflags[i]):
            ion_price_alerts_pflags = np.array([True,True,True,True,True])
            price_relation = price / offset_ion_price
            percent = (1-price_relation)*100
            body = "$"+str(round(price,2))+" ATOMS\n\nToday's Offset: "+str(offset_ion_price)+" ATOMS ---> -"+str(round(percent,2))+"%"
            send_msg("Ion Price", body)
            ion_price_alerts_nflags[i] = False
            print("   -",str(round(percent,2)),"% msg sent")


url_ion_price = "https://api-osmosis.imperator.co/search/v1/price/ion"
# url_osmo_price = "https://api-osmosis.imperator.co/search/v1/price/osmo"

# url_pool_ion_osmo_amount= "https://api-osmosis.imperator.co/search/v1/pools/2"   #80%-20%
# url_pool_ion_osmo_amount= "https://api-osmosis.imperator.co/search/v1/pools/11"  #50%-50%
# url_pool_atom_ion_amount= "https://api-osmosis.imperator.co/search/v1/pools/14"  #50%-50%

time_div = 20       #Seconds

min_max_lock = threading.Lock()

offset_ion_price = price_extract(url_ion_price)                        #change for todays price
hour_max_ion_price = offset_ion_price
hour_min_ion_price = offset_ion_price
ion_price_alerts = np.array([0.05, 0.1, 0.15, 0.2, 0.3])*offset_ion_price
ion_price_alerts_pflags = np.array([True,True,True,True,True])
ion_price_alerts_nflags = np.array([True,True,True,True,True])


send_msg("STARTING Ion Price Feeding", 
        ("Python script started\n\nFeeding ION price each " + str(time_div) + " seconds with an Ion price offset of "+str(round(offset_ion_price,2))+" ATOMS"))


last_price = offset_ion_price

t_offset = threading.Thread(target=reset_offset, daemon=True)
t_offset.start()
print("----------------------STARTING PRICE FEEDER--------------------")
while(1):
    try:
        p = price_extract(url_ion_price)
        
        if (p != last_price):
            if ((p - last_price)>0):
                print("\t\t\t\t\t----------------------------UP--------------------------")
            else: 
                print("\t\t\t\t\t----------------------------DOWN---------------------------")  

        check_alerts(p)
        max_min_setter(p)

        print("\n", time.ctime(), " Ion Price: ", round(p,2), " Atoms")
        print("Last offset: ",round(offset_ion_price,2) ,"Last max: ", round(hour_max_ion_price,2)," Last min: ",round(hour_min_ion_price,2))

        last_price = p

        data = str(time.time())+", "+str(p)+"\n"
        f_name = "ion_price_"+str(time_div)+"s.csv"
        write_csv(f_name, data)

        time.sleep(time_div)

    except KeyboardInterrupt:
        print("\n\nClosing Price_Feeder (Ctrl+C)\n")
        sys.exit()


   