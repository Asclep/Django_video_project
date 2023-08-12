# REI 视频网站

---

基于`Python`和`Django`搭建的视频网站。

## 主要功能

---

- 支持用户的注册，登录，密码找回功能
- 支持用户上传视频
- 支持视频的收藏功能，能够显示视频的观看量以及收藏量
- 支持视频的标题模糊搜索功能

## 安装

---

使用`pip`安装环境依赖包：

```bash
pip install -r requirements.txt
```

## 运行

---

修改`rei/settings.py`中的配置：

### 连接数据库

将以下代码中的相关信息换成你的数据库信息：

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

### 注册APP

在`INSTALLED_APPS`中添加：

```python
"index.apps.IndexConfig",   #用于主页的显示功能
"login.apps.LoginConfig",   #与用户相关的信息
```

### 修改时区和语言

将时区和语言换成：

```python
LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"
```

### 添加静态文件路径

修改静态文件路径为：

```python
STATIC_URL = "static/"
STATICFILES_DIRS=(os.path.join(BASE_DIR,'static'),
                  os.path.join(BASE_DIR, "index/static/"),
                  )
```

### 修改默认的`User`

在末尾添加：

```python
# 修改默认的user类
AUTH_USER_MODEL = 'login.Users'
```

### 配置媒体文件路径

在末尾添加：

```python
# 配置媒体文件路径
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 配置邮件相关信息

在末尾添加：

```python
# 发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# smpt服务地址
EMAIL_HOST = 'xxx'
EMAIL_PORT = 25  # 端口默认都是25不需要修改
# 发送邮件的邮箱，需要配置开通SMTP
EMAIL_HOST_USER = 'xxx'
# 在邮箱中设置的客户端授权密码
# 此处使用邮箱授权码登录
EMAIL_HOST_PASSWORD = 'xxx'
# 收件人看到的发件人
EMAIL_FROM = 'xxx'
```

在`命令行`中运行：

### 迁移数据

```bash
python manage.py makemigrations
python manage.py migrate
```

### 创建超级用户

```bash
python manage.py createsuperuser
```

### 其他文件依赖

需要在`media/icons`目录下提供一张`background.png`的图像文件作为背景。其余的图标也可被替换，但需保证文件名与`html`文件中使用的路径相同。

### 开始运行

在`命令行`中执行：

```python
 python manage.py runserver
```

然后登录网站即可看到效果。

## 效果展示



## 问题相关

这是我制作的第一个`Django`的项目，目前只完成了基本功能，后续还会添加更多的功能。同时，里面肯定也会存在许多的问题，欢迎大家将问题描述发送至我的邮箱：asclep@163.com（虽然不会经常查看:smile:），一起学习，共同进步。