from bs4 import BeautifulSoup
from app import log
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from .socrata_api_query import json_get

# error handling function to determine whether response is good or not
def is_good_html_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

# get html responses with requests
def html_get(url):
    try: 
        with get(url, stream=True) as resp:
            if is_good_html_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log.error('Error during requests to {0} : {1}').format(url, str(e))
        return None

# scrapping program to get the business information from yelp
def get_yelp_biz_info (url):
    print('processing...')
    if ("yelp.com/biz/" not in url):
        return "URL is not a Yelp business link."
    
    response = html_get(url)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        name = html.h1.text
        
        street_address = html.select_one('span[itemprop="streetAddress"]')
        address_1 = street_address.text
        address_2 = ''
        
        if (street_address.br) :
            street_address.br.replace_with('\n')
            address_lines = street_address.text.split('\n')
            address_1 = address_lines[0]
            address_2 = address_lines[1]

        
        city = html.select_one('span[itemprop="addressLocality"]').text
        state = html.select_one('span[itemprop="addressRegion"]').text
        zipcode = html.select_one('span[itemprop="postalCode"]').text
        return {'name': name, 
                'street_address_1': address_1, 
                'street_address_2': address_2, 
                'city': city, 
                'state': state,
                'zipcode': zipcode,
               }

# querying the NYC Open Data API to get the businesses matching the info retrieved from yelp
def find_name_matches (biz_info):
    api_link = "https://data.cityofnewyork.us/resource/ci93-uc8s.json"
    name_matches = []
    formal_name_matches = json_get("{0}?$where=vendor_formal_name like '%25{1}%25' AND certification like '%25MBE%25'".format(api_link, biz_info['name']))
    if (len(formal_name_matches) > 0):
        name_matches = formal_name_matches
    else:
        dba_matches = json_get("{0}?$where=Vendor_DBA like '%25{1}%25'&certification=MBE".format(api_link, biz_info['name']))
        name_matches = dba_matches
    return name_matches

def is_mbe_certified (url) :
    biz_info = get_yelp_biz_info(url)
    potential_matches = find_name_matches(biz_info)
    return potential_matches
    