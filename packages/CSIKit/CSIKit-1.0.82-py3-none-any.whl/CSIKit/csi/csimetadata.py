class CSIMetadata:

    __slots__ = ["chipset", "bandwidth", "antenna_config", "frames", "subcarriers", "time_length", "average_sample_rate", "csi_shape"]
    def __init__(self, data: dict):
        self.chipset = data["chipset"]
        self.bandwidth = data["bandwidth"]
        self.antenna_config = data["antenna_config"]
        self.frames = data["frames"]
        self.subcarriers = data["subcarriers"]
        self.time_length = data["time_length"]
        self.average_sample_rate = data["average_sample_rate"]
        self.csi_shape = data["csi_shape"]