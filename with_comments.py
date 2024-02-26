import random
import math
import RU_LOCAL as RU

stations = {} # словарь. ключ-номер станции, значения-1.макс.вместимость 2.бензины
turns = {} # ключ-номер станции, знач-1.текущая вмест-ть, 2.время отъезда машин
clients = {} # ключ-инф-я о клиенте, значение-время отъезда
cars = {} # ключ-время приезда, значения:1.к-во литров 2.вид бензина нужный
left_clients = 0 # не заправились к-во
result = 0 # выручка за день

volume = {RU.GAS_1: 0, RU.GAS_2: 0, RU.GAS_3: 0, RU.GAS_4: 0} # сколько продали вид бензина в литрах
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

            for i in range(1, len(turns) + 1): # цикл по станциям. если тек время есть в значениях времени отъезда машины по колонкам, то нам нужно уменьшить текущее к-во машин на колонке и удалить это время из словаря turns
                if time in turns[i][1]:
                    turns[i][0] -= turns[i][1].count(time)

                    while time in turns[i][1]:
                        turns[i][1].remove(time) # машина уехала

            val_clients = list(clients.values())
            keys_clients = list(clients.keys())

            for j in range(len(val_clients)):
                if val_clients[j] == time: # если время отъезда совпадает с тек временем, то удаляем ключ клиента из clients
                    clients.pop(keys_clients[j])
                    print(RU.IN, time, RU.CLIENT, keys_clients[j], RU.DONE, file=f_out) # заправился и уехал

                    for number in stations: # текущее состояние на всех станциях
                        print(RU.AUTO, number, RU.MAX_TURN, stations[number][0], RU.GASES,
                              *stations[number][1], '->', turns[number][0] * '*', sep=' ', file=f_out)

            if time in cars: # если в тек время приезжает машина(т.е.время приезда = тек)
                gas_need = cars[time][1] # необходимый вид бензина
                time_car_need = math.ceil(cars[time][0] / 10) + random.randint(-1, 1) # сколько минут с учетом +-1 будет заправляться

                while time_car_need == 0: # на случай, если при рандоме вычитается 1 и время заправки = 0, продолжаем рандомно +-1
                    time_car_need = math.ceil(cars[time][0] / 10) + random.randint(-1, 1)

                time_car_hours = (int(time_hours) * 60 + int(time_minutes) + time_car_need) // 60
                time_car_minutes = (int(time_hours) * 60 + int(time_minutes) + time_car_need) % 60 # переводим во время

                if time_car_hours < 10:
                    time_car_hours = '0' + str(time_car_hours)
                if time_car_minutes < 10:
                    time_car_minutes = '0' + str(time_car_minutes)

                time_car = str(time_car_hours) + ':' + str(time_car_minutes) # время отъезда клиента

                sttns_need_1 = {} # подходящие для заправки станции любые. ключ-номер заправки, значение-текущая вместимость

                for sttns in range(1, len(stations) + 1):
                    gases = list(stations[sttns][1]) # список для каждой станции предоставляемых видов бензина
                    if gas_need in gases: # если нужный клиенту безин в списке возможных видов у станции
                        sttns_need_1[sttns] = turns[sttns][0] # добавляем эту станцию в словарь с ее текущим к-вом машин в очереди

                sttns_need_2 = sttns_need_1.copy() #копия

                for i in sttns_need_1: # перебираем подходящие нам станции
                    if sttns_need_1[i] == stations[i][0]: # если текущая очередь в подходящей станции = макс, то удаляем эту станцию из подходящих нам
                        del sttns_need_2[i]

                client = time + ' ' + cars[time][1] + ' ' + str(cars[time][0]) + ' ' + str(time_car_need)

                if sttns_need_2 == {}: # если подходящих станций нет, то клиент уезжает , не заправившись
                    print(RU.IN, time, RU.NEW_CLIENT, client, RU.FAIL, sep=' ', file=f_out)
                    left_clients += 1 # считаем клиентов уехавших
                else:
                    num_need = list(sttns_need_2.values())  # список со всеми очередями подходящих нам станций
                    stt_choice = num_need.index(min(num_need)) # индекс подходящей нам станции в num_need
                    station = list(sttns_need_2.keys())[stt_choice]  # номер станции с мин очередью

                    print(RU.IN, time, RU.NEW_CLIENT, client, RU.TURN, station, file=f_out)

                    turns[station][0] += 1 # увеличиваем очередь на выбранной клиентом станции
                    turns[station][1].append(time_car) # добавляем время уезда
                    clients[client] = time_car # словарь. ключ-клиент, знач-время отъезда
                    volume[cars[time][1]] += cars[time][0] # к-во литров этого вида бензина, к-рое продано

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
