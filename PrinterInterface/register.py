from solc import compile_source
from web3 import Web3
import getpass
import os

def register(w3):

    print("\nEnter 1 for Printer Friendly Contract")
    print("Enrer 2 for Designer Friendly Contract")
    ch = input("\nEnter your choice : ")
    ch = int(ch)

    if ch == 1:
        contract_name = "Print_Friendly_Agreement"
        print("The contract amount will be deducted from your account")
    elif ch == 2:
        contract_name = "Design_Friendly_Agreement"
    else:
        print("Invalid choice")
        return

    contract_source = '../contracts/' + contract_name + '.sol'
    with open(contract_source, 'r') as source_file:
        contract_source = source_file.read()

    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:' + contract_name]

    w3.eth.defaultAccount = w3.eth.accounts[0]

    contractAddress = input("Enter contract address: ")
    contractAddress = Web3.toChecksumAddress(Web3.toHex(hexstr = contractAddress))

    passphrase = getpass.getpass("Enter passphrase: ")
    w3.personal.unlockAccount(w3.eth.accounts[0], passphrase)

    Agreement = w3.eth.contract(
        address=contractAddress,
        abi=contract_interface['abi'],
    )

    try:
        if ch == 1:
            credit_amount = Agreement.functions.amount().call()
            tx_hash = Agreement.fallback().transact({'value': credit_amount})
        else:
            tx_hash = Agreement.functions.registerPrinter().transact()

    except ValueError:
        if ch == 1:
            print("A printer is already registered or you have insufficient balance")
        else:
            print("A printer is already registered or contract has insufficient balance")
        return

    w3.miner.start(4)
    print("Waiting for transaction to be mined...")
    w3.eth.waitForTransactionReceipt(tx_hash)
    w3.miner.stop()

    printer = Agreement.functions.printer().call()

    if printer == w3.eth.accounts[0]:
        print("Registration successful!!")