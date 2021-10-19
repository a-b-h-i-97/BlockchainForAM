pragma solidity >=0.4.22 < 0.6.0;

contract Print_Friendly_Agreement {

    address public designer;
    address public printer;

    uint public QUANTITY;
    uint public quantityRemaining;
    uint public amount;
    Product[] public products;

    struct Product {
        string id;
        uint time;
    }

    constructor (uint _QUANTITY, uint _amount) public {
        designer = msg.sender;
        QUANTITY = _QUANTITY;
        quantityRemaining = _QUANTITY;
        amount = _amount;
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    // This function is called when a printer registers
    function () public payable {
        require(printer == 0x0, "This agreement already has a printer");
        require(msg.value >= amount, "Cannot credit an amount less than agreed upon amount");
        printer = msg.sender;
    }

    function recordPrint(string designid) public {
        require(quantityRemaining > 0, "No more copies can be authenticated");
        require(msg.sender == printer, "Not authorized to print");

        quantityRemaining--;

        products[products.length++] = Product({id:designid, time:block.timestamp});
        if (quantityRemaining==0) {
            designer.transfer(amount);
        }
    }
}