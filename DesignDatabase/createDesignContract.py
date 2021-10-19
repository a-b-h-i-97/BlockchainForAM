from solc import compile_source
from web3 import Web3
import getpass
import os

def create_contract():
    provider = Web3.IPCProvider(os.path.join(os.path.dirname(__file__), '../DesignNode/geth.ipc'))
    w3 = Web3(provider)

    with open('../contracts/Designdb.sol', 'r') as source_file:
        contract_source = source_file.read()

    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:DesignDB']

    w3.eth.defaultAccount = w3.eth.accounts[0]

    Agreement = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    
    passphrase = getpass.getpass("Enter passphrase: ")

    w3.personal.unlockAccount(w3.eth.accounts[0], passphrase)

    w3.miner.start(4)
    tx_hash = Agreement.constructor().transact()
    print("\nTransaction hash: ", Web3.toHex(tx_hash))

    print("Waiting for transaction to be mined...")
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    print("Contract successfully deployed!!")
    print("Contract address: ", tx_receipt.contractAddress)
    with open('contract_address','w') as file:
        file.write(tx_receipt.contractAddress)
    
    return

create_contract()




