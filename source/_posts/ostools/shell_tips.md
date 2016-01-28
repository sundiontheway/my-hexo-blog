title: shell小技巧
date: 2013-01-04
tags: bash
---

Linux Shell使用技巧整理。

<!--more-->

### 给shell增加每日提示
在`~/.bashrc`里，最后添加一条语句

    echo "Did you know that:"; whatis $(ls /bin | shuf -n 1)

这样每次打开终端，就会打印一条命令提示。


### 让git带颜色
在终端输入如下命令即可

    git config --global color.status auto
    git config --global color.diff auto
    git config --global color.branch auto
    git config --global color.interactive auto 

### 关于目录的操作
查看当前目录大小：

    du -sh
查看指定目录大小：

    du -sh /path/
查看当前目录文件总数：

    find . -type f |wc -l
查看指定目录文件总数：

    find /path/ -type f |wc -l
查看当前目录的目录总数：

    find . -type d |wc -l
查看指定目录的目录总数：

    find /path/ -type d |wc -l

### 网络操作
ssh登录带端口

    ssh -l [username] -p [port] [ip]

scp登录带端口

    scp -P [port] root@192.168.8.138:/home/ligh/index.php    root@192.168.8.139:/root

### kill所有python程序

    ps -ef | grep python | cut -c 10-15 | xargs kill -9
