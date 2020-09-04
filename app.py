from flask import Flask, request, make_response, send_file, jsonify
from flask_cors import CORS

import pyflite
import re
import os
import json
import os
import sys
import wave
import tempfile

# This FLASK server is intended to emulate the MARY-TTS API.
app = Flask("flite")
CORS(app)

pyflite.init()

voices = os.listdir("./voices/")
print(voices) 
#----------------------------------------------------------------
# Primary URL to obtain WAV files.

@app.route("/process")
def process():
    text = request.args["INPUT_TEXT"]
    selectedVoice = "cmu_us_aew.flitevox"
    rate = 175
    if 'VOICE' in request.args:   
        selectedVoice = request.args["VOICE"]
    if 'RATE' in request.args:
        rate = int(request.args["RATE"])

    waveData = generateWaveData(text, selectedVoice, rate)

    if (waveData is not None):
        try:
            filename = (re.sub('[^A-Za-z0-9]+', '', text)) + ".wav"

            # TODO : Add ENV VAR setting to control vocal sample rate.
            sampleRate = 16000.0 # hertz

            # Convert the waveform to a WAV file using the appropriate settings for Flite voices.
            obj = wave.open(filename,'w')
            obj.setnchannels(1) # mono
            obj.setsampwidth(2) 
            obj.setframerate(sampleRate)
            obj.writeframesraw(waveData)
            obj.close()

            wavFileData = None
            with open(filename, 'rb') as wav:
                wavFileData = wav.read()
                wav.close()

            if(wavFileData is not None):
                response = make_response()
                response.headers["Content-Type"] = "audio/wav"
                response.data = wavFileData

                # Now that the WAV file has been constructed, pull the binary data from it.
                # Remove the file on the disk, the data has been loaded into the response.
                os.remove(filename)
                return response

        except Exception as e:
            return str(e)

    return str("!!! ERROR: Failed to synthesize speech.")

#----------------------------------------------------------------

@app.route("/voices")
def returnVoices():
    # availableVoices = {}
    # voiceId = 0
    # for voice in voices:
    #     availableVoices[voiceId] = voice
    #     voiceId += 1
    return jsonify(availableVoices = voices)

#----------------------------------------------------------------

def selectVoice(voice):
    if (not(voice in voices)) :
        return "cmu_us_aew.flitevox"
    return voice

def generateWaveData(text, voice, rate):
    #voice = 
    voice = pyflite.select_voice( "./voices/" + selectVoice(voice))
    output_waveform = pyflite.text_to_wave(text, voice)

    from array import array
    samples = array('h', output_waveform['samples'])

    return samples