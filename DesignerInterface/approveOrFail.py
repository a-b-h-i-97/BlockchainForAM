from solc import compile_source
from web3 import Web3
import getpass

def approve_or_fail(w3):

    with open('../contracts/Design_Friendly_Agreement.sol', 'r') as source_file:
        contract_source = source_file.read()

    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:Design_Friendly_Agreement']

    w3.eth.defaultAccount = w3.eth.accounts[0]

    contractAddress = input("Enter contract address: ")
    contractAddress = Web3.toChecksumAddress(Web3.toHex(hexstr = contractAddress))

    Agreement = w3.eth.contract(
        address=contractAddress,
        abi=contract_interface['abi'],
    )

    quantity = Agreement.functions.QUANTITY().call()
    test_quantity = Agreement.functions.TEST_QUANTITY().call()
    pass_quantity = Agreement.functions.PASS_QUANTITY().call()
    quantity_remaining = Agreement.functions.quantity_remaining().call()
    quantity_tested = Agreement.functions.quantity_tested().call()
    quantity_passed = Agreement.functions.quantity_passed().call()

    quantityPrinted = quantity - quantity_remaining - quantity_tested

    if quantity_passed >= pass_quantity:
        print("\nRequired number of products have already been approved")
        return

    # The contract ensures that quantity_tested cannot be greater than test_quantity
    if quantity_tested == test_quantity:
        print("\nTest quantity has been exceeded")
        return
    if quantity_remaining > 0:
        print("\nTesting can start only after all items are printed")
        return

    passphrase = getpass.getpass("Enter passphrase: ")
    w3.personal.unlockAccount(w3.eth.accounts[0], passphrase)
    

    if quantity_tested > 0:
        print("\nNumber of products tested: ", quantity_tested)
        i = 0
        while(i < quantity_tested):
            product = Agreement.functions.tested_products(i).call()
            approved = "Approved" if product[2] else "Failed"
            print(i+1,":", product[0], product[1], approved)
            i = i+1

    print("\n\nThe current queue of products")
    i = 0
    while(i < quantityPrinted):
        product = Agreement.functions.products(i).call()
        print(i+1, ":", product)
        i = i+1

    index = input("\nEnter an index to approve or fail: ")
    index = int(index)

    if index < 1 or index > quantityPrinted :
        print("Invalid index")
        return

    print("\nEnter 0 to mark product as failed")
    print("Enter 1 to mark product as approved")
    ch = input("\nEnter your choice : ")
    ch = int(ch)

    approved = True if ch == 1 else False

    try:
        tx_hash = Agreement.functions.testProduct(index - 1, approved).transact()

    except ValueError:
        print("Required items haven't been printed or test quantity has exceeded")
        return

    #tx_hash = Agreement.functions.testProduct(index - 1, approved).transact()

    w3.miner.start(1)
    print("Waiting for transaction to be mined...")
    w3.eth.waitForTransactionReceipt(tx_hash)
    w3.miner.stop()

    print("Marking product as approved/failed completed successfully")

    # calculate updated state
    quantity_passed = quantity_passed + 1 if approved else quantity_passed
    quantity_tested = quantity_tested + 1

    if quantity_passed == pass_quantity:
        print("\nRequired number of products have been approved. Transfer complete")
        return
    if quantity_tested == test_quantity:
        print("\nTest quantity has been exceeded. The printer has failed the contract")