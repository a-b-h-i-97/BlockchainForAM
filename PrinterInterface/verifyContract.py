from solc import compile_source
from web3 import Web3

def verify_contract(w3):

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

    tx_hash = input("Enter transaction hash: ")
    tx = w3.eth.getTransaction(tx_hash)

    input_data = tx['input'][2: ]
    input_data = input_data[0: len(contract_interface['bin'])]

    if(input_data == contract_interface['bin']):
        print("Contract byte code matches compiled byte code")
    else:
        print("Contract byte code does not match compiled byte code")
        print(input_data)
        print(contract_interface['bin'])