from app import app
from flask import jsonify
from flask import request
from .yelp_link_mbe import is_mbe_certified
from .socrata_api_query import (fetch_all, json_get)

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

@app.route('/all', methods=['GET'])
def get_all():
    query = fetch_all()
    return jsonify(json_get(query))

@app.route('/female', methods=['GET'])
def get_female():
    query = fetch_all({'female': True, 'ethnicity': None})
    return jsonify(json_get(query))