import requests
import json
from pprint import pprint
import os


class Checker:

    def __init__(self):

        self._check_dir = ['articles/', 'photos/', 'videos/']

        if not os.path.exists('api_key.txt'):
            raise ApiException('Нужно создать файл с api-ключём')

        with open('api_key.txt', 'r') as f:
            self.key = f.readline().strip()

        self.header = {'api-key': self.key}

    def errors(self):
        if not self.status_code == 200:
            if self.status_code == 400:
                raise ConnectionError('Неверный запрос!')
            elif self.status_code == 401:
                raise ConnectionError('Требуется авторизация!')
            elif self.status_code == 403:
                raise ConnectionError('Запрещённый запрос!')
            elif self.status_code == 404:
                raise ConnectionError('Ресурс не найден!')
            elif self.status_code == 422:
                raise ConnectionError('Параметр отсутствует или его значение пустое!')
            elif self.status_code == 429:
                raise ConnectionError('Превышен лимит запросов, попробуйте ещё раз через 30 сек.!')
            else:
                raise ConnectionError('Что-то пошло не так!')


class Articles(Checker):

    @staticmethod
    def published(per_page=10, page=1):
        r = requests.get(f'https://dev.to/api/articles?per_page={per_page}&page={page}')
        Checker.errors(r)
        pprint(r.json())
        return r

    def user(self, per_page=5, page=1):
        r = requests.get(f'https://dev.to/api/articles/me?per_page={per_page}&page={page}', headers=self.header)
        Checker.errors(r)
        pprint(r.json())
        return r

    def user_pub(self, per_page=5, page=1):
        r = requests.get(f'https://dev.to/api/articles/me/published?per_page={per_page}&page={page}', headers=self.header)
        Checker.errors(r)
        pprint(r.json())
        return r

    def user_unpub(self, per_page=5, page=1):
        r = requests.get(f'https://dev.to/api/articles/me/unpublished?per_page={per_page}&page={page}', headers=self.header)
        Checker.errors(r)
        pprint(r.json())
        return r

    def user_all(self, per_page=5, page=1):
        r = requests.get(f'https://dev.to/api/articles/me/all?per_page={per_page}&page={page}', headers=self.header)
        Checker.errors(r)
        pprint(r.json())
        return r

    @staticmethod
    def sorted(per_page=10, page=1):
        r = requests.get(f'https://dev.to/api/articles/latest?per_page={per_page}&page={page}')
        Checker.errors(r)
        pprint(r.json())
        return r

    @staticmethod
    def userid(userid):
        r = requests.get(f'https://dev.to/api/articles/{userid}')
        Checker.errors(r)
        pprint(r.json())
        return r

    @staticmethod
    def path(username='devteam', slug='for-empowering-community-2k6h'):
        r = requests.get(f'https://dev.to/api/articles/{username}/{slug}')
        Checker.errors(r)
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
        Checker.errors(r)
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
        Checker.errors(r)
        print('Статья обновлена!')
        return r


class Tags(Checker):

    @staticmethod
    def tags(per_page=10, page=1):
        r = requests.get(f'https://dev.to/api/tags?per_page={per_page}&page={page}')
        Checker.errors(r)
        pprint(r.json())
        return r

    def followed(self):
        r = requests.get(f'https://dev.to/api/follows/tags', headers=self.header)
        Checker.errors(r)
        pprint(r.json())
        return r


class Content(Checker):

    @staticmethod
    def images(username):
        r = requests.get(f'https://dev.to/api/profile_images/{username}')
        Checker.errors(r)
        pprint(r.json())
        return r

    @staticmethod
    def videos(per_page=10, page=1):
        r = requests.get(f'https://dev.to/api/videos?per_page={per_page}&page={page}')
        Checker.errors(r)
        pprint(r.json())
        return r


class Save(Articles, Content):

    def _check_dir(self):
        for i in self._check_dir:
            if not os.path.exists(i):
                os.mkdir(i)

    def articles(self):
        Save._check_dir(self)
        r = Articles.user_all(self)
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
        Save._check_dir(self)
        r = Content.images(username)
        pic1 = requests.get((r.json()['profile_image']))
        pic2 = requests.get((r.json()['profile_image_90']))
        with open('photos/picture1.jpg', 'wb') as file:
            file.write(pic1.content)
            print('Данные сохранены')
        with open('photos/picture2.jpg', 'wb') as file:
            file.write(pic2.content)
            print('Данные сохранены')

    def video(self):
        Save._check_dir(self)
        r = Content.videos(1)
        head = {"Referer": (r.json()[0]['video_source_url'])}
        vid = requests.get((r.json()[0]['video_source_url']), headers=head)
        with open('videos/video', 'wb') as file:
            file.write(vid.content)
            print('Данные сохранены')