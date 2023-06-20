import os
import time 
permission = '123'

os.system("sudo nmcli con down id 'rpi42'")

ssid = ''
paswd = ''

# if null

#socke bind 및 app한테 ssid / passwd 받기

time.sleep(2)

ssid = 'RTES Lab'
paswd = 'Rtes2021!'

os.system("sudo nmcli dev wifi con '" + ssid + "' password '" + paswd + "' > ./log.txt" )
time.sleep(2)
f =  open('./log.txt',"r")
lines =  f.readlines()
print(lines)


