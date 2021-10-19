from solc import compile_source
from web3 import Web3
import getpass

def record_print(w3):
    
    print("\nEnter 1 for Printer Friendly Contract")
    print("Enrer 2 for Designer Friendly Contract")
    ch = input("\nEnter your choice : ")
    ch = int(ch)

    if ch == 1:
        contract_name = "Print_Friendly_Agreement"
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

    designID = input("Enter designID: ")

    passphrase = getpass.getpass("Enter passphrase: ")
    w3.personal.unlockAccount(w3.eth.accounts[0], passphrase)

    Agreement = w3.eth.contract(
        address=contractAddress,
        abi=contract_interface['abi'],
    )

    try:
        tx_hash = Agreement.functions.recordPrint(designID).transact()

    except ValueError:
        print("Unauthorized printer or agreement has ended")
        return

    w3.miner.start(4)
    print("Waiting for transaction to be mined...")
    w3.eth.waitForTransactionReceipt(tx_hash)
    w3.miner.stop()

    # TODO Update old contract as per new conventions
    if ch == 1:
        quantity_remaining = Agreement.functions.quantityRemaining().call()
    else:
        quantity_remaining = Agreement.functions.quantity_remaining().call()

    print("Print record successful!! \n Quantity remaining as per agreement: ", quantity_remaining)