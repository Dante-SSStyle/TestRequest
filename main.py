from api.api import Articles, Tags, Content, Save

heh = Articles()
hehe = Tags()

#  Методы статей:
# Получает список всех статей
# Articles.published(1)

# Создаёт статью
# Articles.create('heh', 'Hello There Again!', 'Hello World 2', '', '')

# Изменяет созданную статью
# Articles.update(heh, 980916)

# Вывод своих неопубликованных статей
# Articles.user_unpub(heh)

# Вывод всех своих статей
# Articles.user_all(heh)

#   Методы тегов:
# Вывод своих фоллоу тегов
# Tags.followed(hehe)

# Вывод всех возможных тегов
# Tags.tags()

#   Методы фото и видео:
# Вывод информации об изображениях пользователя по юзернейму
# Content.images('diogoosorio')

# Вывод списка статей с видео
# Content.videos()

#   Методы сохранения:

# Сохраняет в отдельный файл список своих статей
# Save.articles(heh)

# Скачивает фотографии профиля по юзернейму
# Save.photos(heh, 'dantessstyle')

# Скачивает видео со статьи
# Save.video(heh)
