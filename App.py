import json, os, hashlib, time
from flask import Flask, jsonify

app = Flask(__name__)
CHAIN_FILE = 'lgn_chain.json'

class Blockchain:
    def __init__(self):
        self.chain = []
        if os.path.exists(CHAIN_FILE):
            try:
                with open(CHAIN_FILE, 'r') as f:
                    self.chain = json.load(f)
            except:
                self.chain = []
        if not self.chain:
            self.new_block(proof=100, previous_hash='1')
    
    def save(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump(self.chain, f)
    
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain)+1,
            'timestamp': time.time(),
            'proof': proof,
            'previous_hash': previous_hash or (self.hash(self.chain[-1]) if self.chain else '1')
        }
        self.chain.append(block)
        self.save()
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while hashlib.sha256(f'{last_proof}{proof}'.encode()).hexdigest()[:4] != "0000":
            proof+=1
        return proof

    @staticmethod
    def hash(block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

blockchain = Blockchain()

@app.route('/')
def index():
    return '<h1>LGN COIN OFFICIAL</h1><p>Blockchain Larantuka</p><p><a href=/chain>Explorer</a> | <a href=/mine>Mine 50 LGN</a></p>'

@app.route('/mine')
def mine():
    proof = blockchain.proof_of_work(blockchain.last_block['proof'])
    block = blockchain.new_block(proof, blockchain.hash(blockchain.last_block))
    return jsonify({'message': 'Block mined', 'block': block})

@app.route('/chain')
def chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
