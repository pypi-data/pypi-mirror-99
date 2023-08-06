## juungle-python
Python package to access Juungle.net API

## Requirements

`$ python -m pip -r requirements.txt`

## User credentials
Create a file `user-config.ini`:
```
LOGIN_USERNAME="username"
LOGIN_PASSWORD="password"
```

## Usage
List nfts 
```python
from juungle.nfts import NFTs

nfts = NFTs()

nfts.available_to_buy = True
nfts.purchased = False
nfts.token_symbol = 'WAIFU'

nfts.get_nfts()

for nft in nfts.list_nfts:
    if nft.price_bch < 0.60 and nft.price_bch > 0.40:
        print(nft.token_name)
```
