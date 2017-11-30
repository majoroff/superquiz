from .base import *


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pdbipk6sg#vjjl-=!dsy=14#ho3v$(n6_b==5dl=2q1)!6529='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']