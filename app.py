from flask import Flask, render_template, request, jsonify
from chatbot_logic import handle_chat

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['message']
    bot_response = handle_chat(user_message)
    return jsonify({'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)
