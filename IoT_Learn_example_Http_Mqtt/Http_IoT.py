from urllib import request, parse
from time import sleep
from seeed_dht import DHT
from random import randint

sensor = DHT('11',5)

def make_param_thingspeak1(data1, data2,data3):
    params = parse.urlencode({'field7':data1,'field8':data2,'field1':data3}).encode()
    return params

def thingspeak_post(params):
    api_key_write = "RC62JQJPACXKP9AE"
    req = request.Request('https://api.thingspeak.com/update',method="POST")
    req.add_header("Content-Type","application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY",api_key_write)
    r = request.urlopen(req, data = params)
    respone_data = r.read()
    return respone_data

while True:
    try:
        data_random = randint(0,100)
        humi,temp = sensor.read()
        print('temperature {}C, humidity {}%, random: {}'.format(temp,humi,data_random))
        params_thingspeak1 = make_param_thingspeak1(temp,humi,data_random)
        thingspeak_post(params_thingspeak1)
        sleep(20)
        
    except:
        print("He thong gap loi!")
        continue
        

