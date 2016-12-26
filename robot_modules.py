import speech_recognition as sr
import random 
import os

#RESPONDER CONFIGURATION
DEFAULT_STATIC_PATH = "/home/pi/hellobot/images/default-eye.jpg"
ANIMATION_PATH = "/home/pi/hellobot/videos/"
START_ANIMATION_COMMAND = "omxplayer -o local --win 0,0,480,800 " # -o alsa
DEFAULT_FRAME_COMMAND = "sudo fbi -T 1 -d /dev/fb0 -a -noverbose /home/pi/hellobot/images/default-eye.jpg &" # remove sudo if necessary
REMOVE_EYE_COMMAND = "sudo killall -3 fbi"
LOW_POWER_COMMAND = "xset dpms force off"

class Responder:

  def __init__(self):
    self.static_eye = DEFAULT_FRAME_COMMAND
    self.animate_key = START_ANIMATION_COMMAND + ANIMATION_PATH
    self.low_power = LOW_POWER_COMMAND
    self.remove_key = REMOVE_EYE_COMMAND

  def show(self, key):
    os.system(self.animate_key + key + ".mp4")
  
  def greet(self):
    self.show("hello" + str(random.randint(1, 6)))
    
  def default(self):
    print self.static_eye
    os.system(self.static_eye)

  def black(self):
    os.system(self.low_power)
  
  def remove(self):
    os.system(self.remove_key)

class Listener:
  
  def __init__(self):
    self.r = sr.Recognizer()

  def hear(self):
    return self.recognize(self.obtain_audio())
  
  def obtain_audio(self):
    with sr.Microphone(device_index = 0, sample_rate = 48000, chunk_size = 1024) as source:
      return self.r.listen(source)
  
  def recognize(self, audio):
    phrase = None

    try:
      phrase = self.r.recognize_google(audio)
    except sr.UnknownValueError:
      pass #print "GIBBERISH"
    except sr.RequestError as e:
      pass #print("REQUEST ERROR: {0}".format(e))

    return phrase

class Directive:

  def __init__(self, trigger):
    self.trigger = trigger

  def check(self, phrase):
    return self.trigger in phrase

  def command(self, phrase):
    command = None

    if self.check(phrase):
      # NOTE: using trigger word consecutively before command will not be detected
      all_words = phrase.split()
      command_index = all_words.index(self.trigger) + 1
      command = all_words[command_index]
    
    return command 

def get_response(phrase):  
  
  if "hello" in phrase or "hey" in phrase or "hi" in phrase: #greet
    key = "hello" + str(random.randint(1, 6))
  elif "how are you" in phrase: #how are you?
    key = "how" + str(random.randint(1,5))
  elif "up" in phrase or "whatsApp" in phrase: #what's up?
    key = "up" + str(random.randint(1, 4))
  elif "name" in phrase: #what's your name?
    key = "name" + str(random.randint(1, 4))
  elif "do you do" in phrase: #what do you do?
    key = "do" + str(random.randint(1, 4))
  elif "office" in phrase: #is anyone in the office?
    key = "" + str(random.randint()) #FIX ME
  elif "plans" in phrase or "tonight" in phrase: #what are your plans tonight?
    key = "plans" + str(random.randint(1, 5))
  elif "bathroom" in phrase: #where is the bathroom?
    key = "bathroom" + str(random.randint(1, 3))
  elif "advice" in phrase: #do you have advice?
    key = "advice" + str(random.randint(1, 7))
  elif "idea" in phrase or "help" in phrase: #i need an idea
    key = "help" + str(random.randint(1,11))
  else:
    key = "catch" + str(random.randint(1, 2))

  return key
  