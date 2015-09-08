title: github新机器配置
date: 2013-01-01
tags: github
---

### 下载ssh,git

    sudo apt-get install ssh git

### 配置git

    git config --global user.name yourname
    git config --global user.email youremail

### 生成公钥
在～/下输入

    ssh-keygen -t rsa -C “address@xxx.com”

一路按回车，或者根据提示设置一个私钥密码。
之后就会在 `~/.ssh/` 下生成密钥，其中 `id\_rsa.pub` 是公钥，用记事本打开它，复制全部，在个
github配置ssh key页面粘贴公钥

### 添加私钥到ssh
我之前一直被服务器拒绝，就是这部没有做。

    ssh -add ~/.ssh/id_rsa

### 测试是否可以登录

    ssh git@github.com

最后在github首页上创建新`repo`，按照网页下边提示的步骤完成仓库初始化
