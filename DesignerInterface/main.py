import createContract
import creditAmount
import viewProducts
import approveOrFail
import os
from web3 import Web3

provider = Web3.IPCProvider(os.path.join(os.path.dirname(__file__), '../DesignNode/geth.ipc'))
w3 = Web3(provider)

print("\nWelcome to the designer interface\n")

choice = 0
while(choice != 6):

    print("\n\nEnter 1 to create a printer friendly contract.")
    print("Enter 2 to create a designer friendly contract")
    print("Enter 3 to credit an amount to the contract")
    print("Enter 4 to view printed product details")
    print("Enter 5 to approve/fail product")
    print("Enter 6 to exit")

    choice = int(input("\nEnter your choice : "))

    if (choice == 1):
        createContract.printer_friendly_contract(w3)
    elif (choice == 2):
        createContract.designer_friendly_contract(w3)
    elif (choice == 3):
        creditAmount.credit_amount(w3)
    elif (choice == 4):
        viewProducts.view_products(w3)
    elif (choice == 5):
        approveOrFail.approve_or_fail(w3)
    elif (choice == 6):
        print("Exiting")
    else:
        print("Invalid option")