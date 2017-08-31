import os;
import datetime;
import re;

path = '/Users/pailie/Desktop/nakedLogs/mock_ip.log'
ip_dict = {}

def search_for_same_ip(fileName, time, ip):
    time_str = time[:19]
    date_time = getTime(time_str)
    f = open(fileName, 'r')
    s = f.readlines()
    for line in s:
        if line.find(ip) >= 0:
            ip_dict[ip] += 1
    f.close()

def getTime(str):
    date_time = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    return date_time

# search_for_same_ip('2017')


dir_path = '/Users/pailie/Desktop/nakedLogs/'
files = os.listdir(dir_path)

