from solc import compile_source
from web3 import Web3
import getpass
from py_essentials import hashing as hs
import os

def create_contract_object(w3):
    with open('../contracts/Designdb.sol', 'r') as source_file:
        contract_source = source_file.read()

    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:DesignDB']

    w3.eth.defaultAccount = w3.eth.accounts[0]
    
    with open('../DesignDatabase/contract_address','r') as file:
        contractAddress = file.read()
    contractAddress = Web3.toChecksumAddress(Web3.toHex(hexstr = contractAddress))

    designDb = w3.eth.contract(
        address = contractAddress,
        abi = contract_interface['abi'],
    )
    return designDb


def upload_design(w3):
    designDb = create_contract_object(w3)
    filePath = input("Enter filepath: ")
    try:
        fileHash = hs.fileChecksum(filePath,'sha256',False)
    except TypeError:
        print("File does not exist")
        return
    
    print("Hash of the given file: ",fileHash)
    
    fileName = input("Enter filename: ")
    version = input("Enter version: ")
    passphrase = getpass.getpass("Enter passphrase: ")
    w3.personal.unlockAccount(w3.eth.accounts[0], passphrase)
    
    try:
        tx_hash = designDb.functions.addDesign(fileName,fileHash,version).transact()
    except ValueError:
        print("File with same hash exists")
        return

    w3.miner.start(4)
    print("Waiting for transaction to be mined...")
    w3.eth.waitForTransactionReceipt(tx_hash)
    w3.miner.stop()

    print("Design uploaded successfully. TX Hash: ",Web3.toHex(tx_hash))     

    
def get_files_length(w3):
    designDb = create_contract_object(w3)
    filesLength = designDb.functions.getFilesLength().call()
    print("No of design files in database:",filesLength)


def get_design(w3):
    designDb = create_contract_object(w3)
    filePath = input("Enter filepath: ")
    try:
        fileHash = hs.fileChecksum(filePath,'sha256',False)    
    except TypeError:
        print("File does not exist")
        return
    print("Hash of the given file: ",fileHash)
    index = designDb.functions.findDesign(fileHash).call()
    if (index==-1):
        print("Design with given hash does not exist in database")
        return 
    design = designDb.functions.getDesign(index).call()
    print("Designer:",design[0])
    print("Filename:",design[1])
    print("Version history \n=================================================================")
    print("Version:",design[3])
    print("Filehash:",design[2])
    print("Timestamp:",design[4])
    print("=================================================================")
    historyLen = designDb.functions.getHistoryLength(index).call()
    for i in range(historyLen):
        version = designDb.functions.getHistory(index,i).call()
        print("Version:",version[0])
        print("FileHash:",version[1])
        print("Timestamp:",version[2])
        print("=================================================================")
    
def update_design(w3):
    designDb = create_contract_object(w3)
    fileName = input("Enter filename: ")
    filesLength = designDb.functions.getFilesLength().call()
    index = -1
    designerAddress = w3.eth.accounts[0]
    design = []
    for i in range(filesLength):
        design = designDb.functions.getDesign(i).call()
        if(design[0] == designerAddress and design[1] == fileName):
            index = i
            break
    if (index == -1):
        print("No design file uploaded by you matches with the name given")
        return
    newFilePath = input("Enter new filepath: ")
    try:
        newFileHash = hs.fileChecksum(newFilePath,'sha256',False)
    except TypeError:
        print("File does not exist")
        return
    print("Hash of the given file: ",newFileHash)
    i = designDb.functions.findDesign(newFileHash).call()
    if(i != -1):
        print("Design not update(design with same hash exists)")
        return 
    version = input("Enter version: ")
    
    passphrase = getpass.getpass("Enter passphrase: ")
    w3.personal.unlockAccount(w3.eth.accounts[0], passphrase)

    try:
        tx_hash = designDb.functions.modifyDesign(index,newFileHash,version).transact()
    except ValueError:
        print("Design can only be updated by designer")
        return
    
    w3.miner.start(4)
    print("Waiting for transaction to be mined...")
    w3.eth.waitForTransactionReceipt(tx_hash)
    w3.miner.stop()
    print("Design updated successfully. TX Hash: ",Web3.toHex(tx_hash))
    design = designDb.functions.getDesign(index).call()

    
def kill(w3):
    designDb = create_contract_object(w3)
    passphrase = getpass.getpass("Enter passphrase: ")
    w3.personal.unlockAccount(w3.eth.accounts[0], passphrase)
    tx_hash = designDb.functions.kill().transact()

    w3.miner.start(4)
    w3.eth.waitForTransactionReceipt(tx_hash)
    w3.miner.stop()




