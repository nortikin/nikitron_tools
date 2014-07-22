##Разное
______________

 Install as usual addon.

###Nikitron tools
  __tools for everyday use. in toolbar SV__    
  __Праздник, который всегда со мной.__    
    a. Converts from 2d curves to 3d, bring them to floor, bring extrusion to 0, so they came wireframe.    
    а. Обратить 3М кривые в 3М и обратно со всеми вытекающими
    b. Spreads objects (flat curves initially) to layout, so you can export them to dxf for work in autocad.    
    б. Расположить объекты по полу, чтобы хоть как-то упорядочить их перед выводом в чертёж
    c. Names objects by 3Dtext.    
    в. Имена объектов в 3М   
    d. INndexes object's vertices by 3Dtext.   
    г. Индексы вершин в 3М
    f. Links all selected object's materials slots to object or data.    
    д. Все материалы выделенных объектов становятся от данных или от объектов, удобно когда часть сцены надо сделать в одном материале, а остальное время оно разноцветное    
    
    g. CONNECT TWO OBJECTS with edges! It is main feature. So, he connects both object's vertices with     
        custom shift and at the end hooks them to initial objects!    
    
    е. СОЕДИНИТЬ ДВА ОБЪЕКТА рёбрами. Основной инструмент этого набора. Соединяет и крючкует, хукает то есть. И двигая и масштабируя объекты, вы меняете топологию рёбер.
        
    h. Make compliment in Russian.    
    ё. Комплимент   
    i. Makes super curves with Clifford Attractors - mathematically sin/cos definitions for cool curves.    
    ж. Супер-кривая. синусо-косинусовая. В сверчке можно узлом генератора формулы делать такое же.  
    j. Make bound boxes of objects.    
    з. Габаритный куб   
    k. Delete orientations (if you made much of them and watn make some order in scene).    
    и. Удалить все ориентации которые вы ctrl+alt+space   
    m. Counts edges length.    
    й. Длина рёбер, можно скопипастить   
    n. Counts Area of object's polygons.    
    к. Площадь - можно скопипастить    
    q. http://blenderaddonlist.blogspot.com/2013/11/addon-nikitron-tools.html    

###Music player 
  __made by edddy and some developed by nikitron. Situated in 3D toolshelf in SV tab.__    
  __Сделан Эдуардом и я доделал. Во вкладке SV.__    
    a. play music and sound from videofiles.    
    а. Играет музыку и аудио с фильмов   
    b. jump to defined seconds (no current sound position).    
    б. ползунок есть чтобы прокрутить песню. Лучшего решения в блендере пока нет.    
    c. you see now playlist and choose sound to play.    
    в. видно плейлист и можно выбрать мелодию чтобы проиграть.
    d. playlist and volume stored in scene properties. just save file  
    г. плейлист и громкость хранятся в бленд файле в сцене, сохраните и оно сохранит плейлист.
    e. http://blenderaddonlist.blogspot.com/2013/12/addon-music-player.html    
    https://cloud.githubusercontent.com/assets/5783432/2811334/042e8b64-ce16-11e3-8a18-3d1846af8e21.png    

###RSS feed reader 
  __made by Nikolay Fomichev. It is 2.5 blender addon, old one. Situated in World properties__    
  __Сделал Фомичёв Коля. Находится в настройках мира__    
    a. Blendernation site RSS by default.     
    а. по умолчанию блендернаци    
    b. width adaptive text.    
    б. адаптивный текст по ширине   
    c. You can add your link.    
    в. вы можете вставить свою ссылку   

###Fedge
  __Tool for finding loose edges, loose vertices.__     
  __Находит потеряшки - вершинки, рёберки и нулевые полигоны.__     
    a. In object mode on hit between selected left selected onlt objects with loose edges/vertices or if there is no vertices at all or zero area polygons    
    а. в объектном режиме оставляет выделенными только калечные объекты   
    b. In edit mode on hit selects loose edges, if no loose edges, select loose vertices, if no loose vertices select zero faces, other turn to object mode    
    б. В редактировании выделяет сначала калечные рёбра, потом вершины-потеряшки, потом нуль-полигоны и кончает в объектный режим  

###Выпадениедней
  __Полностью на русском скрипт, который ищет какие дни выпадают сколько раз в месяц.__     
    а. Скрпт возник как реакция на предположение, будто пять пятниц, суббот и воскресений в месяце     
        выпадают раз в несколько лет. Но проверка показала, что это очень частое событие.    
    б. Для просчёта надо запустить его как >>> python3.4 выпадениедней.py    
    в. Изменить выпадание(['пятница'], 2017, 5) можно на выпадение(['пятница','суббота','воскресенье'],2016,4)    
        тогда считает до 2016 года дни выпадающие 4 раза в месяце.    
