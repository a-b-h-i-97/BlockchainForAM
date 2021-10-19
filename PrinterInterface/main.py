import recordPrint
import register
import verifyContract
import viewDetails
import os
import sys
from web3 import Web3

sys.path.append(os.path.abspath('../DesignDatabase'))
import designHelpers

provider = Web3.IPCProvider(os.path.join(os.path.dirname(__file__), '../PrintNode/geth.ipc'))
w3 = Web3(provider)

print("\nWelcome to the printer interface\n")

choice = 0
while(choice != 6):

    print("\n\nEnter 1 to verify contract.")
    print("Enter 2 to view details of a contract")
    print("Enter 3 to view details of a design file")
    print("Enter 4 to register to a contract")
    print("Enter 5 to record print")
    print("Enter 6 to exit")

    choice = int(input("\nEnter your choice : "))

    if (choice == 1):
        verifyContract.verify_contract(w3)
    elif (choice == 2):
        viewDetails.view_Details(w3)
    elif (choice == 3):
        designHelpers.get_design(w3)
    elif (choice == 4):
        register.register(w3)
    elif (choice == 5):
        recordPrint.record_print(w3)
    elif (choice == 6):
        print("Exiting")
    else:
        print("Invalid option")