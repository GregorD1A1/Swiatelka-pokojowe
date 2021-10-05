import board
import neopixel
import time
piksele=neopixel.NeoPixel(board.D18, 300,auto_write=False)
tStart=time.time()

for i in range(300):	#wezyk startowy przez wszystkie piksele
 piksele[i]=(150,0,0)
 piksele.show()

Rglown=0
Rkier=True
RTkier=True
Rmax=255

while True:
 if Rmax>80:                            #pętla, wygaszająca z czasem jasność
  czasProgramu=int(time.time())-tStart
  Rmax=int(255-175*czasProgramu/1800)   #1800-0,5h, 255-175=80
  G=int(15-14*czasProgramu/1800)   #1800-0,5h, 215-13=2

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
