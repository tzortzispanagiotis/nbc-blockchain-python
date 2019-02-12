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
		##set
		self._private_key = RSA.generate(1024, Crypto.Random.new().read)
		self._public_key = self._private_key.publickey()
		#self.private_key

	@property
	def address(self):
		return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
		#self_address
		#self.transactions

	def balance():
