import binascii
from Scaffold_Code import config , transaction

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4


class Wallet:

	def __init__(self, id):
		self._private_key = RSA.generate(1024, Crypto.Random.new().read)
		self._public_key = self._private_key.publickey()
		self._signer = PKCS1_v1_5.new(self._private_key)
		self.id = id

	@property
	def address(self):
		return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
		# self_address
		# self.transactions

	def balance(self, utxo_list):
		balance = 0
		for tx in utxo_list:
			if tx.get_receiver() == self._public_key:
				balance = balance+tx.amount
		return balance
		# for trans

	# na to dw
	def sign_transaction(self, message, sender_private_key):
		h = SHA.new(str(message).encode('utf8'))
		return binascii.hexlify(self._signer.sign(h)).decode('ascii')


def verify_signature(wallet_address, message, signature):
	pubkey = RSA.importKey(binascii.unhexlify(wallet_address))
	verifier = PKCS1_v1_5.new(pubkey)
	h = SHA.new(message.encode('utf8'))
	return verifier.verify(h, binascii.unhexlify(signature))
