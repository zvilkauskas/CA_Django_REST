import requests

url = 'http://127.0.0.1:8000/posts/9/likes/'
headers = {'Authorization': 'Token c4386e7e33815b90f83d7bb4b71eda9bdf08fe77'}
r = requests.post(url, headers=headers)

print(r.json())