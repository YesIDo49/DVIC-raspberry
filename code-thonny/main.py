import utime	#import des fonction lier au temps
from machine import Pin, I2C # importe dans le code la lib qui permet de gerer les Pin de sortie
from random import*
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import network   #import des fonction lier au wifi
import urequests	#import des fonction lier au requetes http
import ujson	#import des fonction lier aà la convertion en Json

col_list=[1,2,3,4]
row_list=[5,6,7,8]

led1 = Pin(15, mode=Pin.OUT)
led1.off()

for x in range(0,4):
    row_list[x]=Pin(row_list[x], Pin.OUT)
    row_list[x].value(1)


for x in range(0,4):
    col_list[x] = Pin(col_list[x], Pin.IN, Pin.PULL_UP)

key_map=[["1", "4", "7", "10"], ["2", "5", "8", "0"], ["3", "6", "9", "10"], ["10", "10", "10", "10"]]


randcode = []

codeplayer = []

coderesult = []

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

lcd.backlight_on()

wlan = network.WLAN(network.STA_IF) # met la raspi en mode client wifi
wlan.active(True) # active le mode client wifi

ssid = 'Oppo Mehdi'
password = 'stanmamamoo'
wlan.connect(ssid, password) # connecte la raspi au réseau
url = "http://192.168.74.5:3000/"

chiffre = ''

while not wlan.isconnected():
    print("pas co")
    utime.sleep(1)
    pass

def Keypad4x4Read(cols,rows):
  for r in rows:
    r.value(0)
    result=[cols[0].value(),cols[1].value(),cols[2].value(),cols[3].value()]
    if min(result)==0:
      key=key_map[int(rows.index(r))][int(result.index(0))]
      r.value(1) # manages key keept pressed
      return(key)
    r.value(1)

try:
    print("GET")
    r = urequests.get(url) # lance une requete sur l'url
    #print(r.json()["randcode"])
    utime.sleep(1)
    randcode = r.json()["randcode"]

    while codeplayer != randcode:
        print("Veuillez entrer 4 chiffres, compris entre 0 et 9 :")
        while len(codeplayer) !=4 :
            #chiffre=int(input("Choisis un chiffre entre 0 et 9 :"))
            key=Keypad4x4Read(col_list, row_list)
            if key != None:
                print("Vous avez choisi le : "+key)
                utime.sleep(0.3)

                chiffre = int(key)
                if chiffre >=0 and chiffre <=9 :
                    codeplayer.append(chiffre)
                    displayCode = str(chiffre)
                    lcd.putstr(displayCode)
                else:
                    print("Votre chiffre n'est pas valide")

        print(codeplayer)

        if codeplayer[0] == randcode[0]:
            print("Chiffre" , codeplayer[0] , "bien placé !")
            coderesult.append(codeplayer[0])
            led1 = Pin(14, mode=Pin.OUT)
        elif codeplayer[0] in randcode:
            print("Chiffre" , codeplayer[0] , "mal placé")
            coderesult.append('x')
            led1 = Pin(15, mode=Pin.OUT)
        else:
            print("Chiffre" , codeplayer[0] , "incorrect")
            coderesult.append('x')
            led1 = Pin(13, mode=Pin.OUT)

        if codeplayer[1] == randcode[1]:
            print("Chiffre" , codeplayer[1] , "bien placé !")
            coderesult.append(codeplayer[1])
            led2 = Pin(17, mode=Pin.OUT)
        elif codeplayer[1] in randcode:
            print("Chiffre" , codeplayer[1] , "mal placé")
            coderesult.append('x')
            led2 = Pin(16, mode=Pin.OUT)
        else:
            print("Chiffre" , codeplayer[1] , "incorrect")
            coderesult.append('x')
            led2 = Pin(18, mode=Pin.OUT)

        if codeplayer[2] == randcode[2]:
            print("Chiffre" , codeplayer[2] , "bien placé !")
            coderesult.append(codeplayer[2])
            led3 = Pin(21, mode=Pin.OUT)
        elif codeplayer[2] in randcode:
            print("Chiffre" , codeplayer[2] , "mal placé")
            coderesult.append('x')
            led3 = Pin(20, mode=Pin.OUT)
        else:
            print("Chiffre" , codeplayer[2] , "incorrect")
            coderesult.append('x')
            led3 = Pin(22, mode=Pin.OUT)

        if codeplayer[3] == randcode[3]:
            print("Chiffre" , codeplayer[3] , "bien placé !")
            coderesult.append(codeplayer[3])
            led4 = Pin(27, mode=Pin.OUT)
        elif codeplayer[3] in randcode:
            print("Chiffre" , codeplayer[3] , "mal placé")
            coderesult.append('x')
            led4 = Pin(26, mode=Pin.OUT)
        else:
            print("Chiffre" , codeplayer[3] , "incorrect")
            coderesult.append('x')
            led4 = Pin(28, mode=Pin.OUT)

        led = [led1, led2, led3, led4]

        for i in range(4):
            led[i].on()
            utime.sleep(0.5)

        displayresult = str(coderesult).strip("[]")
        displayresult = displayresult.replace(',', '').replace("'", '')

        utime.sleep(0.5)
        if codeplayer == randcode:
            lcd.move_to(0,0)
            lcd.putstr(displayresult)
            lcd.move_to(0,1)
            lcd.putstr("Bravo GG!")
            print("Bravo c'est gagné ! Le code est correct !")
            utime.sleep(2)
            lcd.clear()
            for i in range(4):
                led[i].off()

        else :
            lcd.move_to(0,0)
            lcd.putstr(displayresult)
            lcd.move_to(0,1)
            lcd.putstr("C'est faux")
            print("C'est faux, réessaie")
            codeplayer.clear()
            coderesult.clear()
            utime.sleep(5)
            lcd.clear()
            for i in range(4):
                led[i].off()

except Exception as e:
    print(e)
