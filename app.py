from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
import pandas as pd

from listingDetail import listingDetail

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def index():
    return "<h1>You got it dawg</h1>"

@app.route('/api/data/', methods=['POST'])
@cross_origin()
def get_data():
    print(request.json)
    # print(request.args)
    data = request.json['request']
    result = {}
    concat_list = list()

    try: 
        zip_code_string = data[0]

        zip_code_list = zip_code_string.split()

        for zip_code in zip_code_list: 
            detail = listingDetail(zip_code).get_detail()
            concat_list = concat_list + detail

        df = pd.DataFrame(concat_list)
        result = df.to_dict(orient='records')
    except TypeError as e: 
        pass
    
    return jsonify(result)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True,host='0.0.0.0')