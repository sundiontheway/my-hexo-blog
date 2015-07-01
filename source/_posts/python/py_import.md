title: 关于python上一级目录文件import的问题
date: 2014-01-01
tags: python
---

*引入方式*

    from .. import module_name

_前提_

- Python 2.5+
- 当前文件和上级目录在同一个package内。
- 当前文件不是以`__main__`运行。
