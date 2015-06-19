Title: Arch Linux 配置记录
Date: 2015-06-16
Modified: 2015-06-16
Category: 开源软件
Tags: archlinux
Slug: archlinux
Author: Steve D. Sun


记录一下arch linux配置时的注意事项。
大部分配置只要按照官方wiki上的方法都可以无障碍完成。特别注意以下几个点：

* __设置网络__

（确保virtualbox用的是网络地址转换（NAT））

    systemctl enable dhcpcd.service

* __屏幕分辨率大小问题__

virtualbox的自动调节分辨率功能点一下打开，调节到合适的大小后再点一下关闭，
就不会出现窗口dpi错误的问题了。另外，在外观-字体里修改dpi为96后确定，
也能解决问题。

*  __solarized安装__

终端文件夹显示需要:

    git clone git://github.com/seebi/dircolors-solarized.git

然后拷贝：

    cp ~/dircolors-solarized/dircolors.256dark ~/.dircolors
    eval 'dircolors .dircolors'

* __字体修改__

    yaourt ttf-monaco

选aur里的那个

* __输入法google拼音（fcitx）__

    sudo pacman -S fcitx-im fcitx-googlepinyin fcitx-configtool

在`~/.xinitrc`里追加：

    export GTK_IM_MODULE=fcitx
    export QT_IM_MODULE=fcitx
    export XMODIFIERS=“@im=fcitx”
    exec fcitx &

另外，Arch里的vim非常搓逼（不支持系统剪贴板），所以我换成了gvim
