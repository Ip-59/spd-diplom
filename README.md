# Социальная сеть для обмена фотографиями (backend)

## Запуск проекта

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/Ip-59/spd-diplom.git
   cd spd-diplom/social_network
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```
   python3 -m venv venv
   source venv/bin/activate  # или venv\Scripts\activate на Windows
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Настройте параметры БД в `social_network/settings.py`.

5. Выполните миграции:
   ```
   python manage.py migrate
   ```

6. Создайте суперпользователя:
   ```
   python manage.py createsuperuser
   ```

7. Запустите сервер:
   ```
   python manage.py runserver
   ```

8. Для доступа к API: `http://localhost:8000/api/`
9. Для доступа к админ-панели: `http://localhost:8000/admin/`

---

### Загрузка нескольких изображений

- Для загрузки нескольких фото к одному посту используйте поле `new_images` (list of files) при POST/PUT/PATCH запроса к `/api/posts/`.
- Все изображения выдаются в поле `images`.

---

### Геолокация

- Можно указать либо название локации (`location_name`), либо координаты (`latitude`, `longitude`) при создании поста. 
- Если указано только название — координаты определяются автоматически.
- Если указаны только координаты — название локации подбирается автоматически.
- Для геокодирования используется сервис Nominatim (geopy).

---

## Примечания

- Для загрузки и отображения изображений настроены `MEDIA_URL` и `MEDIA_ROOT`.
- Авторизация через стандартные средства Django и DRF (токены).
- Для тестирования используйте Postman/Swagger или встроенный DRF браузер.
