from api import Save
from fastapi.responses import JSONResponse
from fastapi import APIRouter

router = APIRouter()


@router.get('/save_art', description='Сохранение статей')
def save_art():
    sv = Save()
    res = sv.articles()
    return JSONResponse('Статьи сохранены!')


@router.get('/save_vid', description='Сохранение видео')
def save_video():
    sv = Save()
    res = sv.video()
    return JSONResponse('Данные сохранены')


@router.get('/save_pic', description='Сохранение изображений')
def save_pics(username):
    sv = Save()
    res = sv.photos(username)
    return JSONResponse('Данные сохранены')
