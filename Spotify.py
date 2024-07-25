import requests
import base64
import random

# Your Spotify API credentials
client_id = '#####'
client_secret = '#####'

# Encode the client_id and client_secret
auth_str = f"{client_id}:{client_secret}"
b64_auth_str = base64.b64encode(auth_str.encode()).decode()

# Get access token
auth_url = "https://accounts.spotify.com/api/token"
auth_headers = {
    "Authorization": f"Basic {b64_auth_str}",
}
auth_data = {
    "grant_type": "client_credentials",
}

response = requests.post(auth_url, headers=auth_headers, data=auth_data)
response_data = response.json()

access_token = response_data.get("access_token")
if not access_token:
    print("Failed to get access token")
    exit()

# Using the access token to call the Spotify API
api_urlgenres = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
api_url='https://api.spotify.com/v1/recommendations'
api_headers = {
    "Authorization": f"Bearer {access_token}",
}

trackanalysis_url='https://api.spotify.com/v1/audio-features'
api_headers = {
    "Authorization": f"Bearer {access_token}",
}

analysis_response= requests.get(f'{trackanalysis_url}', headers=api_headers)
songqualities=analysis_response.json()

#Generate playlist based on mood parameter

#Mood options: lively, romantic, melancholy, heroic

heroic_songs=['08QaHlMPWuO5PUxjl61bXn', #Klaus Badelt - He's a Pirate
             '6N10tJfiQqm4wn6KM70aoT', #Hans Zimmer - Up is Down
             '35gFlKdC4Pmo88Go1cVrae', #Klaus Badelt - The Medallion Calls
             '5yPdkiVYsRy9H0p9osaudl', #Klaus Badelt - Will and Elizabeth
             '4u4VElxO7JM4IR4jR4TL1s', #Steve Jablonsky - Arrival to Earth
              ]
heroic_seed_track=random.choice(heroic_songs)


lively_songs=['289nG8bnslnizI3aAa3npM', #Tchaikovsky - La Fee (Sleeping Beauty)
              '6MzJZx1c74T5Vp6FE3ny0X', #Tchaikovsky - Princess Florine (Sleeping Beauty)
              '289nG8bnslnizI3aAa3npM', #Tchaikovsky - Canari qui chante (Sleeping Beauty)
              '7hTnnY0wysFgebsmF0FPvx', #Tchaikovsky - Silver Fairy (Sleeping Beauty)
              '4KLVPRo0f6XUJa4t4dnRW6'  #Mozart - Eine Kleine Nachtmusik
              ]
lively_seed_track=random.choice(lively_songs)

sentimental_songs=['0Ee9oam0N0ZzxZSN9nogTQ', #Ravel - Antar
                '07eYxFCtC3UzWA8XUD4XkZ'  #Tchaikovsky - Sugarplum Pas de Deux
                ]
sentimental_seed_track=random.choices(sentimental_songs)

dark_songs=['19fi3jLiGLhR6AbtfGwize', #Lyubomudrov - The Spider Knows His Craft
            '1Aozvs1CIdllsgoCK5mrSC', #Grieg - Anitra's Dance
            '1OuCn2F9BmyTAdM0Jylo9X', #Wednesday Addams - Paint it Black
            '5cVHRNV1KfOkDP7Ql6nGXe', #Adam Hurst - Dusk
            '6OIo4vJRXwIWyf41JDh1H3', #Yoko Shimomura - Fragments of Sorrow (Kingdom Hearts)
            '6E0AIIq5p8MZCrHf4w64ko', #Hiroyuki Sawano - Vogel im Kafig
            '1lfKd4rk1FjLz0OE0NNKJv', #Adam Hurst - Four Winds
            '6buHoQU9OTdbJrAuniVwGL', #Hans Zimmer - Davy Jones
            '2LiWNkeUOAeibGxJKxmjsD'  #Prokofiev - Dance of the Knights (Romeo & Juliet)
]
dark_seed_track=random.choice(dark_songs)                                                                                                                                                

#Generate mood-based playlist
#options are heroic, lively, sentimental, and dark

def makeplaylist(mood):
  params={'limit': 100,
        'seed_genres': 'classical,soundtrack'}
  
  if mood=="heroic":
    params.update({
      'min_tempo': 50,
      'seed_tracks': heroic_seed_track,
      'max_speechiness': 0.33
      })
  
  elif mood=='lively':
        params = {'energy': (0.7, 1.0),
          'min_tempo': 80,
          'valence': (0.5, 1.0),
          'seed_tracks': lively_seed_track,
          'target_mode': 0 ,
          'max_speechiness': 0.33}
  
  elif mood=='sentimental':
        params = {
          # 'energy': (0.3, 0.7),
          'min_tempo': 60,
          'valence': (0.5, 1.0),
          'max_speechiness': 0.33,
          'seed_tracks': sentimental_seed_track}
  
  elif mood=='dark':
        params.update({
          'min_tempo': 50,
          # 'target_valence': 0.6,
          'target_mode': 0,
          'seed_tracks': dark_seed_track,
          'max_speechiness': 0.2
          })
  
  #Calling the API
  response = requests.get(api_url, headers=api_headers, params=params) 

  #Converting response to JSON
  songdata = response.json()

  #Accessing 'tracks' JSON entry
  big_list=songdata['tracks']

  #Picking 15 random entries from 100 recommendation results
  generated_playlist=random.choices(big_list, k=15)

  #Assigning a number to each track
  j=1 
  print(f"Here is your {mood} playlist: \n")
  for i in generated_playlist:

    #Get track ID to build spotify song URL
    trackid=i['id'] 

    #Printing track info to console
    print(f'{j}. ', i['name']+' by '+i['artists'][0]['name'])
    print(i['external_urls']['spotify'],'\n')

    #Increasing count of j for next entry
    j=j+1

#Get a track's audio features using song ID
def analyzetrack(id):
  analysis_response= requests.get(f'{trackanalysis_url}/{id}', headers=api_headers)
  print(analysis_response.json())
 
makeplaylist('dark')
