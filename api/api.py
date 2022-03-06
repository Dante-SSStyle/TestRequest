import requests
import json
import os
from .exceptions import DevToException, TestRequestException


class AbstractModel:
    """ Базовый класс с проверокой данных"""

    _base_url = 'https://dev.to/api'

    def __init__(self):

        self._check_dirlist = ('articles/', 'photos/', 'videos/')
        self._available_request_path = ('articles/', 'photos/', 'videos/')

        # Проверяем наличие токена авторизации в файле
        if not os.path.exists('api/api_key.txt'):
            raise TestRequestException(400, 'Нужно создать файл с api-ключём')

        with open('api/api_key.txt', 'r') as f:
            self.key = f.readline().strip()

        self.header = {'api-key': self.key}

    def _files_dir_exist(self):
        for i in self._check_dirlist:
            if not os.path.exists(i):
                os.mkdir(i)

    def _pics_dir_exist(self, folder_name):
        if not os.path.exists(f'photos/{folder_name}'):
            os.mkdir(f'photos/{folder_name}')

    def _errors(self, r):
        code = r.status_code
        if not code == 200:
            return

        if code == 400:
            raise DevToException(400, 'Неверный запрос!')
        if code== 401:
            raise DevToException(401, 'Требуется авторизация!')
        if code == 403:
            raise DevToException(403, 'Запрещённый запрос!')
        if code == 404:
            raise DevToException(404, 'Ресурс не найден!')
        if code == 422:
            raise DevToException(422, 'Параметр отсутствует или его значение пустое!')
        if code == 429:
            raise DevToException(429, 'Превышен лимит запросов, попробуйте ещё раз через 30 сек.!')

        raise DevToException(400, 'Что-то пошло не так!')


class Articles(AbstractModel):
    """ Получеине статей"""

    def __init__(self):
        super().__init__()
        self._base_url = f'{self._base_url}/articles'

    def _make_get_request(self, path, per_page=None, page=None, need_header=True):

        get_params = dict()
        get_params['per_page'] = per_page if per_page else None
        get_params['page'] = page if page else None
        request_header = self.header if need_header else None

        request_url = f'{self._base_url}/{path}'
        r = requests.get(request_url, headers=request_header, params=get_params)
        return r

    def published(self, per_page=10, page=1):
        r = self._make_get_request(path='articles', per_page=per_page, page=page)
        self._errors(r)
        return r

    def user(self, per_page=5, page=1):
        r = self._make_get_request(path='me', per_page=per_page, page=page)
        self._errors(r)
        return r

    def user_pub(self, per_page=5, page=1):
        r = self._make_get_request(path='me/published', per_page=per_page, page=page)
        self._errors(r)
        return r

    def user_unpub(self, per_page=5, page=1):
        r = self._make_get_request(path='me/unpublished', per_page=per_page, page=page)
        self._errors(r)
        return r

    def user_all(self, per_page=5, page=1):
        r = self._make_get_request(path='me/all', per_page=per_page, page=page)
        self._errors(r)
        return r

    def sorted(self, per_page=10, page=1):
        r = self._make_get_request(path='articles/latest', per_page=per_page, page=page)
        self._errors(r)
        return r

    def user_id(self, userid):
        r = self._make_get_request(path=f'articles/{userid}', need_header=False)
        self._errors(r)
        return r

    def path(self, username='devteam', slug='for-empowering-community-2k6h'):
        r = self._make_get_request(path=f'articles/{username}/{slug}', need_header=False)
        self._errors(r)
        return r

    def create(self, body, title='unnamed', series='', tags='', pub=False):
        payload = {
            "article": {
                "title": title,
                "published": pub,
                "body_markdown": body,
                "tags": tags,
                "series": series}
        }
        r = requests.post(f'{self._base_url}/articles', json=payload, headers=self.header)
        self._errors(r)
        return r

    def update(self, userid, body='', title='', series='', tags='', pub=''):
        payload = {
            "article": {
                "title": title,
                "published": pub,
                "body_markdown": body,
                "tags": tags,
                "series": series}
        }
        r = requests.put(f'{self._base_url}/{userid}', json=payload, headers=self.header)
        self._errors(r)
        return r


class Tags(AbstractModel):
    """ Получение тегов"""

    def tags(self, per_page=10, page=1):
        r = requests.get(f'{self._base_url}/tags?per_page={per_page}&page={page}')
        self._errors(r)
        return r

    def followed(self):
        r = requests.get(f'{self._base_url}/follows/tags', headers=self.header)
        self._errors(r)
        return r


class Save(AbstractModel):
    """ Сохранение статей, изображений, видео"""

    def __init__(self):
        super().__init__()
        self._files_dir_exist()

    def articles(self):
        arti = Articles()
        r = arti.user_all()
        self._errors(r)

        json_out = []
        for i in r.json():
            form = {
                'title': (i['title']),
                'published': (i['published']),
                'tags': (i['tag_list']),
                'description': (i['description']),
                'url': (i['url'])
            }
            json_out.append(form)

        with open('articles/my_art.json', 'w') as file:
            json.dump(json_out, file, indent=2)

    def photos(self, username):
        self._pics_dir_exist(username)

        r = requests.get(f'{self._base_url}/profile_images/{username}')
        self._errors(r)

        full_size_pic = requests.get((r.json()['profile_image']))
        preview_pic = requests.get((r.json()['profile_image_90']))
        self._errors(full_size_pic)
        self._errors(preview_pic)

        with open(f'photos/{username}/full_size_photo.jpg', 'wb') as file:
            file.write(full_size_pic.content)
        with open(f'photos/{username}/preview_photo.jpg', 'wb') as file:
            file.write(preview_pic.content)

    def video(self, per_page=1, page=1):

        r = requests.get(f'{self._base_url}/videos?per_page={per_page}&page={page}')
        self._errors(r)

        self._errors(r)
        video_src = r.json()[0]['video_source_url']
        vid = requests.get(video_src, headers={'Referer': video_src})
        with open('videos/video', 'wb') as file:
            file.write(vid.content)
