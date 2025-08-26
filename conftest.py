import pytest
from web3 import Web3
import json


@pytest.fixture(scope="session")
def web3_connection():
    """Create Web3 connection to Cronos testnet."""
    rpc_url = "https://evm-t3.cronos.org"
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    # Verify connection
    if not w3.is_connected():
        pytest.skip("Unable to connect to Cronos testnet")
    
    return w3


@pytest.fixture(scope="session")
def contract_abi():
    """Return smart contract ABI."""
    return [
        {
            "inputs": [],
            "name": "getRandomNumber",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getSeed",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]


@pytest.fixture(scope="session")
def smart_contract(web3_connection, contract_abi):
    """Create smart contract instance."""
    contract_address = "0x3906d433Cc3120C44F972E86A9D685803D2cd8AE"
    return web3_connection.eth.contract(
        address=Web3.to_checksum_address(contract_address),
        abi=contract_abi
    )


@pytest.fixture
def valid_addresses():
    """Return list of valid Ethereum addresses for testing."""
    return [
        "0x8aa72B46faEdFe2A5aa520790AE9C05C44599Dc6", #my metamask account with balance
        "0x0000000000000000000000000000000000000000",  # zero address
        "0x3906d433Cc3120C44F972E86A9D685803D2cd8AE",  # contract address
        "0x65FbA919dcD2E8338a30C0c8551110eD6dFcB95F"   # my another metamask account without balance
        
    ]


@pytest.fixture
def invalid_addresses():
    """Return list of invalid Ethereum addresses for testing."""
    return [
        "0x123",                                          # too short
        "0x3906d433Cc3120C44F972E86A9D685803D2cd8AG",    # invalid character 'G'
        "3906d433Cc3120C44F972E86A9D685803D2cd8AE",      # missing 0x prefix
        "0x3906d433Cc3120C44F972E86A9D685803D2cd8AEE",   # too long
        "",                                               # empty string
        "not_an_address",                                 # invalid format
        None                                              # None value
    ]