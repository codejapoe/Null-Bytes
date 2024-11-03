import requests

# username, password, database_id, data
def insert(api, data):
    try:
        response = requests.post('https://nullbytes.pythonanywhere.com/data/insert', json={'api': api, 'data': data})
        return response.json()

    except:
        return {'success': False, 'errors': {'code': 500, 'message': 'External Server Error'}}

# username, password, database_id, data
def delete(api, _id):
    try:
        response = requests.delete('https://nullbytes.pythonanywhere.com/data/delete', json={'api': api, '_id': _id})
        return response.status_code

    except:
        return {'success': False, 'errors': {'code': 500, 'message': 'External Server Error'}}

# username, password, database_id
def fetch(api):
    try:
        response = requests.get('https://nullbytes.pythonanywhere.com/data/fetch', json={'api': api})
        return response.json()

    except:
        return {'success': False, 'errors': {'code': 500, 'message': 'External Server Error'}}

# username, password, database_id, _id
def search(api, _id):
    try:
        response = requests.post('https://nullbytes.pythonanywhere.com/data/search', json={'api': api, '_id': _id})
        return response.json()
        
    except:
        return {'success': False, 'errors': {'code': 500, 'message': 'External Server Error'}}