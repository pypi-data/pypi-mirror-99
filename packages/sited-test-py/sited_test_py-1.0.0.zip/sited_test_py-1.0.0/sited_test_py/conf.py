# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2020-09-11
LastEditors:Do not edit
LastEditTime:2021-03-08
Description:
"""
__version__ = "1.0.0"
# 配置说明：1. 多多猫缓存中的文本缓存sited文件夹在本引擎也默认对应生成（测试插件后在files文件夹下出现，注意有时插件节点没返回数据时可以删除这个文件夹看看）。开启缓存后，异步请求的网页在有效期内再次请求才是同步。如要禁止缓存，可对下行注释，作用于 lib/org_noear_sited___FileCache.py;
enableFileCache = True

# 2. SiteD插件容器/多多猫安卓版设置中有开发者模式开关，控制files文件夹里是否生成 sited_log.txt, sited_error.txt, sited_print.txt文件。多多猫里默认为假，本py版引擎默认为真即生成（测试插件后在files文件夹下出现），如要禁止生成，可取消下行注释，作用于 lib/org_noear_siteder_dao_Setting.py;
isDeveloperModel = True

# 3. 上面1项为真（生成）的前提下，SiteD插件文件中开头的debug参数(1/0)，会控制本引擎files文件夹里生成的sited_log.txt中是否显示各节点parse解析后返回的数据，为0时只显示节点parse/parseUrl所要解析的网址，不影响sited_error.txt, sited_print.txt文件。
# 4. Log模块( lib/android_util_Log.py)是本py版引擎模仿安卓logcat功能转储消息日志，默认生成到 files/logcat_stdout.txt（测试插件后在files文件夹下出现），不受上面2项开关参数的影响且显示消息日志过程会更加丰富。
# 5. 上面1项中，其中VERBOSE类型日志消息写入 files/logcat_stdout文件时，如要同时print打印（每条消息开头部分）到运行本引擎的控制台，取消以下VERBOSE_log注释。也可以取消VERBOSE_trace的注释来打印堆栈跟踪
# VERBOSE_log = 1
# VERBOSE_trace = 1
