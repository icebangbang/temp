# -*- coding: utf-8 -*-

import os;
import re;
import datetime;
from math import *

# path = '/Users/pailie/Desktop/nakedLogs/mock_ip.log'
pattern = "\[\[(.*?)\]\]"  # 找到pattern中的[[]]内的数据
# dir_path = '/Users/pailie/Desktop/nakedLogs/'
dir_path = 'static/example/'


def search_for_same_ip(time, ip, limit_hour, count):
    if limit_hour <= 0:
        return count

    time_str = get_time(time).strftime("%Y%m%d%H")
    filename = dir_path + time_str + '.log'
    try:
        f = open(filename, 'r')
        s = f.readlines()
        for line in s:
            if line.find(ip) >= 0:
                count += 1
        f.close()
        limit_hour -= 1
        time = (get_time(time) - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        return search_for_same_ip(time, ip, limit_hour, count)
    except:
        return count

def search_for_similar_gps(time, origin_lat, origin_lng, limit_hour, count):
    if limit_hour <= 0:
        return count

    time_str = get_time(time).strftime("%Y%m%d%H")
    filename = dir_path + time_str + '.log'
    try:
        f = open(filename, 'r')
        s = f.readlines()
        for line in s:
            guid = re.findall(pattern, line, re.M)
            if len(guid)>0:
                data = guid[0].split(':')
                search_lat = float(data[1])
                search_lng = float(data[2])
                if get_distance_by_lat_lng(origin_lat, origin_lng, search_lat, search_lng) <= 5.0:
                    count += 1
        f.close()
        limit_hour -= 1
        time = (get_time(time) - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        return search_for_similar_gps(time, origin_lat, origin_lng, limit_hour, count)
    except:
        return count


def get_time(str):
    date_time = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    return date_time


def get_client_ip(ips):
    ip_list = ips.split(',')
    print ip_list[0]


def get_distance_by_lat_lng(Lat_A,Lng_A,Lat_B,Lng_B): #第一种计算方法
    ra=6378.140 #赤道半径
    rb=6356.755 #极半径 （km）
    flatten=(ra-rb)/ra  #地球偏率
    rad_lat_A=radians(Lat_A)
    rad_lng_A=radians(Lng_A)
    rad_lat_B=radians(Lat_B)
    rad_lng_B=radians(Lng_B)
    pA=atan(rb/ra*tan(rad_lat_A))
    pB=atan(rb/ra*tan(rad_lat_B))
    xx=acos(sin(pA)*sin(pB)+cos(pA)*cos(pB)*cos(rad_lng_A-rad_lng_B))
    c1=(sin(xx)-xx)*(sin(pA)+sin(pB))**2/cos(xx/2)**2
    c2=(sin(xx)+xx)*(sin(pA)-sin(pB))**2/sin(xx/2)**2
    dr=flatten/8*(c1-c2)
    distance=ra*(xx+dr)
    return distance


ip_count = search_for_same_ip('2017-08-31 14:18:12', '101.68.38.252', 24 , 0)
print ip_count

# print get_distance_by_lat_lng(120.024117, 30.286472, 120.035301, 30.285599)
gps_count = search_for_similar_gps('2017-08-31 14:18:12', float('0.01'), float('0.0'), 24, 0)
print gps_count

