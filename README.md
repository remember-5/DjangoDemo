## 项目介绍
项目是联系django的初级入门项目，只是为了做一些基本的crud和restful风格的api，

也可以当作模版来直接使用

## 使用pymysql错误问题

报错
```
File "/home/www/.local/share/virtualenvs/EduScore-UXZMOCwv/lib/python3.6/site-packages/django/db/backends/mysql/base.py", line 36, in <module>
    raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3.
```

`venv/lib/python3.8/site-packages/django/db/backends/mysql/base.py`
中的35,36行注释掉就好了

如下：
```
#if version < (1, 3, 13):
#    raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
```
---
报错
```
AttributeError: 'str' object has no attribute 'decode'
```
`venv/lib/python3.8/site-packages/django/db/backends/mysql/operations.py`
中的146行 把decode改为encode
如下：
```
query = query.encode(errors='replace')
```

## 初始化admin用户

`python3 manage.py createsuperuser`
输入用户名和密码即可

## 适配中文
在`setting`文件中加入
```
# 把英文改为中文
LANGUAGE_CODE = 'zh-hans'

# 把国际时区改为中国时区（东八区）
TIME_ZONE = 'Asia/Shanghai'
```


## 数据源切换到mysql

1. `pip install pymysql`

2. 在`__init__.py`下新增代码
```
import pymysql

pymysql.install_as_MySQLdb()
```

3.在`settings.py`在增加代码
```
'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spring_boot_demo',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
```

4.迁移默认数据库
```
python manage.py makemigrations # 将类转换成数据表结构
python manage.py migrate # 根据上一句代码生成数据表
```

5.反向生成model

打印到控制台
```
python manage.py inspectdb
```

将model导入到app的model.py文件里
```
python manage.py inspectdb > blog/models.py
```

然后执行
```
python manage.py makemigrations
python manage.py migrate
```

6. 若要在管理端实现数据表信息的管理，只需要在admin.py中添加如下代码即可实现。真可谓言简意赅啊。
```
from blog.models import BlogArticle

admin.site.register(BlogArticle)
```
