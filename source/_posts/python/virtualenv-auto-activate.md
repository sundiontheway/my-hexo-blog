title: 如何进入工程目录自动加载Python VirtualEnv
date: 2015-11-13
tags: python
---

当我们`cd`命令进入Openstack工程目录时会自动加载当前目录`.venv`虚拟环境。我今天研究了一下，发现是一个Linux的环境变量在发挥作用——`PROMPT_COMMAND`

>PROMPT_COMMAND
>
>If set, the value is executed as a command prior to issuing each primary prompt.

这个神奇的环境变量会在每次用户提示符之前出现，通常用于保存用户输入历史记录。利用这个特性，我们可以写一个脚本检查当前用户输入的命令是否为`cd $PROJECT`，如果是，则运行载入虚拟环境的脚本。
下面是一个老外在 Gist 上实现自动进入目录载入虚拟环境的脚本，感受一下：

```bash
#!/bin/bash
# virtualenv-auto-activate.sh
#
# Installation:
#   Add this line to your .bashrc or .bash-profile:
#
#       source /path/to/virtualenv-auto-activate.sh
#
#   Go to your project folder, run "virtualenv .venv", so your project folder
#   has a .venv folder at the top level, next to your version control directory.
#   For example:
#   .
#   ├── .git
#   │   ├── HEAD
#   │   ├── config
#   │   ├── description
#   │   ├── hooks
#   │   ├── info
#   │   ├── objects
#   │   └── refs
#   └── .venv
#       ├── bin
#       ├── include
#       └── lib
#
#   The virtualenv will be activated automatically when you enter the directory.

_virtualenv_auto_activate() {
    # Change if you want different name for virtual environment directory
    local VENV_BASENAME=".venv"

    local _pwd=$(pwd -P)

    if [ ! -z "$VIRTUAL_ENV" ]; then
        local _venv_parent=$(dirname $VIRTUAL_ENV)

        # Check if we are inside project with virtual environment
        if [ "${_pwd:0:${#_venv_parent}}" != ${_venv_parent} ]; then
            echo Deativating virtualenv \"$_VENV_NAME\"...
            deactivate
        fi
    fi

    if [ -e ${VENV_BASENAME} ]; then
        # Check to see if already activated to avoid redundant activating
        if [ "$VIRTUAL_ENV" != "${_pwd}/$VENV_BASENAME" ]; then
            _VENV_NAME=$(basename ${_pwd})
            echo Activating virtualenv \"$_VENV_NAME\"...
            VIRTUAL_ENV_DISABLE_PROMPT=1
            source $VENV_BASENAME/bin/activate
            _OLD_VIRTUAL_PS1="$PS1"
            PS1="($_VENV_NAME)$PS1"
            export PS1
        fi
    fi
}

export PROMPT_COMMAND="_virtualenv_auto_activate; $PROMPT_COMMAND"
```

