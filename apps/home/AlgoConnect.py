
from algosdk.v2client import algod

DEFAULT_ADDRESS = "https://academy-algod.dev.aws.algodev.network/"
DEFAULT_TOKEN = "2f3203f21e738a1de6110eba6984f9d03e5a95d7a577b34616854064cf2c0e7b"

class AlgoConnect:

    def __init__(self):
        self.client = algod.AlgodClient(DEFAULT_TOKEN, DEFAULT_ADDRESS)
        # Change algod_token and algod_address to connect to a different client
        # algod_token = "2f3203f21e738a1de6110eba6984f9d03e5a95d7a577b34616854064cf2c0e7b"
        # algod_address = "https://academy-algod.dev.aws.algodev.network/"
        # algod_client = algod.AlgodClient(algod_token, algod_address)

        # CREATE ASSET
        # Get network params for transactions before every transaction.
        self.params = self.client.suggested_params()
        # comment these two lines if you want to use suggested params
        # params.fee = 1000
        # params.flat_fee = True