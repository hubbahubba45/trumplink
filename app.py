import os 
from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__, static_folder='static')

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/random_joke', methods=['GET'])
def random_joke():
    try:
        prompt = "suggest me something trump would do in one line in his voice"
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        # Extract the joke from the Groq response
        joke = completion.choices[0].message.content
        return jsonify({"joke": joke})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
