import datetime
from pathlib import Path

from abstractions.knapclasses import *
from config import FILE_DIRECTORY


def assembly_ts(knaps, path, idx):
    ts_path = path / (path.name + f'{idx}.ts')
    with open(ts_path, 'wb') as ts:
        for knap in knaps:
            with open(knap.path, 'rb') as byte:
                ts.write(byte.read())


def assembly_video():
    ...
