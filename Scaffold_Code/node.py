import requests, json
from collections import OrderedDict
import hashlib
from multiprocessing.dummy import Pool

import block
import wallet
import config
import transaction

pool = Pool(100)

class Node: #creation of bootstap node
	def __init__(self, ip, port, bootstrapip, bootstrapport):
		#self.NBC=100
		##set
		self.ip = ip
		self.port = port
		self.bootstrapip = bootstrapip
		self.bootstrapport = bootstrapport
		self.current_block  = [] #san transaction pool me transactions<=maximum
		self.chain = []
		#self.current_id_count
		self.wallet = self.create_wallet()
		self.verified_transactions = []
		#utxo==transaction_output
		self.UTXO = []
		self.ring = [{
			'pkey' : self.wallet.address,
			'ip'   : ip,
			'port' : port
		}] 
		self.isMining = False 
		self.blockWhileMining = []
		 #here we store information for every node, as its id, its address (ip:port) its public key and its balance 
	#def create_new_block(previousHash): #an einai to proto 
		
	def create_wallet(self):
		##create a wallet for this node, with a public key and a private key
		return wallet.Wallet()

	def register_node_to_ring(self, newNode): #only bootstrap can do that
		# print("Entered reg_ring")
		temp = {
				'pkey' : newNode['pkey'],
				'ip'		: newNode['ip'],
				'port'   : newNode['port']
			}
		self.ring.append(temp)
		# print(self.ring)
		if len(self.ring) == config.numofnodes:
			body = json.dumps(self.ring)
			for i in self.ring:
				r = requests.post('http://'+i['ip']+':'+i['port']+'/receivewallets', data = body )
			self.create_genesis_transactions()

	def create_genesis_block(self, genesis_transactions):
		genblock = block.GenesisBlock(genesis_transactions)
		trans_dict = []
		for i in genblock.listOfTransactions:
			trans_dict.append(i.to_dict())
		genblock.listOfTransactions = trans_dict
		genblock_final = genblock.to_dict()
		# print(genblock_final)
		body = json.dumps(genblock_final)
		for i in self.ring:
			r = requests.post('http://'+i['ip']+':'+i['port']+'/receivegenesis', data = body )

	def create_genesis_transactions(self):
		genesis_transactions = []
		for i in self.ring:
			new_trans = transaction.GenesisTransaction(i['pkey'], 100)
			genesis_transactions.append(new_trans)
		self.create_genesis_block(genesis_transactions)

	def create_transaction(self, receiver, amount):
		traninput = []
		#inputs ola ta outputs pou exoun os receiver ton torino sender
		bal = 0
		for i in self.UTXO:
			if i.recipient == self.wallet.address:
				traninput.append(i)
				bal = bal + i.amount
				# self.UTXO.remove(i)
		new_transaction = transaction.Transaction(self.wallet, receiver, amount, traninput)
		new_transaction.add_id_to_output()
		# self.UTXO.append(new_transaction.transaction_outputs[0])	
		# self.UTXO.append(new_transaction.transaction_outputs[1])
		# self.verified_transactions.append(new_transaction)
		# self.add_transaction_to_block(new_transaction)
		new= new_transaction.to_dict1(include_hash=True) 
		return new  

	def broadcast_transaction(self, dict):
		body = json.dumps(dict)
		futures = []
		for i in self.ring:
			target_url = 'http://'+i['ip']+':'+i['port']+'/receivetransaction'
			futures.append(pool.apply_async(requests.post, [target_url,body]))

	def getGenesisBlock(self,gblock):
		#put genesis block in chain
		self.chain.append(gblock)
		#crete utxos and append them to the list 
		for i in gblock['transactions']:
			out = transaction.TransactionOutput(i['receiver_address'] , i['amount'])
			self.UTXO.append(out)

	def validate_transaction(self, _transaction):
		tr = {"sender": _transaction['sender'],
			 "receiver": _transaction['receiver'],
             "amount": _transaction['amount'],
             "inputs": _transaction['inputs'],
             "outputs": _transaction['outputs']
		}
		#sos ti object einai to transaction tha einai logika se morfi dict?
		if (wallet.verify_signature(tr["sender"] , tr , _transaction['signature'])):
			print("Je suis verifie")
			traninput=[]
			sum1=0
			for i in self.UTXO:
				i_to_dict = i.to_dict()
				if (i_to_dict['recipient'] == _transaction['sender']):
					traninput.append(i)
					sum1=sum1+i.amount
			if (sum1>=_transaction['amount']):
			#eparki xrimata gia tin metafora
				for t in traninput:
					self.UTXO.remove(t)
				#now create transaction outputs and add them at the utxo list
				out1=transaction.TransactionOutput(_transaction['receiver'] , _transaction['amount'])
				out2=transaction.TransactionOutput(_transaction['sender'] ,sum1-_transaction['amount'])
				self.UTXO.append(out1)
				self.UTXO.append(out2)
				self.verified_transactions.append(_transaction)
				# print(self.verified_transactions)
			return True
		else:
			return False
		
	def add_transaction_to_block(self, _transaction ):
		if self.validate_transaction(_transaction):
			self.current_block.append(_transaction)
			# print (len(self.current_block))
			if len(self.current_block) == config.max_transactions:
				print ("mpika man")
				previousblock = self.chain[-1]
				previousmessage = OrderedDict(
						{'transactions': previousblock['transactions'],
						 'previousHash':  previousblock['previousHash'],
						 #'nonce': self.nonce ,
						 'number': previousblock['number']
						})
				previoushash = hashlib.sha256((str(previousmessage)+previousblock['nonce']).encode()).hexdigest()
				new_block = block.Block(previoushash, self.current_block, previousblock['number'])
				# self.current_block = []
				# new_block.myHash()
				self.mine_block(new_block)
				return

	def mine_block( self, _block):
		print("I am mining")
		self.isMining = True
		# last_block = self.chain[-1]
		message = _block.to_dict(include_nonce=False)
		nonce = self.search_proof(message)
		_block.add_nonce(nonce)
		# +++++++ 
		if not self.blockWhileMining:
			self.chain.append(_block.to_dict())
			self.broadcast_block(_block.to_dict())
			self.isMining = False
			self.current_block = []
		else:
			#kati tha paiksei me ta verified transactions
			self.validate_block(_block)
		return

	def broadcast_block(self,dict):
		# print('i am broadcasting!!!!!!!')
		body = json.dumps(dict)
		futures = []
		for i in self.ring:
			if i['ip'] != self.ip and i['port'] != self.port:
				target_url = 'http://'+i['ip']+':'+i['port']+'/receiveblock'
				futures.append(pool.apply_async(requests.post, [target_url,body]))
		return

	def receive_block(self, _block):
		# print('i am broadcasting!!!!!!!')
		if self.isMining == True:
			self.blockWhileMining.append(_block)
		else:
			self.validate_block(_block)
		return

	def search_proof(self, message):
		i = 0
		prefix = '0' * config.difficulty
		while True:
			nonce = str(i)
			digest = hashlib.sha256((str(message) + nonce).encode()).hexdigest()
			if digest.startswith(prefix):
				print(digest)
				return nonce
			i += 1


	def valid_proof(self , _block):
		d = OrderedDict({'transactions': _block['transactions'],
						 'previousHash':  _block['previousHash'],
						 #'nonce': self.nonce ,
						 'number': _block['blocknumber']
						})
						#i mipos d = block.to_dict??
		nonce = _block['nonce']
		digest = hashlib.sha256(str(d) + nonce).hexdigest()
		if ( digest.startswith('0' * config.difficulty)):
			return True
		else:
			return False
		
	#concencus functions

	def validate_block(self,block):
		#check proof of work 
		flag1 = self.valid_proof(block)
		if (flag1):
		#check previous hash
			previousblock=self.chain[-1]
			previousmessage = OrderedDict(
						{'transactions': previousblock['transactions'],
						 'previousHash':  previousblock['previousHash'],
						 #'nonce': self.nonce ,
						 'number': previousblock['blocknumber']
						})
			previoushash = hashlib.sha256((previousmessage+previousblock['nonce']).hexdigest())
			if (block['previous_hash'] != previoushash):
				flag = self.resolve_conflicts()
				if (flag==False): 
					return False
				return True
			else: 
				transactions=block['transactions']
				#check  all that transactions in received block are verified
				for t in transactions:
					flag=0
					for vt in self.verified_transactions:
						if t['id']==vt['id'] :
							flag=1
					if flag==0:
						return False
					flag=0
				#if all transactions in block are verified remove them from verified_trans
				for t in transactions:
					for vt in self.verified_transactions:
						if t['id']==vt['id'] :
							self.verified_transactions.remove(vt)
			
					for mytrans in self.current_block:
						if (t.transaction_id == mytrans.transaction_id):
							self.current_block.remove(mytrans) 
				self.chain.append(block)
				return True
		return False
			

		 

	def valid_chain(self, chain):
		# check for the longer chain accroose all nodes

		# mallon de mas xreiazetai
		last_block = chain[0]
		current_index = 1

		while current_index < len(chain):
			block = chain[current_index]
			if block['previous_hash'] != hashlib.sha256(last_block.to_dict(include_nonce= False)+last_block['nonce']).hexdigest():
				return False

			# Check that the Proof of Work is correct
			#Delete the reward transaction
			
			# Need to make sure that the dictionary is ordered. Otherwise we'll get a different hash
			
			if not self.valid_proof(block):
				return False

			last_block = block
			current_index += 1

		return True



	def resolve_conflicts(self):
		return True
	# resolve correct chain
	#changed = False

	#if received_block['previousHash'] == current_block['previousHash']:
		#self.block_pool.append(received_block)
	#else:
		#for b in self.block_pool:
		#	if b['previousHash'] == current_block['previousHash'] and received_block[
			#	'previousHash'] == block.getHash(b):
			#	self.chain[-1] = b
			#	self.chain.append(received_block)
			#	changed = True

	#return changed



