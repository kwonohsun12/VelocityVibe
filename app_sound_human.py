import pyttsx3

class VoiceAlert:
    @staticmethod
    def speak_danger_alert():
        engine = pyttsx3.init()
        # Set properties
        engine.setProperty('rate', 150)    # Speaking rate
        engine.setProperty('volume', 0.9)  # Volume (0-1)
        
        # Say "Danger danger"
        engine.say("Danger danger")
        engine.runAndWait()
        
VoiceAlert.speak_danger_alert()
