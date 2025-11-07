// © 2025 Jonathan Huynh. All Rights Reserved.
pragma solidity ^0.8.20;

contract StockToken {
    string public name;
    string public symbol;
    uint8 public decimals = 2;
    uint256 public totalSupply;
    address public owner;
    uint256 public stockPrice;

    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event PriceUpdated(uint256 newPrice, uint256 timestamp);

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    constructor(string memory _name, string memory _symbol, uint256 _supply) {
        name = _name;
        symbol = _symbol;
        totalSupply = _supply * 10 ** uint256(decimals);
        owner = msg.sender;
        balanceOf[msg.sender] = totalSupply;
    }

    function transfer(address _to, uint256 _value) public returns (bool) {
        require(balanceOf[msg.sender] >= _value);
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function updatePrice(uint256 _newPrice) public onlyOwner {
        stockPrice = _newPrice;
        emit PriceUpdated(_newPrice, block.timestamp);
    }

    function getValuation(address holder) public view returns (uint256) {
        return (balanceOf[holder] * stockPrice) / (10 ** uint256(decimals));
    }
}
