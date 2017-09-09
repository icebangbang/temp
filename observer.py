# coding=utf-8
from flask import Flask
from util import rest

from datetime import datetime, timedelta
import os
import re
import time
import get_ip_gps
from conf.logger import logging

app = Flask(__name__, static_folder="static")

pattern = "\[\[(.*?)\]\]"  # 找到pattern中的[[]]内的数据
prefix = '/home/logstash/naked/'


@app.route('/search/<string:mobile>')
def search_by_mobile(mobile):
    now = datetime.now()
    time_str = now.strftime('%Y%m%d%H')
    file_path = prefix + time_str + ".log"
    details = open_file(file_path, now, mobile, 1)
    logging.info("the detail is: %s",details)
    if details is None:
        return rest.response_to({'ip_count': 0, 'user_count': 0})
    ip_count = get_ip_gps.search_for_same_ip(details[0], details[1], 24, 0)
    user_count = get_ip_gps.search_for_similar_gps(details[0], details[2], details[3], 24, 0)
    data = {'ip_count': ip_count, 'user_count': user_count}
    return rest.response_to(data)


def open_file(file_path, date_time, mobile, depth):
    logging.info('current log file path is: ' + file_path + 'search mobile is: ' + mobile)
    if depth == 49:
        return None
    if_find = False
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            for line in f:
                if line.find('>>> api.bid.BidController.apply from') > 0:
                    guid = re.findall(pattern, line, re.M)
                    if len(guid) > 0:
                        datas = guid[0].split(':')
                        logging.info("the key data is: %s", datas)
                        phone_number = datas[0]
                        if mobile == phone_number:
                            if_find = True
                            info_index = line.find('.')
                            str = line[0:info_index]
                            ips = datas[3].split(",")
                            return [str, ips[0], datas[1], datas[2]]
            if if_find is not True:
                depth += 1
                date_time = date_time + timedelta(hours=-1)
                file_path = prefix + date_time.strftime('%Y%m%d%H') + '.log'
                open_file(file_path, date_time, mobile, depth)


# app.run(host='0.0.0.0',port=8091,debug=True,use_reloader=False,threaded=True)
if __name__ == '__main__':
    app.run(threaded=True)
