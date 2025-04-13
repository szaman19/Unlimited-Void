from typing import Optional, Callable, Any
import time
import socket


class ProducerConsumer:
    def __init__(
        self,
        producer: Callable,
        consumer=None,
        cache_size=10,
        fill_ratio=0.5,
        fill_batch_size: int = 10,
    ):
        """
        A relatively simple producer-consumer pattern that uses a list as a cache.
        The producer is a function that produces items. The optional consumer is a
        funtion that updates the item before it is returned.

        Args:
            producer (Callable): Function to produce items.
            consumer (Callable, optional): Function to consume items. Defaults to None.
            cache_size (int, optional): Size of the cache. Defaults to 10.
            fill_ratio (float, optional): Ratio of the cache to be filled. Defaults to 0.5.
            fill_batch_size (int, optional): Number of items to fill the cache with. Defaults to 10.
        """
        self.producer = producer
        self.consumer = consumer
        self.cache_size = cache_size
        self.fill_ratio = fill_ratio

        self.cache = []
        self.fill_batch_size = fill_batch_size

    def pop(self, *args):
        assert self.cache, "Cache is empty. Cannot pop."
        item = self.cache.pop(0)
        if self.consumer:
            item = self.consumer(item)

        # If the cache is less than fill_ratio, refill it
        if len(self.cache) < self.cache_size * self.fill_ratio:
            for _ in range(self.fill_batch_size):
                item = self.producer(*args)
                self.cache.append(item)

                if len(self.cache) >= self.cache_size:
                    break
        return item


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
