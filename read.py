from itertools import cycle
from time import sleep
import os


def read_cpuinfo():
    # read freq from /proc/cpuinfo
    with open('/proc/cpuinfo') as f:
        lines = f.readlines()

    i, freq = 0, {}
    for l in lines:
        cols = l.split(':')
        if cols[0].startswith('cpu MHz'):
            freq[f'core_{i}'] = float(cols[1])/1000
            i+=1

    return freq

def get_lm_sensors_info():
    # get temp using sensors
    os.system('sensors > tmp')
    with open('tmp') as f:
        lines =f.readlines()

    i, temp = 0, {}
    for l in lines:
        cols = l.split(':')
        if cols[0].startswith('Core'):
            temp[f'core_{i}'] = cols[1].split()[0]
            i+=1
    os.system('rm tmp')

    return temp

def main_loop():
    os.system('clear')
    symb = cycle(('|', '/', '-', '\\'))

    while True:
        print(f'Monitoring CPUs: {next(symb)}\n')

        freq = read_cpuinfo()

        temp = get_lm_sensors_info()

        msg = []
        for (k, f), t in zip(freq.items(), temp.values()):
            msg.append(f'| {k} : {f:.4f} Ghz {t} |')
        msg =  '\n'.join(msg)

        print(f'{msg}')

        print('\nType ctr+z or ctr+c to stop !')

        sleep(1.0)

        os.system('clear')

if __name__ == '__main__':

    try:
        main_loop()
    except KeyboardInterrupt:
        os.system('clear')
        print('Stop the monitoring.')
