
from .models import *


def getDefaultContext():
    global EXP
    request = get_request()
    tables = getAllTables()
    context = {
        'EXP': EXP,
        'MS_APP_VERSION': MS_APP_VERSION,
        'password_symbols': '!_@#$%^&*',
        'database': 'database',
        'PHP_SELF': request.META.get('PHP_SELF'),
        'getAppTitle': getAppTitle(),
        'getTmpInfo': getTmpInfo(),
        'sessionSqls': sessionSqls(),
        'printQMenu': printQMenu(tables),
    }
    return context