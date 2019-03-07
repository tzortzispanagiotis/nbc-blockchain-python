import blockchain

class Block:
	def __init__(self, previousHash, currentbl):
		##set

		self._previousHash = previousHash
		self._timestamp =
		self.listOfTransactions = []
		self.blocknumber=currentbl.getblocknum()+1
		self.nonce = ""

	def getblocknum(self):
		return blocknumber

		
	def add_nonce(self,n):
		self.nonce = n

	def myHash:
		#calculate self.hash
	
	def to_dict(self):
        return OrderedDict({'transactions': self.listOfTransactions,
                            'previousHash': self._previousHash,
                            'nonce': self.nonce})


	#def add_transaction(self , transaction):
		#add a transaction to the block