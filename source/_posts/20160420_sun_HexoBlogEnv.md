---
title: Hexo在VPS上用Git Hook部署
date: 2016-04-20 23:23:50
tags: 环境
---

------

# 本地生成RSA Key，拷贝至VPS，无密码登录

## Step1 本地创建RSA Key Pair
```shell
ssh-keygen -t rsa
```
- -t type
    - 指定要创建的密钥类型。可以使用："rsa1"(SSH-1) "rsa"(SSH-2) "dsa"(SSH-2)

## Step2 存储Keys并设置密码(可选)
第一步结束后，会出现下述问题：
```shell
Enter file in which to save the key (/home/demo/.ssh/id_rsa):
```
只需要连续按回车，就会在默认位置无密码产生keys。
```shell
Enter file in which to save the key (/home/demo/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
```
完整的步骤如下：
```shell
ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/demo/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/demo/.ssh/id_rsa.
Your public key has been saved in /home/demo/.ssh/id_rsa.pub.
The key fingerprint is:
4a:dd:0a:c6:35:4e:3f:ed:27:38:8c:74:44:4d:93:67 demo@a
The key's randomart image is:
+--[ RSA 2048]----+
|          .oo.   |
|         .  o.E  |
|        + .  o   |
|     . = = .     |
|      = S = .    |
|     o + = +     |
|      . o + o .  |
|           . o   |
|                 |
+-----------------+
```
其中，公共key是
```shell
/home/demo/.ssh/id_rsa.pub
```
私有key是
```shell
 /home/demo/.ssh/id_rsa
```
## Step3 拷贝共有key至VPS
通过ssh-copy-id可以拷贝共有key至VPS
```shell
ssh-copy-id user@123.45.56.78
```
如果没有ssh-copy-id，比如mac osx，可以通过下面的方法安装
```shell
curl -L https://raw.githubusercontent.com/beautifulcode/ssh-copy-id-for-OSX/master/install.sh | sh
```
------
执行ssh-copy-id命令后，会出现如下结果
```shell
The authenticity of host '12.34.56.78 (12.34.56.78)' can't be established.
RSA key fingerprint is b1:2d:33:67:ce:35:4d:5f:f3:a8:cd:c0:c4:48:86:12.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '12.34.56.78' (RSA) to the list of known hosts.
user@12.34.56.78's password:
Now try logging into the machine, with "ssh 'user@12.34.56.78'", and check in:

  ~/.ssh/authorized_keys

to make sure we haven't added extra keys that you weren't expecting.
```
现在就可已通过
```shell
ssh user@12.34.56.78
```
无密码登录VPS了。

## Step4 配置VPS，禁止ssh密码root登录(可选)
首先登录VPS，
```shell
ssh user@12.34.56.78
```
然后修改配置文件
```shell
sudo nano /etc/ssh/sshd_config
```
找到PermitRootLogin所在处，并修改为
```shell
PermitRootLogin without-password
```
最后，重载ssh
```shell
reload ssh
```

# VPS新建空Git Repo，用Hook在push时部署

## VPS新建空Blog Git Repo

创建静态blog目录
```shell
sudo mkdir -p /var/www/blog
```
创建git repo目录
```shell
sudo mkdir -p /var/www/repo
```
进入repo目录，初始化空repo
```shell
cd /var/www/repo
git init --bare
tree -L 1 repo
    repo/
    ├── branches
    ├── config
    ├── description
    ├── HEAD
    ├── hooks
    ├── index
    ├── info
    ├── objects
    └── refs
```
--bare 的意思是该目录只作为版本控制，但是不实际包含源代码文件。

## 写hook，分别部署版本控制和代码文件
进入hooks目录，
```shell
cd hooks
```
创建post-receive文件，
```shell
vim post-receive
```
并写入
```shell
#!/bin/sh
git --work-tree=/var/www/blog --git-dir=/var/repo checkout -f
```
- 这里的参数
    - --work-tree：本地push后remote端最新版代码存放文件夹
    - --work-dir：本地push后remote端版代控制相关文件存放处

最后设置权限
```shell
chmod +x post-receive
```

------

# 本地添加remote，push
在本地机，进入hexo的目录，比如
```shell
cd ~/blog
```
接着添加代号XXX的remote
```shell
git remote add XXX ssh://user@12.34.56.78/var/www/repo
```
今后，用hexo生成静态文件后，push至VPS
```shell
hexo g
git add .
git commit -m "我的第一篇博客"
git push XXX master
```
即可将版本信息push到VPS的/var/www/repo，
并将最新版代码push到VPS的/var/www/blog。

------

# VPS安装Nginx

首先，安装nginx
```shell
sudo apt-get update
sudo apt-get install nginx
```
然后查询VPS公网IP
```shell
ip addr show eth0 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'
```
Nginx动作确认
通过浏览器访问VPS公网IP，如果有域名，可以设置[DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-host-name-with-digitalocean)等DNS服务商。
如果一切正常，浏览http://server_domain_name_or_IP后可见如下结果
![nginx](https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQL3gkKlCzKAnBJjdy9vCLnEciVZ4LY3Euu9yya-gVFImPsB4xlfw)

- nginx相关基本操作
```shell
sudo service nginx stop     # 停止
sudo service nginx start    # 启动
sudo service nginx restart  # 重启
```
- 确认nginx在reboot后自启动
```shell
sudo update-rc.d nginx defaults
    System start/stop links for /etc/init.d/nginx already exist.
```

# 配置nginx，最终可通过公网访问静态Hexo Blog
编辑下述文件
```shell
sudo vim /etc/nginx/conf.d/default.conf
```
加入
```shell
server {
    # 写上Hexo博客生成文件夹地址
    root /var/www/blog/public;
    index index.html index.htm;

    # 写上自己的VPS的域名或IP
    server_name www.XXX.XXX XXX.XXX *.XXX.XXX;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```
重启nginx
```shell
sudo service nginx restart
```
终于，可以通过VPS公网IP或域名，来访问Hexo Blog了。
比如我的，https://www.sun-is.me
