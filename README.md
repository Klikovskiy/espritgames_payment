### Тестовое задание для **_Espritgames.ru_**

Нужно реализовать сервис на Django, реализующий функции кошелька для пользователей.
То есть для каждого пользователя свой кошелек.


- Должна быть возможность проверить баланс через API и через веб страничку
- Реализовать API ручки списания, пополнения и возврата (Если считаешь нужным добавить ещё какие-то методы - можешь добавить)
- В Django Admin добавить возможность посмотреть хранящиеся в бд данные

В качестве базы можешь использовать SQLite для простоты
Проект нужно разместить на git




### Как запускать проект:

1. Создать файл конфигурации config.env в директории backend:

    #### Пример файла конфигурации:
    ```
    DJANGO_SECRET_KEY=''
    DATABASE_NAME=''
    DATABASE_USER=''
    DATABASE_PASSWORD=''
    DATABASE_HOST=''
    DATABASE_HOST='localhost'
    DATABASE_PORT='5432'
    DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'
    DEBUG=1
    ```


### Для локальных тестов можно использовать Docker:
1. Переходим в папку `cd deploy/docker/`
2. Собираем: `docker-compose -f docker-compose.yml build`
3. Запускаем: `docker-compose -f docker-compose.yml up -d`
4. Подключаемся к контейнеру Django: `docker exec -it <container_id_or_name> /bin/bash`
5. Запускаем процедуру создания супер пользователя `python backend/manage.py createsuperuser`

После запуска, проект доступен по адресам:

* http://localhost/ - Основной домен.
* http://localhost/api/wallet/redoc/ - Документация API Redoc.
* http://localhost/api/wallet/swagger/ - Документация API Swagger.


Для работы с API, потребуется токен. JWT токен можно получить и обновить через соответствующий метод, который
описан в документации по ссылкам выше. Или, использовать обычный Token, который можно создавать через панель администратора.

* Использование JWT токена: Header Authorization: <токен>
* Использование Token токена: Header Token: <токен>