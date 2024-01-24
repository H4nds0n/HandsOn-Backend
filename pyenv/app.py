from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import threading
from run_model import Queue
import concurrent.futures

from getHands import Hands

app = Flask(__name__)
cors = CORS(app)
hand = Hands()
q = Queue()
most_common = {}

@app.route('/streaming', methods=['POST'])
@cross_origin()
def streaming():
    if request.method == 'POST':
        post_data = request.get_json()['img'].split(',')[-1]
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(q.run_queue, post_data)
            
            res = future.result

        res = jsonify({"letter": chr(res)[0], "conf": 0, "handExists": True})
        most_common.clear()
        return res
    
# pass img to function
# if 10 img processed -> take avg conf of most common letter, if conf > 0.75 return 
# else remove oldest img from queue, add newest to queue 

if __name__ == '__main__':
    app.run(debug=False, port=5001)