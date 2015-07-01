title: 使用meld作为git默认diff工具
date: 2013-01-04
tags: meld
---

_1: ubuntu安装meld_

    sudo apt-get install meld

_2: 在`~/`目录下创建文件并编辑_

    vim ~/.git_meld.sh

填入内容，`:w`保存

    #!/bin/sh
    meld $2 $5

_3: 保存后给文件赋予权限_

    chmod +x ~/.git_meld.sh

_4: 修改git diff配置_

    git config --global diff.external ~/.git_meld.sh
