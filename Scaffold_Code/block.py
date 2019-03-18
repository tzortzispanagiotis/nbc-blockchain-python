from import collections

import blockchain
import hashlib
import json
import datetime
import coll
class Block:
	def __init__(self, previousHash, currentbl):
		##set

		self._previousHash = previousHash
		self._timestamp =datetime.datetime.now()
		self.listOfTransactions = []
		self.blocknumber=currentbl.getblocknum()+1
		self.nonce = ""
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

	def add_nonce(self,n):
		self.nonce = n

	def myHash(self):
        
		return hashlib.sha256(json.dumps(self.to_dict(include_nonce=false)))
		#allios tha exw an thelw na ta kanw prin json.dumps
		# block_string = json.dumps(block, sort_keys=True).encode()
        
        # return hashlib.sha256(block_string).hexdigest()


	

