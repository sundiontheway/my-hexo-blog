title: Openstack--Murano环境搭建
p: /openstack/murano_env.md
date: 2016-01-06 10:06:53
tags: openstack
---

官方有两种安装方法，devstack安装和手动安装。因为之前已经安装过其他模块，所以这里按照官方文档进行手动安装。

[官方文档地址](http://murano.readthedocs.org/en/latest/install/manual.html)

由于本人系统是OSX，所以以下操作都在docker中完成，镜像使用官方hub上的ubuntu镜像。

* 安装基本环境

```
sudo apt-get install python-pip python-dev \
  libmysqlclient-dev libpq-dev \
  libxml2-dev libxslt1-dev \
  libffi-dev
```

* 安装tox

```
sudo pip install tox
```

* 安装mysql（这里有问题，官方说使用默认的sqlite也可以，但是当我进行到`6. Create database tables for Murano.`那一步时出现一个错误，所以这里需要特别注意，也希望有人明白原因不吝赐教）

```
apt-get install python-mysqldb mysql-server
```

```
mysql -u root -p

mysql> CREATE DATABASE murano;
mysql> GRANT ALL PRIVILEGES ON murano.* TO 'murano'@'localhost' \
    IDENTIFIED BY 'MURANO_DBPASS';
mysql> exit;
```

* 下载源码，生成配置文件

```
mkdir ~/murano
cd ~/murano/murano
tox -e genconfig
```

```
cd ~/murano/murano/etc/murano
ln -s murano.conf.sample murano.conf
```

* 编辑`murano.conf`配置文件
* 创建虚拟环境，安装依赖

```
cd ~/murano/murano
tox
```

* 创建数据库表

```
cd ~/murano/murano
tox -e venv -- murano-db-manage \
  --config-file ./etc/murano/murano.conf upgrade
```

未完待补充

*20150107 最后更新*

