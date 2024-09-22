from flask import Flask, request, render_template, jsonify
from web3 import Web3, HTTPProvider
import json
import urllib3

blockchain = 'http://127.0.0.1:7545'

def connect():
    web3 = Web3(HTTPProvider(blockchain))
    web3.eth.defaultAccount = web3.eth.accounts[0]

    artifact = "../build/contracts/ValuCoin.json"
    with open(artifact) as f:
        artifact_json = json.load(f)
        contract_abi = artifact_json['abi']
        contract_address = artifact_json['networks']['5777']['address']
    
    contract = web3.eth.contract(
        abi=contract_abi,
        address=contract_address
    )
    return contract, web3

app = Flask(__name__)

@app.route('/addAsset', methods=['GET', 'POST'])
def addAsset():
    id = request.args.get('id')
    id = int(id)
    name = request.args.get('name')
    value = request.args.get('value')
    value = int(value)

    contract, web3 = connect()
    try:
        tx_hash = contract.functions.addAsset(id, name, value).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return 'Transaction successful'
    except Exception as e:
        return f'Transaction error: {str(e)}'

@app.route('/transferAsset', methods=['GET', 'POST'])
def transferAsset():
    id = request.args.get('id')
    id = int(id)
    new_owner = request.args.get('address')
    
    contract, web3 = connect()
    tx_hash = contract.functions.transferAsset(id, new_owner).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return 'Asset transferred'

@app.route('/getAsset', methods=['GET', 'POST'])
def getAsset():
    id = request.args.get('id')
    id = int(id)

    contract, web3 = connect()
    asset_data = contract.functions.getAsset(id).call()
    return jsonify(asset_data)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/addAssetPage', methods=['GET', 'POST'])
def addAssetPage():
    return render_template('addAsset.html')

@app.route('/transferAssetPage', methods=['GET', 'POST'])
def transferAssetPage():
    return render_template('transferAsset.html')

@app.route('/getAssetPage', methods=['GET', 'POST'])
def getAssetPage():
    return render_template('getAsset.html')

@app.route('/addassetform', methods = ['GET', 'POST'])
def addassetform():
    id = request.form['id']
    name = request.form['name']
    value = request.form['value']

    pipe = urllib3.PoolManager()
    response = pipe.request('get', 'http://127.0.0.1:4000?id='+id+'&name='+name+'&value='+value)
    response = response.data
    response = response.decode('utf-8')
    return render_template('addAsset.html', response=response)

@app.route('/transferassetform', methods = ['GET', 'POST'])
def transferassetform():
    id = request.form['id']
    address = request.form['address']

    pipe = urllib3.PoolManager()
    response = pipe.request('get', 'http://127.0.0.1:4000?id='+id+'&address='+address)
    response = response.data
    response = response.decode('utf-8')
    return render_template('transferAsset.html', response=response)

@app.route('/getassetform', methods = ['GET', 'POST'])
def getassetform():
    id = request.form['id']

    pipe = urllib3.PoolManager()
    response = pipe.request('get', 'http://127.0.0.1:4000?id='+id)
    response = response.data
    response = response.decode('utf-8')
    return render_template('transferAsset.html', response=response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', 
            port=4000
            )