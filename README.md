##Разное
==============

 Install as usual addon.

###Nikitron tools
  ==tools for everyday use.==    
    a. Converts from 2d curves to 3d, bring them to floor, bring extrusion to 0, so they came wireframe.
    b. Spreads objects (flat curves initially) to layout, so you can export them to dxf for work in autocad.
    c. Names objects by 3Dtext.
    d. Names object's vertices by 3Dtext.
    e. Makes real bounding boxes of any object.
    f. Links all selected object's materials slots to object or data.
    g. CONNECT TWO OBJECTS with edges! It is main feature. So, he connects both object's vertices with 
        custom shift and at the end hooks them to initial objects!
    h. Make compliment in Russian.
    i. Makes super curves with Clifford Attractors - mathematically sin/cos definitions for cool curves.
    j. Make bound boxes of objects.
    k. Delete orientations (if you made much of them and watn make some order in scene).
    l. Delete node layouts, that not used any more and not have users (or have users, but you need 
        escape node area screen).
    m. Counts edges length.
    n. Counts Area of object's polygons.
    o. Separate objects with defined number of vertices.
    p. Boolean many objects at once by three ways.
    q. http://blenderaddonlist.blogspot.com/2013/11/addon-nikitron-tools.html

###Music player 
  ==made by edddy and some developed by nikitron. Situated in 3D toolshelf in NT tab.==    
    a. play music and sound from videofiles.
    b. jump to defined seconds (no current sound position).
    c. you see now playlist and choose sound to play.
    d. http://blenderaddonlist.blogspot.com/2013/12/addon-music-player.html
    https://cloud.githubusercontent.com/assets/5783432/2811334/042e8b64-ce16-11e3-8a18-3d1846af8e21.png

###RSS feed reader 
  ==made by Nikolay Fomichev. It is 2.5 blender addon, old one. Situated in World properties==    
    a. Blendernation site RSS by default. 
    b. width adaptive text.
    c. You can add your link.

###Fedge
  ==Tool for finding loose edges, loose vertices.==     
    a. In object mode on hit between selected left selected onlt objects with loose edges/vertices or if there is no vertices at all or zero area polygons
    b. In edit mode on hit selects loose edges, if no loose edges, select loose vertices, if no loose vertices select zero faces, other turn to object mode

###Выпадениедней
  ==Полностью на русском скрипт, который ищет какие дни выпадают сколько раз в месяц.==     
    а. Скрпт возник как реакция на предположение, будто пять пятниц, суббот и воскресений в месяце 
        выпадают раз в несколько лет. Но проверка показала, что это очень частое событие.
    б. Для просчёта надо запустить его как >>> python3.4 выпадениедней.py
    в. Изменить выпадание(['пятница'], 2017, 5) можно на выпадение(['пятница','суббота','воскресенье'],2016,4)
        тогда считает до 2016 года дни выпадающие 4 раза в месяце.
