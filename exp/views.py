import time

from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .exp_init import *
import os

pager = Pager()

# кастомный фильтр для шаблонизатора
from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def tables(request):

    response = HttpResponse()

    context = {}

    page = 'table_list'
    data = getData('SELECT `name` FROM SQLITE_SCHEMA WHERE type="table"')
    context['tables'] = list(item[0] for item in data)

    context['page'] = page


    template = loader.get_template('tables.html')
    response.content = template.render(context, request)
    return response


def table_struct(request):

    response = HttpResponse()

    context = {}
    tables = {}

    if 'table' in request.GET and request.GET['table']:
        table = request.GET['table']
        context['data'], context['columns'] = getDataAssoc(f'PRAGMA table_info({table});')
        if len(context['data']):
            context['table_data'] = printSqlTable(f'SELECT * FROM {table}')
        context['table_title'] = tableTitle(title="Структура таблицы", countAll=10, tables=tables)

    template = loader.get_template('table_struct.html')
    response.content = template.render(context, request)
    return response



# вывод с контекстом
@csrf_exempt
def index(request):

    response = HttpResponse()
    context = getDefaultContext()

    if request.method == 'POST' and request.POST.get('search'):
        context['content'] = Search.process(request)

    # context['content'] = archiveFolders(includeArray=[], excludeArray=[])
    # context = Utils.index(request)
    # request.POST = request.POST.copy()
    # request.POST['showList'] = 1
    # context['content'] = removeDir(request, "testx")
    # context['content'] = copyFolder("polls", "polls-copy")
    # context['content'] = textarea(content="123")
    # context['content'] = addRow(['hellow', 2, 3], 'tr', '', {0: 'style="color:red"'})
    # context['content'] = generatePagesLinks(10, 0, 100, 20)
    # context['content'] = isUtf8Codepage("всем привет")
    # context['content'] = SESSION(request, "test", "xxx")
    # context['content'] = redirect(request, "/", 3)
    # context['content'] = url(request, 'id=5', 'id=10&mode=5')
    # context['content'] = getRequestParam(request, 'param')
    # context['content'] = translitx('всем впривет')
    # pager.msg('123')
    # pager.error('123')
    # elog(request, 'test', 4)
    # addLog('test')
    # print(getHistory('code'))
    # saveInHistory('code', 123)
    # context['content'] = getRoot(request)
    # context['content'] = findTempDir()
    # saveSqlHistory(request, "SELECT * FROM ")
    # context['content'] = sessionSqls()
    # context['content'] = printQMenu(tables)
    # context['content'] = printSessionTables()
    # context['content'] = getAppTitle()
    # context['content'] = getTmpinfo()
    # context['content'] = scandirex('.')
    # for item in context['content']:
    #     print(item['name'])


    context['phpcode'] = request.POST.get('phpcode')
    if context['phpcode']:
        context['phpcode'] = phpConverter(context['phpcode'])

    if 'content' in context and type(context['content']) == 'str' and context['content'].find("<") > -1:
        context['content'] = escape(context['content'])

    template = loader.get_template('main.html')
    response.content = template.render(context, request)
    return response


def phpConverter(phpcode):
    phpcode = phpcode.replace('function ', 'def ')
    phpcode = re.sub('if\s*\((.*?)\)', 'if \g<1>', phpcode)
    phpcode = phpcode.replace('if !', 'if not ')
    phpcode = phpcode.replace('.=', '+=')
    phpcode = phpcode.replace('.\'', "+'")
    phpcode = phpcode.replace('\'.', "'+")
    phpcode = re.sub('[$};]', '', phpcode)
    phpcode = re.sub('else\s*if', 'elif', phpcode)
    phpcode = re.sub('\s*{', ':', phpcode)
    return phpcode


