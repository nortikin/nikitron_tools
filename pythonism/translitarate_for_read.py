#!/usr/bin/python3.7

import sys
import os


def openfile(filename):
    file = open(filename, "r")
    text = file.read()
    file.close()
    return text.replace("\n",'. ')

def trans(text):
    cyrillic = 'абсдефгшижклмнопкрстуввсйзАБСДЕФГШИЖКЛМНОПКРСТУВВСЙЗ          '
    latin = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()?!:….,/|' #.split('|')
    text = text.translate({ord(k):v for k,v in zip(latin,cyrillic)})
    #print(text)
    return text


def main(filename):
    text = openfile(filename)
    return trans(text)

if __name__ == '__main__':
    text = main(sys.argv[1])
    cmd = 'echo '+text+' | festival --tts --language russian'
    os.system(cmd)
