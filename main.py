import random
import math
import RU_LOCAL as RU

stations = {}
turns = {}
clients = {}
cars = {}
left_clients = 0
result = 0

volume = {RU.GAS_1: 0, RU.GAS_2: 0, RU.GAS_3: 0, RU.GAS_4: 0}
prices = {RU.GAS_1: 42, RU.GAS_2: 48.9, RU.GAS_3: 52.45, RU.GAS_4: 67.2}

with open('gas_station.txt', encoding="utf8") as gas:
    for x in gas:
        ptr = x.split()
        number = int(ptr[0])
        turn = int(ptr[1])
        stations[number] = [turn, ptr[2:]]
        turns[number] = [0, []]

with open('input.txt', encoding="utf8") as f_inp:
    for x in f_inp:
        time, liter, gs = x.split()
        cars[time] = [int(liter), gs]

with open('output.txt', 'w', encoding="utf8") as f_out:
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
            val_clients = list(clients.values())
            keys_clients = list(clients.keys())
            for j in range(len(val_clients)):
                if val_clients[j] == time:
                    clients.pop(keys_clients[j])
                    print(RU.IN, time, RU.CLIENT, keys_clients[j], RU.DONE, file=f_out)
                    for number in stations:
                        print(RU.AUTO, number, RU.MAX_TURN, stations[number][0], RU.GASES,
                              *stations[number][1], '->', turns[number][0] * '*', sep=' ', file=f_out)
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
                client = time + ' ' + cars[time][1] + ' ' + str(cars[time][0]) + ' ' + str(time_car_need)
                if sttns_need_2 == {}:
                    print(RU.IN, time, RU.NEW_CLIENT, client, RU.FAIL, sep=' ', file=f_out)
                    left_clients += 1
                else:
                    num_need = list(sttns_need_2.values())
                    stt_choice = num_need.index(min(num_need))
                    station = list(sttns_need_2.keys())[stt_choice]
                    print(RU.IN, time, RU.NEW_CLIENT, client, RU.TURN, station, file=f_out)
                    turns[station][0] += 1
                    turns[station][1].append(time_car)
                    clients[client] = time_car
                    volume[cars[time][1]] += cars[time][0]
                for number in stations:
                    print(RU.AUTO, number, RU.MAX_TURN, stations[number][0], RU.GASES,
                          *stations[number][1], '->', turns[number][0] * '*', sep=' ', file=f_out)
with open('result.txt', 'w', encoding="utf-8") as rslt:
    print(RU.VOLUME, file=rslt)
    for i in volume:
        print(i, ':', volume[i], file=rslt)
    for i in prices:
        result += prices[i] * volume[i]
    print(RU.RESULT, result, file=rslt)
    print(RU.COUNT_LEFT, left_clients, file=rslt)
    print(RU.START, file=rslt)
    print(RU.CHANGES, file=rslt)
