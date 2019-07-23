from app import app
from flask import jsonify
from flask import request
from .yelp_link_mbe import is_mbe_certified

@app.route('/', methods=['GET'])
def user():
    return jsonify({'user': 'Ornella'})

@app.route('/yelpcheck', methods=['GET'])
def yelp_check():
    yelp_link = request.args.get('yelplink')
    matches = []
    if (yelp_link != None):
        matches = is_mbe_certified(yelp_link)
    return jsonify(matches)

