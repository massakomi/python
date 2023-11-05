from django.db import models
from django.http import HttpRequest, HttpResponse
import re
import os

from django_middleware_global_request.middleware import get_request

# defines должны быть тут, в последнем файле цепочки, иначе не видно ошибка
TMP_DIR = '.'
MS_APP_VERSION = '1.37'
EXP = '' # todo $a = parse_url($_SERVER['REQUEST_URI']);  = substr($a['path'], 1);

class Pager:
    messages = []
    errors = []

    def add_message(self, message, error='', sql=''):
        self.messages.append([message, error, sql])

    def msg(self, text, error='', sql=''):
        self.messages.append([message, error, sql])

    def add_error(self, message):
        self.errors.append(message)

    def error(self, message):
        self.errors.append(message)

    @staticmethod
    def print_menus():
        if Bitrix.has():
            return '<a href="?action=bitrix">Bitrix</a>'

    @staticmethod
    def on_start(action):
        Bitrix.on_start(action)
        Utils.on_start(action)

    @staticmethod
    def actions_exec(class_name, page='', action=''):
        if action != class_name.lower():
            pass
        if not page:
            page = 'index'
        utils = eval(class_name)()
        try:
            output = getattr(utils, page)()
            Utils.output += output
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            raise ValueError('Метод "' +page+ '" не существует')
        pass

    def actions(self):
        self.actions_exec('Bitrix')
        self.actions_exec('Utils')

    @staticmethod
    def print_sub_menu(menu):
        s = """<hr>
            <ul class="nav nav-pills small">
            """

class Exporter:
    db, table, data = '', '', ''
    tableStructure = []
    comments = True
    fields = []


class Bitrix:

    @staticmethod
    def on_start():
        return False

    @staticmethod
    def has():
        return False

    def test(self):
        print('456789')


class Utils:

    output = ''

    @staticmethod
    def has():
        return False

    @staticmethod
    def on_start(action):
        if action != 'utils':
            return

    @staticmethod
    def index(request):
        content = ''
        if 'extract-links' in request.POST:
            matches = re.findall(r'href\s*=\s*["\'](https?://[^"\']+)["\']', request.POST['content'], re.I)
            content += '<br />'.join(matches)

        if 'generate' in request.POST:
            Utils.generate()

        content += """
            <h2>Генерация тегов</h2>
            <style type="text/css">
                .big-inputs input {min-width: 100px;}
            </style>
            <form method="post">
                <input type="hidden" name="generate" value="1">
                <textarea name="content" id="generateTxt" class="form-control mb-3" style="height: 200px; width:100%"></textarea>
                <div class="big-inputs">
                <input type="submit" name="ul-gen" value="ul" class="btn btn-success" />
                <input type="submit" name="ol-gen" value="ol" class="btn btn-success" />
                <input type="submit" name="p-gen" value="p" class="btn btn-warning"  />
                <input type="submit" name="ph2-gen" value="h2+p" class="btn btn-warning" />
                <input type="submit" name="td" value="td" class="btn btn-danger"/>
                <input type="submit" name="spec" value="spec" class="btn btn-primary" />
                <input type="submit" name="full" value="full" class="btn btn-primary" />
                <input type="submit" name="table" value="table" class="btn btn-primary" />
                <input type="submit" name="extract-links" value="extract-links" class="btn btn-primary" title="Извлечь ссылки из текста" />
                </div>
            </form>
            """

        return {'content': content}

    @staticmethod
    def splitAndClear(rx, content, **opts):
        lines = re.split(rx, content, re.U)
        lines = list(filter(lambda x: x.strip() != '', lines))
        lines = list(map(lambda x: x.strip(), lines))
        if 's' in opts:
            lines = list(map(lambda x: re.sub(r'\s', ' ', x), lines))
        return lines

    @staticmethod
    def tagImplode(lines, tag, tab=''):
        inner = f'</{tag}>\n{tab}<tag>'.join(lines)
        return f'{tab}<{tag}>' + inner + f'</tag>'

    @staticmethod
    def generate():
        # todo реализоавть много кода (функция по преобразованию текста в списки), но мне этот Utils уже так надоел
        # но в плане тренировки это можно написать (200 строк)
        pass


import zipfile

class Zip:

    @staticmethod
    def zipError():
        return 'No error'

    @staticmethod
    def addFiles(files, excludePathArray):
        # todo нудно
        pass

    @staticmethod
    def addFilesDir(dir, baseDir):
        # todo нудно
        pass

    @staticmethod
    def createFile(file, saveTo):
        if os.path.exists(saveTo):
            os.remove(saveTo)
        try:
            with zipfile.ZipFile(saveTo, "w", zipfile.ZIP_DEFLATED) as z:
                z.write(file)
        except Exception as ex:
            print('Ошибка выполнения Zip.createFile ('+type(ex).__name__+') ' + ex.args[1])

    @staticmethod
    def create(file, saveTo, content):
        if os.path.exists(saveTo):
            os.remove(saveTo)
        try:
            with zipfile.ZipFile(saveTo, "w", zipfile.ZIP_DEFLATED) as z:
                z.writestr(file, content)
        except Exception as ex:
            print('Ошибка выполнения Zip.create ('+type(ex).__name__+') ' + ex.args[1])

    @staticmethod
    def unpack(file, folder):
        removeArchivedFiles = []
        try:
            with zipfile.ZipFile(file, "r") as z:
                removeArchivedFiles = z.namelist()
                z.extractall(folder)
        except FileNotFoundError as ex:
            addLog('Не найден файл архива / ' + ex.args[1])
        except Exception as ex:
            print('Ошибка выполнения Zip.unpack ('+type(ex).__name__+') ' + ex.args[1])
        return removeArchivedFiles

    @staticmethod
    def readFiles(file):
        files = []
        with zipfile.ZipFile(file) as z:
            for filename in z.namelist():
                files.append(filename)
        return files



def archiveFolders(includeArray, excludeArray):
    files = []
    for v in listdir('.'):
        if len(includeArray):
            if v not in includeArray:
                continue
        else:
            if len(excludeArray) and v in excludeArray:
                continue
        files.append(v)
    return files

def archiveFile(folder, delete=True):
    file = folder + '/all.zip'
    if os.path.exists(file) and delete:
        os.remove(file)
    return file



from django.db import connection

def getData(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    return rows

def getOne(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        rows = dict(zip(columns, cursor.fetchone()))
    return rows

def getDataAssoc(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        rows = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return rows, columns

def query(sql):
    with connection.cursor() as cursor:
        result = False
        try:
            result = cursor.execute(sql)
            s = sql.strip().lower()[0:6]
            if s == 'insert':
                result = cursor.lastrowid
            elif s == 'update' or s == 'delete':
                result = cursor.rowcount
        except Exception as ex:
            print(repr(ex) + f' (SQL: {sql})')
    return result

"""
from datetime import datetime
mysqlInsert('polls_question',
    {
        'id': '3',
        'question_text': 'anybody',
        'pub_date': str(datetime.now())
    }, type='INSERT')
"""
def mysqlInsert(table, data, type='INSERT', fields=[]):
    values = []
    for fieldName, value in data.items():
        #if isinstance(value, int) is False and isinstance(value, str) is False:
        #    continue
        if (value == '' or value is None) and fields and fields[fieldName]['notnull'] == 0:
            value = 'Null'
        elif isinstance(value, str):
            value = '"'+value+'"'
        values.append(value)
    sql = type + ' INTO `' + table + '` (`' + "`, `".join(data.keys()) + '`) VALUES (' + ", ".join(values) + ')'
    return query(sql)

"""
from datetime import datetime
mysqlUpdate('polls_question',
    {
        'pub_date': str(datetime.now())
    }, where='id=4')
"""
def mysqlUpdate(table, data, where='', fields=[]):
    values = []
    for fieldName, value in data.items():
        #if isinstance(value, int) is False and isinstance(value, str) is False:
        #    continue
        if (value == '' or value is None) and fields and fields[fieldName]['notnull'] == 0:
            value = 'Null'
        elif isinstance(value, str):
            value = '"'+value+'"'
        values.append(f'`{fieldName}`={value}')
    sql = 'UPDATE `' + table + '` SET ' + ", ".join(values) + ' WHERE ' + where
    return query(sql)

def serverVersion():
    pass

def execSql(content, type, max_query, exitOnError=False):
    pass

def getFields(table, onlyNames=False, what='FIELDS'):
    if not table:
        return []
    with connection.cursor() as cursor:
        cursor.execute(f'PRAGMA table_info({table});')
        # name = $what == 'FIELDS' ? $row->Field : $row->Key_name;  ?? это нужно для выборки ключей
        if onlyNames:
            data = [row[1] for row in cursor.fetchall()]
        else:
            # список колонок (cid, name, type, notnull, dflt_value, pk)
            columns = [col[0] for col in cursor.description]
            data = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            # список полей этой таблицы, и далее в data меняем числовые ключи на ключи-поля
            fields = [col['name'] for col in data]
            data = dict(zip(fields, data))
    return data

def getKeys(table, onlyNames=False):
    return getFields(table, onlyNames, 'KEYS')

def fieldKeys(table, field):
    data = []
    keys = getKeys(table)
    for v in keys:
        """
        if ($v->Column_name == $field) {
            if ($v->Key_name == 'PRIMARY') {
                $fieldKeys []= 'primary';
            } elseif ($v->Non_unique) {
                $fieldKeys []= 'index';
            } else {
                $fieldKeys []= 'unique';
            }
        }
        """
        pass
    return data

def getAllTables():

    tables, columns = getDataAssoc('SELECT * FROM sqlite_schema WHERE type="table"')
    tablesAll = {}
    for key, table in enumerate(tables):
        del table['sql']
        tablesAll [table['name']] = table


    #  $mysqli->query('SHOW TABLE STATUS');
    #         $tables = array();
    #         if ($result) {
    #             while ($row = $result->fetch_object()) {
    #                 $tables [$row->Name]= $row;
    return tablesAll

def getTableExport():
    pass

from django.utils.html import strip_tags, escape

def printSqlTable(sql, data=''):
    if not data:
        data, columns = getDataAssoc(sql)
    if len(data) == 0:
        addLog(f'No data in {sql}')
        return False
    content = '<table class="optionstable">'
    printHeaders = False
    max = 250
    for row in data:
        if printHeaders == False:
            printHeaders = True
            content += '<tr>'
            for key, value in row.items():
                content += '<td>{0}</td>'.format(key)
            content += '</tr>'
        tr = '<tr>'
        for key, value in row.items():
            value = strip_tags(value)
            value = escape(value)
            if len(value) > max:
                more = f'<span style="display:none;">{value[max:]}</span>'
                value = value[0:max] + ' <a href="#" class="nsh">еще</a>' + more
            if value.find('http') == 0:
                value = f'<a href="{value}" target="_blank">{value}</a>'
            tr += '<td>{0}</td>'.format(value)
        tr += '</tr>'
        content += tr
    content += '</table>'
    return content

def fieldsSearchWhere(fields, filter, onlyField=False):
    """
    fields = getFields('polls_question')
    where = fieldsSearchWhere(fields, filter='test')
    """
    if not filter:
        pass
    isRus = re.match('[а-я]', filter, re.U)
    isNum = filter.isnumeric()
    where = []
    for fieldName, field in fields.items():
        # список колонок (cid, name, type, notnull, dflt_value, pk)
        if onlyField and field['name'] != onlyField:
            continue
        isInt = field['type'].find('int') != -1
        isDate = field['type'].find('int') != -1
        # Для поиска на русском языке, исключаем даты
        if isRus and (isDate or isInt):
            continue
        if isInt and isNum:
            where.append('`'+field['name']+'`="'+filter+'"')
        else:
            where.append('`'+field['name']+'` LIKE "%'+filter+'%"')
    return where

def ch(key, array={}):
    if array and key in array and array[key]:
        return 'checked'
    else:
        return ''

def fieldForm(request, defaults={}, fields={}, key=''):
    defaults = {'name': '', 'length': '', 'default': ''} | defaults
    columnTypes = [
        'Тип', 'VARCHAR', 'TINYINT', 'TEXT', 'DATE',
        'SMALLINT', 'MEDIUMINT', 'INT', 'BIGINT',
        'FLOAT', 'DOUBLE', 'DECIMAL',
        'DATETIME', 'TIMESTAMP', 'TIME', 'YEAR',
        'CHAR', 'TINYBLOB', 'TINYTEXT', 'BLOB', 'MEDIUMBLOB', 'MEDIUMTEXT', 'LONGBLOB', 'LONGTEXT',
        'ENUM', 'SET', 'BOOLEAN', 'SERIAL'
    ]
    tmode = ''
    if hasattr(request, 'GET') and 'tmode' in request.GET:
        tmode = request.GET['tmode']
    a = f'[{key}]' if tmode == 'createTable' else ''

    options = ''
    for v, k in enumerate(columnTypes):
        add = ''
        if 'type' in defaults and defaults['type'] == v:
            add = 'selected'
        if k == 0:
            add += ' value=""'
        options += f'<option{add}>{v}</option>'

    if tmode == 'createTable':
        chbx = {
            'null': 'NULL',
            'ai': 'autoincrement',
            'pk': 'pk',
            'unique': 'unique',
            'index': 'index'
        }
    else:
        chbx = {
            'null': 'NULL',
            'ai': 'autoincrement'
        }
    chbxString = ''
    for k, v in chbx.items():
        chc = ch(k, defaults)
        chbxString += f"""
        <input type="hidden" name="{k}{a}" value="">
        <div class="form-check form-check-inline">
              <label class="form-check-label"><input class="form-check-input" type="checkbox" {chc} name="{k}{a}" value="1">
              {v}
            </label>
        </div>
        """

    output = f"""
        <div class="row mb-2">
            <div class="col-sm-3">
              <input type="text" name="name{a}" placeholder="Поле" value="{defaults['name']}" class="form-control form-control-sm" />
            </div>
            <div class="col-sm-3">
              <select name="type{a}" class="form-select form-select-sm">{options}</select>
            </div>
            <div class="col-sm-3">
              <input type="text" name="length{a}" placeholder="Длина / значения" value="{defaults['length']}"
                class="form-control form-control-sm" />
            </div>
            <div class="col-sm-3">
              <input type="text" name="default{a}" placeholder="По умолчанию" value="{defaults['default']}"
                class="form-control form-control-sm" />
            </div>
        </div>        
        
        <div class="row mb-2">
            <div class="col-sm-12 small" style="text-align: right; ">
            {chbxString}
            </div>
        </div>
        """

    if hasattr(request, 'GET') and 'table' in request.GET:
        options = ''
        for v in fields:
            add = ''
            if defaults['after'] == v['name']: # фз name или field
                add = ' selected'
            options += f'<option{add}>{v["name"]}</option>'
        output += f"""
            <div class="row mb-2">
                <label class="col-sm-2 col-form-label">After</label>
                <div class="col-sm-10">
                  <select class="form-select form-select-sm" name="after{a}">
                    <option value=""></option>
                    {options}
                  </select>
                </div>
            </div>
            """

    return output


def getFieldDefinition(fieldType=None, null=None, default=None, extra=None, length=None):
    if type(fieldType) == 'dict':

        null = fieldType['Null']
        default = fieldType['Default']
        extra = fieldType['Extra']
        length = fieldType['Length']
        fieldType = fieldType['Type']

        # start
        if fieldType.find('UNSIGNED'):
            extra += ' UNSIGNED'
            fieldType = re.sub('UNSIGNED', '', fieldType, re.I)

    # TODO дальше...
    fieldType = fieldType.upper()
    if fieldType == 'SERIAL':
        return fieldType
    field_info = fieldType
    return field_info


def getFieldDefinitionByData(data):
    extra = ('AUTO_INCREMENT' if data['ai'] else '')
    dd = getFieldDefinition(data['type'], 'YES' if data['null'] else 'NO', data['default'], extra, data['length'])
    return f' `{data["name"]}` {dd}'


def processEdit(fields):
    # TODO тут дохрена
    pass

def getField(name, title, type, req, values):
    # Возвращает наиболее подходящий код инпут-формы для редактирования параметра
    html = ''
    # TODO тут дохрена
    return html


def processAddField(fields):
    # TODO тут дохрена
    pass


class Search:

    onlyExtensionList = ['php', 'js', 'css', 'log', 'html', 'htm', 'tpl', 'txt', 'xml']

    @staticmethod
    def process(request):
        if request.method != 'POST':
            raise NameError('I need POST method!')
            pass
        # if not request.POST.get('search'):
        #     raise NameError('search is empty')
        #     pass

        filter = request.POST.get('search') or ''
        if filter is not None:
            filter = filter.strip()

        searchBy = 'по базе'
        t = f'запросу "{filter}"'
        if 'fileSearch' in request.POST:
            searchBy = 'по файлам'
        if 'fieldSearch' in request.POST:
            searchBy = 'по полям'

        output = f'<h2>Результаты поиска {searchBy} по {t}:</h2>'
        countFounded = 0
        if request.POST.get('fileSearch') or request.POST.get('find_changed'):
            onlyExtensions = False
            if request.POST.get('regexp') or request.POST.get('html-only'):
                onlyExtensions = Search.onlyExtensionList
            options = {
                'maxLevel' :    request.POST.get('depth', 8),
                'maxFileSize':  1024 * 1024,
                'maxFiles':     request.POST.get('maxFiles', 10000),
                'onlyExtensions': onlyExtensions,
                'snipsize':     request.POST.get('snipsize', 20),
                'no-case':      request.POST.get('no-case') is not None,
            }
            if request.POST.get('find_date'):
                options['find_date'] = datetime.strptime(request.POST.get('find_date'), "%Y-%m-%d %H:%M:%S").timestamp()
            folders, skippedFolders = Search.getFolders(request)
            output += '<div><b>Поиск по папкам</b> ' + ', '.join(folders) + '</div>'
            if skippedFolders:
                output += '<div style="color:red"><b>Пропущены</b> папки ' + ', '.join(skippedFolders) + '</div>'
            output += f'<div>Глубина сканирования: {options["maxLevel"]}</div>'

            a = ','.join(onlyExtensions) if onlyExtensions else 'все'
            output += f'<div>Тип файлов: {a}</div>'
            output += f'<div>Макс размер файла: {formatSize(options["maxFileSize"])}</div>'
            output += f'<div>Макс кол-во файлов: {options["maxFiles"]}</div>'

            output += '<hr>'

            output += """
                <div class="row mb-3">
                    <div class="col-sm-3">
                        <input type="text" id="filter-search-include" onkeyup="Search.filterHtmlRows(this)" class="form-control form-control-sm" placeholder="фильтр строк" />
                    </div>
                    <div class="col-sm-3">
                        <input type="text" id="filter-search-exclude" onkeyup="Search.filterHtmlRows(this)" class="form-control form-control-sm" placeholder="исключить строки (var|or)" />
                    </div>
                    <div class="col-auto">
                        <select name="exts" class="form-select form-select-sm">
                            <option value="">ext</option>
                        </select>
                    </div>
                </div>
                <span id="deleteInfo"></span>"""

            # Непосредственно сам поиск и вывод результатов
            for v in folders:
                if not os.path.isdir(v):
                    continue
                cnt, scanned, stat, changed = Search.inFolder(dir=v, recursive=True, level=0, options=options)
                if cnt is False:
                    break
                countFounded += cnt

            zip = False
            if request.POST.get('changed_archive'):
                # TODO код архивации списка changed файлов
                pass

            output += f'<hr /><div>Просканировано файлов: {scanned}</div>'
            output += repr(stat)

        # поиск по базе или полям
        else:
            maxRows = 500000
            skipped = []
            # TODO дальше

        if countFounded == 0:
            output += '<div style="color:red">Ничего не найдено</div>';

        return output

    @classmethod
    def inFolder(cls, dir, recursive, level, options):
        founded = 0
        scanned = []
        stat = []
        changed = []
        # TODO inFolder дальше
        return founded, scanned, stat, changed

    @classmethod
    def getFolders(cls, request):
        if request.POST.get('folders') == '*' or request.POST.get('find_changed'):
            return scandirx('.')
        folders = request.POST.get('folders', request.COOKIES.get('folders', ''))
        if folders:
            folders = folders.split(',')
        if not folders:
            cms = ''
            if os.path.exists('configuration.php'):
                with open('configuration.php', "r") as file:
                    a = file.read()
                    if a.find('JConfig') != -1:
                        cms = 'joomla'
            if os.path.exists('bitrix'):
                cms = 'bitrix'
            if cms == 'joomla':
                folders = '.,administrator,components,modules,templates'.split(',')
            else:
                folders = ['.']
                for v in os.listdir('.'):
                    if os.path.isfile(v):
                        continue
                    if cms == 'bitrix':
                        if v == 'bitrix':
                            if os.path.exists('local'):
                                continue
                            v = 'bitrix/templates'
                            folders.append('bitrix/php_interface')
                        if v == 'upload':
                            continue
                    folders.append(v)
                folders.sort()

        if '.' not in folders:
            folders.append('.')

        allFolders = scandirx('.')
        skippedFolders = list(set(allFolders) - set(folders))

        return folders, skippedFolders

    # TODO целый механизм поиска
    pass


def echolog(txt):
    print(txt)
    with open(LOG_FILE, "a+") as f:
        f.write(txt)


def createTable(tableName, data):
    fields = []
    primary = unique = indexes = []
    for field, k in data:
        if field['pk']:
            primary.append(field['name'])
        if field['unique']:
            unique.append(field['name'])
        if field['index']:
            indexes.append(field['name'])
        fields.push(getFieldDefinitionByData(field))
    if primary:
        implode = '`,`'.join(primary)
        fields.append(f'PRIMARY KEY (`{implode}`)')
    if indexes:
        implode = '`,`'.join(indexes)
        fields.append(f'KEY (`{implode}`)')
    if unique:
        implode = '`,`'.join(unique)
        fields.append(f'UNIQUE (`{implode}`)')
    fields = '\n  '.join(fields)
    sql = f'CREATE TABLE `{tableName}` (\n  {fields}\n) ENGINE=MyISAM DEFAULT CHARSET=utf8;'
    with connection.cursor() as cursor:
        result = False
        try:
            result = cursor.execute(sql)
            msg = 'Запрос выполнен'
        except Exception as ex:
            msg = repr(ex) + f' (SQL: {sql})'
    return result, sql, msg


# Date Array функции block

def sortBy(data, field, dir='asc', mode='numeric'):
    """
    data = {
        'a': {
            'id': '11'
        },
        'b': {
            'id': '1'
        },
        'c': {
            'id': '2'
        }
    }
    field = 'id'
    data = sortBy(data, field, dir='asc', mode='numeric')
    print(repr(data))
    """
    data = sorted(
        data.items(),
        key=lambda x: int(x[1][field]) if mode == 'numeric' else x[1][field],
        reverse=(dir != 'asc')
    )
    return data


from datetime import datetime, time

def date2rusString(format, ldate):
    """
    Время форматирует в русское "Вчера-сегодня-позавчера и последние дни недели"
    ldate = datetime.timestamp(datetime.now()) - 86400*4
    ru = date2rusString('%Y-%m-%d %H:%M:%S', ldate)
    print(ru)
    """
    datetimeDate = datetime.date(datetime.today())
    datetimeTime = time(0, 0, 0)
    dt = datetime.combine(datetimeDate, datetimeTime)
    tmsTodayBegin = round(dt.timestamp())

    datetimeDateOld = datetime.fromtimestamp(ldate)
    datetimeTime = time(0, 0, 0)
    dt = datetime.combine(datetimeDateOld, datetimeTime)
    tmsBegin = round(dt.timestamp())

    params = ['Сегодня', 'Вчера', 'Позавчера']
    weekdays = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

    end = ', ' + datetimeDateOld.strftime("%H:%M")
    for i in range(0, 6):
        tms = tmsTodayBegin - 3600*24*i
        if tmsBegin == tms:
            if i < len(params):
                return params[i] + end
            else:
                weekday = datetime.isoweekday(datetimeDateOld)
                return weekdays[weekday] + end

    return datetimeDateOld.strftime(format)





# File url функции  block

def fileUploadError(code):
    code = str(code)
    codes = {
        '1': 'The uploaded file exceeds the upload_max_filesize directive in php.ini',
        '2': "The uploaded file exceeds the MAX_FILE_SIZE directive that was specified in the HTML form",
        '3': "The uploaded file was only partially uploaded",
        '4': "No file was uploaded",
        '6': "Missing a temporary folder",
        '7': "Failed to write file to disk",
        '8':  "File upload stopped by extension",
    }
    return codes[code] if code in codes else "Unknown upload error"

def fsave(file, content, mode='w'):
    try:
        with open(file, mode) as f:
            f.write(content)
    except:
        raise ValueError(f'Не могу записать файл {file}, нет прав')

import requests
def loadurl(url, opts={}):
    content = requests.get(
        url,
        timeout=15
    )
    for key, value in opts.items():
        requests[key] = value
    if not content:
        raise ValueError(f'Пустой контент при загрузке с урла {url}')
    return content

# Список папок (используется только для определения массива папок поиска) - возвращает пути и еще папку-точку
def scandirx(folder):
    folders = []
    for i in os.listdir(folder):
        path = os.path.join(folder, i) if folder != '.' else i
        if not os.path.isfile(path):
            folders.append(path)
    folders.sort()
    return folders

def dirSize(dir, recursive=False):
    countFiles = size = 0
    for v in os.listdir(dir):
        countFiles += 1
        path = dir + '/' + v
        if recursive and os.path.isdir(path):
            s, c = dirSize(path)
            size += s
            countFiles += c
        else:
            size += os.path.getsize(path)
    return size, countFiles

def formatSize(bytes):
    if bytes < pow(1024, 1):
        return f'{bytes} b'
    elif bytes < pow(1024, 2):
        return str(round(bytes / pow(1024, 1), 2)) + ' Kb'
    elif bytes < pow(1024, 3):
        return str(round(bytes / pow(1024, 2), 2)) + ' Mb'
    elif bytes < pow(1024, 4):
        return str(round(bytes / pow(1024, 3), 2)) + ' Gb'

def removeDir(request, dir):
    if request.method != 'POST' and request.POST.get('showFolder'):
        return '<br />Удалим папку ' + os.path.realpath(dir)
    if not os.path.exists(dir):
        return f'Folder doesnt exist {dir}'

    output = ['Удаляю папку ' + os.path.realpath(dir)]

    for v in os.listdir(dir):
        path = dir + '/' + v;
        if os.path.isdir(path):
            res = removeDir(request, path)
            output.append(res)
            continue
        if request.POST.get('showList'):
            output.append(f'Удалим {path}')
        else:
            os.remove(path)
    if not request.POST.get('noDeleteFirst') or dir != request.POST.get('folder'):
        if request.POST.get('showList'):
            output.append(f'Удалим папку {dir}')
        else:
            os.rmdir(dir)
    return '<br />'.join(output)


def extension(filename):
    return os.path.splitext(filename)[1][1:]

from shutil import copyfile
def copyFolder(folderFrom, folderTo, skip=[]):
    if not os.path.exists(folderTo):
        os.mkdir(folderTo, 750)
    for v in os.listdir(folderFrom):
        copyFromPath = f'{folderFrom}/{v}'
        copyToPath = f'{folderTo}/{v}'
        if os.path.exists(copyToPath):
            continue
        if v in skip:
            continue
        if os.path.isdir(copyFromPath):
            copyFolder(copyFromPath, copyToPath)
        else:
            copyfile(copyFromPath, copyToPath)
            print("copy", copyFromPath, copyToPath)
    pass



# HTML string block

def textarea(content):
    return f'<textarea style="height:500px;" class="autoselect form-control">{content}</textarea>'

import random
def generatePassword(length=8, caps=True):
    symb = 'abcdefghijklmnopqrstuvwzyz123456789'
    if caps:
        symb += 'ABCDEFGHIJKLMNOPQRSTUVWZYZ'
    strlen = len(symb)
    password = ''
    for i in range(length):
        password += symb[random.randint(0, strlen - 1)]
    return password

def addRow(data, t='td', st='', ats={}):
    str = f'\n<tr{st}>'
    for key, value in enumerate(data):
        add = ''
        if key in ats:
            add = ' ' + ats[key]
        str += f'\n    <{t}{add}>{value}</{t}>'
    str += f'\n</tr>'
    return str

import math
def generatePagesLinks(limit, start, countAll, floatlimit):
    pageLinks = '<ul class="pagination pagination-sm">'
    pageCount = math.ceil(countAll / limit)
    if pageCount == 1:
        return ''
    j = 0
    if start > floatlimit:
        href = url('start=0')
        pageLinks += f'<li class="page-item"><a class="page-link" href="{href}">1...</a></li>'
    for i in range(max(1, start - floatlimit), pageCount, 1):
        if j > floatlimit * 2:
            break
        st = ''
        if i - 1 == start:
            st = ' active'
        u = url('start=' + str(i - 1))
        pageLinks += f'<li class="page-item{st}"><a class="page-link" href="{u}">{i}</a></li> '
    if pageCount > floatlimit * 2:
        u = url('start=' + str(pageCount - 1))
        pageLinks += f'<li class="page-item"><a class="page-link" href="{u}">...</a></li> '
    pageLinks += '</ul>'
    return pageLinks

import chardet
def isUtf8Codepage(content):
    return chardet.detect(bytes(content, "utf-8"))['encoding'] == "utf-8"

def jsSafe(js):
    js = re.sub('[\r\n]+', '', js, re.I)
    js = js.replace('\"', '"', js)
    return js.replace('"', '"', js)

def stripslashesRecursive(array):
    if isinstance(array, list):
        return list(map(lambda x: stripslashes(x), array))
    return stripslashes(array)

# todo неудачный вариант, нет аналога
def stripslashes(s):
    r = re.sub(r"\\(n|r)", "\n", s)
    r = re.sub(r"\\", "", r)
    return r

def selector(data, title, attrs, selected):
    content = f'<select{attrs}>'
    if len(data) > 1:
        content += f'<option value="">{title}</option>'
    for v in data:
        add = ''
        if v == selected:
            add = ' selected'
        content += f' <option{add}>{v}</option>'
    content += '</select>'
    return

# Запросы, урлы, реквесты block

def GET(name, default=None):
    request = get_request()
    return request.GET.get(name, default)

def POST(name, default=None):
    request = get_request()
    return request.POST.get(name, default)

def SESSION(name, default=None):
    request = get_request()
    return request.session.get(name, default)

def redirect(url, seconds=0):
    request = get_request()
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return
    # if headers_sent ? redirect(url)
    return '<script> setTimeout(function () {window.location = "'+url+'";}, '+str(seconds * 1000)+');</script>'

def url(request, add='', query=''):
    import urllib.parse
    SERVER = {
        'HTTP_HOST': request.META.get('HTTP_HOST'),
        'SCRIPT_NAME': request.META.get('SCRIPT_NAME'),
        'QUERY_STRING': request.META.get('QUERY_STRING'),
    }
    # print(repr(request.META))
    # print(SERVER)
    # httpHost = 'http:// ' + SERVER['HTTP_HOST']
    path = SERVER['SCRIPT_NAME']
    if query == '':
        query = SERVER['QUERY_STRING']
        if query == '':
            return path + '?' + add

    currentAssoc = dict(urllib.parse.parse_qsl(query))
    if add:
        addAssoc = dict(urllib.parse.parse_qsl(add))
        currentAssoc = {**currentAssoc, **addAssoc}

    a = []
    for key, value in currentAssoc.items():
        a.append(f'{key}={value}')

    return path + '?' + '&'.join(a)

def getRequestParam(request, param, default='', response=None):
    if param in request.POST:
        if response:
            response.set_cookie(param, request.POST.get(param))
        request.session[param] = request.POST.get(param)
        return request.POST.get(param)
    if param in request.GET:
        if response:
            response.set_cookie(param, request.GET.get(param))
        request.session[param] = request.GET.get(param)
        return request.GET.get(param)
    if param in request.session and request.session[param]:
        return request.session[param]
    return request.COOKIES.get(param, default)

from transliterate import slugify
def translitx(string):
    return slugify(string)

# Сообщения, ошибки block

def elog(request, text, newline=0):
    global logfile
    addLog('<br>' * newline + text)
    if request.POST.get('log') == 1 and logfile:
        with open(logfile, "a") as f: # todo в оригинале там просто f.write(logfile)
            s = "\r\n" * newline + strip_tags(text)
            f.write(s)
    return

def addLog(txt, style='', request=''):
    # global DISABLE_ADDLOG
    # print(DISABLE_ADDLOG)
    # if 'DISABLE_ADDLOG' in vars() or 'DISABLE_ADDLOG' in globals():
    #     return
    if type(txt) != 'str':
        txt = repr(txt)
    # геморный метод я записью с глобальный файл лога, использование request - фз как это делать тут, глобалы не работают
    # request надо постоянно передавать. возможно есть более лучший способ
    print(f'ADDLOG: {txt}')

def saveInHistory(code, value):
    file = 'exp.txt'
    data = getHistory()
    if code not in data:
        data[code] = []
    if value not in data[code]:
        data[code].append(value)
        with open(file, 'w') as file:
            json.dump(data, file)

import json
def getHistory():
    file = 'exp.txt'
    if os.path.exists(file):
        with open(file, "r") as file:
            data = json.load(file)
    else:
        data = {}
    return data


# Пути, папки   block

def getRoot(request):
    dir = GET(request, 'root', request.COOKIES.get('folder_root', '.'))
    return dir

def changeroot(request):
    folder_root = request.COOKIES.get('folder_root')
    if folder_root and os.path.exists(folder_root):
        os.chdir(folder_root)


# Временный файл при загрузке sql файла для импорта

def getTempFile():
    filename = ''
    if os.path.exists('temp.sql'):
        filename = 'temp.sql'
    if os.path.exists('temp.zip'):
        filename = 'temp.zip'
    return filename

def findTempDir(skip=''):
    dir = ''
    dirs = 'tmp upload uploads temp cache test assets'.split(' ')
    for v in dirs:
        if os.path.exists(v) and v != skip:
            dir = v
            break
    if dir == '':
        for v in os.listdir('.'):
            if not os.path.isdir(v) or v == skip or v == 'cgi-bin' or v == '.git':
                continue
            status = os.stat(v)
            perm = oct(status.st_mode)[-3:]
            htaccess = v + '/.htaccess'
            if os.path.exists(htaccess):
                with open(htaccess, "r") as file:
                    content = file.read()
                    if content.find('Deny From All') != -1:
                        continue
            if perm == '777':
                dir = v
                break
    if not dir:
        dir = '.'
    return dir


# Специфические block

def sessionSqls():
    request = get_request()
    lastSqls = request.session.get('sql', [])
    if len(lastSqls) == 0:
        return ''
    output = '<div style="max-height:100px; overflow-y:auto"><p style="font-size:11px; margin:3px 0;">Последние запросы:</p>'
    for v in lastSqls:
        output += '<input class="focusselect" style="width:90%; border:none" type="text" value="'+escape(v)+'" /><br />'
    output += '</div>'
    return output

def saveSqlHistory(sql):
    request = get_request()
    if not request.session.get('sql'):
        request.session['sql'] = []
    if sql and len(sql) and sql not in request.session['sql'] :
        request.session['sql'].append(sql)
        addLog(escape(strip_tags(sql)))

import urllib.parse
def tableTitle(title, countAll, tables):
    request = get_request()
    t = request.GET.get('table', '')
    tableInfo = tables[t] if t in tables else {}
    if not 'Auto_increment' in tableInfo:
        tableInfo['Auto_increment'] = ''
    url = '?action=tables&table='+t
    if countAll:
        countAll = f'&nbsp;Строк {countAll} &nbsp;'

    add = ''
    if request.POST.get('where'):
        where = urllib.parse.quote_plus(request.POST.get('where'))
        add = '&where='+where

    oncRename = 'if (t=prompt(\'Введите новое название\', \''+t+'\')) {this.href=\''+url+'&mode=rename&newName=\'+t; } else {return false;}'
    oncCopy = 'if (t=prompt(\'Укажите название таблицы для создания и копирования\', \''+t+'\')) {this.href=\''+url+'&mode=copy&newTable=\'+t; } else {return false;}'

    return f"""<h2>{title}  <a href="{url}">{t}</a>
        <span style="font-size:14px;">
            <a href="{url}">данные</a>
            <a href="{url}&mode=fields">структура</a>
        </span>
        <a style="text-decoration:none;font-size:12px; " href="#" title="Показать другие действия"
        onmouseover="this.nextSibling.style.display=\'inline\'">≡</a><span style="display:none; font-size:14px; ">
        <a href="{url}&mode=delete" onclick="if (!confirm(\'Удалить {t}?\')) return false;">удал</a>
        <a href="{url}&mode=truncate" onclick="if (!confirm(\'Очистить {t}?\')) return false;">'. 'очист</a>
        <a href="#" onclick="{oncRename}">rename</a>
        <a href="#" onclick="{oncCopy}">copy</a>
        <a href="{url}&mode=export{add}">экспорт</a>
        <a href="{url}&tmode=fieldlist">поля</a>
        <a href="{url}&tmode=query">запросы</a>
        <a href="{url}&tmode=compare">сравнить</a></span>
        <span style="color:#aaa; font-size:12px;">{countAll}<a href="#" style="color:#aaa;"
            onclick="changeAi({tableInfo['Auto_increment']}); return false;">Ai {tableInfo['Auto_increment']}</span></a>
        <input type="text" class="form-control form-control-sm" style="display: inline; width: 200px;" value="{t}" 
            onfocus="this.select(); return false;" />
        </h2>"""


def printQMenu(tables):

    sessionTables = printSessionTables()
    pfxCurrent = ''
    table = GET('table')
    if table and table.find("_") > 0:
        pfxCurrent = table[0:table.find("_")]

    output = ''
    if tables:
        pfxAll = {}
        for table in tables.keys():
            a = table.find('_')
            if a:
                pfx = table[0:a]
                pfxAll [pfx] = (pfxAll[pfx] if pfx in pfxAll else 0) + 1
        pfxPrev = ''
        uniquePfx = []
        for table in tables.keys():
            pass
        # todo дописать эту функцию когда будет массив tables
        if uniquePfx:
            output = '<style type="text/css">'
            for i in uniquePfx:
                output += '#qMenu a.pfx_{v} {display:none;}'
            output += '</style>'

    return f"""<div id="qMenu" onmouseover="openMenu();" onmouseout="hideMenu();">
        {sessionTables}
        {output}
        </div>
        """

def getTableStyle(rows):
    add = ''
    if rows == 0:
        add = 'color:#aaa'
    elif rows > 200000:
        add = 'font-weight:bold color:red'
    elif rows > 100000:
        add = 'color:red'
    elif rows > 50000:
        add = 'font-weight:bold'
    if add:
        add = f' style="{add}"'
    return add


def printSessionTables():
    request = get_request()
    sessionTables = request.session.get('tables')
    if not sessionTables:
        return 'no session tables'
    tables = getAllTables()
    if not tables:
        return 'getAllTables empty'
    output = '<b>Таблицы сессии:</b> <br />'
    for table in sessionTables:
        if table not in tables:
            continue
        output += f'<a href="/?action=tables&table={table}">{table}</a>'
    output += '<hr />'
    return output

def getAppTitle():
    request = get_request()
    acts = {
        'tables': request.session.get('db_name'),
        'zip': 'Архив',
        'upload': 'Upload'
    }
    action = GET('action')
    title = 'exp'
    if GET('table'):
        title = GET('table')
        if GET('mode') == 'fields':
            title += ' структура'
    elif GET('folder'):
        title = os.path.basename(GET('folder'))
    elif action in acts:
        title = acts[action]
    elif action:
        title = action.capitalize()
    return title

def getTmpInfo():
    global TMP_DIR
    tmpInfo = 'Указана темп-папка: ' + TMP_DIR
    if os.path.exists(TMP_DIR) and os.path.isdir(TMP_DIR):
        tmpInfo += ' - существует'
        tmpInfo += ' Права: ' + str(oct(os.stat(TMP_DIR).st_mode)[-3:])
        if os.access(TMP_DIR, os.W_OK):
            tmpInfo += ' запись разрешена'
        else:
            tmpInfo += ' запись запрещена!'
    else:
        tmpInfo += ' - отсутствует!'
    return tmpInfo


# функции архивирования block

# Используется в архивировании папки. В архиве только сама папка, без родительских папок
def zipFilesFolder(zip, dir, files, addedAll, errorAll, fromRoot = False):
    pass
    
def scandirex(dir, onlyField=''):
    lists = []
    sort_order = []
    for v in os.listdir(dir):
        path = dir + '/' + v
        isdir = os.path.isdir(path)
        lists.append({
            'name': v,
            'path': path,
            'dir': isdir,
            'size': 0 if isdir else os.path.getsize(path),
            'sort': str(not isdir) + v
        })
    lists = sorted(lists, key=lambda item: item['sort'])
    if onlyField:
        return list(item[onlyField] for item in lists)
    return lists

# todo большая функция сравнения таблиц... вообще не помню такого
def compareDisplay(msg, fields):
    pass

# todo compare фз что это откуда
def compareData(msg, fields):
    pass


def templateLayout(tables, database, pageContent=''):
    pass
