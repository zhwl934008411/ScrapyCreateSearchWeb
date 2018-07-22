# coding:utf8
''''''

'''
深度优先和广度优先
1.深度优先(递归实现)：顺着一条路，走到最深处。然后回头
2.

session和cookie的用法和区别
一、cookie：

在网站中，http请求是无状态的。也就是说即使第一次和服务器连接后并且登录成功后，
第二次请求服务器依然不能知道当前请求是哪个用户。cookie的出现就是为了解决这个问题，
第一次登录后服务器返回一些数据（cookie）给浏览器，然后浏览器保存在本地，当该用户
发送第二次请求的时候，就会自动的把上次请求存储的cookie数据自动的携带给服务器，
服务器通过浏览器携带的数据就能判断当前用户是哪个了。cookie存储的数据量有限，
不同的浏览器有不同的存储大小，但一般不超过4KB。因此使用cookie只能存储一些小量的
数据。
二、session:

session和cookie的作用有点类似，都是为了存储用户相关的信息。不同的是，cookie是
存储在本地浏览器，而session存储在服务器。存储在服务器的数据会更加的安全，不容
易被窃取。但存储在服务器也有一定的弊端，就是会占用服务器的资源，但现在服务器
已经发展至今，一些session信息还是绰绰有余的。
三、cookie和session结合使用：

web开发发展至今，cookie和session的使用已经出现了一些非常成熟的方案。在如今的
市场或者企业里，一般有两种存储方式：

1、存储在服务端：通过cookie存储一个session_id，然后具体的数据则是保存在session
中。如果用户已经登录，则服务器会在cookie中保存一个session_id，下次再次请求的时
候，会把该session_id携带上来，服务器根据session_id在session库中获取用户的
session数据。就能知道该用户到底是谁，以及之前保存的一些状态信息。这种专业术语
叫做server side session。

2、将session数据加密，然后存储在cookie中。这种专业术语叫做client side session。
flask采用的就是这种方式，但是也可以替换成其他形式。


常见 httpcode
code        说明
200         请求被成功处理
301/302     永久性重定向/临时性重定向
403         请求被禁止，没有权限访问
404         地址未找到，表示对应的资源
500         服务器错误
503         服务器停机或正在维护

https://www.zhihu.com/api/v4/questions/29372574/answers?data%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type=best_answerer%29%5D.topics&data%5B%2A%5D.mark_infos%5B%2A%5D.url=&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp&limit=5&offset=0&sort_by=default
pages:
is_end 
next
totals

data[0]:
id
question_created
question_updated_time
author_id 可以为空

url
created_time
updated_time
voteup_count
comment_count
content

'''






