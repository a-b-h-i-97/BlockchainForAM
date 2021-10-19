from solc import compile_source
from web3 import Web3


def view_products(w3):
    
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

    Agreement = w3.eth.contract(
        address=contractAddress,
        abi=contract_interface['abi'],
    )

    quantity = Agreement.functions.QUANTITY().call()

    # TODO Update old contract as per new conventions
    if ch == 1:
        quantity_remaining = Agreement.functions.quantityRemaining().call()
        quantityPrinted = quantity - quantity_remaining

        print("\nNumber of products printed: ", quantityPrinted)
        i = 0
        while(i < quantityPrinted):
            product = Agreement.functions.products(i).call()
            print(product)
            i = i+1
    else:
        quantity_remaining = Agreement.functions.quantity_remaining().call()
        quantity_tested = Agreement.functions.quantity_tested().call()

        if quantity_tested > 0:
            print("\nNumber of products tested: ", quantity_tested)
            i = 0
            while(i < quantity_tested):
                product = Agreement.functions.tested_products(i).call()
                approved = "Approved" if product[2] else "Failed"
                print(i+1, product[0], product[1], approved)
                i = i+1

        print("\n")
        print_queue_length = quantity - quantity_remaining - quantity_tested

        if print_queue_length == 0:
            print("\nNo products in queue to be tested")
        else:
            print("\nNumber of products in queue to be tested: ", print_queue_length)
            i = 0
            while(i < print_queue_length):
                product = Agreement.functions.products(i).call()
                print(product)
                i = i+1

    
