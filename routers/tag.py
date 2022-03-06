from api import Tags
from fastapi.responses import JSONResponse
from fastapi import APIRouter

router = APIRouter()


@router.get('/all_tags', description='Все теги')
def get_all_tags():
    tg = Tags()
    res = tg.tags()
    return JSONResponse(res)


@router.get('/mine_tags', description='Теги, на которые подписаны')
def get_mine_tags():
    tg = Tags()
    res = tg.followed()
    return JSONResponse(res)
