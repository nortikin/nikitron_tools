def выпадание(днидляпросчёта, годконца):
    # месяца - стандартные значения
    янв = мар = май = июл = авг = окт = дек = [i for i in range(1,32)]
    апр = июн = сен = ноя = [i for i in range(1,31)]
    # первый год не менять или найти год начинающийся с воскресенья
    год = 2012
    неделя=['воскресенье','понедельник','вторник','среда','четверг','пятница','суббота']
    днисквозные = 0
    while год<годконца:
        if not год%4:
            фев = [i for i in range(1,30)]
        else:
            фев = [i for i in range(1,29)]
        месяцев_12=[янв,фев,мар,апр,май,июн,июл,авг,сен,окт,ноя,дек]
        for к, месяцсчёт in enumerate(месяцев_12):
            деньсчёт = 0
            for деньмес in месяцсчёт:
                день = неделя[(днисквозные)%7]
                if день in днидляпросчёта:
                    деньсчёт+=1
                if деньсчёт>=(5*len(днидляпросчёта)):
                    днинеделистрочкой = ', '.join(днидляпросчёта)
                    print('Совпало, {4} выпали {0} раз {2} месяца {3} года'.format(деньсчёт, деньмес, (к+1), год, днинеделистрочкой))
                #print(год,к+1,деньмес,день)

                днисквозные+=1
        год += 1


if __name__ == "__main__":
    выпадание(['пятница'], 2017)
