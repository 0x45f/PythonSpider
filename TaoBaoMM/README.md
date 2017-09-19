2017/9/18 21:08:22 
python抓取淘女郎模特实战


原博主地址：http://cuiqingcai.com/1001.html

# 1.抓取的过程 #

我们想要抓取某些数据要先看我们能否实现抓取，并找到抓取的过程。

## 1.1.找淘女郎的信息 ##

原博主是直接给出了一个抓取的url，而我是去了[淘女郎的官网](https://mm.taobao.com/search_tstar_model.htm?spm=5679.126488.640745.2.b17c0adXs2tQb)查看了网站的html代码后发现代码中并没有淘女郎的信息，那么应该是用js加载的，所以我利用谷歌浏览器的开发者工具在network中找到了

    https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8&page=1

这个请求用来淘女郎的信息，返回的是json数据，格式如下： json_MM1.jpg    json_MM2.jpg  json_MM3.png

可以看到返回的json信息有一共有多个MM，分成多少页，当前是第几页，其中searchDOList对应的就是当前页中MM的信息
包含了身高体重，主页，id等信息，这样就得到了MM的部分信息，然后我们再去主页看看选取了其中一个淘女郎的主页

    https://mm.taobao.com/self/aiShow.htm?spm=719.7763510.1998643336.1.RdNykm&userId=176817195

userId就是刚才从json数据中找到的淘女郎的id这样用前面的部分加上id就可以进入每个淘女郎的主页了。

## 1.2.找相册的信息 ##

但是我们想要抓取的是图片所以我们要找到这个淘女郎的每个相册的地址，点进左侧的相册去看一下，发现每个淘女郎都有很多个相册，而且分成了很多页，但是检查网页的源代码发现也没有相册的信息，所以也应该是用js请求。所以f12发现了这个请求

    https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20=176817195

在地址栏输入后回车，出现了该位淘女郎一页的相册。但是应该有多页才对啊，所以我才应该还有个page的参数，所以在后面加上page=2看看

    https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20=176817195&page=2

果然出现了下一页的相册信息。但是！怎么得到一共有多少页的相册呢，查看一下上面这个地址的源代码，在最后被我我先了有这样一行

    <input name="totalPage" id="J_Totalpage" value="9" type="hidden" />

value=9和相册页数一样，没跑了就是你了，到此我们用uer_id和page信息就可以找到所有淘女郎的相册了。同时，我们在源代码中还可以提取到相册的id就是album_id这个属性，相信我后面会用到的！

## 1.3.找照片的信息 ##

点进一个相册看一下情况，同样照片的信息也是用js加载，f12找找找，被我找到了这样一个网址

    https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=176817195&album_id=10000794223&top_pic_id=0&cover=%2F%2Fimg.alicdn.com%2Fimgextra%2Fi2%2F176817195%2FTB1i8OAKXXXXXXUXpXXXXXXXXXX_!!0-tstar.jpg&page=1&_ksTS=1505740411597_155&callback=jsonp156
   
返回的也是json数据，但是url后面的参数太多了，精简一下看看
    
    https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=176817195&album_id=10000794223&page=1

可以也成功得到了json数据，来看一下json数据的具体格式：json_img1.png  json_img2.png
包含了这个相册有多少张照片，分成多少页，以及每张照片的具体信息。picList就是这一页中照片的信息，里面有照片的具体地址。这样我们用user_id，album_id,page加上前面的地址就可以找到一个淘女郎的所有图片辣！

## 1.4.过程 ##

- 找到一共有多少页的淘女郎
- 找到每位淘女郎的id
- 找到每位淘女郎有多少页的相册
- 找到每个相册的id
- 进入相册查看找到相册内的每张照片的地址



# 2.遇到的问题 #

1. response.read().decode()用utf-8解码后出错，说明返回的字符串并不是utf-8编码。python中有可以查看字符串编码方式的模块chardet，该模块的chardet.detect()方法可以查看字符串的编码方式。我们要抓取的网页的信息就是gkb编码方式

2. python中的JSON
   使用 JSON 函数需要导入 json 库：import json。函数`json.dumps`将 Python 对象编码成 JSON 格式。函数`json.loads`	将已编码的 JSON 字符串解码为 Python 对象

3. **json只是一种编码格式，在python中并不是一种具体的类。**JSON的键/值对中的键始终为str类型，而且python中的json模块总是产生str对象

4. python在参数传递时分为两种情况：对于不可变对象作为函数参数，相当于C系语言的值传递；对于可变对象作为函数参数，相当于C系语言的引用传递。

5. Python爬虫--timeout设置--防止访问时间过长造成假死。没有设置timeout参数，结果在网络环境不好的情况下，时常出现read()方法没有任何反应的问题，程序卡死在read()方法里。我在python3中好像没有找到设置全局timeout值的方法，但是在python2中可以设置全局的Socket 的全局 Timeout 值。

    import urllib2  
    import socket  
    socket.setdefaulttimeout(10) # 10 秒钟后超时  
    urllib2.socket.setdefaulttimeout(10) # 另一种方式

6. 使用try expect 可以防止程序崩溃。[这里查看python中错误的继承关系](https://docs.python.org/3/library/exceptions.html#exception-hierarchy) 

7. 刚开始是想把一位淘女郎的照片全部爬取的，但是！一个人照片太多了，一个人爬了2W张还没爬完。就改了代码每个人爬取1000张。以后继续学习后希望可以重新写一下这个程序将所有的照片全部爬取！！！


8. 运行了一段时间出现了这样一个错误：远程主机强迫关闭了一个现有的连接。应该是服务器识别出了爬虫，所以在加header中加入了User-Agent并且爬取一段时间后sleep一秒。

# 3.划重点！！！！！！！！！ #

这是第三次写python了好开心，虽然依旧辣眼睛，希望各位能凑合看，可以加我qq516310189一起交流学习呀！