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

我接下来的几篇文章会以如下大纲来归纳学习进度：  
1. 使用  
2. 源码分析  
3. 应用开发部署  
4. Murano服务的Docker化部署  

--
目录

[Murano的「使用」]()  
[Murano的「源码分析」]()  
[Murano的「应用开发和部署」]()  
[Murano的「部署」](http://www.v2steve.com/2016/01/06/openstack/murano_env/)  
