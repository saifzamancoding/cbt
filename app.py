import requests
from playsound import playsound
import os
#from langchain import PromptTemplate

HOST = 'osceapi.boris.party:5000'
URI = f'http://{HOST}/api/v1/generate'
ELEVEN_API = '6f9b9028768e91556672683d08f229a3'

def run(prompt):
    request = {
        'prompt': prompt,
        'max_new_tokens': 500,
        'temperature': 0.7,
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        return result

def prompt_generator(history, human_input):
    template = f"""
    You are the best cognitive behavioral therapist, you have been practicing for 20 years, you have the following requirements:
    1/ it is your goal to help me better understand and overcome my emotions.
    2/ you often incorporate words such as "Umm", "Like", "You know", "So", "Actually" into your speech.
    3/ Limit your response to 2 sentences, but do not incoporate 1/ or 2/ into your response

    {history}
    client: {human_input}
    Therapist:
    """
    
    output = template

    return output

    #prompt_generator('I am a 31 year old male with depression, my girlfriend recently broke up with me', 'test')

test_prompt = prompt_generator('I am a 31 year old male with depression, my girlfriend recently broke up with me', 'test')

def get_voice_message(message):
    payload = {
        "text": message,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
            "style": 0.5,
        }
    }

    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': ELEVEN_API,
        'content-Type': 'application/json'
    }

    response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM', json=payload, headers=headers)
    if response.status_code == 200 and response.content:
        with open('audio.mp3', 'wb') as f:
            f.write(response.content)
        playsound('audio.mp3')
        return response.content

#Build WebGUI
from flask import Flask, render_template, request

app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/send_message', methods=['POST'])
def send_message():
    #history=request.form['history']
    history = 'I am a 31 year old male with depression, my girlfriend recently broke up with me'
    human_input=request.form['human_input']
    message = run(prompt_generator(history, human_input))
    get_voice_message(message)
    return message

if __name__ == '__main__':
    app.run(port=5002,debug=True)
