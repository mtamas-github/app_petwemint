import json
import hashlib
import os
from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import AssetConfigTxn, wait_for_confirmation
from .create_algo_account import create_account
from .closeout_algo_account import closeout_account
from .AlgoConnect import AlgoConnect


class NFT:

    def __init__(self, image_url, json_url):
        self.image_url = image_url
        self.json_url = json_url
        self.accounts = {}
        self.client = AlgoConnect()


    def get_accounts(self):
        m = create_account()
        self.accounts[1] = {}
        self.accounts[1]['pk'] = mnemonic.to_public_key(m)
        self.accounts[1]['sk'] = mnemonic.to_private_key(m)

    def json_hash(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        f = open(self.json_url, "r")

        # Reading from file
        metadataJSON = json.loads(f.read())
        metadataStr = json.dumps(metadataJSON)

        hash = hashlib.new("sha512_256")
        hash.update(b"arc0003/amj")
        hash.update(metadataStr.encode("utf-8"))
        self.json_metadata_hash = hash.digest()

    def generate(self):
        pass

    def build(self):
        self.txn = AssetConfigTxn(sender=self.accounts[1]['pk'],
                             sp=self.client.params,
                             total=1,
                             default_frozen = False,
                             unit_name = "ALICEART",
                             asset_name = "Alice's Artwork@arc3",
                             manager = "",
                             reserve = "",
                             freeze = "",
                             clawback = "",
                             url = "https://path/to/my/nft/asset/metadata.json",
                             metadata_hash = self.json_metadata_hash,
                             decimals = 0)

    def send(self):
        # Sign with secret key of creator
        stxn = self.txn.sign(self.accounts[1]['sk'])

        # Send the transaction to the network and retrieve the txid.
        txid = algod_client.send_transaction(stxn)
        print("Asset Creation Transaction ID: {}".format(txid))

        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))