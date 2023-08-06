"""
Copyright 2021-2021 The TZIOT Authors. All rights reserved.
日志包.可打印实时日志或者流日志
Authors: jdh99 <jdh821@163.com>
lagan取名来自于宜家的水龙头"拉根"
"""

import logging
import logging.handlers
import os
import threading

from lagan.error import *

# 日志级别
LEVEL_OFF = logging.NOTSET
LEVEL_DEBUG = logging.DEBUG
LEVEL_INFO = logging.INFO
LEVEL_WARN = logging.WARN
LEVEL_ERROR = logging.ERROR

# 日志文件默认大小.单位:M字节
LOG_FILE_SIZE_DEFAULT = 10

_level_ch = {LEVEL_OFF: 'O', LEVEL_DEBUG: 'D', LEVEL_INFO: 'I', LEVEL_WARN: 'W', LEVEL_ERROR: 'E'}

# 日志颜色
# 30 黑色 31 红色 32 绿色 33 黄色 34 蓝色 35 紫红色 36 青蓝色 37 白色
_level_color = {LEVEL_OFF: 30, LEVEL_DEBUG: 37, LEVEL_INFO: 36, LEVEL_WARN: 35, LEVEL_ERROR: 31}

_logger = logging.getLogger('file_log')
_loggerStd = logging.getLogger('console_log')

_log_file_max_size = LOG_FILE_SIZE_DEFAULT * 1024 * 1024
_backup_count = 10
_is_load = False
_is_pause = False
_filter_level = logging.INFO
_is_color = False


def load(log_file_max_size: int = 10, backup_count: int = 10) -> Error:
    """
    模块载入
    :param log_file_max_size: 日志文件切割的大小.单位:M字节.如果为0表示不使用日志文件
    :param backup_count: 备份文件最大数量
    """
    global _is_load, _log_file_max_size, _backup_count

    if _is_load:
        return Error("already load")

    _log_file_max_size = log_file_max_size * 1024 * 1024
    if _backup_count > 0:
        _backup_count = backup_count

    _init_log()
    _is_load = True
    threading.Thread(target=_input).start()
    return Error("")


def _init_log():
    """初始化日志模块"""
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    if _log_file_max_size > 0:
        _logger.setLevel(_filter_level)

        if not os.path.exists('log'):
            os.mkdir('log')
        fh = logging.handlers.RotatingFileHandler('./log/log.log', maxBytes=_log_file_max_size * 1024 * 1024,
                                                  backupCount=_backup_count)
        fh.setFormatter(formatter)
        _logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    _loggerStd.setLevel(_filter_level)
    _loggerStd.addHandler(ch)


def _input():
    while True:
        s = input()
        if s == 'help':
            print_help()
            continue

        if s == "filter_error":
            set_filter_level(LEVEL_ERROR)
            print("set level:ERROR")
            resume()
            continue

        if s == "filter_warn":
            set_filter_level(LEVEL_WARN)
            print("set level:WARN")
            resume()
            continue

        if s == "filter_info":
            set_filter_level(LEVEL_INFO)
            print("set level:INFO")
            resume()
            continue

        if s == "filter_debug":
            set_filter_level(LEVEL_DEBUG)
            print("set level:debug")
            resume()
            continue

        if s == "filter_off":
            set_filter_level(LEVEL_OFF)
            print("set level:OFF")
            resume()
            continue

        if s == "pause":
            pause()
            print("pause print")
            continue

        if s == "resume":
            resume()
            print("resume print")
            continue


def print_help():
    print("*******************************************")
    print("            lagan help shell             ")
    print("current level:%c,is pause:%d\n" % (_level_ch[_filter_level], _is_pause))
    print("help:print help")
    print("filter_error:filter error level")
    print("filter_warn:filter warn level")
    print("filter_info:filter info level")
    print("filter_debug:filter debug level")
    print("filter_off:filter off level")
    print("pause:pause log")
    print("resume:resume log")
    print("*******************************************")


def set_filter_level(level: int):
    """设置日志级别"""
    global _filter_level

    _filter_level = level
    if _log_file_max_size > 0:
        _logger.setLevel(level)
    _loggerStd.setLevel(level)


def enable_color(enable: bool):
    """使能日志带颜色输出"""
    global _is_color
    _is_color = enable


def get_filter_level() -> int:
    """显示日志级别"""
    return _filter_level


def println(tag: str, level: int, msg: str, *args, **kwargs):
    """日志打印"""
    if not _is_load or _is_pause or _filter_level == LEVEL_OFF or level < _filter_level:
        return

    if _log_file_max_size > 0:
        _logger.log(level, _level_ch[level] + '/' + tag + ': ' + msg, *args, **kwargs)
    if _is_color:
        _loggerStd.log(level, '\033[7;' + '%d;' % _level_color[level] + '40m' + _level_ch[
            level] + '/' + tag + ': ' + msg + '\033[0m', *args, **kwargs)
    else:
        _loggerStd.log(level, _level_ch[level] + '/' + tag + ': ' + msg, *args, **kwargs)


def print_hex(tag: str, level: int, data: bytearray):
    """打印16进制字节流"""
    if not _is_load or _is_pause or _filter_level == LEVEL_OFF or level < _filter_level:
        return

    s = '\n****'
    for i in range(16):
        s += '%02x ' % i
    s += '\n---- : '
    for i in range(16):
        s += '-- '

    data_len = len(data)
    for i in range(data_len):
        if i % 16 == 0:
            s += '\n%04x : ' % i
        s += '%02x ' % data[i]

    prefix = '%c/%s' % (_level_ch[level], tag)
    new_format = prefix + ': '
    if _log_file_max_size > 0:
        _logger.log(level, new_format + s)
    if _is_color:
        _loggerStd.log(level, '\033[7;' + '%d;' % _level_color[
            level] + '40m' + new_format + '\033[0m' + s)
    else:
        _loggerStd.log(level, new_format + s)


def pause():
    """暂停日志打印"""
    global _is_pause
    _is_pause = True


def resume():
    """恢复日志打印"""
    global _is_pause
    _is_pause = False


def is_pause() -> bool:
    """是否暂停日志打印"""
    return _is_pause


def debug(tag: str, msg: str, *args, **kwargs):
    """打印debug信息"""
    println(tag, LEVEL_DEBUG, msg, *args, **kwargs)


def info(tag: str, msg: str, *args, **kwargs):
    """打印info信息"""
    println(tag, LEVEL_INFO, msg, *args, **kwargs)


def warn(tag: str, msg: str, *args, **kwargs):
    """打印warn信息"""
    println(tag, LEVEL_WARN, msg, *args, **kwargs)


def error(tag: str, msg: str, *args, **kwargs):
    """打印info信息"""
    println(tag, LEVEL_ERROR, msg, *args, **kwargs)
