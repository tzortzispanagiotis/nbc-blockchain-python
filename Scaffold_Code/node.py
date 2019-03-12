from Scaffold_Code import block, wallet , config ,chain , transaction

class Node: #creation of bootstap node
	def __init__(self):
		#self.NBC=100
		##set
		self.current_block  = [] #san transaction pool me transactions<=maximum
		self.chain = []
		#self.current_id_count
		self.wallet = create_wallet()
		self.transaction_pool = []
		#utxo==transaction_output
		self.UTXO = []
		#slef.ring[]   #here we store information for every node, as its id, its address (ip:port) its public key and its balance 




	#def create_new_block(previousHash): #an einai to proto 
				
		

		
	def create_wallet():
		##create a wallet for this node, with a public key and a private key
		return Wallet()

	def register_node_to_ring():
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
        #return True 

	def create_transaction(sender, receiver,amount ,  signature , wallet):
		traninput = []
		#inputs ola ta outputs pou exoun os receiver ton torino sender
		for i in UTXO:
			if (i.recepient==sender):
				traninput.append(i)
				UTXO.remove(i)
        new_transaction = Transaction(wallet , receiver , amount , traninput)
		new_transaction.add_id_to_output()	
		return new_transaction    
		#remember to broadcast it


	def broadcast_transaction():


	def verify_signature(transaction):
		tr = transaction.to_dict1(False)
		#analoga se ti morfi tha to pairnw , ligika tha einai idi se json
		pubkey= RSA.importKey(binascii.unhexlify(tr)
	    verifier = PKCS1_v1_5.new(pubkey)
		h = SHA.new(message.encode('utf8'))
	    return verifier.verify(h, binascii.unhexlify(transaction.signature))



	def validate_transaction(transaction):
		#sos ti object einai to transaction tha einai logika se morfi dict?
		if (verify_signature(transaction)):
			traninput=[]
			sum1=0
			for i in UTXO:
				if (i.recepient==transaction.sender_address):
					traninput.append(i)
					sum1=sum1+i.amount
			if (sum1>=transaction.amount)
			#eparki xrimata gia tin metafora
				for t in traninput:
					UTXO.remove(t)
				#now create transaction outputs and add them at the utxo list
				out1=TransactionOutput(transaction.receiver_address , transaction.amount)
				out2=TransactionOutput(transaction.sender_address ,sum1-amount)
				UTXO.append(out1)
				UTXO.append(out2)
		

	def add_transaction_to_block(current_block , transaction , previousHash): 
		#if
		#if enough transactions  mine
		if validate_transaction(transaction):
		{
			if (len(current_block) == max_transactions):
				new_block = Block(previousHash , current_block)
				new_block.myHash()
				mine_block(new_block)
			
		    else:
				current_block.append(transaction)
		}



	def mine_block( block , self  ):
		 last_block = self.chain[-1]
		 message = to_dict(last_block)
		 nonce = self.valid_proof(message)
		 block.add_nonce(nonce)
		 self.broadcast_block()
		 chain.add_block_to_mychain(block)



	def broadcast_block():


	

	def valid_proof(message , difficulty):
		i = 0
    	prefix = '0' * difficulty
    	while True:
			nonce = str(i)
			digest = dumb_hash(message + nonce)
			if digest.startswith(prefix):
				return nonce
			i += 1



	#concencus functions
    def validate_block(self ,block):
		#check proof of work 
		#check previous hash
		my_last_block=self.chain[-1]
		 if (block['previous_hash'] != my_last_block.gethash()):
			 resolve_conflicts(self)
		 else return True

	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes


	def resolve_conflicts(self):
		#resolve correct chain



