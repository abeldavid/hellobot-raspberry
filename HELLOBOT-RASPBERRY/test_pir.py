from gpiozero import MotionSensor
from robot_modules import Responder, Listener
from time import sleep

PIR_PIN = 26
pir = MotionSensor(PIR_PIN)
responder = Responder()
listener = Listener()

responder.default()

for _ in range(200):

  if pir.motion_detected:

    responder.default()
    sleep(0.01) 
    responder.wake()
    responder.greet()
    sleep(0.01)
    print "motion detected"
    
    while pir.motion_detected:
      print listener.hear()
      print "motion still detected"
      
  else:
    print "no motion!"
     
  
  responder.sleep() 


