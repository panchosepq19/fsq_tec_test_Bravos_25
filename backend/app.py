from flask import Flask, jsonify, request
from flask_cors import CORS  

import urllib.request
import json

app = Flask(__name__)
CORS(app)

def fetch_from_dog_api(endpoint, params=""):
    url = f"https://dogapi.dog/api/v2/{endpoint}{params}"
    with urllib.request.urlopen(url) as response:
        data = response.read()
        parsed = json.loads(data)
        return parsed

@app.route('/breeds', methods=['GET'])
def get_breeds():
    page = request.args.get('page', default='1')
    size = request.args.get('size', default='10')
    params = f'?page[number]={page}&page[size]={size}'

    api_data = fetch_from_dog_api('breeds', params)

    breeds = [
        {
            "id": item["id"],
            "name": item["attributes"]["name"]
        }
        for item in api_data.get("data", [])
    ]
    return jsonify(breeds)


@app.route('/breeds/<breed_id>', methods=['GET'])
def get_breed(breed_id):
    api_data = fetch_from_dog_api(f'breeds/{breed_id}')
    breed = {
        "id": api_data["data"]["id"],
        "name": api_data["data"]["attributes"]["name"]
    }
    return jsonify(breed)

@app.route('/facts', methods=['GET'])
def get_facts():
    page = request.args.get('page', default='1')
    size = request.args.get('size', default='10')
    params = f'?page[number]={page}&page[size]={size}'

    api_data = fetch_from_dog_api('facts', params)

    #return list of fact bodies
    facts = [item["attributes"]["body"] for item in api_data.get("data", [])]

    return jsonify(facts)

@app.route('/groups', methods=['GET'])
def get_groups():
    page = request.args.get('page', default='1')
    size = request.args.get('size', default='10')
    params = f'?page[number]={page}&page[size]={size}'

    api_data = fetch_from_dog_api('groups', params)

    groups = [
        {
            "id": item["id"],
            "name": item["attributes"]["name"]
        }
        for item in api_data.get("data", [])
    ]
    return jsonify(groups)

@app.route('/groups/<group_id>', methods=['GET'])
def get_group(group_id):
    api_data = fetch_from_dog_api(f'groups/{group_id}')
    group = {
        "name": api_data["data"]["attributes"]["name"]
    }
    return jsonify(group)

@app.route('/group-details/<group_id>', methods=['GET'])
def get_group_details(group_id):
    api_data = fetch_from_dog_api(f'groups/{group_id}')
    group = {
        "name": api_data["data"]["attributes"]["name"]
    }
    return jsonify(group)

@app.route('/group-details/<group_id>/breed/<breed_id>', methods=['GET'])
def get_group_breed_details(group_id, breed_id):
    # You can call both endpoints or just the breed:
    breed_data = fetch_from_dog_api(f'breeds/{breed_id}')
    breed = {
        "id": breed_data["data"]["id"],
        "name": breed_data["data"]["attributes"]["name"]
    }
    return jsonify({
        "group_id": group_id,
        "breed": breed
    })

if __name__ == '__main__':
    app.run(debug=True)