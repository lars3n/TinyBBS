# tiny-BBS-forum-
a tiny BBS(forum) based on Django

##说明:
* 环境: 服务端( Python 2.7 + Django 1.8.3 + SAE + MySQL ),  前端( jQuery + bootstrap )
* 代码中的邮箱配置和SECRET_KEY已清空，如需测试，请自行添加

##功能:
* 用户注册、修改密码、邮箱验证找回密码
* 用户评论、发表文章
* 关注其他用户、收藏文章
* 用户修改个人资料( 头像、签名 )
* 站内信功能

###功能说明:
* 自己实现的找回密码功能，非常简陋，验证code使用 **salt + email + 时间戳 ** 生成哈希。
  同时在用户的reset_url字段存入这段code，并且开启一个Timer 线程，在10分钟后删除这个字段的数据。
  这个功能可能存在应用层DDOS漏洞。
* 评论功能使用AJAX，发表文章的编辑器使用非常简陋的在线编辑器tinymce  
* 验证码模块使用自带的captcha 模块，点击图片可刷新
* 由于SAE 不允许用户直接上传文件，用户修改头像的功能暂时不能使用
* 站内信使用了大量数据库查询，操作速度很慢


##遇到的一些问题:
1. django 自带的password_reset 函数的API已经改了，网上大多数配置的方法都是错误的，这也是导致我重新写一个reset功能的原因
2. 在使用编辑器编辑模板文件时，请注意模板文件的编码格式，如果不是UTF-8，会报UnicodeError
3. 假如你是采取从本地导出数据库到服务器的话，请注意，在本地创建数据库的时候，要注意数据库的**编码格式**！
   如果要在数据库中存储中文数据，请将编码格式设置为 <code>utf8-general-ci</code>
4. 还有其他许许多多的坑，暂且不表   

##感悟
* 最难的地方在于数据库的表结构设计

##运行情况截图：
![](img/bbs1.JPG)

![](img/bbs2.JPG)

![](img/bbs3.JPG)

![](img/bbs4.JPG)

![](img/bbs5.JPG)

![](img/bbs6.JPG)


**此应用暂未完善，仅供参考**
