from flask import Flask, request, make_response, render_template

import pymysql
import re

connection = pymysql.connect(host='localhost',
        user='root',
        password='root',
        db='blog',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__, template_folder="templates")

def printTable(sql):
    data = getData(sql)
    content = '<table>'
    printHeaders = False
    for row in data:
        if printHeaders == False:
            printHeaders = True
            content += '<tr>'
            for key, value in row.items():
                content += '<td>{0}</td>'.format(key)
            content += '</tr>'
        tr = '<tr>'
        #print(type(row.items()))
        for key, value in row.items():
            #print(key, '->', value)
            if isinstance(value, str):
                value = 'string'
            tr += '<td>{0}</td>'.format(value)
        tr += '</tr>'
        content += tr
    content += '</table>'
    return content

def getData(sql):
    with connection:
        cur = connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        # desc = cur.description
        # content += repr(desc)
    return rows


def query(sql):
    res = True
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    except:
        res = False
    finally:
        connection.close()
    return res

def mysqlInsert(table, data, type='INSERT'):
    values = []
    for k, v in data.items():
        if isinstance(v, int) == False and isinstance(v, str) == False:
            continue
        if v == '' or v == None:
            v = 'Null'
        elif isinstance(v, str):
            v = '"'+v+'"'
        values.append(v)
    sql = type + ' INTO `' + table + '` (`' + "`, `".join(data.keys()) + '`) VALUES (' + ", ".join(values) + ')'
    return query(sql)

"""
def getContent():
    content = ''
    with connection:
        cur = connection.cursor()
        cur.execute("SELECT * FROM blog")

        rows = cur.fetchall()
        desc = cur.description
        content += repr(desc)

        for row in rows:
            content += row['title'] + "<br>\n\n\n"
    return content
"""


#index
@app.route('/')
def indexpage():

    content = 1
    #content = printTable('SELECT * FROM blog')

    return render_template('index.html', output=content)

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/registration/', methods=['post', 'get'])
def registration():

    """
    data = {
        'username': 'andrew',
        'password': 'xxx'
    }
    sql = mysqlInsert('users', data)
    """

    title = 'Регистрация'
    message = ''
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        message = 'ok'

        if len(username) == 0 or len(password) == 0:
            message = "Empty username or password"
        elif re.search('[^a-z\d]', username):
            message = "Wrong username"

    return render_template('registration.html', **locals())


if __name__ == "__main__":
    app.run(debug=True)