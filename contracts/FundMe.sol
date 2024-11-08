// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";
contract FundMe {
    //Mappear todas las transacciones fund
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }
    function fund() public payable {
        uint256 MinimunUsd = 0.02 * 10 ** 18;
        require(
            getConversionRate(msg.value) >= MinimunUsd,
            "You need to spend more eth!"
        );
        addressToAmountFunded[msg.sender] = msg.value;
        funders.push(msg.sender);
    }
    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10 ** 10);
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimunUSD = 10 * (10 * 18);
        uint256 price = getPrice();
        uint256 precision = 1 * (10 * 18);
        return ((minimunUSD * precision) / price) + 1;
    }

    function getConversionRate(
        uint256 ethAmount
    ) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / (10 ** 18);
        return ethAmountInUsd;
    }
    //50.539000000000000000

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
    function withdraw() public payable onlyOwner {
        require(address(this).balance > 0, "No hay dinero en este contrato");
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 funderIndex; funderIndex < funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
