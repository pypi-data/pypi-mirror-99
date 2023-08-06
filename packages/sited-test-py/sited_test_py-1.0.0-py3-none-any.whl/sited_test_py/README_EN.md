# sited_test_py

SiteD Engine for Python version, SiteD plugin testing tool, for SiteD developers testing their own plugins on computer/desktop platform.

[ [中文说明](README_CN.md)]

---

## Features

-   To automatically test SiteD plugin on Windows x86/Windows x64/Linux/macOS
-   Support `schema0/1/2`
-   Support running `buildUrl`, `parseUrl(CALL::)`, `parse(get/post/@null)`, `require(include online js library)`
-   Support `header(cookie/referer)`, `ua` configurations
-   Support `hots`, `updates`, `tags`, `tag(subtag)`, `search`, `book[12345678](sections)`, `section[123]` nodes

---

## API

```python
"""
* Outputs nodes' data to console on Python.
* @param sitedPath: A string of .sited or .sited.xml file's path, advises to absolute path.
* @param key: A keyword string that is used for searching on search node.
* @param callback: Outputs the entrance test functions of home/search/book node.
* @param nodeName@doTest@home_test: The string "hots", "updates" or "tags", which starts test function of hots/updates/tags node.
* @param bookUrl@book_test: Url argument of book node function, for test of book node alone.
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
        book_test: (bookUrl: str, from_where: "from_externalValue", cb: () -> None) -> None,
        tag_test: (tagUrl: str, from_where: str, cb: () -> None) -> None,
        section_test: (sectionUrl: str, from_where: str, cb: () -> None) -> None,
        subtag_test: (subtagUrl: str, from_where: str, cb: () -> None) -> None
    ) -> None
): None
```

---

### [ [Features](#Features)|[ API ](#API)|[Usage](#Usage)|[Configuration](#Configuration)|[Dependencies](#Dependencies)|[Todo](#Todo)|[SpecialThanks](#SpecialThanks)|[Links](#Links)|[CHANGELOG.md](CHANGELOG.md)]

## Usage

> #### 1. After pip installs the project as `python -m pip install sited_test_py`

A. Uses Python to run a py script like demo.py which imports the API within the sited_test_py directory.

```python
# demo.py, has written file path of .sited or .sited.xml
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
key = "we"
async def callback(home_test, search_test, book_test, *args):
    async def cb(*args):pass

    async def cback(doTest):
        if doTest:
            await doTest("hots", cb)
            await doTest("updates", cb)
            await doTest("tags", cb)

    await home_test(cback)
    await search_test(cb)
    # bookUrl = "http://... url argument of book node function such as the link in favorites"
    # await book_test(bookUrl, "from_externalValue", cb)

asyncio.run(sited_test(sitedPath, key, callback))
LogWriter.tryClose()
```

```bash
cd /path/to/site-packages/sited_test_py
python demo.py
```

or B.

> need not to cd, input single `sited_test_py` on CLI will get:

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

or C. By the way, using [Code Runner extension](https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner) or built-in debugger to call Python is quick, when you are editing sited plugin file on VS Code.

a. You can start Code Runner when editor focuses sited plugin file, after configuring Code Runner to execute .sited and .sited.xml as python command below, test the plugin directly, need not to write the plugin path, it will be identified by \$fullFileName.

```json
"code-runner.executorMapByGlob": {
    "*.{sited,sited.xml}": "python /path/to/site-packages/sited_test_py/bin.py $fullFileName key"
}
// replace /path/to/node_modules/sited_test_py/bin.py with actual bin.py's path. If (key) be deleted, that built-in keyword of bin.py would be used.
```

or b. You can start debugging (sited_test_py) when editor focuses sited plugin file, after adding a debug configure to execute as python command below, test the plugin directly, need not to write the plugin path, it will be identified by \${file}.

```json
"launch": {
    "version": "0.2.0",
    "configurations": [
        {
            "type": "python",
            "request": "launch",
            "name": "sited_test_py",
            "program": "/path/to/site-packages/sited_test_py/bin.py",
            "args": ["${file}", "searchword"]
        }
    ]
}
```

replace /path/to/site-packages/sited_test_py/bin.py with actual bin.py's path. If `"searchword"` was deleted, that built-in keyword of bin.py would be used.

---

## Configuration

-   Configuration which controls making of sited_log.txt/sited_error.txt/sited_print.txt and sited (cache directory) under the 'files' dir beside this README_EN file, see in conf.py file.

---

## Dependencies

-   [Python](https://www.python.org/) 3.7 or above, for asyncio.run

-   [pyChakraCore](https://github.com/wistn/pyChakraCore) a runtime run SiteD plugin's js code, a python package developed by me

---

## Todo

-   Support login node

---

## SpecialThanks

### The 'lib' library(excludes main_res_raw_xx.js) is totally translated from big parts of Noear's open source [SiteD Engine](https://github.com/noear/SiteD) v35 APP JAVA code to Python language by me. Thank you!

## Links

-   [SiteD plugin center](http://sited.noear.org/): Official SiteD plugin center.

-   [ddcat_plugin_develop](https://www.kancloud.cn/magicdmer/ddcat_plugin_develop): Knowledge about sited plugin development.

-   [DDCat SiteD](https://github.com/Yinr/DDCa-SiteD.vscode-ext): Syntax extension for VS Code, enabled .sited and .sided.xml files in sited language, support syntax highlight.

-   [generators-sited-plugin](https://github.com/htynkn/generators-sited-plugin): Yeoman generator for sited plugin.

-   [sited_test](https://github.com/wistn/sited_test) SiteD Engine for Node JavaScript version, SiteD plugin testing tool.
