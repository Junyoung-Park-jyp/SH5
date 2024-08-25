from flask import Flask, request, jsonify
from modules.preprocess import preprocess_infer
from inference import inference

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['GET'])
def predict():
    try:
        text = '피자스쿨'
        preprocessed_text = inference(preprocess_infer(text))
        prediction = inference(preprocessed_text)

        return jsonify({'category': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
