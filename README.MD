# Flite TTS - Docker
This project aims to provide a minimal version of [Festvox's Flite](https://github.com/festvox/flite) that can be deployed via Docker. 

This has a very specific use-case. The contaienr hosts a Python Flask server which provides a means of outputting WAV files containing synthesized text. Additional features of Flite are currently non-operational (IE: Playing sound directly). 

Additionally, the software is wrapped in Python (as Flite is written in C). The work from https://github.com/happyalu/pyflite has been adapted for use here. 

## Requirements
- Docker

## Setup
To install:
1. Build the container image using: `docker build . -t flitetts`
2. Start the container with the following: `docker run -it -p 5645:5645 flitetts`

## Usage
To obtain synthesized speech in a WAV file from the container, submit a GET request. Below is an example using CURL:
```
curl -G "http://localhost:5645/process?" --data-urlencode "INPUT_TEXT=Welcome to the world of speech synthesis." --data-urlencode "VOICE=cmu_us_rms.flitevox" -o test.wav
```
To retrieve all of the voices available for the TTS engine, submit the following:
```
curl -G "http://localhost:5645/voices"
```
This will return a JSON string similar to the following:
```
{
  "availableVoices": [
    "cmu_us_rxr.flitevox",
    "cmu_us_ahw.flitevox",
    "cmu_us_ksp.flitevox",
    "cmu_us_slt.flitevox",
    "cmu_us_eey.flitevox",
    "cmu_us_ljm.flitevox",
    "cmu_us_aew.flitevox",
    "cmu_us_slp.flitevox",
    "cmu_us_aup.flitevox",
    "cmu_us_clb.flitevox",
    "cmu_us_lnh.flitevox",
    "cmu_us_jmk.flitevox",
    "cmu_us_bdl.flitevox",
    "cmu_us_fem.flitevox",
    "cmu_us_gka.flitevox",
    "cmu_us_axb.flitevox",
    "cmu_us_rms.flitevox",
    "cmu_us_awb.flitevox"
  ]
}
```