import re
import random as r

messness = 8 # define every 5th glitched letter
lib = 'а б в г д е ё ж з и й к л м н о п р с \
       т у ф х ц ч ш щ ъ ы ь э ю я А Б В Г Д \
       Е Ё Ж З И Й К Л М Н О П Р С Т У Ф Х Ц \
       Ч Ш Щ Ъ Ы Ь Э Ю Я \
       - = ! " № ; % : ? * ( ) _ +'.split()
text = '/home/ololo/glitch'
a = open(text)
b = a.read()
a.close()
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
