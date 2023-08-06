# -*- coding: UTF-8 -*-
"""
Author:wistn
since:2020-10-17
LastEditors:Do not edit
LastEditTime:2021-03-14
Description:
"""
import json
from datetime import datetime
from .conf import __version__
from .lib.org_noear_siteder_App import App
from .lib.org_noear_siteder_dao_engine_DdSource import DdSource
from .lib.org_noear_siteder_viewModels_site_MainViewModel import MainViewModel
from .lib.org_noear_siteder_viewModels_site_SearchViewModel import SearchViewModel
from .lib.org_noear_siteder_viewModels_site_TagViewModel import TagViewModel
from .lib.org_noear_siteder_viewModels_site_BookViewModel import BookViewModel
from .lib.org_noear_siteder_viewModels_site_Book4ViewModel import Book4ViewModel
from .lib.org_noear_siteder_viewModels_site_Book5ViewModel import Book5ViewModel
from .lib.org_noear_siteder_viewModels_site_Book6ViewModel import Book6ViewModel
from .lib.org_noear_siteder_viewModels_site_Book7ViewModel import Book7ViewModel
from .lib.org_noear_siteder_viewModels_site_Book8ViewModel import Book8ViewModel
from .lib.org_noear_siteder_viewModels_site_Section1ViewModel import Section1ViewModel
from .lib.org_noear_siteder_viewModels_site_Section2ViewModel import Section2ViewModel
from .lib.org_noear_siteder_viewModels_site_Section3ViewModel import Section3ViewModel
from .lib.org_noear_siteder_models_SectionModel import SectionModel
from .lib.org_noear_siteder_dao_db_BookNode import BookNode
from .lib.org_noear_siteder_utils_LogWriter import LogWriter


async def sited_test(sitedPath, key, callback):
    # ::1.实例化插件引擎 String sited = HttpUtil.get("http://x.x.x/xxx.sited.xml") py版要回调；或者从本地加载插件。
    with open(sitedPath, "r", encoding="utf-8") as fs:
        sited = fs.read()
    App().onCreate()
    source = await DdSource(App.getCurrent(), sited)
    print(
        datetime.now().strftime("%I:%M:%S %p")
        + " 开始测试插件 "
        + source.title
        + ".v"
        + str(source.ver)
        + " @"
        + source.author
        + " schema"
        + str(source.schema)
        + " dtype"
        + str(source.body.dtype()),
    )  # 打印本地时间
    # ::2.使用插件引擎获取数据
    isUpdate = True  # 是否(不读取缓存)刷新

    async def home_test(cback):
        print(
            "插件首面可测试"
            + ("hots " if source.hots.name else "")
            + ("updates " if source.updates.name else "")
            + ("tags " if source.tags.name else "")
            + "节点"
        )

        async def doTest(nodeName, cb):
            if not source.__dict__[nodeName].name:
                print(nodeName + "节点不存在")
                await cb()
                return
            nodeList = viewModel.__dict__[nodeName.replace("s", "List")]
            print(
                "\n获取插件首面"
                + nodeName
                + "节点数据如下（属性和sited_log.txt的有点不一样，为viewModel属性最终值，下同），详细数据见生成的logcat_stdout文件和sited_log.txt等。"
            )
            print(
                json.dumps(
                    nodeList[0:2]
                    if nodeName == "hots" or nodeName == "updates"
                    else nodeList[0:6],
                    ensure_ascii=False,
                    default=lambda obj: obj.__dict__,
                )
                + " ......"
            )
            # 对于返回数据截取前几条打印节省空间，下同。
            for i in range(nodeList.__len__()):
                if nodeList[i].url:
                    if nodeName == "hots" or nodeName == "updates":
                        if source.engine >= 22:
                            # 支持是分类的可能
                            if source.tag(nodeList[i].url).isMatch(nodeList[i].url):
                                await tag_test(nodeList[i].url, "from_" + nodeName, cb)
                            else:
                                await book_test(nodeList[i].url, "from_" + nodeName, cb)
                        else:
                            await book_test(nodeList[i].url, "from_" + nodeName, cb)
                    elif nodeName == "tags":
                        await tag_test(nodeList[i].url, "from_" + nodeName, cb)
                    return  # doTest函数内后面兜底的返回被停掉，下同
            await cb()  # doTest函数内兜底的返回，下同

        async def SdSourceCallback(code):
            # code == 1 表示请求url有返回html但不代表节点解析出正确数据; code == -1 表示请求url没有响应; code == -2 表示请求url过程出错且没有缓存;
            if code == 1:
                await cback(doTest)
            else:
                # 只要有部分有数据就加载（可能会有部分加载出错）
                if viewModel.total() > 0:
                    await cback(doTest)
                else:
                    print("网络请求出错 R.string.error_net")
                    await cback(None)

        viewModel = MainViewModel()
        await source.getNodeViewModel(
            viewModel, source.home, isUpdate, SdSourceCallback
        )

    async def search_test(cb):
        if not source.search.name:
            print("search节点不存在")
            await cb()
            return
        print("\nsearch节点url属性为 " + str(source.search.url.value) + " 搜索关键字为 " + key)

        async def doTest():
            print("\n获取search节点数据如下，详细数据见生成的logcat_stdout文件和sited_log.txt等")
            print(
                json.dumps(
                    viewModel.list[0:2],
                    ensure_ascii=False,
                    default=lambda obj: obj.__dict__,
                )
                + " ......"
            )
            for i in range(viewModel.list.__len__()):
                if viewModel.list[i].url:
                    if source.engine >= 26:
                        if source.tag(viewModel.list[i].url).isMatch(
                            viewModel.list[i].url
                        ):
                            await tag_test(viewModel.list[i].url, "from_search", cb)
                        else:
                            await book_test(viewModel.list[i].url, "from_search", cb)
                    else:
                        await book_test(viewModel.list[i].url, "from_search", cb)
                    return
            await cb()

        async def SdSourceCallback(code):
            # code == -3 表示节点url是空的且没有动态子项目; 其余code含义和home节点的一样
            if viewModel.total() == 0:
                if code < 0:
                    print("网络请求出错 R.string.error_net")
                else:
                    print("没有符合条件的内容 R.string.hint_search_no")
            if code == 1:
                await doTest()
            else:
                await cb()

        viewModel = SearchViewModel()
        await source.getNodeViewModel(
            viewModel, False, key, 1, source.search, SdSourceCallback
        )

    async def tag_test(tagUrl, from_where, cb):
        if not source._tag.name:
            print("tag节点不存在")
            await cb()
            return
        print(
            "\ntag节点<"
            + from_where
            + "> "
            + source.tag(tagUrl).onParse
            + "(或[若有]buildUrl/parseUrl)参数url为 "
            + tagUrl
        )

        async def doTest():
            print("\n获取tag节点数据如下，详细数据见生成的logcat_stdout文件和sited_log.txt等")
            print(
                json.dumps(
                    viewModel.list[0:2],
                    ensure_ascii=False,
                    default=lambda obj: obj.__dict__,
                )
                + " ......"
            )
            for i in range(viewModel.list.__len__()):
                if viewModel.list[i].url:
                    if source.subtag(viewModel.list[i].url).isMatch(
                        viewModel.list[i].url
                    ):
                        await subtag_test(
                            viewModel.list[i].url, "from_tag_" + from_where, cb
                        )
                    else:
                        await book_test(
                            viewModel.list[i].url, "from_tag_" + from_where, cb
                        )
                    return
            await cb()

        async def SdSourceCallback(code):
            # code == -3 表示节点url是空的且没有动态子项目; 其余code含义和home节点的一样
            if code == 1:
                await doTest()
            else:
                print("网络请求出错 R.string.error_net")
                await cb()

        viewModel = TagViewModel()
        await source.getNodeViewModel(
            viewModel,
            False,
            viewModel.currentPage,
            tagUrl,
            source.tag(tagUrl),
            SdSourceCallback,
        )

    async def book_test(bookUrl, from_where, cb):
        if not source._book.name:
            print("book节点不存在")
            await cb()
            return
        config = source.book(bookUrl)
        print(
            "\nbook节点<"
            + from_where
            + "> "
            + config.onParse
            + "(或[若有]buildUrl/parseUrl)参数url为 "
            + bookUrl
        )
        if bookUrl.startswith("sited://") or config.isWebrun():
            print("结果是用app打开 " + config.getWebUrl(bookUrl))
            await cb()
            return

        async def doTest():
            print(
                "\n获取book[dtype="
                + str(dtype)
                + "]节点数据如下，详细数据见生成的logcat_stdout文件和sited_log.txt等"
            )
            if dtype < 4:
                print(
                    "name:"
                    + (viewModel.name + " ," if viewModel.name else "")
                    + "\nauthor:"
                    + (viewModel.author + " ," if viewModel.author else "")
                    + "\nintro:"
                    + (viewModel.intro[0:20] + " ...... ," if viewModel.intro else "")
                    + "\nlogo:"
                    + (viewModel.logo + " ," if viewModel.logo else "")
                    + "\nupdateTime:"
                    + (viewModel.updateTime + " ," if viewModel.updateTime else "")
                    + "\nisSectionsAsc:"
                    + ("1 ," if viewModel.isSectionsAsc == True else "0 ,")
                    + "\nsections:"
                    + json.dumps(
                        viewModel.sections[0:2],
                        ensure_ascii=False,
                        default=lambda obj: obj.__dict__,
                    )
                    + " ......"
                )
                for i in range(viewModel.sections.__len__()):
                    if viewModel.sections[i].url:
                        await section_test(
                            viewModel.sections[i].url, "from_book_" + from_where, cb
                        )
                        return
                if viewModel.name == None:
                    print("网络请求出错 R.string.error_net")
                    await cb()
                    return
                if viewModel.sectionCount() == 0:
                    print("此内容已下架@_@?a R.string.error_no_content")
                await cb()
                return
            else:
                if dtype == 8:
                    tenItems = viewModel.items[0:10]
                for k in viewModel.__dict__:
                    if k == "items" or k == "pictures":
                        viewModel.__dict__[k] = viewModel.__dict__[k][0:2]
                        for j in range(viewModel.__dict__[k].__len__()):
                            if viewModel.__dict__[k][j] and getattr(
                                viewModel.__dict__[k][j], "section", None
                            ):
                                viewModel.__dict__[k][j].section = "省略"
                    elif (
                        type(viewModel.__dict__[k]) != str
                        and type(viewModel.__dict__[k]) != int
                        and type(viewModel.__dict__[k]) != bool
                        and viewModel.__dict__[k] != None
                    ):
                        viewModel.__dict__[k] = "省略"
                print(
                    json.dumps(
                        viewModel, ensure_ascii=False, default=lambda obj: obj.__dict__
                    )
                    + " ......"
                )
                if dtype == 8:
                    for i in range(tenItems.__len__()):
                        if tenItems[i].url and tenItems[i].isSectionOpen:
                            await section_test(
                                tenItems[i].url, "from_book_" + from_where, cb
                            )
                            return
                await cb()

        async def SdSourceCallback(code):
            # code == 99 表示login节点未登录; 其余code含义和home节点的一样
            if code == 1:
                await doTest()
            else:
                if code == 99:
                    print("login节点未登录")
                    await cb()
                else:
                    print("网络请求出错 R.string.error_net")
                    await cb()

        dtype = config.dtype()
        node = BookNode(bookUrl)
        viewModel = None
        if dtype <= 7:
            if dtype < 4:
                viewModel = BookViewModel(source, node)
            elif dtype == 4:
                viewModel = Book4ViewModel(source, node)
            elif dtype == 5:
                viewModel = Book5ViewModel(source, node)
            elif dtype == 6:
                viewModel = Book6ViewModel(source, node)
            elif dtype == 7:
                viewModel = Book7ViewModel(node)
            await source.getNodeViewModel(
                viewModel, isUpdate, bookUrl, source.book(bookUrl), SdSourceCallback,
            )
        elif dtype == 8:
            viewModel = Book8ViewModel(source, node)
            args = dict()
            if config.hasItems():
                for item in config._items:
                    print(
                        "book[8].item "
                        + json.dumps(item.attrs._items, ensure_ascii=False)
                    )
                    if item.key:
                        args[item.key] = "0"
            args["key1"] = "1"
            args["key2"] = "2"
            print("index.py 模拟book[dtype=8]填写输入框 " + json.dumps(args))
            await source.getNodeViewModel(
                viewModel,
                isUpdate,
                bookUrl,
                source.book(bookUrl),
                args,
                SdSourceCallback,
            )

    async def section_test(sectionUrl, from_where, cb):
        if not source._section.name:
            print("section节点不存在")
            await cb()
            return
        config = source.section(sectionUrl)
        print(
            "\nsection节点<"
            + from_where
            + "> "
            + config.onParse
            + "(或[若有]buildUrl/parseUrl)参数url为 "
            + sectionUrl
        )
        if sectionUrl.startswith("sited://") or config.isWebrun():
            print("结果是用app打开 " + config.getWebUrl(sectionUrl))
            await cb()
            return

        async def doTest():
            print(
                "\n获取section[dtype="
                + str(dtype)
                + "]节点数据如下，详细数据见生成的logcat_stdout文件和sited_log.txt等"
            )
            for k in viewModel.__dict__:
                if k == "items":
                    viewModel.__dict__[k] = viewModel.__dict__[k][0:2]
                    for i in range(viewModel.__dict__[k].__len__()):
                        if viewModel.__dict__[k][i] and getattr(
                            viewModel.__dict__[k][i], "section", None
                        ):
                            viewModel.__dict__[k][i].section = "省略"
                elif k == "isSectionsAsc":
                    viewModel.__dict__[k] = "省略"
                elif (
                    type(viewModel.__dict__[k]) != str
                    and type(viewModel.__dict__[k]) != int
                    and type(viewModel.__dict__[k]) != bool
                    and viewModel.__dict__[k] != None
                ):
                    viewModel.__dict__[k] = "省略"
            print(
                json.dumps(
                    viewModel, ensure_ascii=False, default=lambda obj: obj.__dict__
                )
                + " ......"
            )
            await cb()

        async def SdSourceCallback(code):
            # code == 99 表示login节点未登录; 其余code含义和home节点的一样
            if code == 1:
                await doTest()
            else:
                await cb()

        viewModel = None
        dtype = config.dtype()
        if dtype == 1:
            viewModel = Section1ViewModel()
            viewModel.currentSection = SectionModel()
            viewModel.fromSection = SectionModel()
        elif dtype == 2:
            viewModel = Section2ViewModel(SectionModel())
        elif dtype == 3:
            viewModel = Section3ViewModel()
        await source.getNodeViewModel(
            viewModel, False, sectionUrl, source.section(sectionUrl), SdSourceCallback
        )

    async def subtag_test(subtagUrl, from_where, cb):
        if not source._subtag.name:
            print("subtag节点不存在")
            await cb()
            return
        print(
            "\nsubtag节点<"
            + from_where
            + "> "
            + source.subtag(subtagUrl).onParse
            + "(或[若有]buildUrl/parseUrl)参数url为 "
            + subtagUrl
        )

        async def doTest():
            print("\n获取subtag节点数据如下，详细数据见生成的logcat_stdout文件和sited_log.txt等")
            print(
                json.dumps(viewModel.list[0:2], default=lambda obj: obj.__dict__)
                + " ......"
            )
            for i in range(viewModel.list.__len__()):
                if viewModel.list[i].url:
                    await book_test(
                        viewModel.list[i].url, "from_subtag_" + from_where, cb
                    )
                    return
            await cb()

        async def SdSourceCallback(code):
            # code == -3 表示节点url是空的且没有动态子项目; 其余code含义和home节点的一样
            if code == 1:
                await doTest()
            else:
                print("网络请求出错 R.string.error_net")
                await cb()

        viewModel = TagViewModel()
        await source.getNodeViewModel(
            viewModel,
            False,
            viewModel.currentPage,
            subtagUrl,
            source.subtag(subtagUrl),
            SdSourceCallback,
        )

    await callback(
        home_test, search_test, book_test, tag_test, section_test, subtag_test
    )
