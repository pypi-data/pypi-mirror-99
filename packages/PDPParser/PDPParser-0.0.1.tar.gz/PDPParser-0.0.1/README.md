# PDP Parser

Developed by Mrbeastmode of BlazeAIO

## Why?
Well, most PDP parsing functions take about 50-100 lines of chunky, gross code.
Why bother looking through terrible naming conventions, stressing over properly parsing,
insuring that you found the right sizes, when you could leave that to me to solve? : D

In any case, enjoy!

## How to use
PASS IN YOUR TEXT IN JSON FORMAT TO EITHER OF THESE 3 METHODS:

  1. Sizes: Use this to return a list/array of product sizes and pids

  2. Info: Use this to return a list/array of product info
    This will return:
        - Title
        - Image
        - Price

  3. Launch: Check if the product has launched, or is yet to launch


```python
import requests
from PDPParser.pdpparser import Parse

r = requests.get(f'https://footlocker.com/api/pdp/products/{sku}')

sizes = Parse.sizes(r.text)

info = Parse.info(r.text)

launch_time = Parse.launch(r.text)
```



## TODO: Add more information returned under INFO