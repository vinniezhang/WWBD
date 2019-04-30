from flask import Flask, send_file, request #request from Flask interacts with HTML
import requests #interact with API
import os #access env
import json #return dictionary to front end

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

#authentication ?
body_params = {'grant_type': 'client_credentials'}
auth_url='https://accounts.spotify.com/api/token'
response = requests.post(auth_url, data=body_params, auth = (os.getenv("API_CLIENTID"), os.getenv("API_SECRET")))
access_token = response.json()['access_token'] #extract access token from list
print(response)

@app.route('/', methods=['GET','POST'])
def home():
  if request.method == 'GET':
    return send_file('public/index.html',)

  if request.method == 'POST':
    song = request.form['value']
    return do_spotify_request(song)

def do_spotify_request(song):  
  req_url = 'https://api.spotify.com/v1/tracks/' + song
  ret_song = requests.get(req_url, headers={"Authorization": "Bearer " + access_token})
  pull_from = ret_song.json()
  # alb = pull_from['album']['name']
  idsong = song
  name_song = pull_from['name']
  ret_dic = {
    # "album": alb,
    "id": idsong,
    "name": name_song
  }
  ret_obj = json.dumps(ret_dic)
  return ret_obj


if __name__ == '__main__':
  app.run()
    
