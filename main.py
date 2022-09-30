import json
import requests
from flask import Blueprint, Flask, Response, json
from flask_restplus import Api, Resource
import utils as utils

app = Flask(__name__)

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, version="0.1",
          title='XRPL UNL Validator',
          description="A python application for decoding an XRPL UNL from a URL.")

app.register_blueprint(blueprint)

# Decode UNL
@api.route('/decode/<path:unl>', methods=["GET"])
class decode_unl(Resource):
    def get(self, unl=None):
        
        try:
            r = requests.get(unl)
        except:
            response = {'Error': "Please enter a valid URL"}
            return Response(
                json.dumps(response),
                mimetype='application/json',
                status=200
            )
        if r.status_code == requests.codes.ok :
            vlistcont=r.json()
            valist= ','.join(s.decode('utf-8', 'ignore') for s in utils.decodeValList(vlistcont))

            response = {'Pub Keys': valist, 'Verified': utils.verifyUNL(vlistcont)}
            return Response(
                json.dumps(response),
                mimetype='application/json',
                status=200
            )
        else:
            response = {'Error': "Could get a valid response from {} \n Response: {}".format(r.url,r.status_code)}
            return Response(
                json.dumps(response),
                mimetype='application/json',
                status=200
            )
            
        
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)