title: screen | 常用命令小结
date: 2016-01-07 14:54:40
categories: 开源工具

---

Linux多窗口后台工具screen的常用操作。

<!--more-->

进入sceen输入`C-a ?`可以显示快捷键说明。  

__shell命令__：

`screen -S name` 启动一个新screen session  
`screen -x` 恢复到最后一个Detached的session

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
__快捷键__:

`C-a d` 挂起（Detached）当前session
`C-a "` 显示session列表，可以上下切换

_嵌套的 Screen 会话_

在一个嵌套的 screen 会话中卡住是非常容易的。一个常见的情况是：  
你从一个 screen 会话内启动了一个 ssh 会话，在这个 ssh 会话中，你又启动了 screen。默认地，响应 `C-a` 命令的是最先启动的外层screen。如果要向内层 screen 输入命令，用 `C-a a` 加上你的命令。  
例如： 

	C-a a d
	
断开内层 screen 会话

	C-a a K
	
杀死内层 screen 会话

以上基本能够解决我的需要了，其他常用命令可以参考[这里](https://wiki.archlinux.org/index.php/GNU_Screen)

