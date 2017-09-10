#!/usr/bin/env python

# API Module
# Sends datasets of measurement data to the API

# Created for the Smartenergy Hackathon in Bangkok 2017
# by Dominik Schaefer - Team Solar Pi

import requests, json, time, datetime, os



############################
# Blockchain Communication #
############################

def write2blockchain(timestr,energy,address="8Wrc5DaCFFzPBLsBZsnRtaXnrUygGjm6gJ",\
                     walletpassphrase="enterpassphrase"):
    comment = "{\"data-logger\":\"SolarPi\",\"Size_kW\":\"13.37\",\"lat\":\"13.742385N\",\"long\":\"100.528114E\",\"Comment\":\"Hello World!\",\"IoT\":\"RPi 3b, static, solar powered\",\"generation\":\""+timestr+"\",\"MWh\":\""+energy+"\"} Uploaded by Team SolarPi for SEH2017 - http://www.smartenergyhackathon.com"
    os.system("solarcoind walletlock")
    os.system("solarcoind walletpassphrase "+walletpassphrase+" 60")
    os.system("solarcoind sendtoaddress "+address+" 0.000001 \"\" \"\" "+comment)
    os.system("solarcoind walletlock")
    os.system("solarcoind walletpassphrase "+walletpassphrase+" 9999999 true")



#####################
# API Communication #
#####################

url_post = "http://solarpi.herokuapp.com/api/v1/collector/collect"
url_get  = "http://solarpi.herokuapp.com/api/v1/solar/username"

# POST-request
def post(username, data):
    data["username"] = username
    r = requests.post(url_post, data=data)

# GET-request
def get(username):
    print "Getting data..."
    r = requests.get(url_get, data={"username":username})
    #for line in r.text:
    #    print line
    return r.text

# Feed the database with a simulated dataset
def process_data():
    f=open("dataset.csv","r")
    lines=f.readlines()[1:]
    data_map={5:"temperature", 6:"windspeed", 7:"irradiance", 10:"energy"}
    energy_sum = 0.
    energy_chk = 0.
    for l in lines:
        d = l.strip().split(",")
        # Upload data to blockchain every 1 MWh
        energy_sum += float(d[10])
        energy_chk += float(d[10])
        if energy_chk >= 1000000:
            energy_chk -= 1000000
            timestr = "2016-" + d[0] + "-" + d[1] + "-" + d[2] + "-00-00"
            timestr += "-" + timestr[:-1] + "5"
            write2blockchain(timestr,str(energy_sum))
        # Upload data into API
        data_out={}
        data_out["time"] = "2016-"+d[0]+"-"+d[1]+" "+d[2]
        for i in data_map:
            data_out[data_map[i]] = d[i]
        post("SolarPi", data_out)
    f.close()

    

process_data()

