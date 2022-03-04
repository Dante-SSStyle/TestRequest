from api import Articles, Tags, Content, Save
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# todo проверить user_id - int or str
# todo поправить наименования методов

app = FastAPI(
    title='Dev.to wrapper',
    description='Получение данных с сайта dev.to',
    version='0.5.0',
    doc_url='/docs',
    redoc_url='/doc'
)

# Добавление поддержки политик CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['GET', 'POST', 'DELETE'],
    allow_headers=["*"]
)

tags_router = APIRouter()
articles_router = APIRouter()

app.include_router(
    tags_router,
    prefix='tag',
    tags=['tag'],
    dependencies=[]
)

app.include_router(
    articles_router,
    prefix='/articles',
    tags=['articles'],
    dependencies=[]
)


@articles_router.get('mine_articles/published')
def m_published():
    art = Articles()
    res = art.user_pub()
    return JSONResponse(res)


@articles_router.get('mine_articles/unpublished')
def m_unpublished():
    art = Articles()
    res = art.user_unpub()
    return JSONResponse(res)


@articles_router.get('all_articles/latest')
def all_articles():
    art = Articles()
    res = art.sorted()
    return JSONResponse(res)


@articles_router.get('all_articles/by_user')
def all_articles(user_id: int):
    art = Articles()
    res = art.userid(user_id)
    return JSONResponse(res)


@articles_router.post('/create')
def post_article(text: str, title: str = None, series: str = None, tags: str = None, publish: bool = None):
    art = Articles()
    res = art.create(text, title, series, tags, publish)
    return JSONResponse("Статья успешно создана!")


@articles_router.post('/update')
def update_article(user_id: int, text: str, title: str = None, series: str = None, tags: str = None,
                   publish: bool = None):
    art = Articles()
    res = art.update(user_id, text, title, series, tags, publish)
    return JSONResponse("Статья обновлена!")


@tags_router.get('/all_tags', description='Все теги')
def get_all_tags():
    tg = Tags()
    res = tg.tags()
    return JSONResponse(res)


@tags_router.get('/mine_tags', description='Теги, на которые подписаны')
def get_mine_tags():
    tg = Tags()
    res = tg.followed()
    return JSONResponse(res)
