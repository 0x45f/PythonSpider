遍历所有的问题，来抓取每一个详情页面，提取问题，问题内容，回答者，回答时间，回答内容。


XPath

/绝对路径？
//表示选取所有？


Element属性方法

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
　　iter(tag=None)：生成遍历当前元素所有后代或者给定tag的后代的迭代器。＃python2.7新特性
　　iterfind(match)：根据tag或path查找所有的后代。
　　itertext()：遍历所有后代并返回text值。
　　remove(subelement)：删除子元素。


XPath 轴（Axes）

ancestor	   选取当前节点的所有先辈（父、祖父等）。

ancestor-or-self	选取当前节点的所有先辈（父、祖父等）以及当前节点本身。

attribute	选取当前节点的所有属性。

child	选取当前节点的所有子元素。

descendant	选取当前节点的所有后代元素（子、孙等）。

descendant-or-self	选取当前节点的所有后代元素（子、孙等）以及当前节点本身。

following	选取文档中当前节点的结束标签之后的所有节点。

namespace	选取当前节点的所有命名空间节点。

parent	选取当前节点的父节点。

preceding	选取文档中当前节点的开始标签之前的所有节点。

preceding-sibling	选取当前节点之前的所有同级节点。

self	选取当前节点。