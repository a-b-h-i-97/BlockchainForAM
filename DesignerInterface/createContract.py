from solc import compile_source
from web3 import Web3
import getpass


def printer_friendly_contract(w3):
    
    with open('../contracts/Print_Friendly_Agreement.sol', 'r') as source_file:
        contract_source = source_file.read()

    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:Print_Friendly_Agreement']

    w3.eth.defaultAccount = w3.eth.accounts[0]

    Agreement = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    quantity = input("Enter agreement quantity: ")
    quantity = int(quantity)

    amount = input("Enter agreement amount: ")
    amount = int(amount)

    passphrase = getpass.getpass("Enter passphrase: ")
    w3.personal.unlockAccount(w3.eth.accounts[0], passphrase)

    tx_hash = Agreement.constructor(quantity, amount).transact()
    print("\nTransaction hash: ", Web3.toHex(tx_hash))

    w3.miner.start(4)
    print("Waiting for transaction to be mined...")
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    w3.miner.stop()

    print("Contract successfully deployed!!")
    print("Contract address: ", tx_receipt.contractAddress)
    
    return

def designer_friendly_contract(w3):

    with open('../contracts/Design_Friendly_Agreement.sol', 'r') as source_file:
        contract_source = source_file.read()

    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:Design_Friendly_Agreement']

    w3.eth.defaultAccount = w3.eth.accounts[0]
    Agreement = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    quantity = input("Enter agreement quantity: ")
    quantity = int(quantity)

    amount = input("Enter agreement amount: ")
    amount = int(amount)

    while(1):
        test_quantity = input("Enter test quantity: ")
        test_quantity = int(test_quantity)

        if(test_quantity > quantity):
            print("\n Test quantity cannot be greater than contract quantity")
            continue
        else:
            break
    
    while(1):
        pass_quantity = input("Enter pass quantity: ")
        pass_quantity = int(pass_quantity)

        if(pass_quantity > test_quantity):
            print("\n Pass quantity cannot be greater than test quantity")
            continue
        else:
            break
    
    passphrase = getpass.getpass("Enter passphrase: ")
    w3.personal.unlockAccount(w3.eth.accounts[0], passphrase)

    tx_hash = Agreement.constructor(quantity, test_quantity,pass_quantity, amount).transact()
    print("\nTransaction hash: ", Web3.toHex(tx_hash))

    w3.miner.start(4)
    print("Waiting for transaction to be mined...")
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    w3.miner.stop()

    print("Contract successfully deployed!!")
    print("Contract address: ", tx_receipt.contractAddress)

    return