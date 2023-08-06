#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2020-09-11
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
from sited_test_py.conf import __version__  # 该文件里面有配置


async def noop(*args):
    pass


exeCback = noop  # 拓展功能的回调函数
sitedPath = None
key = None


async def execute(sitedPath, key, exeCback):
    key = key or "我们"  # 这里填默认搜索关键字，当外部运行本文件没加上搜索参数时使用。

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


helpMeaasge = """Tests own SiteD plugin on Python
sitedPath: File path of .sited or .sited.xml.
key(optional): A keyword string that is used for searching on search node, if not be inputted, built-in keyword of bin.js would be used.
Usage: sited_test_py <sitedPath> [key]
Usage: sited_test_py [options]
Options:
--version  Show version number
--help     Show help
--demo     Tests a demo sited plugin
Examples:
sited_test_py /path/to/sited.sited.xml  #Outputs nodes' data to console on Python."""


def main():
    global sitedPath
    global key
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["version", "help", "demo"])
    except getopt.GetoptError:
        print(helpMeaasge)
        sys.exit(2)
    if opts.__len__():
        for opt, arg in opts:
            if opt == "--version":
                print(__version__)
                sys.exit()
            elif opt == "--help":
                print(helpMeaasge)
                sys.exit()
            elif opt == "--demo":
                sitedPath = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "demo.sited.xml"
                )
                print("# 该demo不是全部节点正常的，一来插件者未及时修复，二来也可以展示插件坏掉效果（会具体到失效节点的函数名）")
                asyncio.run(execute(sitedPath, None, exeCback))
    elif args.__len__():
        for i in range(0, args.__len__()):
            item = str(args[i])
            if re.search(r".+sited\.xml$", item) and os.path.exists(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), item)
            ):
                sitedPath = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), item
                )
                if args.__len__() == 1:
                    key = None
                elif i < args.__len__() - 1:
                    key = str(args[i + 1])
                else:
                    key = str(args[i - 1])
                asyncio.run(execute(sitedPath, key, exeCback))
                break
        if not sitedPath:
            print("Exception: .sited.xml or .sited file required")
            sys.exit(2)
    else:
        print(helpMeaasge)
        sys.exit()
    LogWriter.tryClose()
    print("-----结束测试引擎-----")


if __name__ == "__main__":
    main()
