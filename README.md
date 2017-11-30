Для работы локальной необходим файл src/quizz/settings/local.py содержащий следующие настройки:

```python
from .base import *

# Стандартные настройки Django
SECRET_KEY = 'keep-it-secret'
DEBUG = True
ALLOWED_HOSTS = ['']

STATIC_ROOT = ''
STATICFILES_DIRS = ''

```

Unit-тесты
```
python manage.py test questions
```

Запуск на сервере
```
docker-compose up -d
```