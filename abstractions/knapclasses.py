class Knap:
    def __init__(self):
        self.idx = 0
        self.hash = id(self)
        self.data = b''

    def serialize(self):
        return [self.idx, self.hash]

    def deserialize(self, state):
        self.idx, self.hash = state


class NullKnap(Knap):
    def __init__(self, ts_lengths):
        super().__init__()
        self.lookup: list[int] = ts_lengths if ts_lengths else []


class KnapVideo:
    def __init__(self, length):
        self.hash = id(self)
        self.knaps: list[Knap | None] = [None] * length

    def __get__(self, index):
        return self.knaps[index]

    def __set__(self, index, knap):
        self.knaps[index] = knap

    def serialize(self):
        return {
            str(knap.hash): knap.serialize()
            for knap in self.knaps
        }

    def deserialize(self, state):
        self.knaps = [
            Knap().deserialize(knap)
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
