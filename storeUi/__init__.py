# -*- coding: utf-8 -*-
# @Time    : 10/23/2019 4:31 PM
# @Author  : HR
# @File    : __init__.py
import hashlib


def curlmd5(src):
    m = hashlib.md5()
    m.update(src.encode('UTF-8'))
    return m.hexdigest()

print(curlmd5('hr'))