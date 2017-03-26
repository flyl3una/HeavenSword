## xadmin使用

xadmin：django的后台管理工具，比原生的admin好看好用

#### 1.安装快速使用

```python
pip install xadmin	#安装xadmin模块
```

打开django项目的setting.py文件，在INTALLED_APPS里面注释掉django.contrib.admin,添加xadmin。

xadmin默认为英语，改为简体中文。在setting.py下添加以下代码。

```python
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
```

修改url.py里的urlpatterns,注释掉原生的urls，改为映射到xadmin的urls。

```python
# url(r'^admin/', admin.site.urls),
url(r'^admin/', include(xadmin.site.urls)),
```

打开网址目录的/admin/即可登录后台。