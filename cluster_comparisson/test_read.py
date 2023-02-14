# Reading test

import time
import random

from clickhouse.client import read_rows as read_from_clickhouse

from vertica.client import read_rows as read_from_vertica

from storage_telemetry import save_telemetry

import constants


ITERATIONS = 100


def test_read():
    ch_count = 0
    test_result = []
    while ch_count < ITERATIONS:
        speed = clickhouse_read()
        test_result.append({'Operation': 'Read', 'Rows': 'all', 'Speed': speed})
        ch_count = ch_count + 1      
    save_telemetry(constants.TYPE_READ, constants.CLICKHOUSE, '', test_result)

    ve_count = 0
    test_result = []
    while ve_count < ITERATIONS:
        speed = vertica_read()
        test_result.append({'Operation': 'Read', 'Rows': 'all', 'Speed': speed})
        ve_count = ve_count + 1
    save_telemetry(constants.TYPE_READ, constants.VERTICA, '', test_result)


def clickhouse_read():   
    timestamp = random.randint(100000, 1000000000)    
    # Меряем скорость записи
    start = time.perf_counter()
    read_from_clickhouse(timestamp)    
    end = time.perf_counter() 
    speed = (end - start) * 10 ** 3
    return f'{speed:.03f} ms'


def vertica_read():        
    timestamp = random.randint(100000, 1000000000)
    # Меряем скорость записи
    start = time.perf_counter()
    read_from_vertica(timestamp)    
    end = time.perf_counter()   
    speed = (end - start) * 10 ** 3
    return f'{speed:.03f} ms'


if __name__ == "__main__":
    test_read()
