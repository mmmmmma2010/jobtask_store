from .common import *

DEBUG = True


INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]


SECRET_KEY = 'django-insecure-hs6j037urx6iav+7#10%-vu4l4f5@@-1_zo)oft4g7$vf2$jmp'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'store',
        'HOST': 'localhost',
        'USER': 'postgres',
        'PASSWORD': '123'
    }
}


EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}
