from hashlib import sha256


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


class NullKnap(Knap):
    def __init__(self, data, ts_lengths, hash=sha256()):
        super().__init__(data, 0, hash)
        self.lookup: list[int] = ts_lengths if ts_lengths else []


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


class KnapSack:
    def __init__(self):
        self.channels: list[KnapChannel] = []

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
