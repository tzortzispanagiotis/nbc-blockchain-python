from Scaffold_Code import block, wallet , config ,chain , transaction
from collections import OrderedDict

class Node: #creation of bootstap node
	def __init__(self):
		#self.NBC=100
		##set
		self.current_block  = [] #san transaction pool me transactions<=maximum
		self.chain = []
		#self.current_id_count
		self.wallet = self.create_wallet()
		self.transaction_pool = []
		#utxo==transaction_output
		self.UTXO = []
		#slef.ring[]   #here we store information for every node, as its id, its address (ip:port) its public key and its balance 




	#def create_new_block(previousHash): #an einai to proto 
				
		

		
	def create_wallet():
		##create a wallet for this node, with a public key and a private key
		return wallet.Wallet()

	def register_node_to_ring():
       		return True 

		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs

	def create_transaction(self, sender, receiver,amount ,  signature , wallet):
			traninput = []
			#inputs ola ta outputs pou exoun os receiver ton torino sender
			for i in self.UTXO:
					if (i.recepient==sender):
						traninput.append(i)
						self.UTXO.remove(i)
			new_transaction = Transaction(wallet , receiver , amount , traninput)
			new_transaction.add_id_to_output()	
			return new_transaction    
		#remember to broadcast it


	def broadcast_transaction():
		return 1


	def verify_signature(transaction):
		tr = transaction.to_dict1(False)
		#analoga se ti morfi tha to pairnw , ligika tha einai idi se json
		pubkey= RSA.importKey(binascii.unhexlify(tr)
	    verifier = PKCS1_v1_5.new(pubkey)
		h = SHA.new(message.encode('utf8'))
	    v = verifier.verify(h, binascii.unhexlify(transaction.signature))
		return v 



	def validate_transaction(self, transaction):
		#sos ti object einai to transaction tha einai logika se morfi dict?
		if (verify_signature(transaction)):
			traninput=[]
			sum1=0
			for i in self.UTXO:
				if (i.recepient==transaction.sender_address):
					traninput.append(i)
					sum1=sum1+i.amount
			if (sum1>=transaction.amount)
			#eparki xrimata gia tin metafora
				for t in traninput:
					self.UTXO.remove(t)
				#now create transaction outputs and add them at the utxo list
				out1=TransactionOutput(transaction.receiver_address , transaction.amount)
				out2=TransactionOutput(transaction.sender_address ,sum1-amount)
				self.UTXO.append(out1)
				self.UTXO.append(out2)
		

	def add_transaction_to_block(current_block , transaction ): 
		#if
		#if enough transactions  mine
		if self.validate_transaction(transaction):
			if (len(current_block) == transaction.max_transactions):
				previousblock = self.chain[-1]
				previousnonce = previousblock['nonce']
				previousHash = sha256(json.dumps(previousblock.to_dict(include_nonce=false)+previousblock['nonce']):
				new_block = Block(previousHash , current_block)
				mine_block(new_block)
			
		    else:
				current_block.append(transaction)



	def mine_block( block , self  ):
		 
		 message = block.to_dict()
		 nonce = self.search_proof(message)
		 block.add_nonce(nonce)
		 self.broadcast_block()
		 chain.add_block_to_mychain(block)



	def broadcast_block():


	

	def search_proof(message , difficulty):
		i = 0
    	prefix = '0' * difficulty
    	while True:
			nonce = str(i)
			digest = sha256(json.dumps((message + nonce))
			if digest.startswith(prefix):
				return nonce
			i += 1


	def valid_proof(self , block):
		d = OrderedDict({'transactions': block['transactions'],
						 'previousHash':  block['previousHash'],
						 #'nonce': self.nonce ,
						 'number': block['blocknumber']
						})
		nonce = block['nonce']
		digest = sha256(json.dumps((message + nonce))
       if ( digest.startswith('0' * difficulty)):
		   return True
	   else:
		return False
		
	#concencus functions

    def validate_block(self ,block):
		#check proof of work 
		flag1 = valid_proof(block)
		if (flag1):
		#check previous hash
			my_last_block=self.chain[-1]
			if (block['previous_hash'] != my_last_block.gethash()):
				flag = resolve_conflicts(self)
				if !(flag): return False
				return True
			else: 
				return True
		return False
			

		 

	def valid_chain(self, chain):
		# check if the chain gven is valid
		current_index=1
		last_block=chain[0]
		while current_index < len(chain):
            block = chain[current_index]
            
            # Check that the hash of the block is correct
            if block['previous_hash'] != sha256(json.dumps(last_block.to_dict(include_nonce=false)+last_block['nonce']):
                return False

            # Check that the Proof of Work is correct
            #Delete the reward transaction
            
            if not self.valid_proof(block):
                return False

            last_block = block
            current_index += 1

        return True
		



def resolve_conflicts(self, received_block, current_block):
	# resolve correct chain
	changed = False

	if received_block['previousHash'] == current_block['previousHash']:
		self.block_pool.append(received_block)
	else:
		for b in self.block_pool:
			if b['previousHash'] == current_block['previousHash'] and received_block[
				'previousHash'] == block.getHash(b):
				self.chain[-1] = b
				self.chain.append(received_block)
				changed = True

	return changed



