from urllib import request, parse  #Khai báo thư viện urllib
import json # Khai báo thư viện json
import time # Khai báo thư viện time 
from gpiozero import Button,LED # Khai báo thư viện gpiozero để sử dụng được led và button
from seeed_dht import DHT # Khai báo thư viện cảm biến nhiệt độ và độ ẩm
from datetime import datetime # Khai báo hàm datetime sử dụng lấy thời gian thực

now = datetime.now() # Khai bóa biến now lưu trữ giá trị thời gian thực
sensor = DHT('11',5) # Khai báo cảm biến nhiệt độ, độ ẩm kết nối chân số 5 trên Raspi
led = LED(12) # Khai báo led kết nối chân số 12 

def make_param_thingspeak1(data1, data2): # Hàm này dùng tạo ra một chuỗi dữ liệu mã hóa để gửi lên server
    params = parse.urlencode({'field1':data1,'field2':data2}).encode() # Câu lệnh tạo ra chuỗi dữ liệu mã hóa
    return params

def thingspeak_post(params): # Hàm để gửi dữ liệu lên server
    api_key_write = "RC62JQJPACXKP9AE" # Key write được lấy từ thingspeak
    req = request.Request('https://api.thingspeak.com/update',method="POST") # tạo ra một request để gửi dữ liệu lên server dùng giao thức POST
    req.add_header("Content-Type","application/x-www-form-urlencoded") # Thêm các tiêu đề đính kèm request giúp request nó tường minh hơn
    req.add_header("X-THINGSPEAKAPIKEY",api_key_write)
    r = request.urlopen(req, data = params) # Câu lệnh gửi dữ liệu lên server
    respone_data = r.read()
    return respone_data

#-------------------------------

def thingspeak_get(): # Hàm đọc về giá trị trạng thái buttons trên server (field 3)
    api_key_read = "Y7EOC8CZFYFMUX6X" # key read trên thingspeak
    TS = request.urlopen("https://api.thingspeak.com/channels/1693595/fields/3/last.json?api_key=%s"%(api_key_read))
    # Câu lệnh đọc dữ liệu từ server thông qua channel ID đã khai báo ở trên (đọc dữ liệu file 3: trạng thái của nút nhấn trên server)
    response = TS.read() 
    data = json.loads(response) # Đọc về dữ liệu trạng thái nút nhấn từ server qua hàm json.loads() 
    TS.close()
    
    value = data['field3'] # value biến lưu trữ giá trị trạng thái button đọc về từ server
    return value

def thingspeak_get1(): # Hàm đọc về giá trị chế độ làm việc của hệ thống trên server (field 4)
    api_key_read = "Y7EOC8CZFYFMUX6X" 
    TS = request.urlopen("https://api.thingspeak.com/channels/1693595/fields/4/last.json?api_key=%s"%(api_key_read))
    # Câu lệnh đọc dữ liệu từ server thông qua channel ID đã khai báo ở trên (đọc dữ liệu file 4: chế độ hoạt động trên server)
    response = TS.read()
    data = json.loads(response) # Đọc về dữ liệu chế độ hoạt động của hệ thống từ server qua hàm json.loads() 
    TS.close()
    
    value = data['field4'] # value biến lưu trữ giá trị chế độ hoạt động của hệ thống đọc về từ server
    return value

def button(): # Hàm nút nhấn ON/OFF
    if (value == "1"): 
        led.on()
        print("1")
    else:
        led.off()
        print("0")
    
while True:
    #try - except : Phần xử lí ngoại lệ đảm bảo hệ thống hoạt động bình thường khi hệ thống gặp lỗi mà không cần reset lại toàn bộ hệ thống
    try:
        humi,temp = sensor.read() #Đọc giá trị cảm biến nhiệt độ - độ ẩm
        print('temperature {}C, humidity {}%'.format(temp,humi))
    
        params_thingspeak1 = make_param_thingspeak1(temp,humi) # Tạo ra chuỗi dữ liệu gửi lên server
        thingspeak_post(params_thingspeak1) # Gửi dữ liệu nhiệt độ - độ ẩm lên server
    
        now = datetime.now() # Giá trị thời gian thực hiện tại
        current_m = now.strftime("%M") # giá trị thời gian thực về phút
        current_h = now.strftime("%H") # giá trị thời gian thực về giờ
        print("Current Time is :", current_h) 
        print("Current Time is :", current_m)
        current_m= int(current_m) # ép kiểu giá trị thời gian thực về phút
        current_h = int(current_h) # ép kiểu giá trị thời gian thực về giờ
        
        value1 = thingspeak_get1() # Đọc trạng thái nút nhấn từ server (dữ liệu đã gửi lên server thông qua website đã tạo)
        value = thingspeak_get() # Đọc trạng thái chế độ hoạt động hệ thống từ server (dữ liệu đã gửi lên server thông qua website đã tạo)
        
        print(value)
        print("-----")
        print(value1)
        # Phần điều kiện để điều khiển các thiết bị thông qua website
        if (value1 == "1"):
            button()
        else:
            print("auto")
            if ( current_m <35 and current_h==16):
                led.on()
            else:
                led.off()
        time.sleep(20)
    
    except:
        print("He thong gap loi!")
        continue



