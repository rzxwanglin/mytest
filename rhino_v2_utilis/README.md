# rhino_v2_utilis
封装的一些第三方库


## 1、rhino_v2_utilis
### 概括

    封装redis模块 使redis异常恢复后时，爬虫仍可正常运行

    封装数据存储方式，支持kafka和redis存储

    封装redis、kafka ssl的支持和ssl证书

    封装数据和任务队列


### 使用方法
**参考example**
```
#向公共组件传入参数,详细参数可参看 ConfigHandler 的引用
rhino_v2_utilis_config={
  "platform_port": 443,
  "site_type": "telegram",
  "platform_proxy": [
    "10.11.203.70:9999"
  ],
  "task_host": "10.11.203.68",
  "task_port": 6382,
  "task_password": "surfilter@1218",
  "task_db": 0,
  "data_host": "183.240.204.129",
  "data_port": 16380,
  "data_password": "surfilter@1218",
  "data_db": 1,
  "project_list": [
    "skynet"
  ],
  "public_ip": "1.1.1.1",
  "private_ip": "0.0.0.0",
  "msg_type": "telegram"
}
ConfigHandler.format(**rhino_v2_utilis_config)


# 公共组件提供对外变量 在settings.py 常用redis相关参数
```
   
    
### 打包方法
**配置**
用户根目录下添加.pypirc文件
```text
[distutils]
index-servers =
    nexus
 
[nexus]
repository=http://192.168.59.89:8081/repository/crwalpypi-hosted/
username=admin
password=rzx@1218
```
** 打包**
python setup.py sdist bdist_wheel
**上传**
```text
pip install twine
```
twine upload -r nexus dist/* 

### 安装方法

### 参数说明
msg_type 为日志中的索引模块 必须要有 

site_type 为在平台配置的 应用类型 必须要有

### 错误反馈


# 编码规范
参考PEP8
## 1、空格的使用
```text
#1、使用空格来表示缩进而不要用制表符（Tab）。这一点对习惯了其他编程语言的人来说简直觉得不可理喻，因为绝大多数的程序员都会用Tab来表示缩进，但是要知道Python并没有像C/C++或Java那样的用花括号来构造一个代码块的语法，在Python中分支和循环结构都使用缩进来表示哪些代码属于同一个级别，鉴于此Python代码对缩进以及缩进宽度的依赖比其他很多语言都强得多。在不同的编辑器中，Tab的宽度可能是2、4或8个字符，甚至是其他更离谱的值，用Tab来表示缩进对Python代码来说可能是一场灾难。

#2、和语法相关的每一层缩进都用4个空格来表示。

#3、每行的字符数不要超过79个字符，如果表达式因太长而占据了多行，除了首行之外的其余各行都应该在正常的缩进宽度上再加上4个空格。

#4、函数和类的定义，代码前后都要用两个空行进行分隔。

#5、在同一个类中，各个方法之间应该用一个空行进行分隔。

#6、二元运算符的左右两侧应该保留一个空格，而且只要一个空格就好。
```
## 2 标识符命名
```text
#1、变量、函数和属性应该使用小写字母来拼写，如果有多个单词就使用下划线进行连接。

#2、类中受保护的实例属性，应该以一个下划线开头。

#3、类中私有的实例属性，应该以两个下划线开头。

#4、类和异常的命名，应该每个单词首字母大写。

#5、模块级别的常量，应该采用全大写字母，如果有多个单词就用下划线进行连接。

#6、类的实例方法，应该把第一个参数命名为self以表示对象自身。

#7、类的类方法，应该把第一个参数命名为cls以表示该类自身。

#8、
```

## 优先级支持
优先级队列名称:priority-1:{tag}:{type}:{task}

需要在爬虫中:
所有获取任务的使用:CTaskInterface.get_task
塞回任务的使用:CTaskInterface.push_task

## 2 表达式和语句
```text
#1、采用内联形式的否定词，而不要把否定词放在整个表达式的前面。例如if a is not b就比if not a is b更容易让人理解。

#2、不要用检查长度的方式来判断字符串、列表等是否为None或者没有元素，应该用if not x这样的写法来检查它。

#3、就算if分支、for循环、except异常捕获等中只有一行代码，也不要将代码和if、for、except等写在一起，分开写才会让代码更清晰。

#4、import语句总是放在文件开头的地方。

#5、引入模块的时候，from math import sqrt比import math更好。

#6、如果有多个import语句，应该将其分为三部分，从上到下分别是Python标准模块、第三方模块和自定义模块，每个部分内部应该按照模块名称的字母表顺序来排列。
```