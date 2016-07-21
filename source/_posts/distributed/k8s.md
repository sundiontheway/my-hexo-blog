title: Kubernetes (k8s) 运行实例总结
date: 2016-07-21 14:39:29
categories: 经验分享
tags: kubernetes

---

关于Kubernetes的结构，最近研究了一下，由于项目需要，所以结合我做的内容简单总结一下。

<!--more-->

## 重要名词解释

- namespace：对象所属的命名空间，如果不指定，系统则会将对象置于名为“default”的系统命名空间中
- Replication Controller：一个管理器，用于创建多个pod副本
- pod：一个包含若干个容器实例的「文件夹」
- rc：一个容器实例
- service：由多个pod副本映射到同一个端口，共同组成的一个服务

## 结构

![](http://ww2.sinaimg.cn/large/4a41845fjw1f61j4m7s3rj20bz0digm3.jpg)

网上的k8s介绍都引用了一张kubernetes后台服务的结构图，但是图中并没有展现实际运行中的状态。我特意画了上图以便理解。

图中一个namespace相当于我们开发中的一个「产品」，这个产品由多个后台服务(service)共同组成。这些服务实例化后就对应Kubernetes的若干个容器实例(rc)。每一组rc由一个pod统一管理，pod类似文件夹，管理着内部rc的生命周期。

有时候我们后台服务需要多个副本(replicas)，就需要在创建服务时候指定pod的数量，即`replicas`这个参数。图中指定`replicas=2`，即产生两组副本，相同的rc副本对外共用端口，构成一个服务的实例。

## 启动一个服务的流程

了解了运行状态，就可以用Kubernetes API来走一遍流程了。

首先创建一个namespace：

```
POST /api/v1/namespaces
```

POST请求的参数可以参考文末的API文档。

然后通过ReplcasController接口创建若干个rc。

```
POST /api/v1/namespaces/{namespace}/relicascontroller
```

之后为rc指定service：

```
POST /api/v1/namespaces/{namespace}/services
```

## 参考资料

http://www.infoq.com/cn/articles/Kubernetes-API
http://blog.liuts.com/post/247/