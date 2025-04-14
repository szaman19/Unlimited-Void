# Serving /dev/random over UDS

This example shows how to use the `Unlimited_Void` library to serve random bytes to obtain a set of random bytes using http over a UNIX domain socket. This example doesn't require any internet access, as it uses the `/dev/random`, so it is the fastest way to get things up and running.

The example also shows the server returning binary data rather than text data, which can be useful for non-text modalities. 

The server will serve a requested random byte string in the following format:

```
tensor([ 84,  97, 121, 111,  44,  32,  97, 108, 115, 111,  32, 107, 110, 111,
        119, 110,  32,  97, 115,  32,  34, 112,  97, 116, 111, 105, 115,  32,
        100, 101, 32,   ...], dtype=torch.uint8)
```


**Run the example with the following command:**
```bash
python main.py
```

The regular `requests` library can't be used and you must instead use a library that can do http over a UNIX domain socket. The `requests_unixsocket2` is used here, and can be installed via:
```bash
pip install requests-unixsocket2
```