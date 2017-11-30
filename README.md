Для работы локальной необходим файл quizz/settings/local.py содержащий следующие настройки:

```python
from .base import *

# Стандартные настройки Django
SECRET_KEY = 'keep-it-secret'
DEBUG = True
ALLOWED_HOSTS = ['']

STATIC_ROOT = ''
STATICFILES_DIRS = ''

EMAIL_BACKEND = ''
EMAIL_FILE_PATH = ''

# Нестандартные настройки

## Реквизиты доступа к API SMSC.RU 
SMSC_LOGIN = ''
SMSC_PASSWORD = ''

## Адреса почты для отправки заказов
EMAIL_FROM = ''
EMAIL_FOR_ORDERS = ''
```

Unit-тесты
```python
python manage.py test questions
```

Запуск на сервере