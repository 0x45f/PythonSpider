2017/10/8 21:49:22 

Python爬虫抓取爱问知识人问题并保存至数据库

原博主地址：http://cuiqingcai.com/1972.html

# 1.过程 #

## 1.1找到问题列表的页面 ##

首先登录爱问知识的首页，选取一个分类，然后就可以看到在这个分类下的问题列表了。

我是选取了电子数码分类的问题，然后选取了已解决的问题，得到的url是：

    http://iask.sina.com.cn/c/95-goodAnswer-1-new.html

然后用检查这工具审查网页，找到选取页码的元素，可以看到一下的html代码：

    <div class="page mt30"  pageCount="100" ss="1-goodAnswer">
            <a href="/c/95-goodAnswer-1-new.html" class="current">1</a><a class="more" style="display:none;">...</a>
            <a href="/c/95-goodAnswer-180-new.html" class="">2</a>
			<a href="/c/95-goodAnswer-191-new.html" class="">3</a>
			<a class="more" style="">...</a>
			<a href="/c/95-goodAnswer-86988-new.html" class="">100</a>
			<a href="/c/95-goodAnswer-180-new.html" class="btn-page">下一页</a><div style="display:none" currentPage="1" id="currentPage"></div>
        </div>

在这里可以看到当前页之后几页的地址：`/c/95-goodAnswer-180-new.html`，`/c/95-goodAnswer-191-new.html`

这样就可以由当前页找到下一页的地址，所以url也自然分成了两部分，一部分是`http://iask.sina.com.cn`，另一部分是`/c/95-goodAnswer-1-new.html`。

## 1.2查看具体的问题 ##

在`http://iask.sina.com.cn/c/95-goodAnswer-1-new.html`的html代码中可以看到多个类似下面代码的部分：

        <li class="list">
            <div class="cf">
                <div class="user-img">
                	<a href="javascript:void(0);"><img src="http://tva3.sinaimg.cn/crop.65.1.111.111.50/006yaJnejw8f6t1b48uzmj305k05kq2w.jpg" width="40" height="40" alt="阳刚2016" /></a>
						</div>
                <div class="question-title">
                	<a href="/b/v4zBdJ439.html" target="_blank" title="">玥玛指纹锁可以储存多少个指纹？</a>
                </div>
                <div class="queation-other">
                    <span>2回答</span>|<span>2017-09-21</span>
                </div>
            </div>
        </li>/b/v4zBdJ439.html部分就是具体问题的url点进去发现完整的地址是`http://iask.sina.com.cn/b/v4zBdJ439.html`，这样就可以在每一个类似上面html代码的部分找到该页面中所有问题的具体地址。点进去具体的地址后审查具体的html代码可以找到具体的问题内容，提问者，时间等内容，以及该问题的好评回答和其他回答。这样我们就可以开始具体的信息抓取了。## 1.3其他 ##

原博主用的是urllib，Beautiful Soup和MySQLdb来抓取和存储数据。而我选择了requests，xpath语法，lxml库以及pymysql来完成这次的任务。

requests库的用法可以参考原博主的文章：http://cuiqingcai.com/2556.html，也可以参考官方文档：http://docs.python-requests.org/en/master/

xpath可以去w3school上去学，下面贴两张图来介绍一下xpath的简单语法：



lxml用法可以去看原博主的另一文章：http://cuiqingcai.com/2621.html学习lxml的用法，也可以参考lxml的官方文档：http://lxml.de/index.html

lxml中Element的属性以及方法：

    　　tag：string，元素代表的数据种类。
    　　text：string，元素的内容。
    　　tail：string，元素的尾形。
    　　attrib：dictionary，元素的属性字典。
    　　
    　　＃针对属性的操作
    　　clear()：清空元素的后代、属性、text和tail也设置为None。
    　　get(key, default=None)：获取key对应的属性值，如该属性不存在则返回default值。
    　　items()：根据属性字典返回一个列表，列表元素为(key, value）。
    　　keys()：返回包含所有元素属性键的列表。
    　　set(key, value)：设置新的属性键与值。
    
    
    　　＃针对后代的操作
    　　append(subelement)：添加直系子元素。
    　　extend(subelements)：增加一串元素对象作为子元素。＃python2.7新特性
    　　find(match)：寻找第一个匹配子元素，匹配对象可以为tag或path。
    　　findall(match)：寻找所有匹配子元素，匹配对象可以为tag或path。
    　　findtext(match)：寻找第一个匹配子元素，返回其text值。匹配对象可以为tag或path。
    　　insert(index, element)：在指定位置插入子元素。
    　　iter(tag=None)：生成遍历当前元素所有后代或者给定tag的后代的迭代器。
       ＃python2.7新特性
    　　iterfind(match)：根据tag或path查找所有的后代。
    　　itertext()：遍历所有后代并返回text值。
    　　remove(subelement)：删除子元素。

# 2.遇到的问题 #

## 2.1 ##

网上很多介绍lxml的文章都是用的lxml的etree模块，但是我用的是python3.5安装lxml后不支持etree。在网上查了一会也没弄好，还是不能用etree，所以就用了lxml的html模块来完成这次任务。

## 2.2 ##

在保存回答的过程会有时出现这个错误：

    1366 Incorrect string value: '\xF0\x9F\x8E\xA7' for column 'qcontent' at row 1

百度后发现\xF0\x9F\x8E\xA7表示的是emoji表情，普通的字符串或者表情都是占位3个字节，所以utf8足够用了，但是表情符号占位是4个字节，普通的utf8就不够用了，网上的建议是涉及无线相关的 MySQL 数据库建议都提前采用 utf8mb4 字符集。

所以需要将数据库表中保存回答内容字段的字符集改成utf8mb4，并将该表的字符集也修改成utf8mb4。还需要将

    self.__db = pymysql.connect(host='localhost', user='root', password='123', database='test', charset='utf8mb4')

中的charset属性设置为utf8mb4，这样就可以在数据库中保存表情符号了。

## 2.3 ##

保存回答的过程中还有这个错误
    
    1064 You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '好评"，谢谢！"," | 14-01-24")' at line 1

查看问题的回答后发现有的回答中有这样的文字：如果我的答案对你有用,麻烦点击"好评"，谢谢！

是因为文字中的""在执行sql语句时文字中的""导致sql语句被错误的分割所以会导致插入错误。可以利用python中的re模块将内容中的双引号去掉，这样插入就不会出错了。

# 3.后记 #

由于时间仓促所以仅仅是完成了大体功能，大家可以看看自己进行修改。

前段时间学校事情比较多，国庆节有偷懒了几天，所以没有更新。溜了溜了