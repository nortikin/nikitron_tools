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
    echo " ·····················································"
    echo -e " · Выберите номер от 1 до 20 и нажмите $BLUE [Enter]$NC      ·"
    echo " ·                                                   ·"
    echo -e " · $BLUE[space]$NC пауза, $BLUE[q]$NC стоп, $BLUE[Ctrl]+[c]$NC выход         ·"
    echo " ·····················································"
    echo ""
    echo " ·····················································" 
    echo -e " ·  $BLUE  1 $NC  Trance               $BLUE 11 $NC  Киссфм-украина  ·"
    echo -e " ·  $BLUE  2 $NC  Ambient              $BLUE 12 $NC  Русское Радио   ·"
    echo -e " ·  $BLUE  3 $NC  DJ Mixes             $BLUE 13 $NC  Авторадио       ·"
    echo -e " ·  $BLUE  4 $NC  Drum'n'bass          $BLUE 14 $NC  Groove Salad    ·"
    echo -e " ·  $BLUE  5 $NC  House                $BLUE 15 $NC  DNB Radio       ·"
    echo -e " ·  $BLUE  6 $NC  Techno               $BLUE 16 $NC  Fréquence Jazz  ·"
    echo -e " ·  $BLUE  7 $NC  Euro Dance           $BLUE 17 $NC  Classic Rock    ·"
    echo -e " ·  $BLUE  8 $NC  Vocal Trance         $BLUE 18 $NC  Roots Reggae    ·"
    echo -e " ·  $BLUE  9 $NC  Lounge               $BLUE 19 $NC  Country         ·"
    echo -e " ·  $BLUE 10 $NC  Breaks               $BLUE 20 $NC  custom link...  ·"
    echo " ·····················································"
    echo ""
    read choix
    case $choix in
        1)
            $PLAYER http://radio02-cn03.akadostream.ru:8106/difmtrance96.mp3
            ;;
        2)
            $PLAYER http://radio02-cn03.akadostream.ru:8106/difmambient96.mp3
            ;;
        3)
            $PLAYER http://radio02-cn03.akadostream.ru:8106/difmdjmixes96.mp3
            ;;
        4)
            $PLAYER http://radio02-cn03.akadostream.ru:8106/difmdrumnbass96.mp3
            ;;
        5)
            $PLAYER http://radio02-cn03.akadostream.ru:8106/difmhouse96.mp3
            ;;
        6)
            $PLAYER http://radio02-cn03.akadostream.ru:8106/difmtechno96.mp3
            ;;
        7)
            $PLAYER http://radio02-cn03.akadostream.ru:8106/difmeurodance96.mp3
            ;;
        8)
            $PLAYER http://radio02-cn03.akadostream.ru:8106/difmvocaltrance96.mp3
            ;;
        9)
            $PLAYER http://radio02-cn03.akadostream.ru:8106/difmlounge96.mp3
            ;;
        10)
            $PLAYER http://radio02-cn03.akadostream.ru:8106/difmbreaks96.mp3
            ;;
        11)
            $PLAYER http://stream.kissfm.ua:8000/kiss  #:8108/shanson128.mp3
            ;;
        12)
            $PLAYER http://online-rusradio.tavrmedia.ua/RusRadio  #:8000/russianradio128.mp3
            ;;
        13)
            $PLAYER http://radio01-cn03.akadostream.ru:8000/avtoradio128.mp3
            ;;
        14)
            $PLAYER http://radio02-cn03.akadostream.ru:8112/somafm_groovesalad128.mp3
            ;;
        15)
            $PLAYER http://radio02-cn03.akadostream.ru:8102/dnbradio128.mp3
            ;;
        16)
            $PLAYER http://broadcast.infomaniak.ch/frequencejazz-high.mp3
            ;;
        17)
            $PLAYER http://radio02-cn03.akadostream.ru:8104/classicrock_sky96.mp3
            ;;
        18)
            $PLAYER http://radio02-cn03.akadostream.ru:8104/reggae_1_sky96.mp3
            ;;
        19)
            $PLAYER http://radio02-cn03.akadostream.ru:8104/country_1_sky96.mp3
            ;;
        20)
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
