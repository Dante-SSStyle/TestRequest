from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import tags_router, save_router, articles_router


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
    allow_methods=['GET', 'POST', 'PUT'],
    allow_headers=["*"]
)

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
    save_router,
    prefix='/save',
    tags=['save'],
    dependencies=[]
)
