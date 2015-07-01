title: Doubango--Demo提供的操作
date: 2014-03-01
tags: doubango
---

###数据结构
cmd_t用来保存从命令行读取的命令内容

```c
    typedef struct cmd_s
    {
        TSK_DECLARE_OBJECT;

        cmd_type_t type;//命令类型，在execute函数内通过switch筛选
        opts_L_t *opts; //命令的参数和操作,是opt_t的集合
        char* sidparam;
    }
    cmd_t;
```
cmd_type_t的声明如下：


```c
    typedef enum cmd_type_e
    {
        cmd_none,

        cmd_audio, /* ++audio | ++a*/
        cmd_audiovideo, /* ++audiovideo | ++av*/
        cmd_config_session, /* ++config-session | ++css */
        cmd_config_stack, /* ++config-stack | ++cst*/
        cmd_dtmf, /*++dtmf*/
        cmd_dump, /*++dump | ++d*/
        cmd_ect, /*++ect*/
        cmd_exit,	/*++exit | ++e | ++quit | ++q*/
        cmd_file, /* ++file | ++f*/
        cmd_hangup, /* ++hangup | ++hu */
        cmd_help, /* ++help | ++h  */
        cmd_hold, /* ++hold | ++ho  */
        cmd_large_message, /* ++large-message | ++lm */
        cmd_message, /* ++message | ++m*/
        cmd_options, /* ++options | ++opt*/
        cmd_publish, /* ++publish | ++pub*/
        cmd_register, /* ++register | ++reg */
        cmd_resume, /* ++resume | ++res */
        cmd_run, /* ++run | ++r*/
        cmd_scenario, /* ++scenario | ++sn*/
        cmd_sleep, /* ++sleep */
        cmd_sms,	/* ++sms */
        cmd_stop, /* ++stop */
        cmd_subscribe, /* ++subscribe | ++sub */
        cmd_video, /* ++video | ++v */
    }
    cmd_type_t;
```

opt_t用来保存命令后的各项参数


```c
    typedef struct opt_s
    {
        TSK_DECLARE_OBJECT;

        opt_type_t type;//操作类型，具体见下
        lv_t lv;        //操作层级
        char* value;    //具体的参数值
    }
    opt_t;
```

opt_type_t的声明如下:


```c
    typedef enum opt_type_e
    {
        opt_none,

        opt_amf,			/* --amf 0x85FF */
        opt_caps,			/* --caps +g.oma.sip-im or language=en,fr*/
        opt_dhcpv4,			/* --dhcpv4 */
        opt_dhcpv6,			/* --dhcpv6 */
        opt_dname,			/* --dname bob */
        opt_dns_naptr,		/* --dns-naptr */
        opt_from,			/* --from sip:alice@open-ims.test */
        opt_event,			/* --event 2 */
        opt_expires,		/* --expires|--xp 30 */
        opt_header,			/* --header Supported=norefersub */
        opt_impi,			/* --impi bob@open-ims.test */
        opt_impu,			/* --impu sip:bob@open-ims.test */
        opt_ipv6,			/* --ipv6 */
        opt_local_ip,		/* --local-ip 192.168.0.10 */
        opt_local_port,		/* --local-port 5060 */
        opt_opid,			/* --opid 0xA712F5D04B */
        opt_password,		/* --password|--pwd mysecret */
        opt_path,			/* --path /cygdrive/c/Projects/sample.cfg */
        opt_payload,		/* --payload|--pay hello world! */
        opt_pcscf_ip,		/* --pcscf-ip 192.168.0.13 */
        opt_pcscf_port,		/* --pcscf-port 5060 */
        opt_pcscf_trans,	/* --pcscf-trans udp */
        opt_realm,			/* --realm open-ims.test */
        opt_sec,			/* --sec 1800 */
        opt_sid,			/* --sid 1234 */
        opt_sigcomp_id,		/* --sigcomp-id urn:uuid:2e5fdc76-00be-4314-8202-1116fa82a473 */
        opt_silent,			/* --silent */
        opt_smsc,			/* --smsc +3315245856 */
        opt_stun_ip,		/* --stun-ip numb.viagenie.ca */
        opt_stun_pwd,		/* --stun-pwd mysecret */
        opt_stun_port,		/* --stun-port 3478 */
        opt_stun_usr,		/* --stun-usr bob@open-ims.test */
        opt_to,				/* --to sip:alice@open-ims.test */
    }
    opt_type_t;
```

lv_t的声明如下：

```c
    typedef enum lv_e
    {
        lv_none,

        lv_stack,	/* @@stack | @@st */
        lv_session,	/* @@session | @@ss */
        lv_action	/* @@action | @@request | @@a | @@r*/
    }
    lv_t;
```

###tinyDEMO操作流程
main函数通过命令行读入命令参数，将参数保存在cmd_t结构中。传给execute函数，
execute通过switch语句判断`cmd->type`分别处理不同的操作，以register和audiovideo操
作为例：

```c
    case cmd_register:
                {
                    TSK_DEBUG_INFO("command=register");
                    /* 把命令和参数传给register.c处理，register.c调用common.c生成
                       session，并调用tinySIP的api进行注册。最后运行成功后返回
                       session的id */
                    if((sid = register_handle_cmd(cmd->type, cmd->opts)) != TSIP_SSESSION_INVALID_ID){
                        if(cmd->sidparam){
                            //更新参数
                            tsk_itoa(sid, &istr);
                            update_param(cmd->sidparam, istr);
                        }
                    }
                    break;
                }

    case cmd_hangup:
                {
                    const opt_t* opt;
                    TSK_DEBUG_INFO("command=hangup");
                    /* opt_get_by_type函数传入命令集合和感兴趣的命令字符串，获
                       取出相关命令和具体的参数值 tsk_strnullORempty顾名思义是判断字符串是否为空 */
                    if((opt = opt_get_by_type(cmd->opts, opt_sid)) && !tsk_strnullORempty(opt->value)){ /* --sid option */
                        //通知common.c挂起
                        ret = session_hangup(tsk_atoll(opt->value));
                    }
                    else{
                        TSK_DEBUG_ERROR("++hangup command need --sid option");
                        ret = -1;
                    }
                    break;
                }
```


继续深入register模块：

```c
    tsip_ssession_id_t register_handle_cmd(cmd_type_t cmd, const opts_L_t* opts)
    {
        const session_t* session = tsk_null;
        tsip_ssession_id_t id = TSIP_SSESSION_INVALID_ID;

        /* session_handle_cmd是common.c里实现用来创建session的函数 */
        if(!(session = session_handle_cmd(cmd, opts))){
            goto bail;
        }
        else{
            /* 获得session id, 注意tsp_这种前缀都是doubango对应模块的api */
            id = tsip_ssession_get_id(session->handle);
        }

        /* action config */

        /* Execute command */
        switch(cmd){
            case cmd_register:
                {	/* Send SIP REGISTER */
                    /* 设置参数，调用common.c里的action_get_config给tsip模块配
                       置环境 */
                    tsip_action_handle_t* action_config = action_get_config(opts);
                    // 发送注册消息
                    tsip_api_register_send_register(session->handle,
                        //把环境参数传进去
                        TSIP_ACTION_SET_CONFIG(action_config),
                        /* Any other TSIP_ACTION_SET_*() macros */
                        TSIP_ACTION_SET_NULL());
                    //释放资源
                    TSK_OBJECT_SAFE_FREE(action_config);
                    break;
                }
            default:
                /* already handled by session_handle_cmd() */
                break;
        }

    bail:
        return id;
    }
```

综上可见，tinyDEMO是对doubango各个模块的简单封装，基本调用顺序是

    main.c 保存命令行参数,分发命令
        |- common.c 创建session，配置环境变量等基础操作
            |- register.c(或其他demo中子模块) 按流程调用doubango的api实现对应功能
                |- doubango API
