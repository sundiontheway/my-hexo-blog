title: Doubango | proxy,pruducer,codec三种插件的创建
date: 2014-03-01
categories: 多媒体
tags: doubango
---

Doubango的生产者-消费者模式，三种插件的注册流程。

<!--more-->

`tmedia_producer.c`中的`tmedia_producer_create`这个函数：

```c
    tmedia_producer_t* tmedia_producer_create(tmedia_type_t type, uint64_t session_id)
    {
        tmedia_producer_t* producer = tsk_null;
        const tmedia_producer_plugin_def_t* plugin;
        tsk_size_t i = 0;

        while((i < TMED_PRODUCER_MAX_PLUGINS) && (plugin = __tmedia_producer_plugins[i++])){
            if(plugin->objdef && plugin->type == type){
                if((producer = tsk_object_new(plugin->objdef))){
                    /* initialize the newly created producer */
                    producer->plugin = plugin;
                    producer->session_id = session_id;
                    break;
                }
            }
        }

        return producer;
    }
```

这个函数通过`plugin->objdef`创建了一个新的producer，这个`plugin->objdef`是什么呢？原来它就是在demo的proxyproducer.c中定义的一个
`tsk_object_def_t`类型的指针，在Doubango中，以`_def_t`结尾的命名代表了定义体（我姑且这么叫它），
定义体的作用的是用来创建实体，定义体定义了实体的大小，构造方法，析构方法和赋值操作方法。这个`plugin->objdef`被存储
在plugin中，plugin也就是注册到系统中的定义体`tmedia_producer_plugin_def_t`,这个定义体里除了包含objdef外，还包含了怕热哦
producer的其他操作方法。


