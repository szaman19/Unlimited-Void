import numpy as np
import torch
import requests
from Unlimited_Void import UnlimitedVoidDataset
import os


def get_data_from_server(idx, server_file_location, port):
    _data = requests.get("http://127.0.01:" + str(port) + "/data?num_bytes=1024")
    _data = _data.content
    _data = np.frombuffer(_data, dtype=np.uint8)
    _data = np.array(_data)
    _data = torch.from_numpy(_data)
    return _data


class DevRandomDataset(UnlimitedVoidDataset):
    def __init__(self, server_file_location="server_code", **kwargs):
        """
        Args:
            server_file_location (str): Path to the server file location.
        """
        super(DevRandomDataset, self).__init__(
            server_file_location=server_file_location,
            get_data_function=get_data_from_server,
            port=5000,
            max_size=10000000,
            transform=None,
            **kwargs,
        )


if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    server_file_location = os.path.join(cur_dir, "app")

    print("Server file location:", server_file_location)
    dataset = DevRandomDataset(
        server_file_location=server_file_location, server_log_file="server_log.txt"
    )
    print(dataset[0])
    print(dataset[1])
