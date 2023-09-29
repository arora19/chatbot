from flask import Flask, request, jsonify, render_template
import requests
import os
import json

# Create a Flask application
app = Flask(__name__)


# Define the AnyScale API base URL
base_url = 'https://api.endpoints.anyscale.com/v1/'

# Function to send user input to the chatbot and get a response
def send_user_input(user_input):
    try:
        # Fetch the environment variables
        api_base = os.getenv("OPENAI_API_BASE")
        token = os.getenv("OPENAI_API_KEY")

        # Construct the URL
        url = f"{api_base}/chat/completions"

        # Set up headers with the Authorization header
        headers = {
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json',
        }

        # Prepare the request body with system message, user input, and model details
        body = {
            "model": "meta-llama/Llama-2-70b-chat-hf",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.7
        }

        # Make a POST request to the AnyScale API
        response = requests.post(url, headers=headers, json=body)
        print("API Response:", response.text)
        if response.status_code == 200:
            data = response.json()
            chatbot_response = data.get('choices')[0].get('message').get('content')
            return chatbot_response
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
       # print(f"An error occurred: {str(e)}")  # Logging the error
        return f"An error occurred: {str(e)}"


# Add a route to serve the chat.html file and handle POST requests
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.json.get('user_input')
        chatbot_response = send_user_input(user_input)
        return jsonify({'chatbot_response': chatbot_response})
    elif request.method == 'GET':
        return render_template('chat.html')  # Render the chat.html template


if __name__ == '__main__':
    app.run(debug=True)
