import os
import os.path as path
import shutil

'''
Destination:
get files from subfolders to curent folder
Author:
Nikitron
Usage:
#python3 get_subfolders_files.py
'''

cd = path.abspath('.')
rmrf = os.removedirs
rem = []

for i in os.walk(cd):
    for f in i[2]:
        if f in os.listdir('.'):
           f2 = 'повтор_'+f
        else:
           f2 = f
        shutil.move(path.join(path.abspath(i[0]),f),path.join(cd,f2))
    if not i[1]:
        # remove folders, but need check for existing files inside
        rem = i[0]
#for i in rem:
#    rmrf(i)
print('done \n')
