import json
import requests
from api.api import MyApi


def save_articles():
    r = MyApi.art_user_all('heh')
    with open('articles/my_art.json', 'w') as file:
        json.dump(r.json(), file, indent=2)
    # print(r.json())


def save_photos(username):
    r = MyApi.profile_images('heh', username)
    pic1 = requests.get((r.json()['profile_image']))
    pic2 = requests.get((r.json()['profile_image_90']))
    with open('photos/picture1.jpg', 'wb') as file:
        file.write(pic1.content)
    with open('photos/picture2.jpg', 'wb') as file:
        file.write(pic2.content)


def save_video():
    r = MyApi.art_video('heh', 1)
    # print(r.json())
    # print((r.json()[0]['video_source_url']))
    head = {"Referer": (r.json()[0]['video_source_url'])}
    vid = requests.get((r.json()[0]['video_source_url']), headers=head)
    with open('videos/video', 'wb') as file:
        file.write(vid.content)