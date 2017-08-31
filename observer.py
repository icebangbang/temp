# coding=utf-8
from flask import Flask
from util import rest

from datetime import datetime,timedelta
import os
import re
import time

app = Flask(__name__, static_folder="static")

pattern = "\[\[(.*?)\]\]"  # 找到pattern中的[[]]内的数据
prefix = '/Users/lifeng/Work/Python/observer/static/example/'



@app.route('/search/<string:mobile>')
def search_by_mobile(mobile):
    now = datetime.now()
    time_str = now.strftime('%Y%m%d%H')
    file_path = prefix+time_str + ".log"
    line = '2017-08-31 14:18:12.089 INFO  [controllers.interceptor.FInterceptor:34] - >>> api.account.ProfileController.profile from [[13456856893:0.0:0.0:101.68.38.252]]'
    details = open_file(file_path, now,mobile,1)
    return rest.response_to("hello")

def open_file(file_path,date_time,mobile,depth):
    if depth == 49:
        return None
    if_find = False
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            for line in f:
                guid = re.findall(pattern, line, re.M)
                if len(guid) > 0:
                    datas = guid[0].split(':')
                    phone_number = datas[0]
                    if (mobile == phone_number):
                        if_find = True
                        info_index = line.find('.')
                        str = line[0:info_index]
                        timeArray = time.strptime(str, "%Y-%m-%d %H:%M:%S")
                        return [timeArray,datas[3]]
            if if_find is not True:
                depth +=1
                date_time = date_time + timedelta(hours=-1)
                file_path = prefix+date_time.strftime('%Y%m%d%H')+'.log'
                open_file(file_path,date_time,mobile,depth)

# app.run(host='0.0.0.0',port=8091,debug=True,use_reloader=False,threaded=True)
if __name__ == '__main__':
    app.run(threaded=True)