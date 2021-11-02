#f = open('test.txt', 'w')
#f.write('1\n')
#f.close()

# списки
s = ['b', 'a', 'c']
s.sort();
s.append(5)
s.extend(['f'])
s.insert(1, 'g');
s.remove('b')
s.pop(3)
s.reverse()
print(s.__sizeof__())

print(s)
s.clear()
# кортежи - то же что и список, но фиксированной длины (константа)
c = (1, 2, 3)


#for line in f:
#    print(line);
#f.close()

import mysql.connector
