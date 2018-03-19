#!/usr/bin/python

"""PM2.5 sensor: plantower PMSA003"""

import serial
import subprocess
import time
import threading
import Queue

def get_pm():
    count = lower = 0
    pm1 = 0
    pm2_5 = 0
    pm10 = 0
    max_count = 31
    while True:
        if count >= max_count:
            return pm1, pm2_5, pm10
        count += 1
        higher = lower
        lower = ord(SENSOR.read())
        data = higher*256 + lower
        if (count == 1) & (lower != 66):
            count = 0
        elif (count == 2) & (lower != 77):
            count = 0
        elif count == 4:
            max_count = data
        elif count == 12:
            pm1 = data
        elif count == 14:
            pm2_5 = data
        elif count == 16:
            pm10 = data

class PmQueueList(object):
    def __init__(self, size):
        self._sum = [0] * size
        self.avg = [0] * size
        self._count = 0
        self._oldest = 0
        self._queue = Queue.Queue()

    def push(self, pm_list, last_time):
        self._sum = [sum(x) for x in zip(self._sum, pm_list)]
        self._count += 1
        self._queue.put({'time': last_time, 'pm': pm_list})
        self.avg = [pm_value/self._count for pm_value in self._sum]

    def update(self, shelf_life):
        while self._oldest < shelf_life:
            record = self._queue.get()
            self._oldest = record['time']
            self._count -= 1
            for index, value in enumerate(self._sum):
                self._sum[index] = value - record['pm'][index]

class PmDb(object):
    def __init__(self, titles, intervals):
        self._titles = titles
        self._pm_db = {interval: PmQueueList(len(titles)) for interval in intervals}
        self.avg = {interval: [0]*len(titles) for interval in intervals}

    def push(self, pm_list):
        now = time.time()
        for interval in self._pm_db:
            self._pm_db[interval].push(pm_list, now)
            self._pm_db[interval].update(now - interval*60)
            self.avg[interval] = self._pm_db[interval].avg

    def discription(self):
        output = ""
        for interval in sorted(self.avg):
            if interval < 60:
                output += "Recent {} mins\n".format(interval)
            else:
                output += "Recent {} hours\n".format(interval/60)
            for index, title in enumerate(self._titles):
                output += "    {}: {}\n".format(title, self.avg[interval][index])
        return output

def sensor_thread():
    while True:
        if SENSOR.inWaiting() > 50:
            PM_DB.push(get_pm()[1:])

def start_sensor():
    server_handler = threading.Thread(target=sensor_thread, args=tuple())
    server_handler.start()

subprocess.call(["systemctl", "stop", "serial-getty@ttyS0.service"])
subprocess.call(["systemctl", "disable", "serial-getty@ttyS0.service"])
SENSOR = serial.Serial("/dev/ttyS0", baudrate=9600, bytesize=8,
                       parity='N', stopbits=1, xonxoff=0, timeout=3.0)
PM_DB = PmDb(['PM2.5', 'PM10'], [1, 60, 600])
