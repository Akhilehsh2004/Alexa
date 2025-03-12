from flask import Flask, render_template, request, jsonify
import pyttsx3
import wikipedia
import datetime
import pyjokes
import webbrowser
import pickle

app = Flask(__name__)

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

assistant_config = {
    'volume': engine.getProperty('volume'),
    'rate': engine.getProperty('rate')
}

def save_configuration():
    with open('assistant_config.pkl', 'wb') as file:
        pickle.dump(assistant_config, file)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    response = ""
    if 'hello' in command:
        response = "Hello, how can I assist you?"
    elif 'your name' in command:
        response = "I am your personal assistant."
    elif 'time' in command:
        now = datetime.datetime.now()
        response = f"The current time is {now.strftime('%H:%M:%S')}"
    elif 'date' in command:
        today = datetime.date.today()
        response = f"Today's date is {today.strftime('%B %d, %Y')}"
    elif 'joke' in command:
        response = pyjokes.get_joke()
    elif 'wikipedia' in command:
        response = "What do you want to know about?"
    elif 'search for' in command:
        response = "What would you like to search for?"
    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube."
    elif 'exit' in command or 'goodbye' in command:
        response = "Goodbye! Have a nice day."
    else:
        response = "Sorry, I didn't understand that. Please try again."
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    command = data.get('command')
    response = process_command(command.lower())
    return jsonify({'response': response})

if __name__ == '__main__':
    save_configuration()
    app.run(debug=True)
