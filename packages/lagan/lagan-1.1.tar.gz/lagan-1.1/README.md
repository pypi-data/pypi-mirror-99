# lagan

## 介绍
基于python语言的日志库.

lagan取名来自于宜家的水龙头"拉根"。

本软件包已上传到pypi，可输入命令直接安装。
```shell
pip install lagan
```

## 功能
- 支持日志在终端实时打印
- 支持日志保存在文件
- 支持日志不保存文件,仅终端打印
- 支持日志文件自动分割
- 支持终端交互控制日志输出级别等功能
- 支持二进制流打印
- 支持带颜色的日志打印

## 示例
```python
# 日志模块载入.全局载入一次,参数是分割文件大小,默认是10M
lagan.load()

# 默认输出界别是info,本行不会打印
lagan.debug("case4", "debug test print")

lagan.info("case4", "info test print")
lagan.warn("case4", "warn test print")
lagan.error("case4", "error test print")
```

输出：
````
2021-03-20 11:59:35,196 - lagan.py:114 - I/case4: info test print
2021-03-20 11:59:35,196 - lagan.py:114 - W/case4: warn test print
2021-03-20 11:59:35,197 - lagan.py:114 - E/case4: error test print
````

在本地会新建log文件夹，并新建日志文件。

## 二进制流打印
```python
lagan.load()
s = bytearray()
for i in range(100):
    s.append(i)
lagan.print_hex('case2', lagan.LEVEL_ERROR, s)
```

输出：
````
2021-03-20 12:25:04,629 - lagan.py:207 - E/case2: 
****00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 
---- : -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
0000 : 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 
0010 : 10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f 
0020 : 20 21 22 23 24 25 26 27 28 29 2a 2b 2c 2d 2e 2f 
0030 : 30 31 32 33 34 35 36 37 38 39 3a 3b 3c 3d 3e 3f 
0040 : 40 41 42 43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f 
0050 : 50 51 52 53 54 55 56 57 58 59 5a 5b 5c 5d 5e 5f 
0060 : 60 61 62 63 
````

## 终端交互
````
*******************************************
            lagan help shell             
current level:I,is pause:false
help:print help
filter_error:filter error level
filter_warn:filter warn level
filter_info:filter info level
filter_debug:filter debug level
filter_off:filter off level
pause:pause log
resume:resume log
*******************************************
````

可以在终端敲对应的命令控制日志功能。

## 颜色控制
可以使用EnableColor函数开控制打开或者关闭日志颜色，默认关闭颜色。
````python
lagan.load()
lagan.set_filter_level(lagan.LEVEL_DEBUG)
lagan.enable_color(True)
lagan.println('case1', lagan.LEVEL_OFF, 'TestPrintOut1:%d', 100)
lagan.println('case1', lagan.LEVEL_DEBUG, 'TestPrintOut1:%d', 100)
lagan.println('case1', lagan.LEVEL_INFO, 'TestPrintOut1:%d', 100)
lagan.println('case1', lagan.LEVEL_WARN, 'TestPrintOut1:%d', 100)
lagan.println('case1', lagan.LEVEL_ERROR, 'TestPrintOut1:%d', 100)

s = bytearray()
for i in range(100):
    s.append(i)
lagan.print_hex('case2', lagan.LEVEL_INFO, s)
````

![图片](https://user-images.githubusercontent.com/1323843/111859054-e66e4800-8978-11eb-9b68-b0c0c77e90ac.png)

## 日志文件控制
文件分割大小设置为0,则不会保存到日志文件,仅终端打印：
```python
lagan.load(0)
```
