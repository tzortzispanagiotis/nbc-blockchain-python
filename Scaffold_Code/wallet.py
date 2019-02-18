import binascii

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

	def __init__(self):
		self._private_key = RSA.generate(1024, Crypto.Random.new().read)
		self._public_key = self._private_key.publickey()
		self._signer = PKCS1_v1_5.new(self._private_key)

	@property
	def address(self):
		return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
		#self_address
		#self.transactions

	def sign_message(self, message):
		hash = SHA.new(message.encode('utf8'))
		signed = self._signer.sign(hash)
		return binascii.hexlify(signed).decode('ascii')


	def balance(self, transactions):
		balance = 0
		for tx in transactions:
			#for transa