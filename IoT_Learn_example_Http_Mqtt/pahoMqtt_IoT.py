import paho.mqtt.client as mqtt
from grove.grove_relay import GroveRelay
from grove.display.jhd1802 import JHD1802
from gpiozero import LED
from time import sleep

lcd = JHD1802()
led = LED(5)
buzzer = LED(12)
relay = GroveRelay(16)

def on_connect(client, userdata,flags,rc):
    print("Connected With Result Code {}".format(rc))
    channel_ID = "1693595"
    client.subscribe("channels/%s/subscribe/fields/field7" % (channel_ID))
    client.subscribe("channels/%s/subscribe/fields/field8" % (channel_ID))
    client.subscribe("channels/%s/subscribe/fields/field1" % (channel_ID))
    
def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")
    
def on_message(client, userdata, message):
    if (message.topic == "channels/1693595/subscribe/fields/field1"):
        print("Random:")
        t = int(message.payload.decode())
        lcd.setCursor(0,11)
        lcd.write('R: {}'.format(t))
        if (t > 50):
            led.on()
        else:
            led.off()
    
    if (message.topic == "channels/1693595/subscribe/fields/field7"):
        print("Nhiet do:")
        to = int(message.payload.decode())
        lcd.setCursor(0,0)
        lcd.write('tempe: {0:2}C'.format(to))
        if (to > 26):
            buzzer.on()
            sleep(0.1)
        elif (to <24):
            buzzer.off()
            sleep(0.1)
        
        
    if (message.topic == "channels/1693595/subscribe/fields/field8"):
        print("Do am: ")
        do = int(message.payload.decode())
        lcd.setCursor(1,0)
        lcd.write('humidity: {0:5}%'.format(do))
        if (do > 78):
            relay.on()
        elif (do <70):
            relay.off()
        
    print(message.payload.decode())
    print(message.topic)

client_id = "OwgsFRwcOg4SDBsSNwQAITg"
client = mqtt.Client(client_id)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username = "OwgsFRwcOg4SDBsSNwQAITg", password = "2vRuYE+NBKgwunLht+rNcOrQ")
client.connect("mqtt3.thingspeak.com",1883,60)
client.loop_forever()