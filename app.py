from flask import Flask, request, jsonify
from flask_cors import CORS
from summarizer import FrequencySummarizer

app = Flask(__name__)
CORS(app)

summarizer = FrequencySummarizer()

@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.json
    text = data.get('text','')
    mode = data.get('mode','sentences')
    value = data.get('value',5)
    try:
        if mode=='percent':
            summary = summarizer.summarize(text, percent=float(value))
        else:
            summary = summarizer.summarize(text, num_sentences=int(value))
        return jsonify({'ok':True,'summary':summary})
    except Exception as e:
        return jsonify({'ok':False,'error':str(e)}),400

@app.route('/api/health')
def health():
    return jsonify({'ok':True,'msg':'running'})

if __name__=='__main__':
    app.run(port=5000,debug=True)
