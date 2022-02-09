import requests
import json
from pprint import pprint
import os


class ApiException(Exception):
    pass


class DevToException(Exception):
    pass


class Checker:

    def __init__(self):

        self._check_dirlist = ['articles/', 'photos/', 'videos/']

        if not os.path.exists('api_key.txt'):
            raise ApiException('Нужно создать файл с api-ключём')

        with open('api_key.txt', 'r') as f:
            self.key = f.readline().strip()

        self.header = {'api-key': self.key}

    def _errors(self, r):
        if not r.status_code == 200:
            if r.status_code == 400:
                raise DevToException('Неверный запрос!')
            elif r.status_code == 401:
                raise DevToException('Требуется авторизация!')
            elif r.status_code == 403:
                raise DevToException('Запрещённый запрос!')
            elif r.status_code == 404:
                raise DevToException('Ресурс не найден!')
            elif r.status_code == 422:
                raise DevToException('Параметр отсутствует или его значение пустое!')
            elif r.status_code == 429:
                raise DevToException('Превышен лимит запросов, попробуйте ещё раз через 30 сек.!')
            else:
                raise DevToException('Что-то пошло не так!')


class Articles(Checker):

    def published(self, per_page=10, page=1):
        r = requests.get(f'https://dev.to/api/articles?per_page={per_page}&page={page}')
        self._errors(r)
        pprint(r.json())
        return r

    def user(self, per_page=5, page=1):
        r = requests.get(f'https://dev.to/api/articles/me?per_page={per_page}&page={page}', headers=self.header)
        self._errors(r)
        pprint(r.json())
        return r

    def user_pub(self, per_page=5, page=1):
        r = requests.get(f'https://dev.to/api/articles/me/published?per_page={per_page}&page={page}', headers=self.header)
        self._errors(r)
        pprint(r.json())
        return r

    def user_unpub(self, per_page=5, page=1):
        r = requests.get(f'https://dev.to/api/articles/me/unpublished?per_page={per_page}&page={page}', headers=self.header)
        self._errors(r)
        pprint(r.json())
        return r

    def user_all(self, per_page=5, page=1):
        r = requests.get(f'https://dev.to/api/articles/me/all?per_page={per_page}&page={page}', headers=self.header)
        self._errors(r)
        pprint(r.json())
        return r

    def sorted(self, per_page=10, page=1):
        r = requests.get(f'https://dev.to/api/articles/latest?per_page={per_page}&page={page}')
        self._errors(r)
        pprint(r.json())
        return r

    def userid(self, userid):
        r = requests.get(f'https://dev.to/api/articles/{userid}')
        self._errors(r)
        pprint(r.json())
        return r

    def path(self, username='devteam', slug='for-empowering-community-2k6h'):
        r = requests.get(f'https://dev.to/api/articles/{username}/{slug}')
        self._errors(r)
        pprint(r.json())
        return r

    def create(self, body,  title='unnamed', series='', tags='', pub='false'):
        payload = {
            "article": {
                "title": title,
                "published": pub,
                "body_markdown": body,
                "tags": tags,
                "series": series}
        }
        r = requests.post(f'https://dev.to/api/articles', json=payload, headers=self.header)
        self._errors(r)
        print('Статья создана!')
        return r

    def update(self, userid, body='',  title='', series='', tags='', pub=''):
        payload = {
            "article": {
                "title": title,
                "published": pub,
                "body_markdown": body,
                "tags": tags,
                "series": series}
        }
        r = requests.put(f'https://dev.to/api/articles/{userid}', json=payload, headers=self.header)
        self._errors(r)
        print('Статья обновлена!')
        return r


class Tags(Checker):

    def tags(self, per_page=10, page=1):
        r = requests.get(f'https://dev.to/api/tags?per_page={per_page}&page={page}')
        self._errors(r)
        pprint(r.json())
        return r

    def followed(self):
        r = requests.get(f'https://dev.to/api/follows/tags', headers=self.header)
        self._errors(r)
        pprint(r.json())
        return r


class Content(Checker):

    def images(self, username):
        r = requests.get(f'https://dev.to/api/profile_images/{username}')
        self._errors(r)
        pprint(r.json())
        return r

    def videos(self, per_page=10, page=1):
        r = requests.get(f'https://dev.to/api/videos?per_page={per_page}&page={page}')
        self._errors(r)
        pprint(r.json())
        return r


class Save(Checker):

    def _check_dir(self):
        for i in self._check_dirlist:
            if not os.path.exists(i):
                os.mkdir(i)

    def articles(self):
        arti = Articles()
        self._check_dir()
        r = arti.user_all()
        json_out = []
        am = 0
        for i in r.json():
            form = {
                'title': (i['title']),
                'published': (i['published']),
                'tags': (i['tag_list']),
                'description': (i['description']),
                'url': (i['url'])
            }
            json_out.append(form)
            am += 1

        with open('articles/my_art.json', 'w') as file:
            json.dump(json_out, file, indent=2)
            print('Сохранено статей: ', am)

    def photos(self, username):
        cont = Content()
        self._check_dir()
        r = cont.images(username)
        pic1 = requests.get((r.json()['profile_image']))
        pic2 = requests.get((r.json()['profile_image_90']))
        with open('photos/picture1.jpg', 'wb') as file:
            file.write(pic1.content)
            print('Данные сохранены')
        with open('photos/picture2.jpg', 'wb') as file:
            file.write(pic2.content)
            print('Данные сохранены')

    def video(self):
        cont = Content()
        self._check_dir()
        r = cont.videos(1)
        head = {"Referer": (r.json()[0]['video_source_url'])}
        vid = requests.get((r.json()[0]['video_source_url']), headers=head)
        with open('videos/video', 'wb') as file:
            file.write(vid.content)
            print('Данные сохранены')