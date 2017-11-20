2017-10-29

# 前言

知乎是自己经常用的一个app，经常看到知乎上很多人说知乎的很多的用户是程序员，也看到过有人爬取过有人知乎的用户然后进行分析。我就在想自己可不可以也通过python实现这个过程。

前面几次写了几个简单的爬虫，熟悉了爬虫基本的思路，这次是想写一个复杂一点的爬虫，尽量多的爬取更多的数据，并且能够避免爬取重复的内容。可能会用到的数据库mysql、redis、mongodb以及python多线程等内容。

# 准备内容

### 数据库

1. 这次用到的数据库是redis、mongodb。mongo在课上接触过一点，大体上知道一点概念。但是redis是第一次接触之前只是听说过用redis来做队列，这次算是第一次尝试使用redis。
2. 用redis是当队列来用，存储用户的url。mongo是用来存储用户的具体信息，之前是想用mysql来存储用户信息，但是看到知乎返回的用户信息都是json格式的，而且用户的信息不统一，考虑到mongo可能能好一点，返回的json信息可以当作一整个document存储起来。
3. 我实在windows上写代码的，在win上redis和mongo的安装可能比较繁琐，所及就直接使用了云主机上跑的数据库。配置的过程在我上一篇的博客中都有，感兴趣的可以看一下。当然可以在win上配置这两个数据库，都是可以的。
4. 用到的数据库模块redis模块：redis；mongodb模块：pymongo

### 多线程

1. 想要加快爬取的速度所以用到了python多线程的内容。之前在学校学的都是java，这次接触python多线程的内容类比着java中的内容来学习。很多概念都是相同的，比如说线程锁啊、父进程和子进程之间的关系啊。
2. 多线程使用的模块是threading.Thread

### 用到的其他模块

1. configparser模块：用ini配置文件来配置数据库的连接信息，用configparser模块了读取配置信息。
2. cookiejar模块：用来读取文件的cookies登录信息。
3. json模块：处理返回的json信息。
4. 其他的模块比如requests、time、lxml模块都是之前用过的模块，不再说明。

# 实现过程

### 具体内容的爬取

1. 首先在`https://www.zhihu.com/explore`爬取该页上出现的用户的信息。在该页面上的用户一般都有较多的粉丝数目，比较容易开始我们的爬取。

2. `https://www.zhihu.com/people/xingrima`是某位用户的主页，前一部分`https://www.zhihu.com/people/`每个用户都是相同的，后面的尾巴是每个用户的标识。在该页面中可以看到用户具体的信息包括该用户关注的人以及关注该用户的人。然后分析一下打开用户主页时发送的请求，可以看到有一个这样的请求：

   ```
   https://www.zhihu.com/api/v4/members/xingrima?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cincluded_answers_count%2Cincluded_articles_count%2Cincluded_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_bind_phone%2Cis_force_renamed%2Cis_bind_sina%2Cis_privacy_protected%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cis_org_createpin_white_user%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics
   ```

   同样的`xingrima`部分是用户的标识，其他部分每个用户都是相同的。

   这个请求返回的用户的所有信息，而且是json格式的。再来看一下返回的具体信息（只截取了一部分）：

   ​							用户json格式的信息图片

   这样返回的整个json信息就可以作为整体存进mongo了

3. 在用户主页上我们也可以看到该用户关注的人和关注该用户的人。点击主页上“关注了”按钮可以看到发送了这样一个请求：

   ```
   https://www.zhihu.com/api/v4/members/xingrima/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20
   ```

   同样的`xingrima`部分是用户的标识，其他部分每个用户都是相同的。

   这个请求返回了20（最多只能一次返回20个）个该用户关注的人。看一下返回的具体信息（只截取了一部分）：

   ​							关注人的信息图片

   我们只关注其中的几个信息就可以了。is_end表示是否是最后一页；next表示返回下20个用户的url；data表示的是具体的用户信息，但是这其中用户信息并不全，想要获得用户全部的信息还是需要对第二步中的url进行访问。所以我们只要用户数据的url_token属性就可以了，用url_token替换第二步中用户标识的部分来获取用户的全部信息。

   这是获取用户关注的人的过程，想要获取关注该用户的人，只要将上面的url中followees改变成followers就可以获取关注该用户的人了。返回的数据格式和上面介绍的是一样的

### 数据库部分

1. 用redis当作用户url的队列。redis中维护了一个list和一个hash。

   list存储了还没存储信息的用户的url_token，hash中记录的是已经存储过信息的用户的url_token

   这样当找到新的用户url_token的时候，先在hash中查询是否存在该url_toekn，如果不存在，就将该url_token加入到list和hash中。要爬取用户数据的时候，从list弹出一条记录，进行爬取

2. 用ini配置文件来配置数据库的连接信息

### 多线程部分

1. 多线程部分的实现比较简单，每个线程执行的任务是一样的，流程如下：
   - 开始判断redis的list中是否有等待爬取信息的url_token，如果没有则从主页`https://www.zhihu.com/explore`爬取用户（一般只要一个线程执行此步骤之后其他线程就不需要执行此步了）
   - 如果redis的list中有等待爬取信息的url_token，则从list头部弹出一个url_toekn。
   - 请求该用户的详细信息并保存进mongo，然后分别获取该用户关注的人和关注该用户的人的url_token并存入redis
   - 之后线程循环执行上面的步骤
2. 使用的线程模块是threading.Thread，并且给每个线程分配了一个编号（也可以直接用python给分配的编号threading.current_thread().name）

# 问题和想法总结

### 爬虫被屏蔽

### redis和mongo几个操作函数

### 去重

Bloom Filter算法(布隆过滤器)

### python多线程

### 其他几个问题





防止爬虫被屏蔽

代理IP、ua、cookies、减速减速再减速



```
                        CookieJar____
                        /     \      \
            FileCookieJar      \      \
             /    |   \         \      \
 MozillaCookieJar | LWPCookieJar \      \
                  |               |      \
                  |   ---MSIEBase |       \
                  |  /      |     |        \
                  | /   MSIEDBCookieJar BSDDBCookieJar
                  |/
               MSIECookieJar
```

Python中cookielib库（python3中为http.cookiejar）

CookieJar，FileCookieJar，MozillaCookieJar,LWPCookieJar

CookieJar对象存储在内存中

FileCookieJar(filename)创建FileCookieJar实例，检索cookie信息并将信息存储到文件中，filename是文件名。

MozillaCookieJar(filename)创建与Mozilla cookies.txt文件兼容的FileCookieJar实例。

LWPCookieJar(filename)创建与libwww-perl Set-Cookie3文件兼容的FileCookieJar实例。

参数ignore_discard=True表示即使cookies将被丢弃也把它保存下来，它还有另外一个参数igonre_expires表示当前数据覆盖（overwritten）原文件。注意，除非你通过传递一个真实的*ignore_discard*参数，否则`save()`方法不会保存会话cookie。



它们并不返回布尔值，而是返回它们实际进行比较的值之一。

对于and操作符：只要左边的表达式为真，整个表达式返回的值是右边表达式的值，否则，返回左边表达式的值对于or操作符：只要两边的表达式为真，整个表达式的结果是左边表达式的值。如果是一真一假，返回真值表达式的值如果两个都是假，比如空值和0，返回的是右边的值。（空值或0）

dump和dumps是将python对象转换成json格式；load和loads是将json格式转换成python对象

redis操作

在redis中维护两个集合：一个hash，一个list。 当从网页中抓取到一个url_token时，检查在hash中时候存在，如果不存在就将它放入list的尾部，作为还没有抓取的用户。当需要抓取用户信息的时候从list 的头部弹出一个url_token，进行抓取。当抓取完成后，将该url_token存取hash

redis数据库中的原始命令

HSET key field value 将哈希表 key 中的字段 field 的值设为 value 。

HEXISTS key field 查看哈希表 key 中，指定的字段是否存在。

BLPOP key1 [key2 ] timeout 移出并获取列表的第一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。

RPUSH key value1 [value]在列表中添加一个或多个值



python random

random.random():生成一个[0, 1)之间的随机浮点数

random.uniformrandom.uniform(a, b):生成[a,b)之间的浮点数

random.randint(a, b):生成[a,b]之间的整数

random.randrange(a, b, step):在指定的集合[a,b)中,以step为基数随机取一个数.如random.randrange(0, 20, 2),相当于从[0,2,4,6,...,18]中随机取一个

python 多线程

join（）的作用是，在子线程完成运行之前，子线程会将主线程一直阻塞在调用join地方

setDaemon() 默认情况下，主线程在退出时会等待所有子线程的结束。如果希望主线程不等待子线程，而是在退出时自动结束所有的子线程，就需要设置子线程为后台线程(daemon)。方法是通过调用线程类的setDaemon()方法。注意setDaemaon()需要在start之前调用



java中继承（只能单继承）的构造函数

1、子类的构造过程中必须调用其基类的构造方法。

2、如果子类的构造方法中没有显示的调用基类的构造方法，则系统默认调用基类的无参数构造方法。

3、如果父类只有有参的构造方法，没有无参的构造方法，则子类必须在构造方法中必须显式调用super(参数列表)来指定某个有参的构造方法

python中继承（可以多继承）的构造函数

1：在继承中基类的构造不会被自动调用，它需要在其派生类的构造中亲自专门调用。有别于java

2：在调用基类的方法时，需要带上self参数变量。



python继承

        OBJ
         |
       -----
      |     |  
    obj1   obj2
在继承关系中，属性查找的时候是从上到下查找，而设置属性的时候是从下到上查找

python静态方法和类方法

静态方法：类对象和实例都可以调用静态方法，使用装饰器@staticmethod定义静态方法，不能对类或实例中的属性进行操作

类方法：类对象和实例都可以调用类方法，类方法使用@classmethod装饰器定义，其第一个参数是类，约定写为cls。可以操作类中的属性

python 定时任务

threading的Timer模块

sched模块



# 源代码地址



# 后记

这几天都在忙学校的实验而且！！！！要考试了啊啊啊啊啊，没有更新，一定要坚持啊啊啊啊啊啊啊啊！！！！！