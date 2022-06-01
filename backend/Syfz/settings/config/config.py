#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import configparser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'config/conf.ini'))

if __name__ == '__main__':
    print(BASE_DIR)
    print(config.get('mysql', 'DB_NAME'))
    print(config.get('WEBMONITOR', 'PhantomJSPath'))
