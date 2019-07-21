from app import app
from flask import jsonify
from flask import request
from app.yelp_link_mbe import is_mbe_certified

@app.route('/', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/yelpcheck', methods=['GET'])
def yelp_check():
    yelp_link = request.args.get('yelplink')
    return jsonify(is_mbe_certified(yelp_link))

