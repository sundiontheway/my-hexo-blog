title: Openstack--Murano篇
p: openstack/
date: 2016-01-05 15:16:07
tags: openstack
---

从今天开始学习Openstack关于应用商店的模块——Murano。我的将以官方源码为基础，以文档为辅助，首先梳理出部署方法、调试方法、源码结构、应用开发流程。

[源码下载地址](https://git.openstack.org/cgit/?q=murano)  
[开发者文档地址](http://murano.readthedocs.org/en/latest/)

根据源码结构，可以分成以下几个repo：

* murano - is the main repository. It contains code for Murano API server, Murano engine and MuranoPL.
* murano-agent - agent which runs on guest VMs and executes deployment plan.
* murano-dashboard - Murano UI implemented as a plugin for OpenStack Dashboard.
* python-muranoclient - Client library and CLI client for Murano.

[Murano的「部署」]()  
[Murano的「调试」]()  
[Murano的「源码结构」]()  
[Murano的「应用开发」]()  
