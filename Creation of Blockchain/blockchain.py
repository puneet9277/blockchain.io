
#creation of blockchain.

import datetime
import hashlib
import json
from flask import Flask, jsonify

#building of blockchain

class Blockchain:
    
         def __init__(self):
            self.chain = []
            self.create_block(proof = 1, previous_hash = '0')  #for the first block,previous hash in double quote as it is checked by sha256 hash code 
         
         def create_block(self,proof,previous_hash):
             block = {'index' : len(self.chain) + 1, # for the index value
                      'timestamp': str(datetime.datetime.now()), #for the time block was created and then using the date time libhrary, taking the value in str type for thr json format conversion
                       'proof' : proof,
                       'previous_hash' : previous_hash}
             self.chain.append(block)
             return block
         
            
         def get_previous_block(self):
             return self.chain[-1] #it will return the previous block info required
         
         def proof_of_work(self,previous_proof):
                new_proof = 1
                check_proof = False
                while check_proof is False:
                    hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() #we use minus so that the statement becomes unsymmetrical.encode used for some changings in format for usage in sha256
                    if hash_operation[ :4] == '0000': #checking for the four zeros of the 64 bit number.
                        check_proof = True
                    else:
                       new_proof += 1
                    return new_proof 
                
         def hash(self, block):  #this function will check if everything is right or not that is, it will  check for the proof of work and secondly it will check the previous_hash value of the block and the previous block hash..
            encoded_block = json.dumps(block, sort_keys = True).encode() #the json dump is for conversion in string type and will directly convert that into json format for further usage .the encoded function is used for putting d that is required for sha256.
            return hashlib.sha256(encoded_block).hexdigest() 
        
         def is_chain_valid(self, chain):  #function will check for the valid chain by comparing the hash and previous hash values of the block 
            previous_block = chain[0]
            block_index = 1
            while block_index < len(chain):
                block = chain[block_index]
                if block['previous_hash'] != self.hash(previous_block):
                    return False
                previous_proof = previous_block['proof']
                proof = block['proof']
                hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
                if hash_operation[ :4] != '0000':
                    return False
                previous_block  = proof
                block_index += 1
         
            return True

 #mining from the blockchain
    
      #part 1 = creating a web app to interact with the blockchain using get requests from our postman interface
  #app  =  Flask(__name__)
  #app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False      

# Creating a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

      #part 2 creatining a blockchain (creating object instance for the class blockchain)
blockchain = Blockchain()        


#mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']  # Corrected from previous_proof = previous_block('proof')
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Congrats, mined a block successfully!!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200





@app.route('/get_chain' , methods = ['GET'] )
def get_chain():
     response = { 'chain' : blockchain.chain, 
                   'length' : len(blockchain.chain) }
     return jsonify(response),200


@app.route('/is_chain_valid' , methods = ['GET'])
def valid_chain():
    valid_chain = blockchain.is_chain_valid(blockchain.chain)
    if valid_chain:
        response = { 'message' : 'The Blockchain is Valid.'}
    else:
        response = {'message' :  'INVALID BLOCKCHAIN!!!.'}
    return jsonify(response),200
    
#running the app 
app.run(host = '0.0.0.0', port = 5000)



















