from Unlimited_Void import UnlimitedVoidDataset
import numpy as np
import torch
import requests
import json
import os
import subprocess

NUM_BYTES = 128


def get_data_function(idx, server_file_location, port):
    _data = requests.get(
        "http://127.0.0.1:" + str(port) + f"/get_data?num_characters={NUM_BYTES}"
    )
    _data = _data.json()
    _data = _data["data"]
    string_to_int = np.frombuffer(_data.encode("utf-8"), dtype=np.uint8)
    _data = np.array(string_to_int)
    _data = torch.from_numpy(_data)
    return _data


class UnlimitedWikiData(UnlimitedVoidDataset):
    def __init__(
        self,
        server_file_location="server_code",
    ):
        """
        Args:
            server_file_location (str): Path to the server file location.
        """
        super(UnlimitedWikiData, self).__init__(
            server_file_location=server_file_location,
            get_data_function=get_data_function,
            port=5000,
            max_size=10000000,
            transform=None,
        )


if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    server_file_location = os.path.join(cur_dir, "app")
    print("Server file location:", server_file_location)
    dataset = UnlimitedWikiData(
        server_file_location=server_file_location,
    )
    for i in range(2):
        _data = dataset[i]
        torch_to_bytes = _data.numpy().tobytes()
        bytes_to_string = torch_to_bytes.decode("utf-8")
        print(_data)
        print(bytes_to_string)
