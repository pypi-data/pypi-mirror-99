# -*- coding: utf-8 -*-
import sys
import json
import time
import os


PY2 = sys.version_info[0] == 2


class Utils(object):

    @staticmethod
    def try_to_json(data, k):
        if k in data and data[k]:
            try:
                return json.loads(data[k])
            except Exception:
                return data[k]
        return None

    @staticmethod
    def split_str_bk(pre, src, step):
        if PY2:
            src = src.decode("utf-8")
        dst = ""
        strlist = src.split("\n")
        for s in strlist:
            start = 0
            size = len(s)
            while start < size:
                dst += (pre + s[start:start+step] + "\n")
                start += step
            dst += "\n"
        dst += "\n"
        return dst

    @staticmethod
    def split_str(pre, src, line_size):
        if PY2:
            src = src.decode("utf-8")
        dst = ""
        strlist = src.split("\n")
        for s in strlist:
            lsize = 0
            line = pre
            for c in s:
                line += c
                if ord(c) < 256:
                    lsize += 1
                else:
                    lsize += 2
                if lsize >= line_size:
                    dst += (line + "\n")
                    line = pre
                    lsize = 0
            dst += (line + "\n")
        dst += "\n"
        if PY2:
            dst = dst.encode("utf-8")
        return dst

    @staticmethod
    def is_valid_version(version):
        try:
            time.strptime(version, "%Y-%m-%d")
            return True
        except Exception as err:
            return False

    @staticmethod
    def file_existed(path, file_name):
        file_path = os.path.join(path, file_name)
        if os.path.exists(file_path):
            return True, file_path
        return False, file_path

    @staticmethod
    def load_json_msg(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            return data

    @staticmethod
    def dump_json_msg(filename, data):
        file_dir = os.path.split(filename)[0]
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        if not os.path.exists(filename):
            os.system(r'touch %s' % filename)
        with open(filename, "w") as f:
            json.dump(data, f,
                      indent=2,
                      separators=(',', ': '),
                      ensure_ascii=False,
                      sort_keys=True)