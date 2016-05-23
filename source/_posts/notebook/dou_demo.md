title: Doubango | DEMO
date: 2014-03-01
categories: VoIP
tags: doubango

---

Doubango模块DEMO的调试。

<!--more-->

###启动脚本
doubango的demo可以在终端输入命令，也可以使用dssl语法写的脚本文件来执行(可以仿照tinyDEMO 目录下的sample.sn 来写)
以下就是根据我们自己的环境配置的启动脚本,假设保存为test.sn文件

```bash
    ## For more information about scenarios, please refer to the Programmer's Guide

    # user's parameters (like ANSI-C #define)
    #---> 根据当前配置，设置子网，用户名，密码，代理服务器，端口等相关信息
    %%domain 192.168.9.5
    %%user 1015
    %%pwd vctest123
    %%proxy_ip 192.168.9.5 # IP address or FQDN
    %%proxy_port 5060
    %%proxy_trans tcp # udp, tcp, tls or sctp
    %%expires 100 # expires used by all dialogs
    %%sleep-sec 1.0 # number of seconds to wait before sending next sip message

    %%reg-sid
    %%sub-reg-sid
    %%sub-pres-sid

    # Configure the stack
    #---> 配置协议栈，这一步必须在register之前进行
    # Realm, IMPI and IMPU are mandatory
    ++cst --realm $$(domain) --impi $$(user)@$$(domain) --impu sip:$$(user)@$$(domain) --pwd $$(pwd) \
        --pcscf-ip $$(proxy_ip) --pcscf-port $$(proxy_port) --pcscf-trans $$(proxy_trans)\
        --header Privacy=header;id --header Allow=INVITE, ACK, CANCEL, BYE, MESSAGE, OPTIONS, NOTIFY, PRACK, UPDATE, REFER \
        --header P-Access-Network-Info=ADSL;utran-cell-id-3gpp=00000000 \
        --header User-Agent=IM-client/OMA1.0 doubango/v1.0.0 # last should not have backslash

    # Run the engine
    #---> 启动
    ++r

    # REGISTER
    #---> 注册，这里将本机的用户名和地址注册到ims服务器上，这样别人就可以给这台机器打电话了
    ++reg --xp $$(expires) >>(reg-sid) \
        --header Myheader-name=Myheader-value \

    #---> av (audiovideo), 拨打视频通话,目标地址是sip:1005@192.168.9.5,将返回的session id保存在inv_audio_sid中
    ++av --to sip:1005@$$(domain) \
            --header Action-Header=Myheader-value @@action \
            >>(inv_audio_sid)

    ++sleep --sec -1
    #---> hu (hungup),挂断指定会话
    ++hu --sid $$(inv_audio_sid)
    ++sleep --sec -1

    # sleep
    #---> 等待
    ++sleep --sec $$(sleep-sec)

    # unregister
    #---> 从服务器注销
    #++hu --sid $$(reg-sid)

    # sleep
    ++sleep --sec $$(sleep-sec)

    # Exit the application
    #---> 退出demo
    #++e

```

###demo里需要修改的地方
由于demo默认使用了h263的视频编码，所以在我们的板子上直接运行会出问题。需要在demo的配置协议栈
阶段添加一条命令，让doubango选择h264编码方式
在文件tinyDEMO/common.c里,stack_cfg函数里添加下面这句：

    tdav_set_codecs(tdav_codec_id_h264_bp |tdav_codec_id_h264_mp|tdav_codec_id_h264_hp |tdav_codec_id_pcmu);

###运行Demo
这样demo就可以运行了，把demo文件和上边的.sn脚本文件同时拷贝到板子上，我是拷贝
到/data/路径下。运行：

```bash
    root@android:/data # ./demo
    Doubango Project (tinyDEMO)
    Copyright (C) 2009 - 2010 Mamadou Diop

    SSL is enabled :)
    DTLS supported: no
    DTLS-SRTP supported: no
    ***ERROR: thread tid=20190 function: "tnet_get_addresses()"
    file: "src/tnet_utils.c"
    line: "526"
    MSG: Failed to create new DGRAM socket and errno= [124]
    *INFO thread tid=20190  : Calling 'tnet_dns_resolvconf_parse()' to load DNS servers
    *INFO thread tid=20190  : Failed to open [/etc/resolv.conf]. But don't panic, we have detected that you are using Google Android/iOS Systems.
    You should look at the Progammer's Guide for more information.
     If you are not using DNS functions, don't worry about this warning.

```
出现提示信息后，载入脚本文件

```c
    *INFO thread tid=20376  : Command-Line:

    ++sn --path ./test.sn
```

之后demo就会按照脚本的顺序一步步执行脚本上的命令
