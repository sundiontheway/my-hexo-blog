Title: makefile常用函数
Date: 2014-01-04
Modified: 2014-01-04
Category: 学习笔记
Tags: makefile
Slug: makefile
Author: Steve D. Sun

###文件名操作函数
下面我们要介绍的函数主要是处理文件名的。每个函数的参数字符串都会被当做一个或是一系列的文件名来对待。

`$(dir <names...>)`

    名称：取目录函数——dir。
    功能：从文件名序列<names>中取出目录部分。目录部分是指最后一个反斜杠（“/”）之前的部分。如果没有反斜杠，那么返回“./”。
    返回：返回文件名序列<names>的目录部分。
    示例： $(dir src/foo.c hacks)返回值是“src/ ./”。

`$(notdir <names...>)`

    名称：取文件函数——notdir。
    功能：从文件名序列<names>中取出非目录部分。非目录部分是指最後一个反斜杠（“/”）之后的部分。
    返回：返回文件名序列<names>的非目录部分。
    示例： $(notdir src/foo.c hacks)返回值是“foo.c hacks”。

`$(suffix <names...>)`

    名称：取後缀函数——suffix。
    功能：从文件名序列<names>中取出各个文件名的后缀。
    返回：返回文件名序列<names>的后缀序列，如果文件没有后缀，则返回空字串。
    示例：$(suffix src/foo.c src-1.0/bar.c hacks)返回值是“.c .c”。

`$(basename <names...>)`

    名称：取前缀函数——basename。
    功能：从文件名序列<names>中取出各个文件名的前缀部分。
    返回：返回文件名序列<names>的前缀序列，如果文件没有前缀，则返回空字串。
    示例：$(basename src/foo.c src-1.0/bar.c hacks)返回值是“src/foo src-1.0/bar hacks”。

`$(addsuffix <suffix>,<names...>)`

    名称：加后缀函数——addsuffix。
    功能：把后缀<suffix>加到<names>中的每个单词后面。
    返回：返回加过后缀的文件名序列。
    示例：$(addsuffix .c,foo bar)返回值是“foo.c bar.c”。

`$(addprefix <prefix>,<names...>)`

    名称：加前缀函数——addprefix。
    功能：把前缀<prefix>加到<names>中的每个单词后面。
    返回：返回加过前缀的文件名序列。
    示例：$(addprefix src/,foo bar)返回值是“src/foo src/bar”。

`$(join <list1>,<list2>)`

    名称：连接函数——join。
    功能：把<list2>中的单词对应地加到<list1>的单词后面。如果<list1>的单词个数要比<list2>的多，那么，<list1>中的多出来的单词将保持原样。如果<list2>的单词个数要比<list1>多，那么，<list2>多出来的单词将被复制到<list2>中。
    返回：返回连接过后的字符串。
    示例：$(join aaa bbb , 111 222 333)返回值是“aaa111 bbb222 333”。

