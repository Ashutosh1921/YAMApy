from django.urls import path
from yamapy_app import views

urlpatterns = [
    path('', views.home, name='index'),
    path('download/<str:ext>/<int:fid>/', views.download_video, name='video_downloads'),
    path('download/<str:ext>/', views.download_audio, name='audio_downloads'),
    path('thanks/', views.youtube, name='youtube')
]
