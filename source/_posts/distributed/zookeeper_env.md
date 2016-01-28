title: ZooKeeper环境搭建
date: 2014-10-11
tags: zookeeper
---

简单的说，zookeeper设计来解决分布式应用中的统一命名服务，状态同步服务，集群管理，分布式应用配置等问题。

<!--more-->

### zookeeper的安装

* __单机模式__

1 官网下载3.4.6版本。<http://mirror.bit.edu.cn/apache/zookeeper/zookeeper-3.4.6/zookeeper-3.4.6.tar.gz>, 解压到任意目录（我放在`~/`下）。
2 配置java7环境，centos需要先卸载系统自带的java环境。

    rpm -qa|grep java                       # 查找安装的openjdk版本
    yum -y remove java <查到的openjdk版本>  # 卸载

从SUN官网下载最新版本的JDK安装包，然后执行`rpm -ivh`命令安装：

    rpm -ivh jdk-8u20-linux-x64.rpm

安装成功后，执行`java -version`查看java版本是否为最新，然后执行`jps`若命令可执行，则jdk没问题，继续下一步。

3 修改`/etc/profile`， 增加两行：

    export ZOOKEEPER_HOME=/home/<你的家目录名>/zookeeper-3.4.6
    export PATH=$PATH:$ZOOKEEPER_HOME/bin:$ZOOKEEPER_HOME/conf

4 配置`zookeeper-3.4.6/conf/`目录下的zoo.cfg文件。（如果没有，可以重命名zoo_sample.cfg为zoo.cfg），第一次使用都使用默认即可。

    tickTime：基本事件单元，以毫秒为单位。它用来指示心跳，最小的 session 过期时间为两倍的 tickTime
    dataDir：存储内存中数据库快照的位置，如果不设置参数，更新事务日志将被存储到默认位置
    dataLogDir: 如果设置此项，则日志文件会存储该位置下，和数据库快照文件分开存放
    clientPort：监听客户端连接的端口

* __伪集群模式__
* __集群模式__

## zookeeper的python接口zkpython安装
1 进入zookeeper的`zookeeper-3.4.6/src/c/`目录，编译安装C语言库。

    cd zookeeper-3.4.6/src/c/
    ./configure
    make
    make install

2 下载zkpython安装包<http://pypi.python.org/packages/source/z/zkpython>，解压到任意目录，在目录下执行：

    python setup.py install

3 测试是否安装成功：

    python
    > import zookeeper

如果提示错误`ImportError: libzookeeper_mt.so.2: cannot open shared object file: No such file or directory`，则在`/etc/profile`文件最后添加

    export LD_LIBRARY_PATH=/usr/local/lib



