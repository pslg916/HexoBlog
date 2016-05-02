---
title: 过去的Django Blog
date: 2016-04-18 21:20:31
tags: Django
categories: Web
---

记录过去体验Django时搭的博客。

------

# 概要

1. 系统[Ubuntu14.04LTS]
2. Apache2 + libapache2-mod-wsgi
3. 用[VirtualEnv12.0.7](http://virtualenv.readthedocs.org/en/latest/)隔离。
4. 域名在[Godaddy](https://www.godaddy.com/)，全是广告。
5. DNS和Nameservers全都用的[CloudFlare](https://www.cloudflare.com/)，免费。
6. 主机本来用树莓派，实在太慢了受不了了，就用了的linode的VPS。
7. Github: https://github.com/pslg916/SLGBlog.git （此系统现已废弃，博客已改用Hexo）

------

# 依赖安装

```shell
$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-wsgi
$ sudo apt-get install python3-pip
$ sudo pip3 install virtualenv
```

------

# 使用virtualenv

## 生成指定python版本的虚拟环境。
```shell
$ virtualenv -p /path/to/your/python2.7 ENV2.7      # 对于python2.7
$ virtualenv -p /path/to/your/python3.4 ENV3.4      # 对于python3.4
```

*   -p PYTHON_EXE 选项在创建虚拟环境的时候指定python版本
*   lib, 所有安装的python库都会放在这个目录中的lib/pythonx.x/site-packages/下，
    并且在配置apache2时，mod_wsgi的WSGIPythonPath必须要写加上这个目录的路径。
    WSGIPythonPath /path/to/mysite.com:/path/to/your/venv/lib/python2.X/site-packages
*   bin,bin/python是在当前环境是使用的python解释器

## 激活/取消 virtualenv
```shell
$ source ./ENVx.x/bin/activate           # 激活
$ deactivate                             # 取消
```

## pip安装依赖
```shell
(ENV3.4)$ pip install  django            # 安装最新版本的Django
(ENV3.4)$ pip install -v django==1.7.1   # 或者指定安装版本
(ENV3.4)$ pip install bootstrap-admin    # 安装bootstrap-admin(可选，美化用)
(ENV3.4)$ pip install markdown           # 安装markdown
```

------

# apache2的mod配置

1. apache2安装后的module的位置在/usr/lib/apache2/modules/mod_wsgi.so
2. 配置apache2的mod的文件夹在/etc/apache2/下，LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so

------

# apache2的sites-available配置文件

1. apache的site相关文件位置/etc/apache2/sites-available/***.conf。
2. 可以自行添加.conf文件，其实这里的.conf即为apache2 VirtualHost的配置，理论上一个.conf中是可以配置多个VirtualHost的，没实践过。

下面是本次用的配置。用mod-wsgi和django配合，初学，目标是能工作就行，优化啊，安全啊什么的以后再说吧。
```shell
   WSGIPythonPath /var/www/html/my_blog:/var/www/html/ENV3.4/lib/python3.4/site-packages
   <VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.

        ServerName sun-is.me
        ServerAlias www.sun-is.me

        DocumentRoot /var/www/html/my_blog

        Alias /static /var/www/html/my_blog/static
        <Directory /var/www/html/my_blog/static>
                #Order allow,deny
                Require all granted
        </Directory>

        <Directory /var/www/html/my_blog/templates>
                #Order allow,deny
                Require all granted
        </Directory>

        WSGIScriptAlias / /var/www/html/my_blog/my_blog/wsgi.py

        <Directory /var/www/html/my_blog/my_blog>
                <Files wsgi.py>
                        #Order allow,deny
                        Require all granted
                </Files>
        </Directory>


        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
    </VirtualHost>

    # vim: syntax=apache ts=4 sw=4 sts=4 sr noet
```

------

# 细节的坑

- 多看error.log，可节约很多时间。
- base.html中一定引用静态文件时，一定要以"/"开头，比如“/static/xxx/xxx.css"。
- Linux下的配置文件基本都在/etc/下。
- Linux下的apache2相关的module，安装后都在/usr/lib/apache2/modules下。
- 不要用Goddady的免费DNS，如果一定要用，把默认的那个删了，否则域名有50%机会被解析到Goddady的广告页上，太坑跌。
- Django的项目结构不合理，有空再看看什么”最佳实践“之类的吧，或者别人的代码。
- 静态文件设置
```
    STATIC_URL = '/static/'
    STATIC_ROOT = '/var/www/html/my_blog/static/'
    STATICFILES_DIRS = (
          # 除了STATIC_ROOT之外的各APP的静态文件地址
     )
```
- 生产环境上线前， 要执行collectstatic，把django-admin相关的静态文件都收集到STATIC_ROOT里。
```
python3 manage.py collectstatic
```
