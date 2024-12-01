import moviepy.tools
from config import FILE_DIRECTORY
from pathlib import Path
import datetime


def partition(full_video, res='1280x760', *args):
    videoname = Path(full_video).stem
    converted_path = Path(
        FILE_DIRECTORY,
        str(videoname) + str(datetime.datetime.now())
    )
    converted_path.mkdir()

    FFMPEG = moviepy.ffmpeg_tools.FFMPEG_BINARY
    moviepy.ffmpeg_tools.subprocess_call([
        FFMPEG,
        '-i', full_video, '-s', res,
        '-start_number', '0', '-hls_wrap', '0.2', '-f',
        'hls', str(Path(converted_path, 'part.m3u8'))
    ], logger=None)
    return converted_path


full_video = "assets/full.mp4"

# import vlc
# import time

'''medialist = vlc.MediaList([vlc.Media(media) for media in ['vids/meme/meme.m3u8']])
player = vlc.MediaListPlayer()
player.set_media_list(medialist)
player.next()
player.play()

time.sleep(current_duration)'''
