import os
import pathlib
from django.shortcuts import render, redirect

from yamapy_app.forms import YAMAPy
import youtube_dl


def home(request):
    global context
    context = {}
    form = YAMAPy()
    context['form'] = form
    if request.POST:
        url = request.POST['yt_vid_url']
        context['yt_vid_url'] = url
        file_type = request.POST['file_type']
        with youtube_dl.YoutubeDL({}) as ydl:
            meta = ydl.extract_info(url, download=False)
            formats = meta.get('formats', [meta])
            vid_info = {
                'title': meta.get('title', None),
                'description': meta.get('description'),
                'likes': f'{int(meta.get("like_count", 0)):,}',
                'duration': str(round(int(meta.get('duration', 1)) / 60, 2)) + ' minutes',
                'views': f'{int(meta.get("view_count")):,}'
            }
            vid_keyword = str(url).removeprefix('https://www.youtube.com/watch?v=')
            context['vid_info'] = vid_info
            context['vid_keyword'] = vid_keyword
            context['dl'] = True
            if int(file_type) == 0:
                context['ext'] = "video"
            elif int(file_type) == 1:
                context['ext'] = "audio"
            return render(request, 'yamapy_app/index.html', context)
    else:
        context['dl'] = []
        return render(request, 'yamapy_app/index.html', context)


def download_video(request, ext, fid):
    video_url = context['yt_vid_url']
    print(video_url)
    if video_url:
        if os.path.exists("media/video.mp4"):
            os.remove("media/video.mp4")
        if os.path.exists("media/video.webm"):
            os.remove("media/video.webm")
        if os.path.exists("media/video.mp3"):
            os.remove("media/video.mp3")
        if os.path.exists("media/video.m4a"):
            os.remove("media/video.m4a")
        ydl_out = {'format': 'bestvideo/best', 'outtmpl': 'media/video.%(ext)s'}
        with youtube_dl.YoutubeDL(ydl_out) as ydl:
            ydl.download([video_url])
        l = list(pathlib.Path('media').glob('video*'))
        for path in l:
            file = str(path)
        extension = file.split('.')[1]
        context['extension'] = extension
        context['dl_file'] = 1
        return redirect('youtube')
    else:
        return redirect('youtube')


def download_audio(request, ext):
    video_url = context['yt_vid_url']
    print(video_url)
    if video_url:
        if os.path.exists("media/audio.mp4"):
            os.remove("media/audio.mp4")
        if os.path.exists("media/audio.webm"):
            os.remove("media/audio.webm")
        if os.path.exists("media/audio.mp3"):
            os.remove("media/audio.mp3")
        if os.path.exists("media/audio.m4a"):
            os.remove("media/audio.m4a")
        ydl_out = {'format': 'bestaudio/best', 'outtmpl': 'media/audio.%(ext)s'}
        with youtube_dl.YoutubeDL(ydl_out) as ydl:
            ydl.download([video_url])
        file = ""
        l = list(pathlib.Path('media').glob('audio*'))
        for path in l:
            file = str(path)
        extension = file.split('.')[1]
        context['dl_file'] = 2
        context['extension'] = extension
        return redirect('youtube')
    else:
        return redirect('youtube')


def youtube(request):
    context['MEDIA_URL'] = '/media/'
    return render(request, 'yamapy_app/youtube.html', context)
