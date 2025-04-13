# Unlimited Void

In a hamfisted analogy to [Unlimited Void](https://jujutsu-kaisen.fandom.com/wiki/Unlimited_Void), a small library to provide deep learning models with a large amount (some might even say [limitless](https://jujutsu-kaisen.fandom.com/wiki/Limitless)) of information through a simple server interface. 


## What is it?
PyTorch models load the data through a combination of `torch.utils.data.Dataset` and `torch.utils.data.DataLoader`. This is a great way to load data, but it has some limitations. For example, if you want to load a large amount of data, you need to have enough memory to store it. You could potentially get around with it by doing some sharding, using memory mapping, or some other techniques, but it is not trivial. It also requires you to have the data somewhere on disk, which is not always the case. Also, this requires your preprocessing to be done in advance or in the same code, which increases the complexity of your code.

This library provides a simple way to start a server that can serve data to your model.
We wrap the `torch.utils.data.Dataset` with a simple server that can serve the data to your model. The server is concerned with obtaining the data (from disk, from a database, from the internet, etc.) sufficiently pre-process it, and serve it to the model process. 

## Is this the best way to do it?

No, but I wanted to do this. This adds all sorts of latency, going through http and tcp and what not. Most of which can be overcome with some caching and other techniques. In general, this is not the best way to do it. But it is a fun way to do it.

## How do I use it?

Checkout the examples in the `examples` folder. 

## How do I install it?

You can install it with pip:

```bash
pip install git+https://github.com/szaman19/Unlimited-Void
```