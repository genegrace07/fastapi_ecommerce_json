import json

users = 'users.json'

users_cached={}

def users_cache():
        with open(users,'r') as f:
            users_cached = json.load(f)
        print(users_cached)
users_cache()
