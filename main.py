import random
stations = {}
with open('gas_station.txt') as gas:
    for x in gas:
        number, turn, gs = x.split()
        stations[number] = (turn, gs)
cars = {}
with open('input.txt') as f_inp:
    for x in f_inp:
        time, liter, gs = x.split()
        cars[time] = (liter, gs)

for i in range(24):
    for j in range(60):
