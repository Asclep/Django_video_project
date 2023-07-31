from django.db import models
from login.models import Users
import uuid #生成唯一id标识
from django.core.files.storage import FileSystemStorage
# Create your models here.

'''生成8位短id时会用到的数组'''
array = [ "0", "1", "2", "3", "4", "5","6", "7", "8", "9",
          "a", "b", "c", "d", "e", "f","g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s","t", "u", "v", "w", "x", "y", "z",
          "A", "B", "C", "D", "E", "F", "G", "H", "I","J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V","W", "X", "Y", "Z"
          ]
'''生成8位短id时会用到的函数'''
def get_short_id():
    id = str(uuid.uuid4()).replace("-", '') # 注意这里需要用uuid4
    buffer = []
    for i in range(0, 8):
        start = i *  4
        end = i * 4 + 4
        val = int(id[start:end], 16)
        buffer.append(array[val % 62])
    return "".join(buffer)

class Videos(models.Model):
    '''Video 是视频的相关信息，比如：id，发布者等信息'''

    video_id = get_short_id()  # 获取一个随机的视频ID
    id = models.CharField('ID', primary_key=True, max_length=10,  default=video_id, help_text='视频的唯一id（八位）')   # 视频的唯一id（八位数字加英文字母）
    author = models.ForeignKey(Users, null=True, blank=True, on_delete=models.SET_NULL, help_text="视频的作者")  # 视频的作者（一对多）
    title = models.CharField('Title', max_length=40, unique=False, help_text="视频的标题")    # 视频的标题(唯一的，限制字符50)
    sum = models.TextField(max_length=500, help_text="视频的简介")    # 视频的简介（限制字符500）
    view_counts = models.IntegerField('ViewCounts', default=0, help_text="视频的播放量")   # 视频的播放量（暂时不用）
    favorites_counts = models.IntegerField('Favorites_counts', default=0, help_text="视频的收藏量") # 视频的收藏量（暂时不用）
    address = models.FileField('Address',upload_to=video_id)  # 视频的存储地址
    cover = models.FileField('Cover', upload_to=video_id)  # 视频封面的存储地址
    STATES = [('n','Normal'), ('e','Examing'), ('i','Illegal')]
    state = models.TextField('State', choices=STATES, default='e')    # 视频的状态（正常播放，审核中，非法的）
    
    def __str__(self):
        return self.title
    
class Favorites(models.Model):
    '''Favorites存储了相关的收藏信息'''

    id = models.AutoField(primary_key=True, help_text=" 收藏的id")
    video = models.ForeignKey(Videos, null=True, on_delete=models.SET_NULL, help_text="收藏的视频")
    user_src = models.ForeignKey(Users, on_delete=models.CASCADE, help_text="用户")
    add_time = models.DateTimeField(auto_now_add=True)

class Views(models.Model):
    '''Views存储了相关的收藏信息'''

    id = models.AutoField(primary_key=True, help_text=" 观看的id")
    video = models.ForeignKey(Videos, null=True, on_delete=models.SET_NULL, help_text="观看的视频")
    user_src = models.ForeignKey(Users, on_delete=models.CASCADE, help_text="用户")
    add_time = models.DateTimeField(auto_now=True)
