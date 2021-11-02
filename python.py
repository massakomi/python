

                          

"""

import pymysql

connection = pymysql.connect(host='localhost',
        user='root',
        password='root',
        db='blog',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

with connection:
    cur = connection.cursor()
    cur.execute("SELECT * FROM cities WHERE id IN (1, 2, 3)")

    # rows = cur.fetchall()

    # for row in rows:
    #     print("{0} {1} {2}".format(row[0], row[1], row[2]))

    print("The query affected {} rows".format(cur.rowcount))
    
    
    
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

def getContent():
    content = ''
    with connection:
        cur = connection.cursor()
        cur.execute("SELECT * FROM blog")

        rows = cur.fetchall()
        # desc = cur.description
        # content += repr(desc)

        for row in rows:
            content += row['title'] + "\n"
    return content


sql = "SELECT * FROM blog"
content = printTable(sql)

print(content)




s = ' myuser name '

s = s.strip()
if re.search('[^a-z\d]', s):
    print('error!')

print(len(''))



a = [1, 2, 3, 3, 3, 3]
a[2] = 5

b = {
    'test': 1,
    'xxx': [1, 2]
}

#a = set(a)

print(b)

"""


