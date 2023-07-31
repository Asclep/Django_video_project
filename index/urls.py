from django.urls import path
from index import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/video/', views.upload_video, name='upload'),
    path('video/<v_id>/', views.video_play, name="video_play")
]
