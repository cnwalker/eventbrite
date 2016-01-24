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

def categories_to_id_pairs(category_list):
    choices = []
    for category in category_list:
        choices.append((category.get('id'), category.get('short_name_localized')))
    return choices

def get_events_by_category_id(category_ids, location, page_num):
    API_BASE_URL = os.environ.get('API_BASE_URL', "https://www.eventbriteapi.com/v3/")
    category_search_url =  API_BASE_URL + 'events/search/?categories=' + ",".join(category_ids)
    if location:
        category_search_url += '&location.address=' + location
    if page_num:
        category_search_url += '&page=' + str(page_num)
    response = safe_request(category_search_url, str(os.environ.get('API_TOKEN', 'RFCEYTQBPPOPTIJJ32B4')))
    return response
