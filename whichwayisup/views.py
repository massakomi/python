import hashlib

from django.shortcuts import render


def md5(str):
    m = hashlib.md5()
    m.update(str.encode('utf8'))
    return m.hexdigest()


def home(request):
    return render(request, 'home.html')