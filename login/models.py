from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class Users(AbstractUser):
    '''Users 是相关的用户信息'''
    id = models.AutoField('ID', primary_key=True, help_text="用户ID")   # 用户ID，唯一标识
    sum = models.TextField(max_length=500, default="这个人没有写简介", help_text="个人简介")    # 个人的简介（限制字符500）
    icon = models.FileField('Icon', null=True, upload_to="users_icon")  # 视频封面的存储地址

    AUTHORITY_OF_CHOICES = [    # 用户权限
        ('n', 'nomal'),  # 普通用户
        ('m', 'member'), # 会员
        ('s', 'super'),  # 管理员
    ]

    authority = models.CharField('Authority', max_length=10, choices=AUTHORITY_OF_CHOICES, default='n', help_text="用户权限")   # 用户权限

    def __str__(self):
        return self.username
    
class Verification(models.Model):
    code = models.TextField('Code', max_length=20, help_text="验证码")
    gen_time = models.DateTimeField(default=timezone.now)
    email = models.EmailField('Email', max_length=50, help_text="邮箱")