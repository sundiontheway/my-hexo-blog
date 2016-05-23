title: Doubango | C++接口层
date: 2014-03-01
categories: VoIP
tags: doubango

---

讲解一下Doubango模块C++接口层的封装分析。

<!--more-->

### 封装方法
doubango把所有ANSI C层库提供的方法都封装在doubango/bindings/\_common/
路径下的cxx文件中。我们只需要根据头文件给出的下层接口，组合出我们自己的接口提供给上层应用调用。
ANSI C层封装接口主要依据了tinyDEMO下提供的配置脚本样例,如core-doubango.sn（关于脚本的用法需要参考doubango提供的文档programmer-guide.pdf)


举例来说： 脚本中的这一行用于配置子网。

    ++cst --realm $$(domain) // ++cst config stack命令， --realm 操作， domain 操作参数

对应在\_common/中接口就是SipStack.h中的

    setRealm(const char* realm_uri);

也就是说，我们根据脚本中命令的顺序，依次调用\_common/下提供的接口，就可以完成音
视频环境的配置等操作。

