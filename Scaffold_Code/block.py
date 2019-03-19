from collections import OrderedDict
import hashlib
import json
import datetime

class GenesisBlock:
	def __init__(self, genesis_tr):
		print("a")
		self._previousHash = 0
		self._timestamp = datetime.datetime.now()
		self.listOfTransactions = genesis_tr
		self.blocknumber = 0
		self.nonce = "0"

	def to_dict(self, include_nonce = True):
		if include_nonce == False:
			d = OrderedDict({
				'transactions': self.listOfTransactions,
				'previousHash': self._previousHash,
				'number': self.blocknumber
			})
		else:
			d = OrderedDict({
				'transactions': self.listOfTransactions,
				'previousHash': self._previousHash,
				'nonce': self.nonce,
				'number': self.blocknumber
			})
		return d
		
class Block:
	def __init__(self, previousHash, listoftransactions, last_block):
		##set
		self._previousHash = previousHash
		self._timestamp = datetime.datetime.now()
		self.listOfTransactions = listoftransactions
		self.blocknumber = last_block+1
		self.nonce = None
		#self.currenthash = None

	def getblocknum(self):
		return self.blocknumber

	def to_dict(self, include_nonce = True):
		if include_nonce == False:
			d = OrderedDict({
				'transactions': self.listOfTransactions,
				'previousHash': self._previousHash,
				'number': self.blocknumber
			})
		else:
			d = OrderedDict({
				'transactions': self.listOfTransactions,
				'previousHash': self._previousHash,
				'nonce': self.nonce,
				'number': self.blocknumber
			})
		return d

	def add_nonce(self, n):
		self.nonce = n

	def add_hash(self, n):
		self.currenthash = n

	# def myHash(self):
	# 		h = hashlib.sha256(json.dumps(self.to_dict()))
	# 		self.currenthash = h
	# 		return h

		#calculate self.hash
	def getHash(self):
		return self.currenthash


	

