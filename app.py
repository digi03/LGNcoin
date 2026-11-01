import json, os, hashlib, time
from flask import Flask, jsonify
app = Flask(__name__)
CHAIN_FILE='lgn_chain.json'
class Blockchain:
 def __init__(self):
  self.chain=[]
  if os.path.exists(CHAIN_FILE):
   try: self.chain=json.load(open(CHAIN_FILE))
   except: self.chain=[]
  if not self.chain: self.new_block(100,'1')
 def save(self): json.dump(self.chain, open(CHAIN_FILE,'w'))
 def new_block(self,p,ph=None):
  b={'index':len(self.chain)+1,'timestamp':time.time(),'proof':p,'previous_hash':ph or self.hash(self.chain[-1]) if self.chain else '1'}
  self.chain.append(b);self.save();return b
 @property
 def last_block(self): return self.chain[-1]
 def proof_of_work(self,last):
  p=0
  while hashlib.sha256(f'{last}{p}'.encode()).hexdigest()[:4]!="0000": p+=1
  return p
 @staticmethod
 def hash(b): return hashlib.sha256(json.dumps(b,sort_keys=True).encode()).hexdigest()
bc=Blockchain()
@app.route('/')
def i(): return '<h1>LGN COIN LARANTUKA AKTIF!</h1><a href=/mine>MINE 50 LGN</a> | <a href=/chain>EXPLORER</a>'
@app.route('/mine')
def mine():
 pr=bc.proof_of_work(bc.last_block['proof'])
 bl=bc.new_block(pr,bc.hash(bc.last_block))
 return jsonify(bl)
@app.route('/chain')
def chain(): return jsonify({'chain':bc.chain,'length':len(bc.chain)})
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
