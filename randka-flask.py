from flask import Flask
import board
import neopixel
import time

piksele=neopixel.NeoPixel(board.D18, 300,auto_write=False)
tStart=int(time.time())
appSerwer=Flask(__name__)

@appSerwer.route('/start')   #dekorator,mówiący co uruchamia funkcję
def wlacz():
 for i in range(300):    #wezyk startowy przez wszystkie piksele
  piksele[i]=(0,0,255)
 piksele.show()
 return 'witaj!'
appSerwer.run('localhost',8000)

for i in range(300):	#wezyk startowy przez wszystkie piksele
 piksele[i]=(150,0,0)
 piksele.show()

Rglown=12
Rmax=255
G=14
Rkier=True
RTkier=True

while True:
 if Rmax>150:                            #pętla, wygaszająca z czasem jasność
  czasProgramu=int(time.time())-tStart
  Rmax=int(255-155*czasProgramu/10800)   #10800-3h, 255-155=100
  G=int(15-13*czasProgramu/10800)   #10800-3h, 215-13=2

 if Rkier: Rglown+=1                #stan pierwszej diody
 else: Rglown-=1
 if Rglown==Rmax: Rkier=False
 elif Rglown==12: Rkier=True

 Rtymcz=Rglown
 RTkier=Rkier
 for i in range(300):               #stan każdej diody
  if Rtymcz==Rmax: RTkier=False
  elif Rtymcz==12: RTkier=True
  if RTkier: Rtymcz+=1
  else: Rtymcz-=1
  piksele[i]=(Rtymcz,G,0)

 piksele.show()
 
 time.sleep(0.04)
