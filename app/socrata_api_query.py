from requests import get
import json

# get json responses with requests
def json_get(api_url):
    resp = get(api_url).json()
    return resp

def fetch_all (conditions={'female': False, 'ethnicity': None}):
    query = "https://data.cityofnewyork.us/resource/ci93-uc8s.json?"
    if ((conditions['ethnicity'] != None) or (conditions['female'] == True)):
        query += '$where='
    if (conditions['ethnicity'] != None):
        query += ('ethnicity={0}'.format(conditions['ethnicity']))
    if (conditions['female'] == True):
        query += ("certification like '%25WBE,MBE%25'")
    return query