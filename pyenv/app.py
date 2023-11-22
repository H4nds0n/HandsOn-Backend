from flask import Flask, request, jsonify
from getHands import getHands

app = Flask(__name__)

@app.route('/streaming', methods=['POST'])
def streaming():
    if request.method == 'POST':
        post_data = request.get_json()['base64']
        try:
            letter, conf = getHands(post_data)
        except e:
            letter = ""
            conf = ""
            print(e)
        res = f'{{"letter": "{letter}", "conf": "{conf}"}}'
        return res
        


if __name__ == '__main__':
    app.run(port=5001, debug=True)