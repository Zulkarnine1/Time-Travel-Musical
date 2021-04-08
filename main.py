import requests as req
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from env import SPOTIFY_ID,SPOTIFY_SECRET

target_time = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD\n")

res = req.get(url=f"https://www.billboard.com/charts/hot-100/{target_time}")
res.raise_for_status()


soup = BeautifulSoup(res.text,"html.parser")
thisweek = soup.find_all(name="span",class_="chart-element__information__song text--truncate color--primary")
top100 = [song.getText() for song in thisweek]
print(top100)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)


songs = []
year = target_time.split("-")[0]
for song in top100:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")




playlist = sp.user_playlist_create(user=user_id, name=f"{target_time} Billboard 100", public=False)


sp.playlist_add_items(playlist_id=playlist["id"], items=songs)
print(playlist["external_urls"]["spotify"])