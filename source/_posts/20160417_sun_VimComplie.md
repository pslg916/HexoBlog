---
title: Vim配置-源码编译篇
date: 2016-04-17 23:12:42
tags: 工具
---


------

# 安装python

果然如果需要python支持，下面的几个源码编译时，python的版本必须统一。

------

# Install gmp package

用cygwin自带的setup-x86.exe安装gmp相关的包。vim源码编译的时候要用这个。

------

# 编译ncurses源码

http://ftp.gnu.org/gnu/ncurses/ncurses-5.9.tar.gz
open a cygwin terminal,
cd to directory containing downloaded file
```shell
$ tar zxf ncurses-5.9.tar.gz
$ cd ncurses-5.9
$ ./configure --prefix=/usr
$ make && make install
```

------

# 编译lua源码

http://www.lua.org/ftp/lua-5.3.1.tar.gz
```shell
$ tar zxf lua-5.3.1.tar.gz
$ cd lua-5.3.1
$ make mingw
$ make install
```

------

# 编译vim源码

ftp://ftp.vim.org/pub/vim/unix/vim-7.4.tar.bz2
```shell
$ ./configure --with-features=huge \
              --enable-pythoninterp \
              --enable-perlinterp \
              --enable-rubyinterp \
              --enable-luainterp \
              --with-lua-prefix=/usr/local \
              --enable-gui=no \
              --without-x \
              --enable-multibyte \
              --prefix=/usr
$ make && make install
```
注意这里python和python3只能选一个，两个都选不行。
但是有解决方案，懒得折腾了。

------

# 查看是否有+lua

打开vim，输入:version, 查看vim编译时间，如果是本次编译生成，则说明正确，然后查看是否有+lua。

------

# 可能出现的问题

## not found lua.h
在./configure命令后加上 | grep lua grep出来的不满足的项目一个一个全部修正。
最容易出错的就是

     --with-lua-prefix=/usr/local

## vim源码的bug
编译时，出现下述error:
```shell
objects/if_lua.o: In function 'luaV_list_insert':
/home/spch2008/vim74/src/if_lua.c:777: undefined reference to 'luaL_optlong' collect2: error: ld returned 1 exit status
```
修改src/if_lua.c:777
```c
...
//long pos = luaL_optlong(L, 3, 0); // 修正前
long pos = (long)luaL_optinteger(L, 3, 0); // 修正后
...
```

编译时，还可能出现下述error:
```shell
if_python3.c:66:20: fatal error: Python.h: No such file or directory
 #include <Python.h>
```
修改src/if_python.c:66
```c
...
//#include "Python.h" // 修正前
#include "E:\cygwin\usr\include\python2.7\Python.h" // 修正后
...
```
修改之后注意可能需要dos2unix一下，视编辑器而定。

---

# Todo
- [x] 编译安装篇
- [ ] 主题美化篇
- [ ] 自动补全篇
- [ ] 键位配置篇
- [ ] 编译调试篇
