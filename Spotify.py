import requests
import base64
import random

# Your Spotify API credentials
client_id = 'ad0a8a8060204743b49d7c939c75563b'
client_secret = '8352057de410404aaa4ff72e91333c3c'

# Encode the client_id and client_secret
auth_str = f"{client_id}:{client_secret}"
b64_auth_str = base64.b64encode(auth_str.encode()).decode()

# Get the access token
auth_url = "https://accounts.spotify.com/api/token" #always the same bc ...
auth_headers = {
    "Authorization": f"Basic {b64_auth_str}",
}
auth_data = {
    "grant_type": "client_credentials",
}

response = requests.post(auth_url, headers=auth_headers, data=auth_data) #sensitive data is sent via body of api (post request). if it were a get request it would be iN browser url which is not secure -- sensitive data exposed
response_data = response.json()
print(response_data)
access_token = response_data.get("access_token")
if not access_token:
    print("Failed to get access token")
    exit()
#NOW WE ARE DONE GETTING SPOTIFY ACCESS ^^^

# Use the access token to call the Spotify API
api_urlgenres = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
api_url='https://api.spotify.com/v1/recommendations'
api_headers = {
    "Authorization": f"Bearer {access_token}",
}


trackanalysis_url='https://api.spotify.com/v1/audio-features'
api_headers = {
    "Authorization": f"Bearer {access_token}",
}

response2= requests.get(f'{trackanalysis_url}+', headers=api_headers)
songqualities=response2.json()
#check what the api wants and pass it in th parameters or post request

# response = requests.get(api_url, headers=api_headers, params=params) #OK TO Use get bc the artist id is not sensitive info.
# songdata = response.json()

# print(songdata)
# Print the artist data
# biglist=songdata['tracks'] #came from a much bigger dictionary
# print(biglist)


def makeplaylist(mood):
  params={'limit': 10,
        'seed_genres': 'classical,soundtracks'}
  if mood=="grand":
    params.update({
      'target_energy': 1.0,
      'min_tempo': 50,
      'target_valence': 0.6
      # 'seed_tracks': ['08QaHlMPWuO5PUxjl61bXn', '4u4VElxO7JM4IR4jR4TL1s']  #he's a pirate, arrival to earth,
      })
  elif mood=='lively':
        params = {'energy': (0.7, 1.0),
          'tempo': (100, 160),
          'valence': (0.5, 1.0)}
          # 'seed_tracks': '6N10tJfiQqm4wn6KM70aoT'} #up is down
  elif mood=='romantic':
        params = {
          'energy': (0.3, 0.7),
          'tempo': (50, 90),
          'valence': (0.6, 1.0)}
  elif mood=='dark':
        params.update({
          'target_energy': 1.0,
          'min_tempo': 50,
          'target_valence': 0.6
          })
  
  response = requests.get(api_url, headers=api_headers, params=params) #OK TO Use get bc the artist id is not sensitive info.
  songdata = response.json()
  print("ABCD",songdata['tracks'])
  biglist=songdata['tracks'] #came from a much bigger dictionary


  for i in biglist:
    print(i)
    trackid=i['id']
    response2= requests.get(f'{trackanalysis_url}/{trackid}', headers=api_headers)
    # print(response2)
    analysis=response2.json()
    print(i['name']+' by '+i['artists'][0]['name'])
    print(i['external_urls']['spotify'])
    # print(analysis)


def analyzetrack(id):
  response3= requests.get(f'{trackanalysis_url}/{id}', headers=api_headers)
  print(response3.json())


makeplaylist('dark')

