title: screen常用命令小结
p: /ostools/screen.md
date: 2016-01-07 14:54:40
tags: screen
---
进入sceen厚输入`C-a ?`都可以显示快捷键说明。  

__外部常用命令__：

`screen -S name` 启动一个新screen session  
`screen -x` 恢复到最后一个Detached的session`

如果想杀死一个已经detached的screen会话，可以使用以下命令：

    screen -X -S [session # you want to kill] quit

举例：

```
[root@localhost ~]# screen -ls
There are screens on:
        9975.pts-0.localhost    (Detached)
        4588.pts-3.localhost    (Detached)
2 Sockets in /var/run/screen/S-root.

[root@localhost ~]# screen -X -S 4588 quit
[root@localhost ~]# screen -ls
There is a screen on:
        9975.pts-0.localhost    (Detached)
1 Socket in /var/run/screen/S-root.
```
__内部常用命令__:

`C-a d` 挂起（Detached）当前session
`C-a "` 显示session列表，可以上下切换

以上基本能够解决我的需要了，其他常用命令可以参考[这里](https://www.ibm.com/developerworks/cn/linux/l-cn-screen/)

