## Разное
______________

 Install as usual addon.

### Nikitron tools
  __tools for everyday use, in toolbar SV__    
    a. Converts from 2d curves to 3d, bring them to floor, bring extrusion to 0, so they came wireframe.    
    b. Spreads objects (flat curves initially) to layout, so you can export them to dxf for work in autocad.    
    c. Names objects by 3Dtext.    
    d. Indexes object's vertices by 3Dtext.   
    f. Links all selected object's materials slots to object or data.   
    g. Join text and mesh if matrix location equal    
    h. CONNECT TWO OBJECTS with edges! It is main feature. So, he connects both object's vertices with custom shift and at the end hooks them to initial objects!    
    i. Make compliment in Russian.    
    j. Makes super curves with Clifford Attractors - mathematically sin/cos definitions for cool curves.  
    k. Make bound boxes of objects.      
    l. Delete orientations (if you made much of them and want make some order in scene).    
    m. Counts edges length.    
    n. Counts Area of object's polygons.    
    q. http://blenderaddonlist.blogspot.com/2013/11/addon-nikitron-tools.html    
    
  __Праздник, который всегда со мной.__    
    а. Обратить 2М кривые в 3М и обратно со всеми вытекающими     
    б. Расположить объекты по полу, чтобы хоть как-то упорядочить их перед выводом в чертёж     
    в. Имена объектов в 3М   
    г. Индексы вершин в 3М      
    д. Все материалы выделенных объектов становятся от данных или от объектов, удобно когда часть сцены надо сделать в одном материале, а остальное время оно разноцветное    
    е. Соединить текст и сетку если положение объектов совпадает (прикладная задача в моём рабочем процессе)
    ё. СОЕДИНИТЬ ДВА ОБЪЕКТА рёбрами. Основной инструмент этого набора. Соединяет и крючкует, хукает то есть. И двигая и масштабируя объекты, вы меняете топологию рёбер.     
    ж. Комплимент   
    з. Супер-кривая. синусо-косинусовая. В сверчке можно узлом генератора формулы делать такое же.  
    и. Габаритный куб   
    й. Удалить все ориентации которые вы ctrl+alt+space   
    к. Длина рёбер, можно скопипастить   
    л. Площадь - можно скопипастить    
    м. http://blenderaddonlist.blogspot.com/2013/11/addon-nikitron-tools.html    

### Music player 
  __made by edddy and some developed by nikitron. Situated in 3D toolshelf in SV tab.__    
    a. play music and sound from videofiles.    
    b. jump to defined seconds (no current sound position).    
    c. you see now playlist and choose sound to play.    
    d. playlist and volume stored in scene properties. just save file  
    e. http://blenderaddonlist.blogspot.com/2013/12/addon-music-player.html    
    https://cloud.githubusercontent.com/assets/5783432/2811334/042e8b64-ce16-11e3-8a18-3d1846af8e21.png    
    
  __Сделан Эдуардом и я доделал. Во вкладке SV.__    
    а. Играет музыку и аудио с фильмов   
    б. ползунок есть чтобы прокрутить песню. Лучшего решения в блендере пока нет.    
    в. видно плейлист и можно выбрать мелодию чтобы проиграть.    
    г. плейлист и громкость хранятся в бленд файле в сцене, сохраните и оно сохранит плейлист.    
    e. http://blenderaddonlist.blogspot.com/2013/12/addon-music-player.html    
    https://cloud.githubusercontent.com/assets/5783432/2811334/042e8b64-ce16-11e3-8a18-3d1846af8e21.png    

### RSS feed reader 
  __made by Nikolay Fomichev. It is 2.5 blender addon, old one. Situated in World properties__    
    a. Blendernation site RSS by default.     
    b. width adaptive text.    
    c. You can add your link.    
    
  __Сделал Фомичёв Коля. Находится в настройках мира__    
    а. по умолчанию блендернаци    
    б. адаптивный текст по ширине     
    в. вы можете вставить свою ссылку     

### Fedge
  __Tool for finding loose edges, loose vertices.__     
    see 1D scripts on github
    a. In object mode on hit between selected left selected only objects with loose edges/vertices or if there is no vertices at all or zero area polygons    
    b. In edit mode on hit selects loose edges, if no loose edges, select loose vertices, if no loose vertices select zero faces, other turn to object mode    
    
  __Находит потеряшки - вершинки, рёберки и нулевые полигоны.__     
    а. в объектном режиме оставляет выделенными только калечные объекты    
    б. В редактировании выделяет сначала калечные рёбра, потом вершины-потеряшки, потом нуль-полигоны и кончает в объектный режим    

### Выпадениедней
  __Полностью на русском скрипт, который ищет какие дни выпадают сколько раз в месяц.__     
    а. Скрпт возник как реакция на предположение, будто пять пятниц, суббот и воскресений в месяце     
        выпадают раз в несколько лет. Но проверка показала, что это очень частое событие.    
    б. Для просчёта надо запустить его как >>> python3.4 выпадениедней.py    
    в. Изменить выпадание(['пятница'], 2017, 5) можно на выпадение(['пятница','суббота','воскресенье'],2016,4)    
        тогда считает до 2016 года дни выпадающие 4 раза в месяце.    
### do_backgrounds    
  __do mate DE for linux backgrounds slideshow__    
    Destination:    
    Mate DE animated backgrounds creator    
    Author:    
    Nikitron    
    Usage:    
    #sudo python3 do_backgrounds.py    
    It will open --/%your_folder/-- at the end    
    $mate-appearance-properties -p background    
    drug-n-drop xml from --/%your_folder/--    
    to mate-appearance window    
### get_subfolders_files    
  __get all recursive subfolders files to current folder with rename doubles__    
    usage:     
    #python3 get_subfolders_files.py    
### context printer    
  __print context of blender current screen__        
    see 1D scripts on github    
### camswitch    
  __just switch active camera__    
    see 1D scripts on github    
### camstore    
  __store cameras with backgrounds__    
    see 1D scripts on github    
    same as __bgimageshower__    
    make collection property of pointer properties to store images    
    and backgrounds and bind it to cameras    
### docub    
  __wastes__    
### interface reset    
  __Blender - reset default interface layout for current window__    
    see 1D scripts on github    
### zwcad pattern    
  __attempt to make pattern generator for zwcad__    
    use at own risk    
### trans    
  __если вводишь с ангшлийской раскладкой, но не любишьт пунтосвитчер, то это решение для тебя__    
    копируешь свой текст, вставляешь после выполнения команды и вуаля - у тебя по-русски    
### radio.sh    
  __bash radio with 30 channels__    
### replace    
  __don't remember what is it__    
### ui_layer_manager    
  __custon ui for blender layers fork__    
    uses group of layers instead of mask    
### poweroff    
  __WIP__    
    RIP - attempt to poweroff at the end    
### mosaic
  __Игра в мозаику, тыкайте и выигрывайте__
