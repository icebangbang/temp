# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from conf.logger import logging

dir_path = 'static/resource/'


class CheckRes:
    def __init__(self):
        self.cid_check = False
        self.mobile_check = False


def check_cid_mobile_in_black(cid, mobile):
    filename = dir_path + 'Blacklist.csv'
    black_check_res = CheckRes()

    f = open(filename, 'r')
    s = f.readlines()
    for line in s:
        if line.find(cid) >= 0:
            black_check_res.cid_check = True
        if line.find(mobile) >= 0:
            black_check_res.mobile_check = True
    f.close()
    return black_check_res


def check_cid_mobile_in_gray(cid, mobile):
    filename = dir_path + 'Graylist.csv'
    gray_check_res = CheckRes()

    f = open(filename, 'r')
    s = f.readlines()
    for line in s:
        if line.find(cid) >= 0:
            gray_check_res.cid_check = True
        if line.find(mobile) >= 0:
            gray_check_res.mobile_check = True
    f.close()
    return gray_check_res


def check_cid_mobile_in_reject(cid, mobile):
    filename = dir_path + 'ApplyRejectedList.csv'
    reject_check_res = CheckRes()

    f = open(filename, 'r')
    s = f.readlines()
    for line in s:
        if line.find(cid) >= 0:
            reject_check_res.cid_check = True
        if line.find(mobile) >= 0:
            reject_check_res.mobile_check = True
    f.close()
    return reject_check_res



