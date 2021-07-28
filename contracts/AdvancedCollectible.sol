pragma solidity 0.8.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";

interface KeeperCompatibleInterface {
    function checkUpkeep(bytes calldata checkData) external returns (bool upkeepNeeded, bytes memory performData);
    function performUpkeep(bytes calldata performData) external;
}

contract AdvancedCollectible is ERC721, VRFConsumerBase, KeeperCompatibleInterface {
    uint256 public tokenCounter;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    // add other things
    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event requestedCollectible(bytes32 indexed requestId); 
    LinkTokenInterface public linkToken;

    bytes32 internal keyHash;
    uint256 internal fee;
    address public backupWallet;
    uint256 public transferAmount;
    
    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash, uint256 _fee, address _backupWallet, uint256 _backupAmount)
    public 
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("Dogie", "DOG")
    {   
        linkToken = LinkTokenInterface(_LinkToken);
        tokenCounter = 0;
        keyHash = _keyhash;
        fee = _fee;
        backupWallet = _backupWallet;
        transferAmount = _backupAmount;
    }

    function createCollectible(string memory tokenURI) 
        public returns (bytes32){
            bytes32 requestId = requestRandomness(keyHash, fee);
            requestIdToSender[requestId] = msg.sender;
            requestIdToTokenURI[requestId] = tokenURI;
            emit requestedCollectible(requestId);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        address dogOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter;
        _safeMint(dogOwner, newItemId);
        Breed breed = Breed(randomNumber % 3); 
        tokenIdToBreed[newItemId] = breed;
        requestIdToTokenId[requestId] = newItemId;
        tokenCounter = tokenCounter + 1;
    }
    //2.000000000000000000
    function checkUpkeep(bytes calldata checkData) external override returns (bool upkeepNeeded, bytes memory performData) {
        upkeepNeeded = linkToken.balanceOf(address(this)) < 2000000000000000000;
        // We don't use the checkData in this example
        // checkData was defined when the Upkeep was registered
        performData = checkData;
    }

    function performUpkeep(bytes calldata performData) external override {
        linkToken.transferFrom(backupWallet, address(this), transferAmount);
        performData;
    }
     function doTransfer() public returns(uint256){
        linkToken.transferFrom(backupWallet, address(this), transferAmount);
    }
}
