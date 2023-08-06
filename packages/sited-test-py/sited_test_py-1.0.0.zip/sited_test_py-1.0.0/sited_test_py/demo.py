#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2020-04-28
LastEditors:Do not edit
LastEditTime:2021-03-14
Description:
"""
import asyncio
import re
import os
import sys
import getopt

if __package__ == "" or __package__ == None:
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
    sys.path.insert(0, path)
from sited_test_py import sited_test, LogWriter


async def noop(*args):
    pass


exeCback = noop  # 拓展功能的回调函数
sitedPath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "demo.sited.xml"
)  # 或'单个插件的绝对路径.sited.xml'
key = "我们"  # 这里填搜索关键字


async def execute(sitedPath, key, exeCback):
    async def callback(
        home_test, search_test, tag_test, book_test, section_test, subtag_test
    ):
        async def cb(*args):
            print("-----结束测试本入口节点-----")

        async def cback(doTest):
            if doTest:
                await doTest("hots", cb)
                await doTest("updates", cb)
                await doTest("tags", cb)

        # 每个入口流程测试，会运行到最终section/book节点，不想测试的入口可以注释，也可以取消bookUrl所在注释直接测试book节点（bookUrl填写书目资源的url）
        await home_test(cback)
        await search_test(cb)
        # bookUrl = "http://comic.oacg.cn/index.php?m=Index&a=comicinfo&comic_id=MEbIk7ReT0CuK1vP21DMcQ"
        # await book_test(bookUrl, "from_外部传值", cb)
        print("-----结束测试本插件-----\n")

    await sited_test(sitedPath, key, callback)


print("# 该demo不是全部节点正常的，一来插件者未及时修复，二来也可以展示插件坏掉效果（会具体到失效节点的函数名）")
asyncio.run(execute(sitedPath, key, exeCback))
sitedDirPath = "多个插件所在文件夹路径"
# 这里可以填多个插件共同所在的文件夹路径，后面几行注释的内容在取消注释后为多个插件批量测试模式(同时要注释上面一行 asyncio.run(execute(sitedPath, key, exeCback)) ，保留注释则只测试上面sitedPath填写的插件

# fileNames = os.listdir(sitedDirPath)
# fileNames = list(filter(lambda item: re.search(r".+sited\.xml$", item), fileNames))
# for name in fileNames[0:3]:
#     sitedPath = os.path.join(sitedDirPath, name)
#     asyncio.run(execute(sitedPath, key, exeCback))

LogWriter.tryClose()
print("-----结束测试引擎-----")
