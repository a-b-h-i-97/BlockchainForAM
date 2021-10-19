from solc import compile_source
from web3 import Web3
import getpass


def credit_amount(w3):

    with open('../contracts/Print_Friendly_Agreement.sol', 'r') as source_file:
        contract_source = source_file.read()

    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:Print_Friendly_Agreement']

    w3.eth.defaultAccount = w3.eth.accounts[0]

    contractAddress = input("Enter contract address: ")
    contractAddress = Web3.toChecksumAddress(Web3.toHex(hexstr = contractAddress))

    credit_amount = input("Enter credit amount: ")
    credit_amount = int(credit_amount)

    passphrase = getpass.getpass("Enter passphrase: ")
    w3.personal.unlockAccount(w3.eth.accounts[0], passphrase)

    Agreement = w3.eth.contract(
        address=contractAddress,
        abi=contract_interface['abi'],
    )

    try:
        tx_hash = Agreement.fallback().transact({'value': credit_amount})

    except ValueError:
        print("Something went wrong. The amount could not be credited")
        return

    w3.miner.start(4)
    print("Waiting for transaction to be mined...")
    w3.eth.waitForTransactionReceipt(tx_hash)
    w3.miner.stop()

    print("Amount credited successfully!!")
    print("Transaction hash: ", Web3.toHex(tx_hash))
