pragma solidity >=0.4.22 < 0.5.0;

contract Design_Friendly_Agreement {
    
    address public designer;
    address public printer;

    uint public QUANTITY;
    uint public TEST_QUANTITY;
    uint public PASS_QUANTITY;
    uint public CONTRACT_AMOUNT;

    // the number of items yet ot be printed
    uint public quantity_remaining;
    
    // the number of items testted by designer
    uint public quantity_tested;

    // the number of items that have passed the quality test
    uint public quantity_passed;

    struct Product {
        string id;
        uint time;
    }

    struct Tested_Product {
        string id;
        uint time;
        bool approved;
    }

    Product[] public products;
    Tested_Product[] public tested_products;

    constructor (uint _quantity, uint _test_quantity, uint _pass_quantity, uint _contract_amount) public {

        // No sanity checks are done here.
        // The client is expected to do that
        
        designer = msg.sender;
        QUANTITY = _quantity;
        TEST_QUANTITY = _test_quantity;
        PASS_QUANTITY = _pass_quantity;
        CONTRACT_AMOUNT = _contract_amount;
        quantity_remaining = _quantity;
    }

    // Function modifier to allow only designer to call certain functions
    modifier designeronly() {require(msg.sender == designer, "Only creator is authorized to do this operation"); _;}

    // Function modifier to allow only designer to call certain functions
    modifier printeronly() {require(msg.sender == printer, "Only printer is authorized to do this operation"); _;}

    function () public payable {
        // Fallback function to suuport recieving ether
        require(msg.data.length == 0, "Invalid function call"); // to prevent invalid function calls       
    }

    // Functino to view balance of the contract
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    // Function to register printer
    function registerPrinter() public {
        require(printer == 0x0, "This agreement already has a printer");
        require(address(this).balance >= CONTRACT_AMOUNT, "Insufficient balance in contract account");
        
        printer = msg.sender;
    }

    function recordPrint (string designid) public printeronly {
        require(quantity_remaining > 0, "No more copies can be authenticated");
        require(msg.sender == printer, "Not authorized to print");

        quantity_remaining--;

        products.push(Product({id:designid, time:block.timestamp}));
    }

    // Function to approve/fail product at a specific index in products
    // Note: Bound checks are not done here, the client is expected to do that
    function testProduct (uint index, bool approved) public designeronly {
        require(quantity_remaining == 0, "Testing can start only after all items are printed");
        require(quantity_tested < TEST_QUANTITY, "Test quantity has exceeded");

        quantity_tested++;
        if(approved) 
            quantity_passed++;

        tested_products.push(Tested_Product({
            id: products[index].id,
            time: products[index].time,
            approved: approved
        }));

        for (uint i = index; i < products.length - 1; i++) {
            products[i] = products[i+1];
        }

        delete products[products.length - 1];
        products.length--;

        if(quantity_passed == PASS_QUANTITY)
            printer.transfer(CONTRACT_AMOUNT);
    
    }
}