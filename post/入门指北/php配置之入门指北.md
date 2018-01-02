### 写在前面

php是世界上最好的语言（滑稽

## 正文

php也是脚本语言的一种，它可以在服务器上执行，主要面向的对象是超文本，也就是网页。

也是由于这个，我们往往需要通过浏览器来看php程序的生成结果，既然要用浏览器来访问，那么就需要配置服务器那些东西了，也就是写这篇东西的主要目的。

一般架构是，Apache/Nginx + php-fpm + php，这种结构对应到python就类似是Apache/Nginx + gunicorn + python，也就是说php-fpm的作用类似gunicorn。那么整个逻辑就很明显了，nginx在最前面做反向代理，php-fpm在中间负责处理套接字通信那些，将请求内容那些传到最后面，让php来生成响应。

而php这个解释器真正做的就是，扫描整个文件，找到`<?php code ?>`这部分，将其翻译成对应的html超文本。

## 具体配置

###Nginx部分

```
    server {
        listen       9090;
        server_name  localhost;        
        location / {
            root /Users/nanrou/code/php;
            index  index.php index.html index.htm;
        }
        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        
        location ~ \.php$ {
			root           /Users/nanrou/code/php;
            fastcgi_index  index.php;
            fastcgi_pass   127.0.0.1:9000;
            include        fastcgi_params;
            fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
            fastcgi_param  SCRIPT_NAME  $fastcgi_script_name;

            fastcgi_pass_request_headers on;
        }
    }
```

其实也就是监听某个端口，然后跟据fastcgi协议将请求转到php-fpm负责的那个端口。

### php-fpm

其实完全不改也是可以的，我是php7.2，自带的配置就够了。