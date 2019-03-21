import requests, json
from collections import OrderedDict
import hashlib
from multiprocessing.dummy import Pool

import block
import wallet
import config
import transaction
import time
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
			'port' : port,
			'id'   : int(port) % 10 #works for up to 10 nodesS
		}] 
		self.bcounter = 0
		self.isMining = False 
		self.usingChain = False
		self.resolvingConflicts = False
		self.blockWhileMining = []
		self.mining_useless = False
		self.start_time = None
		self.end_time = None
		self.total_time = None
		self.tcounter = 0
		self.stop_if_empty = False
		 #here we store information for every node, as its id, its address (ip:port) its public key and its balance 
	#def create_new_block(previousHash): #an einai to proto 

	def continuous_mining(self):
		print("STARTED CONTINUOUS WORK")
		while True:	 
			if len(self.verified_transactions) >= config.max_transactions and not self.current_block:
				self.mine_job()
			if len(self.verified_transactions) < config.max_transactions and self.stop_if_empty:
				self.end_time = time.time()
				self.total_time = self.end_time - self.start_time
				self.stop_if_empty = False

	def create_wallet(self):
		##create a wallet for this node, with a public key and a private key
		return wallet.Wallet()

	def register_node_to_ring(self, newNode): #only bootstrap can do that
		# print("Entered reg_ring")
		temp = {
				'pkey' : newNode['pkey'],
				'ip'		: newNode['ip'],
				'port'   : newNode['port'],
				'id'   : int(newNode['port']) % 10
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
		for future in futures:
			print(future.get())	

	def getGenesisBlock(self,gblock):
		#put genesis block in chain
		self.chain.append(gblock)
		#crete utxos and append them to the list 
		for i in gblock['transactions']:
			out = transaction.TransactionOutput(i['receiver_address'] , i['amount'])
			self.UTXO.append(out)

	def validate_transaction(self, _transaction, resolve_confl = False):
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
				if not resolve_confl:
					self.verified_transactions.append(_transaction)
				# print(self.verified_transactions)
			return True
		else:
			return False

	# def force_mine(self):
	# 	while self.isMining:
	# 		pass
	# 	if len(verified_transactions) >= config.max_transactions):
	# 		for i in range(config.max_transactions):
	# 			self.current_block.append(self.verified_transactions[i])
	# 	else:
	# 		return 42
	# 	print ("mpika man")	
	# 	previousblock = self.chain[-1]
	# 	previousmessage = OrderedDict(
	# 			{'transactions': previousblock['transactions'],
	# 				'previousHash':  previousblock['previousHash'],
	# 				#'nonce': self.nonce ,
	# 				'number': previousblock['number'],
	# 				'timestamp': previousblock['timestamp']
	# 			})
	# 	previoushash = hashlib.sha256((str(previousmessage)+previousblock['nonce']).encode()).hexdigest()
	# 	new_block = block.Block(previoushash, self.current_block, previousblock['number'])
	# 	# self.current_block = []
	# 	# new_block.myHash()
	# 	self.mine_block(new_block)
	# 	return 0

	def mine_job(self):
		for i in range(config.max_transactions):
			self.current_block.append(self.verified_transactions[i])

		print ("mpika man")	
		previousblock = self.chain[-1]
		previousmessage = OrderedDict(
				{'transactions': previousblock['transactions'],
					'previousHash':  previousblock['previousHash'],
					#'nonce': self.nonce ,
					'number': previousblock['number'],
					'timestamp': previousblock['timestamp']
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
		#### EDW THA PREPEI NA APOTHIKEUW TO PREVIOUSHASH gia to block pou tha kanw mine, wste na to
		#### tsekarw otan teleiwsw to mining
		last_block = self.chain[-1]
		previousmessage = OrderedDict(
						{'transactions': last_block['transactions'],
						 'previousHash': last_block['previousHash'],
						 'timestamp': last_block['timestamp'],

						 #'nonce': self.nonce ,
						 'number': last_block['number']
						})
		my_previous_hash = hashlib.sha256((str(previousmessage)+last_block['nonce']).encode()).hexdigest()
		message = _block.to_dict(include_nonce=False)
		nonce = self.search_proof(message)
		_block.add_nonce(nonce)
		if nonce == "nope":
			self.isMining = False
			return

		# +++++++
		while self.usingChain:
			pass
		self.usingChain = True
		last_block = self.chain[-1]
		self.usingChain = False
		previousmessage = OrderedDict(
						{'transactions': last_block['transactions'],
						 'previousHash': last_block['previousHash'],
						 'timestamp': last_block['timestamp'],
						 #'nonce': self.nonce ,
						 'number': last_block['number']
						})
		new_previous_hash = hashlib.sha256((str(previousmessage)+last_block['nonce']).encode()).hexdigest()
		if new_previous_hash == my_previous_hash:
			# self.chain.append(_block.to_dict())
			self.broadcast_block(_block.to_dict())
			self.current_block = []
		self.isMining = False
		return

	def broadcast_block(self,dict):
		print('i am broadcasting!!!!!!!')
		body = json.dumps(dict)
		futures = []
		for i in self.ring:
			target_url = 'http://'+i['ip']+':'+i['port']+'/receiveblock'
			futures.append(pool.apply_async(requests.post, [target_url,body]))
		for future in futures:
			print(future.get())			
		return

	def receive_block(self, _block):
		# print('i am broadcasting!!!!!!!')
		while self.usingChain:
			pass
		self.usingChain = True
		self.validate_block(_block)
		self.usingChain = False
		return

	def search_proof(self, message):
		i = 0
		prefix = '0' * config.difficulty
		self.mining_useless = False
		while not self.mining_useless:
			nonce = str(i)
			digest = hashlib.sha256((str(message) + nonce).encode()).hexdigest()
			if digest.startswith(prefix):
				print(digest)
				return nonce
			i += 1
		if self.mining_useless == True:
			print("Mining process interrupted, block was mined somewhere else :(\n")
			return "nope"
		


	def valid_proof(self , _block):
		d = OrderedDict({'transactions': _block['transactions'],
						 'previousHash':  _block['previousHash'],
						 #'nonce': self.nonce ,
						 'number': _block['number'],
						 'timestamp': _block['timestamp']
						})
						#i mipos d = block.to_dict??
		print("I received block, i check the proof. block is:")
		# print(d)
		print("nonce:")

		
		nonce = _block['nonce']
		# print(nonce)
		digest = hashlib.sha256((str(d) + nonce).encode()).hexdigest()
		if ( digest.startswith('0' * config.difficulty)):
			return True
		else:
			return False
		
	#concencus functions

	def validate_block(self,_block):
		#check proof of work 
		flag1 = self.valid_proof(_block)
		if (flag1):
		#check previous hash
			previousblock=self.chain[-1]
			previousmessage = OrderedDict(
						{'transactions': previousblock['transactions'],
						 'previousHash':  previousblock['previousHash'],
						 #'nonce': self.nonce ,
						 'number': previousblock['number'],
						 'timestamp': previousblock['timestamp']
						})
			previoushash = hashlib.sha256((str(previousmessage)+previousblock['nonce']).encode()).hexdigest()
			if len(self.chain) >= 2:
				previousblock=self.chain[-2]
				previousmessage = OrderedDict(
							{'transactions': previousblock['transactions'],
							'previousHash':  previousblock['previousHash'],
							#'nonce': self.nonce ,
							'number': previousblock['number'],
							'timestamp': previousblock['timestamp']
							})
				previoushash_2 = hashlib.sha256((str(previousmessage)+previousblock['nonce']).encode()).hexdigest()
				if _block['previousHash'] == previoushash_2:
					return False	
			
			if (_block['previousHash'] != previoushash):
				print("wrong prev hash")
				flag = self.resolve_conflicts()
				if (flag==False): 
					return False
				return True
			else: 
				self.mining_useless = True
				transactions=_block['transactions']
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
				self.chain.append(_block)
				self.current_block = []
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
		print("ENTERED RESOLVE CONFL")
		max_chain = -1
		node_max_chain = None
		for i in self.ring:
			r = requests.get('http://'+i['ip']+':'+i['port']+'/chainlength')
			res = r.json()
			if res['length'] > max_chain:
				node_max_chain = res['length']
				node_max_chain = i
		r = requests.get('http://'+node_max_chain['ip']+':'+node_max_chain['port']+'/chain')
		res = r.json()
		chain = res['chain']
		self.resolvingConflicts = True #LOCK THE TRANSACTIONS
		self.UTXO = [] # new utxo list
		for bloc in chain: # foreach 
			trans = bloc['transactions']
			for t in trans: # foreach transaction in block
				if bloc['number'] == 0:
					out = transaction.TransactionOutput(t['receiver_address'] , t['amount'])
					self.UTXO.append(out)
				else:
					self.validate_transaction(t, True)
					try:
						self.verified_transactions.remove(t)
					except ValueError:
						pass
		for tr in self.verified_transactions:
			self.validate_transaction(tr, True)
		self.resolvingConflicts = False
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



