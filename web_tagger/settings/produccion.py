
from base import *

print("Running Produccion Conf")



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'taggersys',
        'USER': 'crojas',
        'PASSWORD': '123qweasd',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

