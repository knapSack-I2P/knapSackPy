from hashlib import sha256
from pathlib import Path
from config import FILE_DIRECTORY


# Knap is atomic video unit that is 25(or sometimes less) Kilobytes length
class Knap:
    def __init__(self, path, idx=1, hash=sha256()):
        self.idx = idx
        self.hash = hash
        self.hash16 = hash.hexdigest()
        self.path = path

    def serialize(self):
        return [self.idx, self.hash]

    def deserialize(self, state):
        self.idx, self.hash = state


# NullKnap is arbitrary Knap that can be either less than 25 Kylobytes or
# more than 25 Kylobytes. It contains video info such as preview or description
# Furthemore, it contains m3u8 file.
class NullKnap(Knap):
    def __init__(self, data, ts_lengths, hash=sha256()):
        super().__init__(data, 0, hash)
        self.lookup: list[int] = ts_lengths if ts_lengths else []
        self.knaps_hashes = []


# KnapVideo is an objects that consists of Knaps and the NullKnap that
# are parts of the video
class KnapVideo:
    def __init__(self, length, hash=sha256()):
        self.hash = hash.hexdigest()
        self.knaps: list[Knap | None] = [None] * length

    def __getitem__(self, index):
        return self.knaps[index]

    def __setitem__(self, index, knap):
        self.knaps[index] = knap

    def serialize(self):
        return [
            knap.serialize()
            if knap else None
            for knap in self.knaps
        ]

    def deserialize(self, state):
        self.knaps = [
            Knap().deserialize(knap)
            if knap else None
            for knap in state.values()
        ]
        return self

    async def assembly_ts(self, knaps, idx):
        ts_path = Path.cwd() / 'tmp' / self.hash / f'part{idx}.ts'
        knaps = await knaps
        async with open(ts_path, 'wb') as ts:
            async for knap in knaps:
                async with open(knap.path, 'rb') as byte:
                    ts.write(byte.read())

    def assembly(self):
        async def collect_knaps(idx, ts_layout):
            cursor = sum(layout[:idx]) + 1
            to_assembly = []
            async for i in range(cursor, cursor + ts_layout):
                knap_path = Path(FILE_DIRECTORY / 'sack' /
                                 (self.knaps[0].knaps_hashes[i] + '.knap'))
                if not self.knaps[i] and knap_path.exists():
                    self.knaps[i] = Knap(
                        knap_path, i, self.knaps[0].knaps_hashes[i])

        layout = self.knaps[0].layout
        for idx, ts_layout in enumerate(layout):
            self.assembly_ts(collect_knaps(idx, ts_layout), idx)


# KnapChannel is an object that represents the author of KnapVideos
class KnapChannel:
    def __init__(self):
        self.hash = id(self)
        self.videos: list[KnapVideo] = []

    def serialize(self):
        return {
            str(video.hash): video.serialize()
            for video in self.videos
        }

    def deserialize(self, state):
        self.videos = [
            KnapVideo().deserialize(video)
            for video in state.values()
        ]
        return self


# KnapSack is a list of KnapChannels
# which Video's knaps are stored on user's device
class KnapSack:
    def __init__(self):
        self.channels: list[KnapChannel] = []
        self.b32 = ''

    def serialize(self):
        return {
            str(channel.hash): channel.serialize()
            for channel in self.channels
        }

    def deserialize(self, state):
        self.channels = [
            KnapChannel().deserialize(channel)
            for channel in state.values()
        ]
        return self
