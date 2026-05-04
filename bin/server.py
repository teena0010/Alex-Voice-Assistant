from flask import Flask, request, jsonify
from gpt4all import GPT4All

app = Flask(__name__)

# Correct model path and filename
model = GPT4All("gpt4all-lora-quantized.bin", model_path=r"/Personal assistant/models")

@app.route('/command', methods=['POST'])
def handle_command():
    try:
        user_input = request.json.get('command', '')

        with model.chat_session():
            response = model.generate(user_input, max_tokens=200)

        return jsonify({'response': response})

    except Exception as e:
        print("❌ GPT4All Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)