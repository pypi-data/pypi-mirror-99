# sited_test_py

SiteD 引擎 Python 版、SiteD 插件测试工具，用于多多猫插件者在电脑/桌面平台测试自己的插件。

[ [README-EN](README_EN.md)]

---

## 特性

-   在 Windows x86/Windows x64/Linux/macOS 上自动测试 SiteD 插件
-   支持 `schema0/1/2`
-   支持运行 `buildUrl`, `parseUrl(CALL::)`, `parse(get/post/@null)`, `require(含网络 js 库)`
-   支持 `header(cookie/referer)`, `ua` 配置
-   支持 `hots`, `updates`, `tags`, `tag(subtag)`, `search`, `book[12345678](sections)`, `section[123]` 节点

---

## 应用接口

```python
"""
* 在 Python 环境输出节点数据到控制台
* @param sitedPath: .sited或.sited.xml文件路径, 建议填绝对路径
* @param key: 用于在搜索节点上搜索的关键词字符串
* @param callback: 输出home/search/book节点的入口测试函数
* @param nodeName@doTest@home_test: 字符串"hots", "updates" 或者 "tags", 用于开始hots/updates/tags节点的测试函数
* @param bookUrl@book_test: book节点函数的url参数, 用于book节点单独测试
"""
sited_test(
    sitedPath: str,
    key: str,
    callback: (
        home_test: (
            cback: (
                doTest: (nodeName: "hots" | "updates" | "tags", cb: () -> None
                ) -> None
            ) -> None
        ) -> None,
        search_test: (cb: () -> None) -> None,
        book_test: (bookUrl: str, from_where: "from_外部传值", cb: () -> None) -> None,
        tag_test: (tagUrl: str, from_where: str, cb: () -> None) -> None,
        section_test: (sectionUrl: str, from_where: str, cb: () -> None) -> None,
        subtag_test: (subtagUrl: str, from_where: str, cb: () -> None) -> None
    ) -> None
): None
```

---

### [[特性](#特性)|[应用接口](#应用接口)|[使用](#使用)|[配置](#配置)|[依赖](#依赖)|[待办](#待办)|[致谢](#致谢)|[友链](#友链)|[CHANGELOG.md](CHANGELOG.md)]

## 使用

> #### 1. 以 `python -m pip install sited_test_py` 在 pip 安装项目之后

A. 在 sited_test_py 文件夹里通过 Python 运行像 demo.py 般调用 API 接口的 py 脚本：

```python
# demo.py文件，已经写了 .sited 或 .sited.xml 文件路径
import asyncio
import os
import sys

if __package__ == "" or __package__ == None:
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
    sys.path.insert(0, path)
from sited_test_py import sited_test, LogWriter
sitedPath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "demo.sited.xml"
)
key = "我们"
async def callback(home_test, search_test, book_test, *args):
    async def cb(*args):pass

    async def cback(doTest):
        if doTest:
            await doTest("hots", cb)
            await doTest("updates", cb)
            await doTest("tags", cb)

    await home_test(cback)
    await search_test(cb)
    # bookUrl = "http://... book节点函数的url参数如已收藏漫画链接"
    # await book_test(bookUrl, "from_外部传值", cb)

asyncio.run(sited_test(sitedPath, key, callback))
LogWriter.tryClose()
```

```bash
cd /path/to/site-packages/sited_test_py
python demo.py
```

或者 B.

> 不需要 cd，在命令行界面单独输入 `sited_test_py` 会看到:

```bash
Tests own SiteD plugin on Python

sitedPath: File path of .sited or .sited.xml.
key(optional): A keyword string that is used for searching on search node, if not be inputted, built-in keyword of bin.py would be used.

Usage: sited_test_py <sitedPath> [key]
Usage: sited_test_py [options]

Options:
  --version  Show version number
  --help     Show help
  --demo     Tests a demo sited plugin

Examples:
  sited_test_py /path/to/sited.sited.xml  #Outputs nodes' data to console on Python.
```

或者 C. 其实，在 VS Code 上编辑 sited 插件文件时用 [Code Runner 插件](https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner) 或者内置的调试器来调用 Python 是很快的。

a. 配置 Code Runner 对.sited 和 .sited.xml 文件通过以下 python 命令运行，就可以在编辑器当前焦点所处 sited 插件文件时启动 Code Runner，直接测试插件，不需要填写插件路径，会通过 \$fullFileName 识别。

```json
"code-runner.executorMapByGlob": {
    "*.{sited,sited.xml}": "python /path/to/site-packages/sited_test_py/bin.py $fullFileName key"
}
// 把 /path/to/site-packages/sited_test_py/bin.py 替换为bin.py实际路径。如果删除(key)，会使用 bin.py 内置的关键词
```

或者 b. 增加新的调试配置通过以下 python 命令运行，就可以在编辑器当前焦点所处 sited 插件文件时启动调试(sited_test_py)，直接测试插件，不需要填写插件路径，会通过 \${file} 识别。

```json
"launch": {
    "version": "0.2.0",
    "configurations": [
        {
            "type": "python",
            "request": "launch",
            "name": "sited_test_py",
            "program": "/path/to/site-packages/sited_test_py/bin.py",
            "args": ["${file}", "搜索词"]
        }
    ]
}
```

把 /path/to/site-packages/sited_test_py/bin.py 替换为 bin.py 实际路径。如果删除 `"搜索词"` ，会使用 bin.py 内置的关键词

---

## 配置

-   控制本 README_CN 文件旁边的'files'文件夹里的 sited_log.txt/sited_error.txt/sited_print.txt 和 sited(缓存文件夹) 的生成的配置，见 conf.py 文件

---

## 依赖

-   [Python](https://www.python.org/) 3.7 或以上，为了 asyncio.run

-   [pyChakraCore](https://github.com/wistn/pyChakraCore) 一个运行 SiteD 插件 js 代码的虚拟机，是由我开发的 python 包

---

## 待办

-   支持 login 节点

---

## 致谢

### 里面 'lib' 库（不含 main_res_raw_xx.js）是我将 Noear 开源的 [SiteD 引擎](https://github.com/noear/SiteD) v35 容器大部分 JAVA 代码翻译成的 Python 语言。感谢！

## 友链

-   [SiteD plugin center](http://sited.noear.org/) SiteD 插件中心官方版

-   [ddcat_plugin_develop](https://www.kancloud.cn/magicdmer/ddcat_plugin_develop) 多多猫插件开发指南，关于多多猫插件开发相关知识

-   [DDCat SiteD](https://github.com/Yinr/DDCa-SiteD.vscode-ext) VS Code 扩展插件，对 .sited 和 .sited.xml 文件识别为 SiteD 语言，提供语法高亮

-   [generators-sited-plugin](https://github.com/htynkn/generators-sited-plugin) Yeoman 生成器快速初始化项目

-   [sited_test](https://github.com/wistn/sited_test) SiteD 引擎 Node.js 版、SiteD 插件测试工具
