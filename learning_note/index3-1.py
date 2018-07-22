''''''
'''
正则表达式:
字符串操作,如何判断字符串是否是合法的Email地址
正则表达式是一种用来匹配字符串的强有力的武器,
他的设计思想是用一种描述性的语言来给字符串定义一个规则
凡是符合规则的字符串,我们就认为它'匹配'了,否则字符串就是不合法的
所以我们判断字符串是否是合法Email地址的步骤是:
1.创建一个匹配Email地址的正则表达式
2.用该正则表达式来匹配用户的输入是否合法

使用字符来描述字符:'.'可以匹配任意字符
\d 可以匹配数字
\w 可以匹配字母或数字
'py.'可以匹配'pyc','pyo','py!'
\s 匹配一个空格
\- 匹配一个'-'

匹配一個手機號碼
\d{3}\s\d{8}

要匹配变长的字符
* 表示任意个字符
+ 表示至少一个字符
? 表示0或1个字符
{n} 表示n个字符
{n,m} 表示n到m个字符

要做更精确的匹配,可以用[]表示范围:
[0-9a-zA-Z\_]可以匹配一个数字,字母或者下划线;'\'表示转义
[0-9a-zA-Z\_]+可以匹配至少由一个数字,字母或者下划线组成的字符串;
[a-zA-Z\_][0-9a-zA-Z\_]*可以匹配由字母或下划线开头,后接任意个
由一个数字字母或下划线组成的字符串，也就是python合法的變量
限制變量的長度是1-20个字符
[a-zA-Z\_][0-9a-zA-Z\_]{0,19}

A|B 可以匹配Ａ或Ｂ,
^表示行的开头,^\d
$表示行的结束，\d$
Python提供了're'模块包含所有正则表达式的功能
s=r'ABC\-001'
#对应的正则表示式字符串不变:
#'ABC\-001'
'''

import re

# re.match()方法判断是否匹配,
# 你现在是没有代码思维啊哥

test = input("please input string")
if re.match(r'^\d{3}\-\d{3,8}$', test):
    print('ok')
else:
    print('failed')

# 切分字符串
re.match(r'^\d{3}\-\d{3,8}$', '010-12345')

# 除了简单的判断是否匹配之外,正则表达式还有提取子串的功能
# 如果正则表达式定义了组,就可以在match对象用group方法提取子串
m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
print(m)
print(m.group(0))  # 表示原始字符串
print(m.group(1))
print(m.group(2))
t = '19:05:30'
m = re.match(r'^(0[0-9]|1[0-9]|2[0-3]|[0-9])\:'
             r'(0[0-9]|1[0-9]|2[0-9]|3[0-9]|'
             r'4[0-9]|5[0-9]|[0-9])\:(0[0-9]'
             r'|1[0-9]|2[0-9]|3[0-9]|4[0-9]|'
             r'5[0-9]|[0-9])$', t)
print(m.groups())
# 正则匹配默认是贪婪匹配，也就是匹配尽可能多的字符。
# 举例如下，匹配出数字后面的0

# 贪婪匹配
print(re.match(r'^(\d+)(0*)$', '102300').groups())
# 非贪婪匹配
print(re.match(r'^(\d+?)(0*)$', '10134000').groups())

# 每次使用正则表达式匹配字符串的时候需要编译,无法复用,一般采用预编译

re_telephone = re.compile(r'^(\d{3})-(\d{3,8})$')

print(re_telephone.match('010-1333').groups())

print(re_telephone.match('010-244733').groups())


def is_valid_email(addr):
    re_email = re.compile(r'^([0-9a-zA-Z\_\.\-]+)@(\w{1,20}).com$')
    if re_email.match(addr):
        print('ok')
        print(re_email.match(addr).groups())

    else:
        print('failed')


def name_of_email(addr):
    re_email = re.compile(r'^([0-9a-zA-Z\_\.\-]+)@(\w{1,20})(.com|.org)$')
    if re_email.match(addr):
        print('ok')
        print(re_email.match(addr).group(1))

    else:
        print('failed')


is_valid_email('someone@gmail.com')
is_valid_email('bill.gates@microsoft.com')
is_valid_email('bob#example.com')
is_valid_email('mr-bob@example.com')

# name_of_email('<Tom Paris> tom@voyager.org>)'
name_of_email('tom@voyager.org')




