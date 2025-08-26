import pytest
import allure
from web3 import Web3
from web3.exceptions import InvalidAddress, BlockNotFound, Web3TypeError, Web3RPCError


@allure.epic("Blockchain QA Testing")
@allure.feature("Balance Queries")
class TestCronosGetBalance:
    """Test cases for eth_getBalance method using web3.py."""

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Valid Address Balance Retrieval")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("positive", "balance", "valid_addresses")
    def test_get_balance_valid_addresses(self, web3_connection, valid_addresses):
        """Test balance retrieval for valid Ethereum addresses."""
        with allure.step("Validate balance retrieval for valid addresses"):
            for address in valid_addresses:
                with allure.step(f"Check address: {address}"):
                    try:
                        balance = web3_connection.eth.get_balance(address)
                        allure.attach(str(balance), f"Balance for address {address}: {balance} (wei)", allure.attachment_type.TEXT)
                        assert isinstance(balance, int), f"Balance should be integer (wei), got {type(balance)}"
                        assert balance >= 0, f"Balance should be non-negative, got {balance}"
                    except Exception as e:
                        allure.attach(str(e), "Error information", allure.attachment_type.TEXT)
                        pytest.fail(f"Unexpected error for valid address {address}: {str(e)}")

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Block Parameter Testing")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("positive", "block_params", "latest")
    def test_get_balance_latest_block(self, web3_connection, valid_addresses):
        """Test balance retrieval using 'latest' block parameter."""
        address = valid_addresses[0]
        with allure.step("Check balance using 'latest' block parameter"):
            balance_latest = web3_connection.eth.get_balance(address, 'latest')
            allure.attach(str(balance_latest), "Latest block balance (wei)", allure.attachment_type.TEXT)
        
        with allure.step("Check balance using default parameter"):
            balance_default = web3_connection.eth.get_balance(address)
            allure.attach(str(balance_default), "Default balance (wei)", allure.attachment_type.TEXT)
        
        assert isinstance(balance_latest, int), "Balance should be integer (wei)"
        assert balance_latest >= 0, "Balance should be non-negative"
        assert balance_latest == balance_default, "Latest block balance should match default balance"

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Block Parameter Testing")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("positive", "block_params", "specific_block")
    def test_get_balance_specific_block_number(self, web3_connection, valid_addresses):
        """Test balance retrieval from specific block numbers."""
        address = valid_addresses[0]
        
        # Get current block number
        current_block = web3_connection.eth.block_number
        
        # Test using current block
        balance_current = web3_connection.eth.get_balance(address, current_block)
        assert isinstance(balance_current, int), "Balance should be integer (wei)"
        assert balance_current >= 0, "Balance should be non-negative"
        
        # Test using earlier block (if available)
        if current_block > 100:
            earlier_block = current_block - 100
            balance_earlier = web3_connection.eth.get_balance(address, earlier_block)
            assert isinstance(balance_earlier, int), "Balance should be integer (wei)"
            assert balance_earlier >= 0, "Balance should be non-negative"

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Block Parameter Testing")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("positive", "block_params", "pending")
    def test_get_balance_pending_block(self, web3_connection, valid_addresses):
        """Test balance retrieval using 'pending' block parameter."""
        address = valid_addresses[0]
        balance_pending = web3_connection.eth.get_balance(address, 'pending')
        
        assert isinstance(balance_pending, int), "Balance should be integer (wei)"
        assert balance_pending >= 0, "Balance should be non-negative"

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Block Parameter Testing")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("positive", "block_params", "earliest")
    def test_get_balance_earliest_block(self, web3_connection, valid_addresses):
        """Test balance retrieval using 'earliest' block parameter."""
        address = valid_addresses[0]
        balance_earliest = web3_connection.eth.get_balance(address, 'earliest')
        
        assert isinstance(balance_earliest, int), "Balance should be integer (wei)"
        assert balance_earliest >= 0, "Balance should be non-negative"

    @pytest.mark.regression
    @allure.story("Error Handling")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("negative", "invalid_addresses", "error_handling")
    def test_get_balance_invalid_addresses(self, web3_connection, invalid_addresses):
        """Test error handling for invalid addresses."""
        for invalid_address in invalid_addresses:
            print(f"Testing invalid address: {invalid_address}")
            if invalid_address is None:             
                with pytest.raises(Web3TypeError, match=".*[Aa]ddress.*"):
                    web3_connection.eth.get_balance(invalid_address)              
            else:                
                with pytest.raises((InvalidAddress, ValueError), 
                                    match=".*[Ii]nvalid.*|.*address.*|.*checksum.*") as excinfo:
                    web3_connection.eth.get_balance(invalid_address)
                print(f"Exception type: {excinfo.type}")
                print(f"Exception value: {excinfo.value}")
                print(f"Exception message: {str(excinfo.value)}")

    @pytest.mark.regression
    @allure.story("Error Handling")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "invalid_block", "error_handling")
    def test_get_balance_invalid_block_number(self, web3_connection, valid_addresses):
        """Test error handling for invalid block numbers."""
        address = valid_addresses[0]
        
        # Test using negative block number
        with pytest.raises((ValueError, BlockNotFound, Web3RPCError)) as excinfo:
            web3_connection.eth.get_balance(address, -1)
        
        print(f"Exception type: {excinfo.type}")
        print(f"Exception value: {excinfo.value}")
        print(f"Exception message: {str(excinfo.value)}")    
        
        # Test using extremely large block number (future block)
        current_block = web3_connection.eth.block_number
        future_block = current_block + 1000000
        
        with pytest.raises((BlockNotFound, Web3RPCError)):
            web3_connection.eth.get_balance(address, future_block)
      

    @pytest.mark.regression
    @allure.story("Error Handling")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "invalid_block_string", "error_handling")
    def test_get_balance_invalid_block_string(self, web3_connection, valid_addresses):
        """Test error handling for invalid block string parameters."""
        address = valid_addresses[0]
        
        invalid_block_strings = ["invalid", "123abc", "0xg123", ""]
        
        for invalid_block in invalid_block_strings:
            with pytest.raises((ValueError, Web3RPCError), match=".*invalid.*|.*hex string.*|.*prefix.*") as excinfo:
                web3_connection.eth.get_balance(address, invalid_block)
            print(f"Testing block: {invalid_block}")
            print(f"Exception type: {excinfo.type}")
            print(f"Exception value: {excinfo.value}")
            print(f"Exception message: {str(excinfo.value)}") 
            # try:
            #     web3_connection.eth.get_balance(address, invalid_block)
            # except Exception as e:
            #     print(f"Exception type: {type(e).__name__}")
            #     print(f"Exception value: {e}")
            #     print(f"Exception message: {str(e)}")

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Edge Cases")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("edge_case", "zero_address", "boundary")
    def test_get_balance_zero_address(self, web3_connection):
        """Test balance retrieval for zero address (boundary case)."""
        zero_address = "0x0000000000000000000000000000000000000000"
        balance = web3_connection.eth.get_balance(zero_address)
        
        assert isinstance(balance, int), "Balance should be integer (wei)"
        assert balance >= 0, "Balance should be non-negative"

   

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Data Format Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("validation", "data_format", "wei")
    def test_get_balance_return_format(self, web3_connection, valid_addresses):
        """Test that balance is returned in correct format (wei as integer)."""
        address = valid_addresses[0]
        balance = web3_connection.eth.get_balance(address)
        
        # Balance should be returned as integer (wei), not hex string
        assert isinstance(balance, int), f"Balance should be integer, got {type(balance)}"
        assert balance >= 0, "Balance should be non-negative"
        
        # Convert to ether for additional validation
        balance_ether = web3_connection.from_wei(balance, 'ether')
        print(f"ETH balance for address {address}: {balance_ether}")
        assert balance_ether > 0, "Ether balance should be positive"
        # from_wei method returns decimal.Decimal type
        from decimal import Decimal
        assert isinstance(balance_ether, ( float, Decimal)), \
            f"Ether balance should be numeric, got {type(balance_ether)}"

    @pytest.mark.regression
    @allure.story("Consistency Testing")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("consistency", "multiple_calls", "reliability")
    def test_get_balance_multiple_calls_consistency(self, web3_connection, valid_addresses):
        """Test multiple calls to get_balance return consistent results."""
        address = valid_addresses[0]
        
        # Make multiple calls and ensure consistency
        balances = []
        for _ in range(3):
            balance = web3_connection.eth.get_balance(address)
            balances.append(balance)
        
        # All balances should be the same (assuming no transactions during the period)
        assert all(b == balances[0] for b in balances), \
            f"Multiple balance calls should return consistent results: {balances}"

    @pytest.mark.regression
    @allure.story("Network Testing")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("network", "connection", "error_handling")
    def test_get_balance_connection_error_handling(self, web3_connection, valid_addresses):
        """Test behavior when connection issues occur."""
        address = valid_addresses[0]
        
        # This test validates whether the connection is working properly
        # In real scenarios, you might simulate connection failures
        try:
            balance = web3_connection.eth.get_balance(address)
            assert isinstance(balance, int), "Balance should be integer when connection works properly"
        except Exception as e:
            # If connection fails, ensure it's a reasonable exception
            assert any(error_type in str(type(e)).lower() 
                      for error_type in ['connection', 'timeout', 'http', 'network']), \
                f"Connection error should be network-related, got: {type(e).__name__}: {str(e)}"

    @pytest.mark.regression
    @allure.story("Edge Cases")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("edge_case", "block_params", "boundary", "hex_conversion")
    def test_get_balance_edge_case_block_parameters(self, web3_connection, valid_addresses):
        """Test edge cases for block parameters."""
        address = valid_addresses[0]
        
        # Test using block number 0 (genesis block)
        try:
            balance_genesis = web3_connection.eth.get_balance(address, 0)
            assert isinstance(balance_genesis, int), "Balance should be integer"
            assert balance_genesis >= 0, "Balance should be non-negative"
        except BlockNotFound:
            # Some networks may not have access to block 0
            pass
        
        # Test using hexadecimal block number
        current_block = web3_connection.eth.block_number
        hex_block = hex(current_block)
        balance_hex = web3_connection.eth.get_balance(address, hex_block)
        balance_int = web3_connection.eth.get_balance(address, current_block)
        
        assert balance_hex == balance_int, \
            "Hexadecimal and integer block numbers should return the same balance"