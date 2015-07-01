title: Redis环境搭建
date: 2015-02-27
tags: redis
---

###1 Redis的安装


1 下载安装包：

    wget http://download.redis.io/releases/redis-2.8.18.tar.gz

2 编译源代码：

    tar xvf redis-2.8.18.tar.gz
    cd redis-2.8.18
    make
    make install

注：make完成后，有产生可执行文件
    redis-server：redis服务器的启动程序
    redis-cli：redis命令行工具，也可为客户端
    redis-benchmark：redis性能测试工具（读写）
    redis-stat：redis状态检测工具（状态参数延迟）

3 启动redis服务

    redis-server(有警告，没有加载配置文件)
    redis-server redis.conf

注：Redis服务端的默认连接端口是6379
Redis默认不是后台运行

4 客户端连接
    redis-cli
或者其他客户端：如phpredis

5 停止Redis
    redis-clishutdown
or
    pkill redis-server

Redis的配置redis.conf

    daemonize 如果需要在后台运行，把该项改为yes
    pidfile 配置多个pid的地址，默认在/var/run/redis.pid
    bind 绑定ip，设置后只接受自该ip的请求
    port 监听端口，默认为6379
    timeout 设置客户端连接时的超时时间，单位为秒
    loglevel 分为4级，debug、verbose、notice、warning
    logfile 配置log文件地址
    databases 设置数据库的个数，默认使用的数据库为0
    save 设置redis进行数据库镜像的频率，保存快照的频率，第一个*表示多长时间，第三个*表示执行多少次写操作。在一定时间内执行一定数量的写操作时，自动保存快照。可设置多个条件。
    rdbcompression 在进行镜像备份时，是否进行压缩
    Dbfilename 镜像备份文件的文件名
    Dir 数据库镜像备份的文件放置路径
    Slaveof 设置数据库为其他数据库的从数据库
    Masterauth 主数据库连接需要的密码验证
    Requirepass 设置登录时需要使用的密码
    Maxclients 限制同时连接的客户数量
    Maxmemory 设置redis能够使用的最大内存
    Appendonly 开启append only模式
    appendfsync 设置对appendonly.aof文件同步的频率
    vm-enabled 是否虚拟内存的支持
    vm-swap-file 设置虚拟内存的交换文件路径
    vm-max-memory 设置redis使用的最大物理内存大小
    vm-page-size 设置虚拟内存的页大小
    vm-pages 设置交换文件的总page数量
    vm-max-threads 设置VMIO同时使用的线程数量
    glueoutputbuf 把小的输出缓存存放在一起
    hash-max-zipmap-entries 设置hash的临界值
    activerehashing 重新hash


###2 基本操作

*操作相关的命令连接*

    quit：关闭连接（connection）
    auth：简单密码认证

*持久化*

    save：将数据同步保存到磁盘
    bgsave：将数据异步保存到磁盘
    lastsave：返回上次成功将数据保存到磁盘的Unix时戳
    shundown：将数据同步保存到磁盘，然后关闭服务

*远程服务控制*

    info：提供服务器的信息和统计
    monitor：实时转储收到的请求
    slaveof：改变复制策略设置
    config：在运行时配置Redis服务器

*对value操作的命令*

    exists(key)：确认一个key是否存在
    del(key)：删除一个key
    type(key)：返回值的类型
    keys(pattern)：返回满足给定pattern的所有key
    randomkey：随机返回key空间的一个
    keyrename(oldname, newname)：重命名key
    dbsize：返回当前数据库中key的数目
    expire：设定一个key的活动时间（s）
    ttl：获得一个key的活动时间
    select(index)：按索引查询
    move(key, dbindex)：移动当前数据库中的key到dbindex数据库
    flushdb：删除当前选择数据库中的所有key
    flushall：删除所有数据库中的所有ke

*对String操作的命令*

    set(key, value)：给数据库中名称为key的string赋予值value
    get(key)：返回数据库中名称为key的string的value
    getset(key, value)：给名称为key的string赋予上一次的value
    mget(key1, key2,…, key N)：返回库中多个string的value
    setnx(key, value)：添加string，名称为key，值为value
    setex(key, time, value)：向库中添加string，设定过期时间time
    mset(key N, value N)：批量设置多个string的值
    msetnx(key N, value N)：如果所有名称为key i的string都不存在
    incr(key)：名称为key的string增1操作
    incrby(key, integer)：名称为key的string增加integer
    decr(key)：名称为key的string减1操作
    decrby(key, integer)：名称为key的string减少integer
    append(key, value)：名称为key的string的值附加value
    substr(key, start, end)：返回名称为key的string的value的子串

*对List操作的命令*

    rpush(key, value)：在名称为key的list尾添加一个值为value的元素
    lpush(key, value)：在名称为key的list头添加一个值为value的 元素
    llen(key)：返回名称为key的list的长度
    lrange(key, start, end)：返回名称为key的list中start至end之间的元素
    ltrim(key, start, end)：截取名称为key的list
    lindex(key, index)：返回名称为key的list中index位置的元素
    lset(key, index, value)：给名称为key的list中index位置的元素赋值
    lrem(key, count, value)：删除count个key的list中值为value的元素
    lpop(key)：返回并删除名称为key的list中的首元素
    rpop(key)：返回并删除名称为key的list中的尾元素
    blpop(key1, key2,… key N, timeout)：lpop命令的block版本。
    brpop(key1, key2,… key N, timeout)：rpop的block版本。
    rpoplpush(srckey, dstkey)：返回并删除名称为srckey的list的尾元素，并将该元素添加到名称为dstkey的list的头部

*对Set操作的命令*

    sadd(key, member)：向名称为key的set中添加元素member
    srem(key, member) ：删除名称为key的set中的元素member
    spop(key) ：随机返回并删除名称为key的set中一个元素
    smove(srckey, dstkey, member) ：移到集合元素
    scard(key) ：返回名称为key的set的基数
    sismember(key, member) ：member是否是名称为key的set的元素
    sinter(key1, key2,…key N) ：求交集
    sinterstore(dstkey, (keys)) ：求交集并将交集保存到dstkey的集合
    sunion(key1, (keys)) ：求并集
    sunionstore(dstkey, (keys)) ：求并集并将并集保存到dstkey的集合
    sdiff(key1, (keys)) ：求差集
    sdiffstore(dstkey, (keys)) ：求差集并将差集保存到dstkey的集合
    smembers(key) ：返回名称为key的set的所有元素
    srandmember(key) ：随机返回名称为key的set的一个元素

*对Hash操作的命令*

    hset(key, field, value)：向名称为key的hash中添加元素field
    hget(key, field)：返回名称为key的hash中field对应的value
    hmget(key, (fields))：返回名称为key的hash中field i对应的value
    hmset(key, (fields))：向名称为key的hash中添加元素field
    hincrby(key, field, integer)：将名称为key的hash中field的value增加integer
    hexists(key, field)：名称为key的hash中是否存在键为field的域
    hdel(key, field)：删除名称为key的hash中键为field的域
    hlen(key)：返回名称为key的hash中元素个数
    hkeys(key)：返回名称为key的hash中所有键
    hvals(key)：返回名称为key的hash中所有键对应的value
    hgetall(key)：返回名称为key的hash中所有的键（field）及其对应的value

