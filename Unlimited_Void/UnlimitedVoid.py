from torch.utils.data import Dataset
import os
import os.path as osp
import subprocess
from typing import Callable, Optional, Any
from Unlimited_Void.helpers import wait_for_port
import sys


class UnlimitedVoidDataset(Dataset):
    def __init__(
        self,
        server_file_location: str,
        get_data_function: Callable[[int, str, int], Any],
        port: int = 5000,
        max_size: int = 10000000,
        transform: Optional[Callable] = None,
        timeout: float = 10.0,
        server_log_file: Optional[str] = None,
    ):
        """
        Args:
            server_file_location (str): Path to the server file location.
            get_data_function (Callable): Function to get data from the server.
            Currently must have the signature (idx, server_file_location, port).
            port (int): Port to run the server on. Defaults to 5000.
            max_size (int): Maximum size of the dataset. Defaults to 10000000.
            transform (Callable, optional): Optional transform to be applied on a sample.
                Defaults to None.
            timeout (float, optional): Timeout for the server to start. Defaults to 10.0.
        """
        super(UnlimitedVoidDataset, self).__init__()
        self.server_file_location = server_file_location

        assert osp.exists(
            self.server_file_location + ".py"
        ), f"Server file location {self.server_file_location} does not exist."
        assert osp.isfile(
            self.server_file_location + ".py"
        ), f"Server file location {self.server_file_location} is not a file."
        assert os.access(
            self.server_file_location + ".py", os.R_OK
        ), f"Server file location {self.server_file_location} is not readable."

        # TODO: Check if the server is already running. Coult be done with
        # a simple ping to the server. Since the situation will probably only
        # happen if we have multiple dataset processes running (like in DDP),
        # we can just make the rank 0 run the process and the others wait
        # for it to finish. This could be done by spinning until we get a
        # response from the server.

        assert port > 0 and port < 65536, f"Port {port} is not valid."
        self.port = port
        # TODO: allow other server types
        env = os.environ.copy()
        env["FLASK_ENV"] = "development"

        file_dir = osp.dirname(server_file_location)

        if server_log_file is not None:
            log_f = open(server_log_file, "a")
            self.log_file = log_f
        else:
            log_f = sys.stdout
            self.log_file = None
        p = subprocess.Popen(
            ["flask", "run", "--port", str(self.port)],
            cwd=file_dir,
            stdout=log_f,
            stderr=log_f,
            preexec_fn=os.setsid,
            env=env,
        )

        # Wait for the server to start
        if not wait_for_port(self.port, timeout=timeout):
            # Check if the server is running
            if p.returncode != 0:
                raise RuntimeError("Server failed to start.")
        self.server_process = p
        self.max_size = max_size
        self.transform = transform
        self.get_data_function = get_data_function

    def __len__(self):
        """
        Returns:
            int: The length of the dataset, which is arbitrarily set by the constructor.
            Useful for defining an "epoch" in the dataloader.
        """
        return self.max_size

    def __getitem__(self, idx):
        item = self.get_data_function(idx, self.server_file_location, self.port)
        if self.transform:
            item = self.transform(item)
        return item

    def __del__(self):
        """
        Clean up the server process when the dataset is deleted.
        """
        # Check if object has a server_process attribute
        if not hasattr(self, "server_process"):
            # This is triggered when the constructor failed and the
            # server_process was never created. Cleans up the error
            # message.
            return

        if hasattr(self, "log_file") and self.log_file:
            self.log_file.flush()
            self.log_file.close()

        if self.server_process:
            os.killpg(os.getpgid(self.server_process.pid), 9)
            self.server_process = None
