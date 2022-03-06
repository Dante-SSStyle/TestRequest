from api import Articles
from fastapi.responses import JSONResponse
from fastapi import APIRouter

router = APIRouter()


@router.get('mine_articles/published', description='Опубликованные статьи')
def m_published():
    art = Articles()
    res = art.user_pub()
    return JSONResponse(res)


@router.get('mine_articles/unpublished', description='Неопубликованные статьи')
def m_unpublished():
    art = Articles()
    res = art.user_unpub()
    return JSONResponse(res)


@router.get('all_articles/latest', description='Статьи, сортированные по дате создания')
def all_articles():
    art = Articles()
    res = art.sorted()
    return JSONResponse(res)


@router.get('all_articles/by_id', description='Статья пользователя по id')
def article_id(user_id: int):
    art = Articles()
    res = art.user_id(user_id)
    return JSONResponse(res)


@router.post('/create', description='Создание статьи')
def post_article(text: str, title: str = None, series: str = None, tags: str = None, publish: bool = None):
    art = Articles()
    res = art.create(text, title, series, tags, publish)
    return JSONResponse("Статья успешно создана!")


@router.post('/update', description='Обновление статьи')
def update_article(user_id: int, text: str, title: str = None, series: str = None, tags: str = None,
                   publish: bool = None):
    art = Articles()
    res = art.update(user_id, text, title, series, tags, publish)
    return JSONResponse("Статья обновлена!")
