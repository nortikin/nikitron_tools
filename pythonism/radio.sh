#!/bin/bash

# set colors
RED='\e[41m'
BLUE='\e[44m'
CYAN='\e[46m'
NC='\e[0m'

# set player
PLAYER="/usr/bin/mplayer"

# verify if $PLAYER is installed
if [ -e $PLAYER ]; then
    # stop current $PLAYER session
    if [ "$(pidof mplayer)" ]; then
        killall mplayer
    fi
    while true; do
    clear
    echo " ·············································································"
    echo " · Выберите номер от 1 до 30 и нажмите $CYAN [Enter]$NC                              ·"
    echo " ·                                                                           ·"
    echo " · $CYAN[space]$NC пауза, $CYAN[q]$NC стоп, $CYAN[Ctrl]+[c]$NC выход                                 ·"
    echo " ·············································································"
    echo ""
    echo " ·············································································" 
    echo " ·$BLUE  1 $RED  Вести                $BLUE 11 $RED  Ваня            $BLUE 21 $RED  Классика            $NC·"
    echo " ·$BLUE  2 $RED  Амстердам транс      $BLUE 12 $RED  Русское Радио   $BLUE 22 $RED  Классика            $NC·"
    echo " ·$BLUE  3 $RED  Романтика            $BLUE 13 $RED  Дача            $BLUE 23 $RED  Классика            $NC·"
    echo " ·$BLUE  4 $RED  Рекорд электроника   $BLUE 14 $RED  Юмор фм         $BLUE 24 $RED  ДНБ                 $NC·"
    echo " ·$BLUE  5 $RED  90-е гг              $BLUE 15 $RED  Транс           $BLUE 25 $RED  Кантри              $NC·"
    echo " ·$BLUE  6 $RED  Электроскай          $BLUE 16 $RED  Маяк            $BLUE 26 $RED  Жаз                 $NC·"
    echo " ·$BLUE  7 $RED  1фм лаунж            $BLUE 17 $RED  Наше радио      $BLUE 27 $RED  80-е гг             $NC·"
    echo " ·$BLUE  8 $RED  Атмосфера ланж       $BLUE 18 $RED  Электроника     $BLUE 28 $RED  Дабстеп             $NC·"
    echo " ·$BLUE  9 $RED  Сумерьки             $BLUE 19 $RED  Энергия         $BLUE 29 $RED  Прогрессивное       $NC·"
    echo " ·$BLUE 10 $RED  ЛанжФМ               $BLUE 20 $RED  Хип Хоп         $BLUE 30 $RED  custom link...      $NC·"
    echo " ·············································································"
    echo ""
    read choix
    case $choix in
        1)
            $PLAYER http://icecast.vgtrk.cdnvideo.ru/vestifm_mp3_192kbps
            ;;
        2)
            $PLAYER http://strm112.1.fm/atr_mobile_mp3
            ;;
        3)
            $PLAYER http://ic2.101.ru:8000/v4_1
            ;;
        4)
            $PLAYER http://online.radiorecord.ru:8101/rr_320
            ;;
        5)
            $PLAYER http://air.radiorecord.ru:8102/sd90_320
            ;;
        6)
            $PLAYER http://46.105.180.202:8040/sr_128
            ;;
        7)
            $PLAYER http://strm112.1.fm/chilloutlounge_mobile_mp3
            ;;
        8)
            $PLAYER http://185.53.169.128:8000/192
            ;;
        9)
            $PLAYER http://sumerki.su:8000/Sumerki
            ;;
        10)
            $PLAYER http://myradio.ua:8000/loungefm128.mp3
            ;;
        11)
            $PLAYER http://icecast.piktv.cdnvideo.ru/vanya  #:8108/shanson128.mp3
            ;;
        12)
            $PLAYER http://icecast.rmg.cdnvideo.ru/rr.mp3  #:8000/russianradio128.mp3
            ;;
        13)
            $PLAYER http://81.30.54.74:8000/radio4
            ;;
        14)
            $PLAYER http://ic2.101.ru:8000/v5_1
            ;;
        15)
            $PLAYER http://radio.globaltranceinvasion.com:8000/radiohi
            ;;
        16)
            $PLAYER http://icecast.vgtrk.cdnvideo.ru/mayakfm_mp3_192kbps
            ;;
        17)
            $PLAYER http://nashe1.hostingradio.ru/nashe-128.mp3
            ;;
        18)
            $PLAYER http://icecast.radiodfm.cdnvideo.ru/dfm.mp3
            ;;
        19)
            $PLAYER http://ic2.101.ru:8000/v1_1
            ;;
        20)
            $PLAYER http://listen1.myradio24.com:9000/4455
            ;;
        21)
            $PLAYER http://174.36.206.197:8000/;stream.nsv
            ;;
        22)
            $PLAYER http://pianosolo.streamguys.net:80/live
            ;;
        23)
            $PLAYER http://sc1c-sjc.1.fm:7070/?type=.flv
            ;;
        24)
            $PLAYER http://source.dnbradio.com:10128/128k.mp3
            ;;
        25)
            $PLAYER http://sc3b-sjc.1.fm:7802/?type=.flv
            ;;
        26)
            $PLAYER http://quarrel.str3am.com:7990/;stream.nsv&type=mp3
            ;;
        27)
            $PLAYER http://s7.radioheart.ru:8003/live
            ;;
        28)
            $PLAYER http://stream.dubstep.fm/stream/1/
            ;;
        29)
            $PLAYER http://176.104.22.115:8000/192.mp3
            ;;
        30)
            echo ""
            echo "put your custom link here"
            echo ""
            read customlink
            $PLAYER $customlink
            ;;
        *)
            echo -e "$RED wrong choice $NC"
            echo "try again..."
            echo ""
            sleep 2
            clear
            ;;
    esac
    done
else
    echo " this script need mplayer"
    echo " install it or change the PLAYER"
    echo "exiting ..."
    exit 0
fi
