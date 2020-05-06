class BlobToSide:

    def __init__(self, d):
        self.type = d["type"]
        self.category = d["category"]
        self.side = d["side"]


class BlobsToSide:

    def __init__(self, serialized_blobs_to_side):
        self.blobs_to_side = [BlobToSide(d) for d in serialized_blobs_to_side]
