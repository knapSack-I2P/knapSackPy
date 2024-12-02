import datetime
from pathlib import Path

import moviepy.tools

from abstractions.knapclasses import *
from config import FILE_DIRECTORY
from rich.progress import track


# Function that makes list of knaps from the original video
def partition(full_video, res='1280x760', *args):
    videoname = Path(full_video).stem  # Original video name
    converted_path = Path(
        FILE_DIRECTORY,
        str(videoname) + datetime.datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    )  # Path to a directory which contains Knaps

    # Creating a directory for Knaps
    converted_path.mkdir()

    # Making temporary .m3u8 and .ts files from original video
    FFMPEG = moviepy.ffmpeg_tools.FFMPEG_BINARY
    moviepy.ffmpeg_tools.subprocess_call([
        FFMPEG,
        '-i', full_video, '-s', res,
        '-start_number', '1', '-hls_wrap', '0.2', '-f',
        'hls', str(Path(converted_path, 'part.m3u8'))
    ], logger=None)

    ts_knaps: dict[int, list[Knap]] = {}
    video_hash = sha256()
    idx = 1

    # Making Knaps from .ts files
    for ts in track(converted_path.iterdir(), description='Knapping...'):
        if ts.suffix != '.ts' or not ts.stem:
            continue
        ts_idx = int(ts.stem[4:])
        ts_knaps[ts_idx] = []
        with open(ts, 'rb') as _ts:
            byte = _ts.read(25 * 1024)  # reading first knap
            while byte:
                # making knap's hash
                hash = sha256(byte)

                # making a file which contains knap's data
                with open(FILE_DIRECTORY / 'sack' / (hash.hexdigest() + '.knap'), 'wb') as knap_file:
                    knap_file.write(byte)

                # making knap representation
                knap = Knap(FILE_DIRECTORY / 'sack' /
                            (hash.hexdigest() + '.knap'), idx, hash)
                ts_knaps[ts_idx].append(knap)

                # reading next knap
                idx += 1
                byte = _ts.read(25 * 1024)
        ts.unlink()  # deleting temporary file

    # Making NullKnap from the .m3u8 file
    m3u8 = converted_path / 'part.m3u8'
    with open(m3u8, 'rb') as _m3u8:
        byte = _m3u8.read()
        null_knap = NullKnap(
            byte,
            [len(ts_knaps[i + 1]) for i in range(len(ts_knaps))],
            sha256(byte)
        )
    m3u8.unlink()
    converted_path.rmdir()
    ts_knaps[0] = [null_knap]

    # Making KnapVideo
    cnt = 0
    for i in track(range(len(ts_knaps)), description='Hashing...'):
        for knap in ts_knaps[i]:
            video_hash.update(knap.hash16.encode('utf-8'))
            cnt += 1

    knap_video = KnapVideo(cnt, video_hash)
    # Adding Knaps to KnapVideo
    for i in track(range(len(ts_knaps)), description='Creating knapVideo...'):
        for idx, knap in enumerate(ts_knaps[i]):
            knap_video[i + idx] = knap
