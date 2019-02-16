import os
import os.path as path
from shutil import copyfile as cf

'''
Destination:
Mate DE animated backgrounds creator
Author:
Nikitron
Usage:
#sudo python3 do_backgrounds.py
#mate-appearance-properties -p background
drug-n-drop xml from /usr/share/backgrounds/%your_folder/
to mate-appearance window
'''

cd = path.abspath('.')
cdname = path.split(cd)[-1]
bd = '/usr/share/backgrounds'
dd = path.join(bd,cdname)
if not cdname in os.listdir(bd):
    os.symlink(cd,dd)
    #os.mkdir(dd)
list = os.listdir(cd)
text = '<background> \n\
  <starttime> \n\
    <year>2017</year> \n\
    <month>05</month> \n\
    <day>07</day> \n\
    <hour>00</hour> \n\
    <minute>00</minute> \n\
    <second>00</second> \n\
  </starttime> \n\
  <!-- This animation will start at midnight. --> \n'

st =    '  <static>\n'
dur =   '    <duration>60.0</duration>\n'
dure =  '    <duration>5.0</duration>\n'
ste =   '  </static>\n'
tr =    '  <transition>\n'
tre =   '  </transition>\n'

def ends(item):
    for i in ['.jpg','.png','.tiff','.jpeg','.gif','.svg','.bmp']:
        if item.endswith(i):
            return True
    return False

for i, item in enumerate(list):
    if not ends(item):
        continue
    if i != len(list)-1:
        f1_s = path.join(cd,item)
        f1   = path.join(dd,item)
        f2_s = path.join(cd,list[i+1])
        f2   = path.join(dd,list[i+1])
        #cf(f1_s, f1)
        file_ = '    <file>'+f1+'</file>\n'
        from_ = '    <from>'+f1+'</from>\n'
        to =    '    <to>'+f2+'</to>\n'
    else:
        f1_s = path.join(cd,item)
        f1   = path.join(dd,item)
        f2_s = path.join(cd,list[0])
        f2   = path.join(dd,list[0])
        #cf(f1_s, f1)
        file_ = '    <file>'+f1+'</file>\n'
        from_ = '    <from>'+f1+'</from>\n'
        to =    '    <to>'+f2+'</to>\n'
    text_ = st+dur+file_+ste+tr+dure+from_+to+tre
    os.chown(f1,1000,1000)
    text += text_
text += '</background>'
os.chdir(cd)
df = cdname+'_bg.xml'
f= open(df,"w+")
f.write(text)
f.close()
os.chown(dd,1000,1000)
os.chown(df,1000,1000)
print('done \n\
#mate-appearance-properties -p background \n\
drug-n-drop xml from /usr/share/backgrounds/%your_folder/ \n\
to mate-appearance window)')
#uid=pwd.getpwnam('ololo')[2]
#os.setuid(uid)
#os.setuid(1000)
#os.setgid(1000)
#os.chdir(bd)
os.system('caja %s' % dd)
#os.system('mate-appearance-properties -p background')
