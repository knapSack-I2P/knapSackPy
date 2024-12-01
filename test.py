import moviepy.tools
from moviepy import VideoFileClip

full_video = "assets/full.mp4"
current_duration = VideoFileClip(full_video).duration
single_duration = 1
vlist = []
print(full_video, current_duration, single_duration, sep=' | ')

FFMPEG = moviepy.ffmpeg_tools.FFMPEG_BINARY
moviepy.ffmpeg_tools.subprocess_call([
    FFMPEG,
    '-i', 'assets/full.mp4', '-s', '1280x760',
    '-start_number', '0', '-hls_wrap', '0.2', '-f',
    'hls', 'vids/meme/meme.m3u8'
], logger=None)

import vlc
import time

'''medialist = vlc.MediaList([vlc.Media(media) for media in ['vids/meme/meme.m3u8']])
player = vlc.MediaListPlayer()
player.set_media_list(medialist)
player.next()
player.play()

time.sleep(current_duration)'''
