#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 Городецкий
# Licensed GPL 3.0
# http://nikitron.cc.ua/
# Python 3

import sys
import calendar

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print ('''да, нужно ввести год начала, год конца, месяц и день
                  например: $python3.5 деньнедели.py 1984 2158 2 7''')
        sys.exit(1)
    годначала = int(sys.argv[1])
    мес = int(sys.argv[3])
    дни = int(sys.argv[4])
    год = int(sys.argv[2])
    нед = ['понедельник','вторник','среда','четверг','пятница','суббота','воскресенье']
    вывод = ''
    for годик in range(годначала,год):
        вывод += 'В {0} году это {1} \n'.format(годик,нед[calendar.weekday(годик, мес, дни)])
    print(вывод)
