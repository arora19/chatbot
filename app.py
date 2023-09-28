import export as export
from flask import Flask, request, jsonify, render_template
import requests
import os
import json
# Set the OPENAI_API_BASE environment variable
os.environ["OPENAI_API_BASE"] = "https://api.endpoints.anyscale.com/v1"


# create a Flask application
# instance of the Flask class is created and assigned to the variable 'app'. This instance represents the web app.

app = Flask(__name__)


# define a Route and View function


@app.route('/')
def hello():  # function called when user accesses the root url.
    # print('inside hello func')
    return 'Hello, this is your chatbot!'


# Define the URL for the chatbot interaction
chatbot_url = 'http://127.0.0.1:5000/chat'




# Function to process user input and generate a chatbot response
def process_user_input(user_input):
    print("Inside process_user_input function")
    # basic chatbot logic: Echo the user's input
    return f' {user_input}'


@app.route('/chat', methods=['POST'])
#@app.route('/chat', methods=['GET', 'POST'])
def chat():
    # print('inside chat func')
    if request.method == 'POST':
        print('Request method is POST')
        user_input = request.json.get('user_input')
        if user_input == 'hi' or user_input == 'hello':
            return "Hello, I hope you are having a great day. How can I help?"
        else:
            # Make an API request
            try:
                # Get the API key from the environment variable
                api_key = os.environ.get("ANYSCALE_API_KEY")

                # Define the base URL for the AnyScale API
                base_url = 'https://api.endpoints.anyscale.com/v1/'

                # Construct the URL for a sample recipe (you can modify this)
                url = f'{base_url}random'

                # Set up request parameters, including your API key
                headers = {
                    'Authorization': f'Bearer {api_key}',
                }

                # Make the API request
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                     # If the request is successful, parse the response JSON
                    data = response.json()
                    recipe_title = data.get('title', 'Title not found in response')
                    return f"Here's a random recipe: {recipe_title}"
                else:
                    return 'Sorry, I couldn\'t fetch a recipe at the moment.'

            except Exception as e:
                return f"An error occurred: {str(e)}"
    else:
        return jsonify({'chatbot_response': 'This endpoint only supports POST requests'})

    '''
        # print("Inside chat func where method= POST")
        # Retrieve user's input from the request's JSON data.
        user_input = request.json.get('user_input')

        # Process the user input and generate a response.
        chatbot_response = process_user_input("Did you say: " + user_input + "?")

        # Return the chatbot's response as JSON
        return jsonify({'chatbot_response': chatbot_response})
    else:
        return render_template('chat.html')
'''


if __name__ == '__main__':
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
            api_key = config["api_key"]
    except FileNotFoundError:
        print("The configuration file 'my_config.json' does not exist.")
    except KeyError:
        print("The 'api_key' key is missing in the configuration file.")
    except json.JSONDecodeError:
        print("Error decoding the JSON configuration file.")

    # user_input = 'Hello, chatbot!'
    app.run(debug=True)

