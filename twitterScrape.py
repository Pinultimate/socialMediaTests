import oauth2 as oauth
import json

CONSUMER_KEY = 'zEeYqSgskeQPiuX1J1tttg'
CONSUMER_SECRET = 'ZEA9YCnQ8PQ8k06kLyaBBXJXCFppcGvgMi7xpslRmI'

SEARCH_URL = "https://api.twitter.com/1.1/search/tweets.json"
GEOCODE_URL = "https://api.twitter.com/1.1/geo/search.json"

ACCESS_KEY = '236588284-SzCOK2fOC6IPYrcW0e72wxj6Zv1oe0wtflRVM3hk'
ACCESS_SECRET = 'AibVTmxw7NHNpBfY4VydC5Qe63zXBq95JdlJVBSV4'

def oauth_req(url, key, secret, http_method="GET", post_body=None, http_headers=None):
    
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
    #print url

    resp, content = client.request(
        url,
        method=http_method,
        body=post_body,
        headers=http_headers,
        force_auth_header=True
    )
    return content

def oauth_get_req_with_params(url,key,secret,params):

    url_with_params = url + "?"
    for params_key in params.keys():
        url_with_params += params_key + "=" + str(params[params_key]) + "&"
    # Remove extraneous '?' or '&'
    url_with_params = url_with_params[:-1]
    return oauth_req(url_with_params,key,secret)

# EXAMPLE 1: Reverse Geo-encode --> find place based on coordinates

params = {
    'lat' : '37.4470610984003',
    'long' : '-122.160917799844',
    'granularity' : 'poi'
}

# Get JSON Response
geo_location_json_str = oauth_get_req_with_params(
    GEOCODE_URL,ACCESS_KEY,ACCESS_SECRET,params
)

# Convert JSON response to dict
geo_location_dict = json.loads(geo_location_json_str)

# Print results
geo_location_results = geo_location_dict["result"]["places"]
for place in geo_location_results:
    full_name = place["full_name"]
    id = place["id"]
    place_type = place["place_type"]
    print "Full Name: " + full_name
    print "ID: " + id
    print "Place Type: " + place_type

# EXAMPLE 2: Search Tweets near Cheesecake factory
tweets_search_params = {
    'q' : "%20", # Hack to search all tweets (that contain a space)
    'geocode' : "37.4470610984003,-122.160917799844,0.05km", # Within 50 meters of cheesecake factory
    'result_type' : 'recent'
}

# Get JSON response
tweets_search_results_json_str = oauth_get_req_with_params(
    SEARCH_URL,ACCESS_KEY,ACCESS_SECRET,tweets_search_params
)

tweets_search_dict = json.loads(tweets_search_results_json_str)

# Print results
for status in tweets_search_dict["statuses"]:
    print "Tweet: " + status["text"]
    print "Full Name Of Place: " + place["full_name"]
    print "Place Type: " + place["place_type"]