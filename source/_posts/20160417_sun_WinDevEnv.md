---
title: Win7开发环境配置
date: 2016-04-17 15:50:42
tags: Cygwin
categories: 工具
---

# 记录Win7开发的一些设置，但已过时，好多不会再用了。

------

# Cygwin, tmux配置

## 安装，美化cygwin
- install cygwin 2.871
  - just using default setting to install.
- install yahei consolas hybrid
  - https://uigroupcode.googlecode.com/files/YaHei.Consolas.1.12.zip
- set font and xterm-256color for cygwin
  - Right click on mintty, and just do it as the menu shown.
- add tomorrow-color-scheme fot mintty
  - add fellowing content into .minttyrc under home.

```shell
    BoldAsFont=no
    Font=YaHei Consolas Hybrid
    FontHeight=12
    FontSmoothing=full
    Locale=C
    Charset=UTF-8
    Columns=68
    Rows=28
    Term=xterm-256color
    ForegroundColour=197,200,198
    BackgroundColour=29,31,33
    CursorColour=253,157,79
    Black=29,31,33
    BoldBlack=150,152,150
    Red=204,102,102
    BoldRed=173,57,57
    Green=181,189,104
    BoldGreen=142,150,66
    Yellow=240,198,116
    BoldYellow=234,171,47
    Blue=129,162,190
    BoldBlue=82,125,159
    Magenta=178,148,187
    BoldMagenta=145,100,157
    Cyan=138,190,183
    BoldCyan=90,162,152
    White=197,200,198
    BoldWhite=255,255,255
    Scrollbar=none
    CursorType=underscore
```

## 在cygwin中安装最新的vim,tmux

## 设置tmux
```shell
    set -g status-bg black
    set -g status-fg white
    set -sg escape-time 1
    set -g base-index 1
    setw -g pane-base-index 1

    bind | split-window -h
    bind - split-window -v

    bind h select-pane -L
    bind j select-pane -D
    bind k select-pane -U
    bind l select-pane -R

    setw -g mode-mouse off
    set -g status-utf8 on

    set -g status-interval 60

    # 对齐方式
    set-option -g status-justify centre

    # 左下角
    set-option -g status-left '#[bg=black,fg=green][#[fg=cyan]#S#[fg=green]]'
    set-option -g status-left-length 20

    # 窗口列表
    setw -g automatic-rename on
    set-window-option -g window-status-format '#[dim]#I:#[default]#W#[fg=grey,dim]'
    set-window-option -g window-status-current-format '#[fg=cyan,bold]#I#[fg=blue]:#[fg=cyan]#W#[fg=dim]'

    # 右下角
    set -g status-right '#[fg=green][#[fg=cyan]%d %b %R#[fg=green]]'
```

## 如果can't create socket: Permission denied
解決法：
tmuxは(/tmp/tmux-[uid]/default)を生成するがなぜか書き込めない。権限を777にしてもだめしょうがないからソケットを指定してあげたらいけた
```shell
    tmux -S /tmp/tmux-[uid]/default
```
为了方便可以在.bashrc中加入alias
```shell
    alias tmux='tmux -S /tmp/tmux-197608/default'
```

------

# Python开发环境

## 安装Python3和最新pip
python3直接装官网最新的就行。
To install pip, securely download get-pip.py.
https://bootstrap.pypa.io/get-pip.py
Then run the following (which may require administrator access):
```shell
    $ python get-pip.py
```
最后安装几个pakages，作为测试
```shell
    $ pip install pep8, pyflakes, pylint, ipython
```

------

# Qt(with mingw)

## 安装Qt and MingW
  套件选择mingw4.9.2
  tools也选mingw4.9.2

## 美化Qt
  cd 到Qt安装目录
```shell
  git clone https://github.com/mervick/Qt-Creator-Darcula.git
  cd Qt-Creator-Darcula
  cp darcula.xml ../Tools/QtCreator/share/qtcreator/styles/
```

## 添加Path
为了后面的bulid opencv，要把
```shell
Qt/5.5/mingw492_32/
Qt/Tools/QtCreator/
Qt/Tools/mingw492_32/
```
里面的bin和lib都添加到path中吧。

------

# CMake(GUI)

  目前最新是3.2.3

------

# OpenCV

## 编译OpenCV 2.4.11
  版本选linux源码版。
  运行cmake的GUI版，
  input: 解压后的opencv源码包。
  output: /usr/include/opencv2411
  使用qt中的mingw去编译。
  选择native compiler。
  c++的选g++，c的选gcc。
  search QT, 把with_Qt选上。
  config的之前要把/bin/sh.exe改个名字，
  要不然会有sh不能在path中存在的错误。
  然后generate。
  最后，cygwin中cd去/usr/include/opencv2411
  执行mingw32-make.exe
  执行mingw32-make.exe install
