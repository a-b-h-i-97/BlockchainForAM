from solc import compile_source
from web3 import Web3

def view_Details(w3):

    print("\nEnter 1 for Printer Friendly Contract")
    print("Enrer 2 for Designer Friendly Contract")
    ch = input("\nEnter your choice : ")
    ch = int(ch)

    if ch == 1:

        with open('../contracts/Print_Friendly_Agreement.sol', 'r') as source_file:
            contract_source = source_file.read()

        compiled_sol = compile_source(contract_source)
        contract_interface = compiled_sol['<stdin>:Print_Friendly_Agreement']

        w3.eth.defaultAccount = w3.eth.accounts[0]

        contractAddress = input("Enter contract address: ")
        contractAddress = Web3.toChecksumAddress(Web3.toHex(hexstr = contractAddress))

        Agreement = w3.eth.contract(
            address = contractAddress,
            abi=contract_interface['abi'],
        )

        quantity = Agreement.functions.QUANTITY().call()
        amount = Agreement.functions.amount().call()
        balance = Agreement.functions.getBalance().call()
        quantityRemaining = Agreement.functions.quantityRemaining().call()

        print("\n")
        print("Quantity: ", quantity)
        print("Amount: ", amount)
        print("Balance: ", balance)
        print("Quantity Remaining ", quantityRemaining)

    elif ch == 2:

        with open('../contracts/Design_Friendly_Agreement.sol', 'r') as source_file:
            contract_source = source_file.read()

        compiled_sol = compile_source(contract_source)
        contract_interface = compiled_sol['<stdin>:Design_Friendly_Agreement']

        w3.eth.defaultAccount = w3.eth.accounts[0]

        contractAddress = input("Enter contract address: ")
        contractAddress = Web3.toChecksumAddress(Web3.toHex(hexstr = contractAddress))

        Agreement = w3.eth.contract(
            address = contractAddress,
            abi=contract_interface['abi'],
        )

        quantity = Agreement.functions.QUANTITY().call()
        amount = Agreement.functions.CONTRACT_AMOUNT().call()
        balance = Agreement.functions.getBalance().call()
        quantity_remaining = Agreement.functions.quantity_remaining().call()
        test_quantity = Agreement.functions.TEST_QUANTITY().call()
        pass_quantity = Agreement.functions.PASS_QUANTITY().call()

        print("\n")
        print("Quantity: ", quantity)
        print("Amount: ", amount)
        print("Balance: ", balance)
        print("Test Quantity: ", test_quantity)
        print("Pass Quantity: ", pass_quantity)
        print("Quantity Remaining ", quantity_remaining)

    else:
        print("Invalid choice")




