title: Doubango——音视频插件的注册和初始化机制
date: 2014-03-01
tags: doubango
---

### 插件的定义
先来看一段demo里音频输入插件audio producer的代码：

```c
    /* object definition */
    static const tsk_object_def_t twrap_producer_proxy_audio_def_s =
    {
        sizeof(twrap_producer_proxy_audio_t),
        twrap_producer_proxy_audio_ctor,
        twrap_producer_proxy_audio_dtor,
        tdav_producer_audio_cmp,
    };
    /* plugin definition*/
    static const tmedia_producer_plugin_def_t twrap_producer_proxy_audio_plugin_def_s = 
    {
        &twrap_producer_proxy_audio_def_s,

        tmedia_audio,
        "Audio Proxy Producer",

        twrap_producer_proxy_audio_set,
        twrap_producer_proxy_audio_prepare,
        twrap_producer_proxy_audio_start,
        twrap_producer_proxy_audio_pause,
        twrap_producer_proxy_audio_stop
    };

```
如上边代码所见，插件的定义由两部分组成——object（基类）的定义和插件本体（子类）的定义。object是Doubango利用ANSI C面向对象编程的方法，将
抽象结构（类）的构造函数，析构函数和操作符重构函数模拟C++基类的方式，定义在object结构体中，再让抽象结构继承这个结构体来实现
面向对象的效果。上边代码中`twrap_producer_proxy_audio_plugin_def_s`定义的开始部分就放入了一个
`twrap_producer_proxy_audio_def_s`的地址，目的就是模仿C++子类继承基类时将基类定义放在子类内存地址的开头部分。这样子类指针
就可以指向基类的方法。

这样定义后的插件子类就拥有了基类的全部操作和自己内部定义的操作。接下来我们看一下音视频插件是如何被注册到Doubango运行插件
列表中的。

### 插件的注册
再看demo里的这个注册函数

```c
    tsk_bool_t proxyaudioproducer_registerPlugin()
    {
        /* HACK: Unregister all other audio plugins */
        TSK_DEBUG_INFO("function=%s,line=%d",__FUNCTION__,__LINE__);
        tmedia_producer_plugin_unregister_by_type(tmedia_audio);
        /* Register our proxy plugin */
        return (tmedia_producer_plugin_register(twrap_producer_proxy_audio_plugin_def_t) == 0);
    }
```

这个函数的结尾部分调用了`tmedia_producer_plugin_register`来将音频插件注册到`__tmedia_producer_plugins`插件数组里:


```c
    /* add or replace the plugin */
    for(i = 0; i<TMED_PRODUCER_MAX_PLUGINS; i++){
        if(!__tmedia_producer_plugins[i] || (__tmedia_producer_plugins[i] == plugin)){
            __tmedia_producer_plugins[i] = plugin;
            return 0;
        }
    }
```

我们看到在`tmedia_producer_plugin_register`内部把刚才注册进来的音频插件放在数组尾部。

### 插件的初始化
了解了Doubango插件注册的方法，我们这回用自顶向下的方式看这些插件如何从上到下被一步步注册并初始化的。
首先从main函数里调用`tdav_init()`来初始化所有音视频相关的内容。在`tdav_init()`里有这么一句：


```c
    tmedia_session_plugin_register(tdav_session_audio_plugin_def_t);
```

这句将音频session注册到tdav这一层的`__tmedia_session_plugins`数组里, 回头看`tdav_session_audio_plugin_def_t`里的构造函数里调用了这
这么一句：

```c
    /* init() base */
    if((ret = tdav_session_av_init(base, tmedia_video)) != 0){
        TSK_DEBUG_ERROR("tdav_session_av_init(video) failed");
        return tsk_null;
    }
`tdav_session_av_init`这个函数做了什么呢，继续深入:

    // producer
    TSK_OBJECT_SAFE_FREE(self->producer);
    if(!(self->producer = tmedia_producer_create(self->media_type, session_id))){
        TSK_DEBUG_ERROR("Failed to create producer for media type = %d", self->media_type);
    }
```

看`tmedia_producer_create`的函数名，貌似是将producer插件初始化的，进去看看：


```c
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
```

果然，这里将`__tmedia_producer_plugins`插件数组里所有插件依次`tsk_object_new`(这句相当于C++里的new)初始化。
那么重新理清一下思路，`__tmedia_session_plugins`这个插件数组包含了音频session插件，而音频session插件初始化的时候就会初始化
音频producer插件，也就是说，我们要找到音频producer插件在哪里初始化，关键就要找到`__tmedia_session_plugins`这个session插件数组
是在哪里初始化的。

经过千辛万苦的跳转，终于找到了这一条初始化流程。

首先是在拨打视频通话时，通过事先创建的session发送邀请给对方：


```c
    tsip_api_invite_send_invite(session->handle, (tmedia_audio|tmedia_video),
                                                    TSIP_ACTION_SET_CONFIG(action_config),
                                                    /* Any other TSIP_ACTION_SET_*() macros */
```


在这个函数里，创建了一个dialog layer:


```c
    if(!(dialog = tsip_dialog_layer_find_by_ss(_ss->stack->layer_dialog, ss))){
        dialog = tsip_dialog_layer_new(_ss->stack->layer_dialog, tsip_dialog_INVITE, ss);
        new_dialog = tsk_true;
    }
```

在`tsip_dialog_layer_new`里：


```c
    case tsip_dialog_INVITE:
        {
            if((dialog = (tsip_dialog_t*)tsip_dialog_invite_create(ss, tsk_null))){
                ret = tsk_object_ref(dialog);
                tsk_list_push_back_data(self->dialogs, (void**)&dialog);
            }
            break;
        }
```

初始化了一个`tsip_dialog_invite_def_t` :


```c
    tsk_object_new(tsip_dialog_invite_def_t,  ss, call_id);
```

这个`tsip_dialog_invite_def_t`初始化的时候，调用了：


```c
    tsip_dialog_invite_init(self);
```

接着进入这个函数：


```c
    /* Client-Side dialog */
    tsip_dialog_invite_client_init(self);
    /* Server-Side dialog */
    tsip_dialog_invite_server_init(self);

```

这两个函数分别调用`c0000_Started_2_Outgoing_X_oINVITE`来发送邀请,之后调用：


```c
    /* send the request */
    ret = send_INVITE(self, tsk_false);
```

这里调用到`tmedia_session_mgr_get_lo`寻找本地session,然后调用`tmedia_session_mgr_load_sessions`加载本地session,如果没有
找到本地session，就调用`tmedia_session_create`创建session，这时就会初始化所有音频session插件。


```c
    while((i < TMED_SESSION_MAX_PLUGINS) && (plugin = __tmedia_session_plugins[i++])){
        if(plugin->objdef && (plugin->type == type)){
            if((session = tsk_object_new(plugin->objdef))){
                if(!session->initialized){
                    tmedia_session_init(session, type);
                }
                session->plugin = plugin;
            }
            break;
        }
    }
```

至此就理清了整个流程。
