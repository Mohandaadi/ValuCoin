// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract ValuCoin {
    address owner;

    struct Asset {
        uint id;
        string name;
        uint256 value;
        address currentOwner;
        bool exists;
    }

    mapping(uint => Asset) public assets;

    constructor() {
        owner = msg.sender;
    }

    function addAsset(uint _id, string memory _name, uint256 _value) public {
        require(msg.sender == owner, "Only the owner can add assets.");
        require(!assets[_id].exists, "Asset ID already exists.");
        Asset memory new_asset = Asset(_id, _name, _value, owner, false);
        assets[_id] = new_asset;
    }

    function transferAsset(uint _id, address _newOwner) public {
        require(assets[_id].exists, "Asset does not exist.");
        require(msg.sender == assets[_id].currentOwner, "Not the owner.");
        
        assets[_id].currentOwner = _newOwner;
    }

    function getAsset(uint _id) public view returns (string memory, uint256, address) {
        require(assets[_id].exists, "Asset does not exist.");
        Asset memory asset = assets[_id];
        return (asset.name, asset.value, asset.currentOwner);
    }
}