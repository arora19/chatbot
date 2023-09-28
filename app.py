import export
from flask import Flask, request, jsonify, render_template
import requests
import os
import json

# Create a Flask application
app = Flask(__name__)

# Load API key and model ID from config.json
with open('config.json') as config_file:
    config = json.load(config_file)
    anyscale_api_key = config["anyscale_api_key"]
    model_id = config["model_id"]

# Define the AnyScale API base URL
#export OPENAI_API_BASE='https://api.endpoints.anyscale.com/v1'
base_url = 'https://api.endpoints.anyscale.com/v1/'

# Function to send user input to the chatbot and get a response
def send_user_input(user_input):
    try:
        # Construct the URL for your specific model
        url = f'{base_url}{model_id}/completions'

        # Set up headers with the Authorization header
        headers = {
            'Authorization': f'Bearer {anyscale_api_key}',
            'Content-Type': 'application/json',
        }

        # Prepare the request body with user input
        body = {
            "messages": [{"role": "user", "content": user_input}],
        }

        # Make a POST request to the AnyScale API
        response = requests.post(url, headers=headers, json=body)
        print("API Response:", response.text)
        if response.status_code == 200:
            data = response.json()
            chatbot_response = data.get('choices')[0].get('message').get('content')
            return chatbot_response
        else:
            return 'Sorry, I couldn\'t fetch a response at the moment.'
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Add a route to serve the chat.html file
@app.route('/chatpage', methods=['GET', 'POST'])
def chat_page():
    return render_template('chat.html')  # Render the chat.html template

# Modify the /chat route to handle both GET and POST requests
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.json.get('user_input')
        chatbot_response = send_user_input(user_input)
        return jsonify({'chatbot_response': chatbot_response})
    elif request.method == 'GET':
        # Handle GET requests here
        initial_message = "Welcome to the chat! Start by typing a message."
        return jsonify({'chatbot_response': initial_message})

if __name__ == '__main__':
    app.run(debug=True)
