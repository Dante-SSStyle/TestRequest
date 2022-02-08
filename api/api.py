import requests
from pprint import pprint

with open('api/api_key.txt', 'r') as f:
    key = f.readline().strip()


class MyApi:

    def art_published(self, per_page=10):
        r = requests.get(f'https://dev.to/api/articles?per_page={per_page}')
        # pprint(r.json())

    def art_user(self, per_page=5):
        head = {'api-key': key}
        r = requests.get(f'https://dev.to/api/articles/me?per_page={per_page}', headers=head)
        # pprint(r.json())

    def art_user_pub(self, per_page=5):
        head = {'api-key': key}
        r = requests.get(f'https://dev.to/api/articles/me/published?per_page={per_page}', headers=head)
        # pprint(r.json())

    def art_user_unpub(self, per_page=5):
        head = {'api-key': key}
        r = requests.get(f'https://dev.to/api/articles/me/unpublished?per_page={per_page}', headers=head)
        # pprint(r.json())

    def art_user_all(self, per_page=5):
        head = {'api-key': key}
        r = requests.get(f'https://dev.to/api/articles/me/all?per_page={per_page}', headers=head)
        # pprint(r.json())
        return r

    def art_sorted(self, per_page=10):
        r = requests.get(f'https://dev.to/api/articles/latest?per_page={per_page}')
        # pprint(r.json())

    def art_id(self, id):
        r = requests.get(f'https://dev.to/api/articles/{id}')
        # pprint(r.json())

    def art_path(self, username='devteam', slug='for-empowering-community-2k6h'):
        r = requests.get(f'https://dev.to/api/articles/{username}/{slug}')
        # pprint(r.json())

    def art_video(self, per_page=10):
        r = requests.get(f'https://dev.to/api/videos?per_page={per_page}')
        # pprint(r.json())
        return r

    def art_create(self, body,  title='unnamed', series='', tags='', pub='false'):
        head = {'api-key': key}
        payload ={
        "article": {
            "title": title,
            "published": pub,
            "body_markdown": body,
            "tags": tags,
            "series": series}
        }
        r = requests.post(f'https://dev.to/api/articles', json=payload, headers=head)
        # pprint(r.json())

    def art_update(self, id, body='',  title='', series='', tags='', pub=''):
        head = {'api-key': key}
        payload = {
            "article": {
                "title": title,
                "published": pub,
                "body_markdown": body,
                "tags": tags,
                "series": series}
        }
        r = requests.put(f'https://dev.to/api/articles/{id}', json=payload, headers=head)
        # pprint(r.json())

    def tags(self, per_page=10):
        r = requests.get(f'https://dev.to/api/tags?per_page={per_page}')
        # pprint(r.json())

    def tags_followed(self):
        head = {'api-key': key}
        r = requests.get(f'https://dev.to/api/follows/tags', headers=head)
        # pprint(r.json())

    def profile_images(self, username):
        r = requests.get(f'https://dev.to/api/profile_images/{username}')
        # pprint(r.json())
        return r
