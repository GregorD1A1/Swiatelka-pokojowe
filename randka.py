from wit import Wit
from wit.wit import WitError
from os import system as sys
import pyaudio
from threading import Thread
import board
import neopixel
import time

client=Wit("Q7I3QBGHHUNXA3VA7KZCGTBW5QHIPHSG")
piksele=neopixel.NeoPixel(board.D18,300,auto_write=False)

def swiatelka():
 tStart=int(time.time())
 Rglown=100
 Rmax=255
 G=14
 Rkier=True
 RTkier=True
 global stanSw

 for i in range(300):    #wezyk startowy przez wszystkie piksele
  piksele[i]=(150,10,0)
  piksele.show()

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


  if stanSw==2:    #obróbka mrygnięcia #0-wył, 1-wł, 2-mrygnięcie
   Rpocz=[]
   Gpocz=[]
   for i in range (0,300):
    Rpocz.append(piksele[i][0])
    Gpocz.append(piksele[i][1])
    mnoznik=1.0
   while mnoznik>0.001:
    mnoznik-=0.04
    for i in range (0,300):
     R=int(mnoznik*Rpocz[i])
     G=int(mnoznik*Gpocz[i])
     piksele[i]=(R,G,0)
    piksele.show()
    time.sleep(0.005)
   time.sleep(0.15)
   while mnoznik<0.999:
    mnoznik+=0.04
    for i in range (0,300):
     R=int(mnoznik*Rpocz[i])
     G=int(mnoznik*Gpocz[i])
     piksele[i]=(R,G,0)
    piksele.show()
    time.sleep(0.005)
   stanSw=1

  elif stanSw==0:   #wyjscie z pętli nieskończonej
   for i in range(0,300):piksele[i]=(0,0,0)
   piksele.show()
   break

stanSw=0      #0-wył, 1-wł, 2-mrygnięcie
swThread=[]
numerThreadu=0



while True:
 # device=hw:2,0 oznacza kartę dźwiękową nr 2. Jej numer można sprawdzić
 # za pomocą   cat /proc/asound/cards
 sys("arecord --device=hw:2,0 --format S16_LE --rate 44100 -d 4 -c1 Swiatelka/glos.wav")
 print('Przetwarzam...')
 with open('Swiatelka/glos.wav','rb') as mowa:
  try:  #na przypadek błędu serweru
   resp=client.speech(mowa, {'Content-Type': 'audio/wav'})
  except WitError:
   print("dzik")
   continue

 try:  #gdzyby nic nie usłyszał, pole text wtedy jest w innym miejscu
  print("Usłyszałem:{}".format(resp['text']))
 except KeyError:
  print('Nic nie słyszałem')
  continue

 try:     #gdyby list był pusty, bo wypowiedź nie zawiera znanej intencji
  intent=resp['intents'][0]['name']
 except IndexError:
  continue

 if intent=='enable': # and entity2=='selection'
  if stanSw==0:
   swThread.append(None)
   swThread[numerThreadu]=Thread(target=swiatelka)
   swThread[numerThreadu].start()
   stanSw=1
  else:
   stanSw=2
 if intent=='disable': # and entity2=='selection':
  stanSw=0
  try:  #na przypadek wyłączenia threadu, który jeszcze nie powstał
   swThread[numerThreadu].join()
  except IndexError:
   pass
