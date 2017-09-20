# coding=utf-8
from flask import Flask, request
from util import rest

from datetime import datetime, timedelta
import os
import re
import time
import get_ip_gps
import check_history
from conf.logger import logging

app = Flask(__name__, static_folder="static")

pattern = "\[\[(.*?)\]\]"  # 找到pattern中的[[]]内的数据
prefix = '/home/logstash/naked/'
# prefix = '/Users/pailie/Downloads/naked/'


@app.route('/search/<string:mobile>', methods=['POST'])
def search_by_mobile(mobile):
    cid = request.form.get("cid")
    name = request.form.get("name")

    # default value
    apply_time = None
    ip_no = None
    ip_count = -1
    user_count = -1
    ip_set = set()
    is_black_check = check_history.CheckRes()
    is_gray_check = check_history.CheckRes()

    if cid is not None and len(cid)>0 and len(mobile)>0:
        is_black_check = check_history.check_cid_mobile_in_black(cid, mobile)
        is_gray_check = check_history.check_cid_mobile_in_gray(cid, mobile)


    now = datetime.now()
    time_str = now.strftime('%Y%m%d%H')
    file_path = prefix + time_str + ".log"
    details = open_file(file_path, now, mobile, 1)
    logging.info("the detail is: %s",details)

    if details is not None:
        apply_time = details[0]
        ip_no = details[1]
        ip_count = get_ip_gps.search_for_same_ip(details[0], details[1], 24, 0)
        user_count = get_ip_gps.search_for_similar_gps(details[0], details[1], details[3], 24, 0)
        ip_set = get_ip_gps.search_ips_for_same_mobile(details[0], mobile, 48, ip_set)
    data = {'ip_count': ip_count,
            'user_count': user_count,
            'ip_no': ip_no,
            'apply_time': apply_time,
            'ip_set': list(ip_set),
            'cid_in_black': is_black_check.cid_check,
            'mobile_in_black': is_black_check.mobile_check,
            'cid_in_gray': is_gray_check.cid_check,
            'mobile_in_gray': is_gray_check.mobile_check
            }
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
                return open_file(file_path, date_time, mobile, depth)

    logging.debug("File " + file_path + " not found")

# app.run(host='0.0.0.0',port=8091,debug=True,use_reloader=False,threaded=True)
if __name__ == '__main__':
    app.run(threaded=True)
