from typing import Optional, Callable, Any
import time
import socket
import multiprocessing as mp
import time


class ProducerConsumer:
    def __init__(
        self,
        producer: Callable,
        consumer=None,
        cache_size=10,
    ):
        """
        A relatively simple producer-consumer pattern that uses a list as a cache.
        The producer is a function that produces items. The optional consumer is a
        funtion that updates the item before it is returned.

        Args:
            producer (Callable): Function to produce items.
            consumer (Callable, optional): Function to consume items. Defaults to None.
            cache_size (int, optional): Size of the cache. Defaults to 10.
        """
        self.producer = producer
        self.consumer = consumer
        self.cache_size = cache_size

        self.cache = mp.Queue(maxsize=cache_size)
        self._start_producer()

    def _produce(self):
        while True:
            if not self.cache.full():
                item = self.producer()
                self.cache.put(item)
            else:
                time.sleep(0.1)

    def _start_producer(self):
        self.process = mp.Process(target=self._produce)
        self.process.daemon = True
        self.process.start()

    def update_producer(self, producer: Callable):
        if self.process.is_alive():
            self.process.terminate()
            self.process.join()
        self.producer = producer
        self._start_producer()

    def pop(self, num_retries=10, timeout=None, *args):

        for i in range(num_retries):
            try:
                item = self.cache.get(timeout=timeout)
                if self.consumer:
                    item = self.consumer(item, *args)
                return item
            except Exception as e:
                time.sleep(0.1)
                if i == num_retries - 1:
                    return None

        return item

    def __del__(self):
        if self.process.is_alive():
            self.process.terminate()
            self.process.join()


def wait_for_port(port, host="127.0.0.1", timeout=10.0):
    """Wait until a TCP port is open (up to a timeout)."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.2)
    return False


def wait_for_uds(uds_socket: str, timeout: float = 10.0) -> bool:
    """Wait until a UDS socket is open (up to a timeout)."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.connect(uds_socket)
                return True
        except OSError:
            time.sleep(0.2)
    return False
