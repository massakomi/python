
from os import listdir

#print listdir('..')
from os.path import isfile
from os.path import join as joinpath
import os

def viewDirFiles(mypath, add=''):
    for i in listdir(mypath):
        subFile = joinpath(mypath, i);
        if isfile(subFile):
            print(add + i)
        else:
            print(add + 'dir '+i)
            viewdir(subFile, '--- ')

def renameFilesInDir(dir, search, replace) :
    renamed = 0
    for i in listdir(dir):
        newName = i.replace(search, replace);
        if newName != i:
            print(newName)
            os.rename(joinpath(dir, i), joinpath(dir, newName))
            renamed = renamed + 1
    print("Переименовано - " + str(renamed))
            
d = 'C:/Музыка/1 Бумажные города'
renameFilesInDir(d, 'ВсеСаундтреки.рф - ', '')
