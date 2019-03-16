import collections

from Scaffold_Code import chain

import hashlib
import json
import datetime
# import coll

class Block:
	def __init__(self, previousHash, currentbl):
		##set

		self._previousHash = previousHash
		self._timestamp =datetime.datetime.now()
		self.listOfTransactions = []
		self.blocknumber=currentbl.getblocknum()+1
		self.nonce = ""
		self.currenthash = None

	def getblocknum(self):
		return self.blocknumber

	def to_dict(self):				
		return {
			'transactions': self.listOfTransactions,
			'previousHash': self._previousHash,
			#'nonce': self.nonce , 
			'number':self.blocknumber
		}

	def add_nonce(self,n):
		self.nonce = n

	def myHash(self):
			h=hashlib.sha256(json.dumps(self.to_dict()))
			self.currenthash = h
			return h

		#calculate self.hash
	def getHash(self):
		return self.currenthash



	#def add_transaction(self , transaction):
		#add a transaction to the block