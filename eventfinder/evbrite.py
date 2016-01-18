import sys, os, requests

def safe_request(URL, API_TOKEN):
    response = None
    try:
        response = requests.get(URL,
                        headers = {
                            "Authorization": 'Bearer ' + API_TOKEN,
                        },
                        verify = True,)
    except:
        return {'error': sys.exc_info()[0]}
    return response.json()

def get_categories():
    API_BASE_URL = os.environ.get('API_BASE_URL', "https://www.eventbriteapi.com/v3/")
    category_url = API_BASE_URL + '/categories/'
    response = safe_request(category_url, str(os.environ.get('API_TOKEN', 'RFCEYTQBPPOPTIJJ32B4')))
    return response

def get_events_by_category_id(category_ids):
    API_BASE_URL = os.environ.get('API_BASE_URL', "https://www.eventbriteapi.com/v3/")
    category_search_url =  API_BASE_URL + 'events/search/?categories=' + ",".join(category_ids)
    response = safe_request(category_search_url, str(os.environ.get('API_TOKEN', 'RFCEYTQBPPOPTIJJ32B4')))
    return response
