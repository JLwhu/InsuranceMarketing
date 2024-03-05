# -*- coding:utf-8 -*-
import logging
import os
from datetime import date


class Logger:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Logger.__instance == None:
            Logger()
        return Logger.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Logger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            #创建一个logger
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)

            #创建一个handler，用于写入日志文件
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_dir = os.path.join(BASE_DIR, 'logs')# 指定文件输出路径，注意logs是个文件夹，一定要加上/，不然会导致输出路径错误，把logs变成文件名的一部分了
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            logname = os.path.join(log_dir,'%s.log'%(str(date.today().isoformat()))) #指定输出的日志文件名
            fh = logging.FileHandler(logname,encoding = 'utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码

            #创建一个handler，用于将日志输出到控制台
            ch = logging.StreamHandler()

            # 定义handler的输出格式
            formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # 给logger添加handler
            logger.addHandler(fh)
            logger.addHandler(ch)

            Logger.__instance = logger

