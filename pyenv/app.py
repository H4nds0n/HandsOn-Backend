from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from getHands import getHands

app = Flask(__name__)
cors = CORS(app)

@app.route('/streaming', methods=['POST'])
@cross_origin()
def streaming():
    if request.method == 'POST':
        post_data = request.get_json()['img'].split(',')[-1]
        try:
            letter, conf = getHands(post_data)
            conf = conf.item()
        except Exception as e:
            letter = ""
            conf = ""
            print(e)
        print(type(conf), type(letter))
        res = jsonify({"letter": letter, "conf": conf})
        return res

        


if __name__ == '__main__':
    app.run(debug=True, port=5001)