import tensorflow as tf
import mouse, sys
import time 
import serial
import numpy as np

dir = {
'up' : "\U00002B06" + ' UP',
'down' : "\U00002B07" + ' DOWN',
'left' : "\U00002B05" + ' LEFT',
'right' : "\U000027A1" + ' RIGHT',
'clockwise' : "\U000021A9" + ' CLOCKWISE',
'anti_clockwise' : "\U000021AA" + ' ANTI-CLOCKWISE',
}
def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)
  
    
mouse.FAILSAFE=False
ArduinoSerial=serial.Serial('com3',9600)  #Specify the correct COM port

gestures = ["clockwise",'anti_clockwise','up','down','left','right']

print('Please wait till the Deep Neural Network Loads')
model = tf.keras.models.load_model('final.h5')
print('The Network is loaded sucessfully')
# model.summary()
X = []
counter  = 0
while 1:
   data=str(ArduinoSerial.readline().decode('ascii')).replace("\r\n","")   #read the data
# =============================================================================
#    if data[-1] == '1':                        # read the Status of SW
#       mouse.click(button="left")
#       print('yes')
#       continue
# =============================================================================
   (x,y,z)=data.split(":")           # assigns to x,y and z        #read the cursor's current position
   (x,y)=(int(x),int(y))                           #convert to int
   X +=  [x,y]
   counter +=1
   if counter == 50:
       # print(X)
       d = np.array([X],dtype = 'int32')
       # print(gestures[np.argmax(model.predict(d), axis=-1)[0]])
       print(colored(123, 212, 13, dir[gestures[np.argmax(model.predict(d), axis=-1)[0]]]))
       counter,X = 0,[]
       