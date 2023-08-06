from juungle.auth import Auth


class NFTs(Auth):
    def __init__(self):
        Auth.__init__(self)
        self.list_nfts = list()
        self.search_options = {
            'offset': 0,
            'limit': 10000
        }

    def add_nft(self, nft_info):
        self.list_nfts.append(NFT(nft_info))

    def get_nfts(self):
        response = self.call_get_query('/nfts', self.search_options)
        if response.status_code == 200:
            l_nfts = response.json()
            for nft in l_nfts['nfts']:
                self.add_nft(nft)
        else:
            raise BaseException('Query failed {}'.format(response.content))

    @property
    def token_group(self):
        return self.search_options['groupTokenId']

    @token_group.setter
    def token_group(self, value):
        self.search_options['groupTokenId'] = value

    @property
    def offset(self):
        return self.search_options['offset']

    @offset.setter
    def offset(self, value):
        self.search_options['offsite'] = value

    @property
    def limit(self):
        return self.search_options['limit']

    @limit.setter
    def limit(self, value):
        # limit has to be less than 10 000
        if value < 10000:
            self.search_options['limit'] = value

    @property
    def purchased(self):
        if 'purchaseTxidSet' in self.search_options:
            return self.search_options['purchaseTxidSet']

    @purchased.setter
    def purchased(self, value):
        if isinstance(value, bool):
            self.search_options['purchaseTxidSet'] = str(value).lower()
        else:
            raise ValueError('Purchased must be True or False')

    @property
    def deposited(self):
        if 'depositTxidSet' in self.search_options:
            return self.search_options['depositTxidSet']

    @deposited.setter
    def deposited(self, value):
        if isinstance(value, bool):
            self.search_options['depositTxidSet'] = str(value).lower()
        else:
            raise ValueError('Deposited must be True or False')

    @property
    def available_to_buy(self):
        if 'priceSatoshisSet' in self.search_options:
            return self.search_options['priceSatoshisSet']

    @available_to_buy.setter
    def available_to_buy(self, value):
        if isinstance(value, bool):
            self.search_options['priceSatoshisSet'] = str(value).lower()
        else:
            raise ValueError('Available to buy must be True or False')


class NFT(Auth):
    def __init__(self, nft_info):
        self.nft_id = nft_info["id"]
        self.user_d = nft_info["userId"]
        self.deposit_txid = nft_info["depositTxid"]
        self.withdraw_txid = nft_info["withdrawTxid"]
        self.purchase_txid = nft_info["purchaseTxid"]
        self.token_id = nft_info["tokenId"]
        self.token_name = nft_info["tokenName"]
        self.token_symbol = nft_info["tokenSymbol"]
        self.group_tokenid = nft_info["groupTokenId"]
        self.price_satoshis = nft_info["priceSatoshis"]
        self.price_bch = nft_info["priceSatoshis"] / 100000000
        self.ts = nft_info["ts"]
        self.purchase_hold = nft_info["purchaseHold"]

    @property
    def token_group(self):
        return self.token_symbol

    @property
    def name(self):
        return self.token_name
