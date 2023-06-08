from flask import Flask, render_template, request, send_file
import openai
from gtts import gTTS
import tempfile
import logging
import base64


app = Flask(__name__, static_url_path='/static')
openai.api_key = "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"


def chatgpt_api_call(condition, severity):
    messages = []
    messages.append({"role": "system", "content": f"Condition: {condition}\nSeverity: {severity}"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = response["choices"][0]["message"]["content"]
    audio_file = generate_audio(reply)
    return reply, audio_file


def generate_audio(text):
    try:
        # Generate audio from the text using gTTS
        tts = gTTS(text=text, lang="en")
        
        # Create a temporary file for storing the audio
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        audio_file = temp_file.name
        temp_file.close()

        # Save the audio to the temporary file
        tts.save(audio_file)

        with open(audio_file, 'rb') as file:
            encoded_audio = base64.b64encode(file.read()).decode('utf-8')

        return encoded_audio
    except Exception as e:
        logging.error(f"Error generating audio: {str(e)}")
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        condition = request.form['condition']
        severity = request.form['severity']
        reply, audio_file = chatgpt_api_call(condition, severity)
        return render_template('index.html', reply=reply, audio_file=audio_file)
    else:
        conditions = [
            'Headache',
            'Fever',
            'Cough',
            'Back Pain',
            'Allergies',
            'Asthma',
            'Diabetes'
            'High Blood Preassure',
            'Insomnia',
            'Migrane',
            'Respiratory Infections',
            'Anxiety',
            'Depression',
            'Arthritis',
            'Heartburn',
            'Influenza (flu)',
            'Acne',
            'Eczema',
            'Psoriasis'
        ]
        return render_template('index.html', conditions=conditions)

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

