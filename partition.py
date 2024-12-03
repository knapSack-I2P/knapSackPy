import datetime
from pathlib import Path

from abstractions.knapclasses import *
from config import FILE_DIRECTORY


def partition(full_video, res='1280x760', *args):
    videoname = Path(full_video).stem
    converted_path = Path(
        FILE_DIRECTORY,
        str(videoname) + datetime.datetime.now().strftime("%Y_%m_%d %H-%M-%S")
    )

    converted_path.mkdir()
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

    for ts in converted_path.iterdir():
        if ts.suffix != '.ts' or not ts.stem:
            continue
        ts_idx = int(ts.stem[-1])
        ts_knaps[ts_idx] = []
        with open(ts, 'rb') as _ts:
            byte = _ts.read(25 * 1024)
            while byte:
                (FILE_DIRECTORY / 'sack').mkdir(exist_ok=True)
                hash = sha256(byte)
                with open(FILE_DIRECTORY / 'sack' / (hash.hexdigest() + '.knap'), 'wb') as knap_file:
                    knap_file.write(byte)
                knap = Knap(FILE_DIRECTORY / 'sack' / (hash.hexdigest() + '.knap'), idx, hash)
                ts_knaps[ts_idx].append(knap)
                idx += 1
                byte = _ts.read(25 * 1024)
                del byte
        ts.unlink()

    m3u8 = converted_path / 'part.m3u8'
    with open(m3u8, 'rb') as _m3u8:
        byte = _m3u8.read()
        null_knap = NullKnap(
            byte,
            [len(ts_knaps[i + 1]) for i in range(len(ts_knaps))],
            sha256(byte)
        )
    m3u8.unlink()
    ts_knaps[0] = [null_knap]

    cnt = 0
    for i in range(len(ts_knaps)), description='Hashing...':
        for knap in ts_knaps[i]:
            video_hash.update(knap.hash16.encode('utf-8'))
            cnt += 1

    knap_video = KnapVideo(cnt, video_hash)
    for i in range(len(ts_knaps)), description='Creating knapVideo...':
        for idx, knap in enumerate(ts_knaps[i]):
            knap_video[i + idx] = knap

