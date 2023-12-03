from flask import Flask, jsonify, request
import os
from openai import OpenAI
from flask_cors import CORS

print('test string')
my_secret = os.environ['openaiapikey']

client = OpenAI(
   api_key = my_secret,
)

app = Flask(__name__)
CORS(app)
print('test string2')
@app.route('/generate-initial-string', methods=['GET'])
def generate_initial_string():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Describe a product that solves a problem. Dont use any quotations or other talk."},
        ]
    )
    return {'string': response.choices[0].message.content}





@app.route('/generate-next-tokens', methods=['POST'])
def generate_next_tokens():
    user_input = request.json.get('userInput')  # Get the user input from the request body
    if not user_input:
        return jsonify({'error': 'No user input provided'}), 400

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You will provide the most probably single next token. Format as '{token}'"},
            {"role": "user", "content": user_input}
        ]
    )
    print("returning string:")
    print(response.choices[0].message.content)
    words_str = response.choices[0].message.content
    words_list = words_str.replace("{", "").replace("}", "").split(", ")
    return jsonify({'apiWords': words_list})
    #return jsonify({'apiWords': response.choices[0].message.content})

#@app.route('/get-words', methods=['GET'])


#def get_words():
#    print('test string4')
    # Logic to get five random words
    # Here, you can use OpenAI or any other method to generate words
#    words = ['Word1', 'Word2', 'Word3', 'Word4', 'Word5'] # Placeholder words
#    return jsonify({'apiWords': words})

@app.route('/')
def home():
    return "Flask server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    print('test string5')

   