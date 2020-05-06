class ConnectivityBlob:

    def __init__(self, d):
        self.type = d["type"]
        self.category = d["category"]
        self.length = d["length"]


class ConnectivityBlobs:

    def __init__(self, serialized_blobs):
        self.blobs = [ConnectivityBlob(d) for d in serialized_blobs]

