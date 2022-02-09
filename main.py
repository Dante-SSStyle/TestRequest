from api import Articles, Tags, Content, Save

art = Articles()
tag = Tags()
save = Save()
cont = Content()

#  Методы статей:
# Получает список всех статей
# art.published(1)

# Создаёт статью
# art.create('Hello There Again!', 'Hello World 2', '', '')

# Изменяет созданную статью
# art.update(980916)

# Вывод своих неопубликованных статей
# art.user_unpub()

# Вывод всех своих статей
# art.user_all()

#   Методы тегов:
# Вывод своих фоллоу тегов
# tag.followed()

# Вывод всех возможных тегов
# tag.tags()

#   Методы фото и видео:
# Вывод информации об изображениях пользователя по юзернейму
# cont.images('diogoosorio')

# Вывод списка статей с видео
# cont.videos()

#   Методы сохранения:

# Сохраняет в отдельный файл список своих статей
# save.articles()

# Скачивает фотографии профиля по юзернейму
# save.photos('dantessstyle')

# Скачивает видео со статьи
# save.video()
