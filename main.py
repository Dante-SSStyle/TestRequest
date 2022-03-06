from api import Articles, Tags, Content, Save
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


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
content_router = APIRouter()
save_router = APIRouter()

app.include_router(
    tags_router,
    prefix='/tag',
    tags=['tag'],
    dependencies=[]
)

app.include_router(
    articles_router,
    prefix='/articles',
    tags=['articles'],
    dependencies=[]
)

app.include_router(
    content_router,
    prefix='/content',
    tags=['contents'],
    dependencies=[]
)

app.include_router(
    save_router,
    prefix='/save',
    tags=['save'],
    dependencies=[]
)


@articles_router.get('mine_articles/published', description='Опубликованные статьи')
def m_published():
    art = Articles()
    res = art.user_pub()
    return JSONResponse(res)


@articles_router.get('mine_articles/unpublished', description='Неопубликованные статьи')
def m_unpublished():
    art = Articles()
    res = art.user_unpub()
    return JSONResponse(res)


@articles_router.get('all_articles/latest', description='Статьи, сортированные по дате создания')
def all_articles():
    art = Articles()
    res = art.sorted()
    return JSONResponse(res)


@articles_router.get('all_articles/by_id', description='Статья по id')
def article_id(user_id: int):
    art = Articles()
    res = art.userid(user_id)
    return JSONResponse(res)


@articles_router.post('/create', description='Создание статьи')
def post_article(text: str, title: str = None, series: str = None, tags: str = None, publish: bool = None):
    art = Articles()
    res = art.create(text, title, series, tags, publish)
    return JSONResponse("Статья успешно создана!")


@articles_router.post('/update', description='Обновление статьи')
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


@content_router.get('/images', description='Изображения пользователя')
def get_user_images(username: str):
    cnt = Content()
    res = cnt.images(username)
    return JSONResponse(res)


@content_router.get('/videos', description='Cписок видео')
def get_videos():
    cnt = Content()
    res = cnt.videos()
    return JSONResponse(res)


@save_router.get('/save_art', description='Сохранение статей')
def save_art():
    sv = Save()
    res = sv.articles()
    return JSONResponse('Статьи сохранены!')


@save_router.get('/save_vid', description='Сохранение видео')
def save_video():
    sv = Save()
    res = sv.video()
    return JSONResponse('Данные сохранены')


@save_router.get('/save_pic', description='Сохранение изображений')
def save_pics(username):
    sv = Save()
    res = sv.photos(username)
    return JSONResponse('Данные сохранены')
