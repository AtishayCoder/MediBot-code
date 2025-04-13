from openai import OpenAI
from googletrans import *
import flask
import nltk_related_stuff as nlptk
import speech_recognition as sr
import langdetect as detect
import wave
import noisereduce
from scipy.io import wavfile
import base64

app = flask.Flask(__name__)
audio_file = None
supported_langs = ["en", "es", "fr", "de", "ja", "ms", "pt", "it", "sw", "id"]

"""
Plan for two way communication.

I will enter the message to be displayed in the else statements and start it with 'ask/{question}'.
Then I just return it. Then on the client's side, I check if the string starts with ask. 
If so, it will display the question and prompt the user to enter that data. 
If the processing was complete, it will start the string with 'result/'. 
If that is prefix, then the server will display just that and the server will clean the thing and start afresh.
"""


@app.route("/")
def main():
    print("Client connected to server.")
    result = reset()
    return "Client connected."


@app.route("/get-tests", methods=["GET"])
def tests():
    print("Tests requested.")
    return nlptk.return_tests()


@app.route("/post-recording", methods=["GET"])
def receive_recording():
    print("Recording received.")
    return process_recording()


@app.route("/get-specialist", methods=["GET"])
def get_specialist():
    return nlptk.specialist()


@app.route("/reset", methods=["GET"])
def reset():
    print("Initiating reset.")
    with open("audios/received_audio.wav", mode="w") as f:
        f.write("")
    nlptk.reset()
    print("Reset is complete.")
    return "{'status': 'reset complete'}"


def process_recording():
    global audio_file
    if flask.request.method == "GET":
        audio_file = flask.request.data.decode("utf-8")
        with wave.open("audios/received_audio.wav", mode="wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(44100)
            if audio_file is not None or audio_file != "":
                decoded_string = base64.b64decode(audio_file)
                f.writeframes(decoded_string)
    try:
        remove_background_noise()
        client = OpenAI()
        translator = Translator()
        audio_file = open("audios/received_audio.wav", mode="rb")
        text_of_audio = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        language = str(detect_language())
        result = str(nlptk.initialize_api_session(text_of_audio))
        part_to_be_translated = result.split(sep="/")
        for lang in supported_langs:
            if lang == language:
                return f"{part_to_be_translated[0]}/{str(translator.translate(part_to_be_translated[1], language))}"
        audio_file.close()
        return f"{part_to_be_translated[0]}/{part_to_be_translated[1]}"

    except Exception as error:
        print(error)


def detect_language():
    recognizer = sr.Recognizer()
    audio = sr.AudioFile("audios/received_audio.wav")
    audio = recognizer.record(audio)
    text = recognizer.recognize_amazon(audio)
    return detect.detect(str(text))


def remove_background_noise():
    rate, data = wavfile.read("audios/received_audio.wav")
    background_noise_free_audio = noisereduce.reduce_noise(y=data, sr=rate)
    wavfile.write(rate=rate, filename="audios/received_audio.wav", data=background_noise_free_audio)


if __name__ == "__main__":
    app.run(port=5000)

# To host server, use command line command - py main.py
# To deploy with static address, use the following command.
# ngrok http --url=glowworm-charmed-jointly.ngrok-free.app --host-header=rewrite 5000

# Go to glowworm-charmed-jointly.ngrok-free.app to visit server.
