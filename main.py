import random
import math

stations = {}
turns = {}
with open('gas_station.txt', encoding="utf8") as gas:
    for x in gas:
        ptr = x.split()
        number = int(ptr[0])
        turn = int(ptr[1])
        stations[number] = [turn, ptr[2:]]
        turns[number] = [0, []]
cars = {}
with open('input.txt', encoding="utf8") as f_inp:
    for x in f_inp:
        time, liter, gs = x.split()
        cars[time] = [int(liter), gs]
prices = {'АИ-80': 42, 'АИ-92': 48.9, 'АИ-95': 52.45, 'АИ-98': 67.2}
for hours in range(24):
    for minutes in range(60):
        time_hours = hours
        time_minutes = minutes
        if time_hours < 10:
            time_hours = '0' + str(time_hours)
        if time_minutes < 10:
            time_minutes = '0' + str(time_minutes)
        time = str(time_hours) + ':' + str(time_minutes)
        for i in range(1, len(turns) + 1):
            if time in turns[i][1]:
                turns[i][0] -= turns[i][1].count(time)
                while time in turns[i][1]:
                    turns[i][1].remove(time)

        if time in cars:
            gas_need = cars[time][1]
            time_car_need = math.ceil(cars[time][0] / 10) + random.randint(-1, 1)
            while time_car_need == 0:
                time_car_need = math.ceil(cars[time][0] / 10) + random.randint(-1, 1)
            time_car_hours = (int(time_hours) * 60 + int(time_minutes) + time_car_need) // 60
            time_car_minutes = (int(time_hours) * 60 + int(time_minutes) + time_car_need) % 60
            if time_car_hours < 10:
                time_car_hours = '0' + str(time_car_hours)
            if time_car_minutes < 10:
                time_car_minutes = '0' + str(time_car_minutes)
            time_car = str(time_car_hours) + ':' + str(time_car_minutes)
            sttns_need_1 = {}
            for sttns in range(1, len(stations) + 1):
                gases = list(stations[sttns][1])
                if gas_need in gases:
                    sttns_need_1[sttns] = turns[sttns][0]
            sttns_need_2 = sttns_need_1.copy()
            for i in sttns_need_1:
                if sttns_need_1[i] == stations[i][0]:
                    del sttns_need_2[i]
            client = time + cars[time][1] + cars[time][0] + time_car_need
            if sttns_need_2 == {}:
                print('В', time, 'новый клиент:', client, 'не смог заправить автомобиль и покинул АЗС', sep=' ')
            else:
                num_need = list(sttns_need_2.values())  # список со всеми очередями подходящих нам станций
                stt_choice = num_need.index(min(num_need))
                station = list(sttns_need_2.keys())[stt_choice]  # номер станции с мин очередью
                print('В', time, 'новый клиент:', client, 'встал в очередь к автомату №', station)
                turns[station][0] += 1
                turns[station][1].append(time_car)
            for number in stations:
                print('Автомат №', number, 'максимальная очередь:', stations[number][0], 'Марки бензина:',
                      *stations[number][1], '->', turns[number][0] * '*', sep=' ')
