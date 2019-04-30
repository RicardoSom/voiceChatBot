import aiml
import speech_recognition as sr
import pyttsx3
import os

# Create the kernel and learn AIML files
kernel = aiml.Kernel()
if os.path.isfile("bot_brain.brn"):
     kernel.bootstrap(brainFile = "bot_brain.brn")
else:
     kernel.bootstrap(learnFiles = "zoe-startup.xml", commands = "load aiml b")
     kernel.saveBrain("bot_brain.brn")

# Start the TTS engine
engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')

# obtain audio from the microphone
r = sr.Recognizer()

# Press CTRL-C to break this loop
while True:
     # obtain audio from microphone
     with sr.Microphone() as source:
         print("Say something!")
         audio = r.listen(source)
     try:
         myinput = r.recognize_google(audio, language='es-ES')
     except sr.UnknownValueError:
         print("Google Speech Recognition could not understand audio")
     except sr.RequestError as e:
         print("Could not request results from Google Speech Recognition service; {0}".format(e))

         print ("You said: {}".format(myinput))
     if myinput == "exit":
         exit()   
     # Get Zoe's response
     zoes_response = kernel.respond(myinput)
     print ("Zoe said: {}".format(zoes_response))
     engine.setProperty('voice',voices[1].id)
     # have Zoe say the response
     if myinput == "chao":
         engine.say(zoes_response)
         engine.runAndWait()
         exit()
     myinput = ""
     engine.say(zoes_response)
     engine.runAndWait()