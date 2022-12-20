from selvbet_schedule import *

def prettify_schedule():
    with open('schedule.txt', 'r') as file:
        lines = file.readlines()
            
    # delete the first 2 lines because they're empty
    with open('schedule.txt', 'w') as file:
        for number, line in enumerate(lines):
            if number not in [0, 1]:
                file.write(line)

    with open('schedule.txt', 'r') as file:
        lines = file.readlines()

    with open('schedule.txt', 'w') as file:
        file.write('')


    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    with open('schedule.txt', 'a') as file:
        for number, line in enumerate(lines):
            if (line[0] in nums):
                file.write('--------\n')
                file.write(line)
            else:
                file.write(line)
