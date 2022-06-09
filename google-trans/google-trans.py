from googletrans import Translator
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os

# in infinite loop, words spoken into the microphone, are translated  into Ukrainian, the recording in the .mp3 file
# than mp3 file is automatically runing to play recoded auio

def main():
    translator = Translator()
    input_lang = "pl_PL"
    output_lang = "uk"
    recognizer = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio = recognizer.listen(mic)
                text = recognizer.recognize_google(audio, language=input_lang)
                text = text.lower()
                print(text)
                translated_text = translator.translate(text, "uk").text
                output = gTTS(text=translated_text, lang=output_lang, slow=False)
                output.save("output.mp3")
                os.system("start output.mp3")

        except sr.UnknownValueError():
            recognizer = sr.Recognizer()
            continue

main()