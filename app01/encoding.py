from django.conf import settings
import hashlib

def md5(data):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data.encode('utf-8'))
    return obj.hexdigest()