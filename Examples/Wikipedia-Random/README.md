# Random WikiPedia Article

This example shows how to use the `Unlimited_Void` library to serve random Wikipedia articles to a PyTorch model. The server will serve a requested random Wikipedia article

If you with `NUM_BYTES` set to 128, you can get a random Wikipedia article in the following format:

```
tensor([ 84,  97, 121, 111,  44,  32,  97, 108, 115, 111,  32, 107, 110, 111,
        119, 110,  32,  97, 115,  32,  34, 112,  97, 116, 111, 105, 115,  32,
        100, 101,  32,  83,  97, 105, 110, 116,  45,  76, 111, 117, 105, 115,
         34,  44,  32, 105, 115,  32,  97,  32,  70, 114, 101, 110,  99, 104,
         45,  98,  97, 115, 101, 100,  32,  67, 114, 101, 111, 108, 101,  32,
        115, 112, 111, 107, 101, 110,  32, 105, 110,  32,  78, 101, 119,  32,
         67,  97, 108, 101, 100, 111, 110, 105,  97,  46,  32,  73, 116,  32,
        105, 115,  32, 115, 112, 111, 107, 101, 110,  32,  98, 121,  32,  97,
         98, 111, 117, 116,  32,  51,  48,  48,  48,  32, 112, 101, 111, 112,
        108, 101], dtype=torch.uint8)
Tayo, also known as "patois de Saint-Louis", is a French-based Creole spoken in New Caledonia. It is spoken by about 3000 people
```

Of course the way you decode the text is entirely up to you and you can add any logic you'd like in `get_data_function`. You may want to run this retrieved text through a tokenizer or some other pre-processing step.

The way the data is obtain and returned is also entirely up to you and done in `app.py`.


**Run the example with the following command:**
```bash
python dataset.py
```