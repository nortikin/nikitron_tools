import re
import random as r
import sys

messness = 8 # define every n-th glitched letter
lib = 'а б в г д е ё ж з и й к л м н о п р с \
       т у ф х ц ч ш щ ъ ы ь э ю я А Б В Г Д \
       Е Ё Ж З И Й К Л М Н О П Р С Т У Ф Х Ц \
       Ч Ш Щ Ъ Ы Ь Э Ю Я \
       - = ! " № ; % : ? * ( ) _ +'.split()

def spoil(b):
    # основная функция, портит как может
    c = b.splitlines()
    e = [i.split() for i in c if i]
    out = ''
    for i in e:
        y = list(' '.join(i))+['\n']
        n = len(y)-2
        m = [r.randint(0,n-1) for k in range(n//messness)]
        for t in m:
            y[t] = r.choice(lib)
        out += ''.join(y)
    print(out)

def spoilfile(file_):
    # только читает файл
    a = open(file_)
    b = a.read()
    a.close()
    out = spoil(b)

if __name__ == '__main__':
    sa = sys.argv
    if len(sa) > 1:
        if sa[1] == '-f':
            if len(sa)>2:
                spoilfile(sa[2])
            else:
                file_ = input('file path:')
                spoilfile(file_)
        else:
            text = sa[1:]
            print()
            spoil(' '.join(text))
    else:
        print('usage: python3 text_spoiler.py -f <filepath>')
        print('   or: python3 text_spoiler.py <your text here>')

