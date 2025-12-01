// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VoucherVerifier {
    struct Voucher {
        string brand;
        uint256 value;
        bool isActive;
        bool exists;
    }

    mapping(bytes32 => Voucher) public vouchers;
    address public owner;

    event VoucherAdded(bytes32 indexed codeHash, string brand, uint256 value);
    event VoucherRedeemed(bytes32 indexed codeHash, address indexed redeemer);

    constructor() {
        owner = msg.sender;
        // Initialize with some demo data (hashes of demo codes)
        // In a real app, these would be added via addVoucher
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    function addVoucher(string memory code, string memory brand, uint256 value) public onlyOwner {
        bytes32 codeHash = keccak256(abi.encodePacked(code));
        require(!vouchers[codeHash].exists, "Voucher already exists");
        
        vouchers[codeHash] = Voucher({
            brand: brand,
            value: value,
            isActive: true,
            exists: true
        });
        
        emit VoucherAdded(codeHash, brand, value);
    }

    function getVoucherDetails(string memory code) public view returns (string memory brand, uint256 value, bool isActive) {
        bytes32 codeHash = keccak256(abi.encodePacked(code));
        require(vouchers[codeHash].exists, "Voucher does not exist");
        Voucher memory v = vouchers[codeHash];
        return (v.brand, v.value, v.isActive);
    }

    function redeemVoucher(string memory code) external returns (uint256) {
        bytes32 codeHash = keccak256(abi.encodePacked(code));
        require(vouchers[codeHash].exists, "Voucher does not exist");
        require(vouchers[codeHash].isActive, "Voucher already redeemed");

        vouchers[codeHash].isActive = false;
        emit VoucherRedeemed(codeHash, msg.sender);
        
        return vouchers[codeHash].value;
    }
}
