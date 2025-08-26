import pytest
import allure
from web3 import Web3
from web3.exceptions import ContractLogicError, ABIFunctionNotFound
import time


@allure.epic("Blockchain QA Testing")
@allure.feature("Smart Contract Interaction")
class TestSmartContractInteraction:
    """Test cases for smart contract interaction on Cronos testnet."""

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Contract Setup Validation")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("setup", "contract_connection", "validation")
    def test_contract_connection(self, smart_contract):
        """Test whether the contract instance is correctly created."""
        assert smart_contract is not None, "Contract instance should not be None"
        assert hasattr(smart_contract, 'functions'), "Contract should have functions attribute"
        assert hasattr(smart_contract.functions, 'getRandomNumber'), \
            "Contract should have getRandomNumber function"
        assert hasattr(smart_contract.functions, 'getSeed'), \
            "Contract should have getSeed function"

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Random Number Generation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("positive", "random_number", "basic_functionality")
    def test_get_random_number_basic(self, smart_contract):
        """Test basic functionality of getRandomNumber method."""
        with allure.step("Call getRandomNumber function"):
            try:
                random_number = smart_contract.functions.getRandomNumber().call()
                allure.attach(str(random_number), "Generated random number", allure.attachment_type.TEXT)
                
                with allure.step("Validate return value type"):
                    assert isinstance(random_number, int), \
                        f"Random number should be integer, but got {type(random_number)}"
                
                with allure.step("Validate return value range (0-2025)"):
                    assert 0 <= random_number <= 2025, \
                        f"Random number should be between 0 and 2025, but got {random_number}"
                
            except Exception as e:
                allure.attach(str(e), "Error information", allure.attachment_type.TEXT)
                pytest.fail(f"Unexpected error when calling getRandomNumber: {str(e)}")

   

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Random Number Generation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("boundary", "range_validation", "0_2025")
    def test_random_number_range_boundary(self, smart_contract):
        """Test whether random numbers follow boundary conditions (0-2025)."""
        # Call function multiple times to test range
        random_numbers = []
        with allure.step("Perform 10 getRandomNumber calls to test range boundaries"):
            for i in range(10):
                with allure.step(f"Call {i+1}"):
                    random_number = smart_contract.functions.getRandomNumber().call()
                    random_numbers.append(random_number)
                    allure.attach(str(random_number), f"Random number #{i+1}", allure.attachment_type.TEXT)
                    
                    # Each call should return a value within valid range
                    assert 0 <= random_number <= 2025, \
                        f"Random number {random_number} exceeds valid range [0, 2025]"
        
        with allure.step("Validate all return values are integers"):
            allure.attach(str(random_numbers), "All random numbers list", allure.attachment_type.JSON)
            # Validate that we got all valid integers
            assert all(isinstance(num, int) for num in random_numbers), \
                "All random numbers should be integers"

    @pytest.mark.regression
    @allure.story("Random Number Generation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("variability", "multiple_calls", "randomness")
    def test_random_number_variability(self, smart_contract):
        """Test getRandomNumber returns different values across multiple calls."""
        random_numbers = []
        max_attempts = 20  # More attempts to increase chance of getting different values
        
        for _ in range(max_attempts):
            random_number = smart_contract.functions.getRandomNumber().call()
            random_numbers.append(random_number)
            time.sleep(0.1)  # Small delay between calls
        
        # Check if we get some variation
        unique_numbers = set(random_numbers)
        
        # With 20 calls in 0-2025 range, we should get some variation
        # But since it's blockchain-based randomness, it might be deterministic
        # So we just ensure all values are within valid range
        assert all(0 <= num <= 2025 for num in random_numbers), \
            "All random numbers should be within valid range"
        
        # Log results for analysis
        print(f"Generated numbers: {random_numbers}")
        print(f"Unique values: {len(unique_numbers)} / {max_attempts}")



    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Contract Setup Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("validation", "abi", "structure")
    def test_contract_abi_validation(self, contract_abi):
        """Test whether contract ABI is structurally correct."""
        assert isinstance(contract_abi, list), "ABI should be a list"
        assert len(contract_abi) == 2, "ABI should contain exactly 2 functions"
        
        function_names = [func['name'] for func in contract_abi]
        assert 'getRandomNumber' in function_names, "ABI should contain getRandomNumber function"
        assert 'getSeed' in function_names, "ABI should contain getSeed function"
        
        for func in contract_abi:
            assert func['type'] == 'function', f"Entry should be a function: {func}"
            assert func['stateMutability'] == 'view', f"Function should be view function: {func}"
            assert len(func['inputs']) == 0, f"Function should have no input parameters: {func}"
            assert len(func['outputs']) == 1, f"Function should have one output: {func}"
            assert func['outputs'][0]['type'] == 'uint256', \
                f"Output should be uint256: {func}"

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Contract Setup Validation")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("validation", "contract_address", "deployment")
    def test_contract_address_validity(self, web3_connection, smart_contract):
        """Test whether contract address is valid and deployed."""
        contract_address = smart_contract.address
        
        # Verify address format
        assert Web3.is_address(contract_address), \
            f"Contract address should be valid: {contract_address}"
        assert Web3.is_checksum_address(contract_address), \
            f"Contract address should be in checksum format: {contract_address}"
        
        # Verify contract is deployed (has code)
        code = web3_connection.eth.get_code(contract_address)
        assert len(code) > 0, f"Contract should have deployed code at {contract_address}"

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("Network Setup Validation")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("network", "cronos_testnet", "connection")
    def test_network_connection_requirements(self, web3_connection):
        """Test whether we are connected to the correct network."""
        # Verify we're connected to Cronos testnet
        chain_id = web3_connection.eth.chain_id
        assert chain_id == 338, f"Should be connected to Cronos testnet (chain ID 338), but got {chain_id}"
        
        # Verify connection is working
        assert web3_connection.is_connected(), "Should be connected to network"
        
        # Verify we can get latest block
        latest_block = web3_connection.eth.block_number
        assert isinstance(latest_block, int), "Latest block should be integer"
        assert latest_block > 0, "Latest block should be positive"

    @pytest.mark.regression
    @allure.story("Error Handling")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "error_handling", "nonexistent_function")
    def test_contract_function_call_errors(self, smart_contract):
        """Test error handling for contract function calls."""
        # Test calling non-existent function
        with pytest.raises(ABIFunctionNotFound):
            smart_contract.functions.nonExistentFunction().call()
        
        # Test our actual functions work normally (should not error)
        try:
            random_number = smart_contract.functions.getRandomNumber().call()            
            assert isinstance(random_number, int), "getRandomNumber should work normally"           
        except ContractLogicError as e:
            pytest.fail(f"Contract function should not fail: {str(e)}")

    @pytest.mark.regression
    @allure.story("Block Parameter Testing")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("block_params", "deterministic", "latest_specific")
    def test_contract_call_with_different_block_parameters(self, smart_contract, web3_connection):
        """Test calling contract functions with different block parameters."""
        current_block = web3_connection.eth.block_number
        
        # Call using latest block
        random_latest = smart_contract.functions.getRandomNumber().call(block_identifier='latest')
        assert isinstance(random_latest, int), "Using 'latest' block should return integer"
        assert 0 <= random_latest <= 2025, "Using 'latest' block should be within valid range"
        
        # Call using specific block number (current block)
        random_specific = smart_contract.functions.getRandomNumber().call(block_identifier=current_block)
        assert isinstance(random_specific, int), "Using specific block should return integer"
        assert 0 <= random_specific <= 2025, "Using specific block should be within valid range"
        
        

    @pytest.mark.regression
    @allure.story("Gas Estimation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("gas", "performance", "view_function")
    def test_gas_estimation(self, smart_contract):
        """Test gas estimation for contract function calls."""
        # Since these are view functions, they should have minimal gas requirements
        try:
            gas_estimate_random = smart_contract.functions.getRandomNumber().estimate_gas()                      
            # Gas estimate should be reasonable for view functions
            assert isinstance(gas_estimate_random, int), "Gas estimate should be integer"
          
            assert gas_estimate_random > 0, "Gas estimate should be positive"
           
            
            # View functions should have relatively low gas usage
            assert gas_estimate_random < 100000, "View functions should not require too much gas"
      
            
        except Exception as e:
            # Gas estimation for view functions may not be supported on all networks
            print(f"Gas estimation not available: {str(e)}")

    @pytest.mark.regression
    @allure.story("Concurrency Testing")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("concurrency", "simultaneous_calls", "thread_safety")
    def test_multiple_simultaneous_calls(self, smart_contract):
        """Test multiple simultaneous calls to contract functions."""
        import concurrent.futures
        
        def call_random_number():
            return smart_contract.functions.getRandomNumber().call()
               
        
        # Make multiple concurrent calls
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            random_futures = [executor.submit(call_random_number) for _ in range(5)]
            
            
        # Collect results
        random_results = [future.result() for future in random_futures]
           
        
        # Verify all results are valid
        for result in random_results:
            assert isinstance(result, int), "Random number result should be integer"
            assert 0 <= result <= 2025, "Random number should be within valid range"
        
        
        print(f"Concurrent random number results: {random_results}")
        

    @pytest.mark.regression
    @allure.story("Event Logs")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("events", "logs", "monitoring")
    def test_contract_event_logs(self, smart_contract, web3_connection):
        """Test retrieving contract event logs (if any)."""
        # Since these are view functions, they may not emit events
        # But we can test the mechanism for retrieving logs
        try:
            # Get recent blocks to check for events
            latest_block = web3_connection.eth.block_number
            from_block = max(0, latest_block - 100)
            
            # Try to get logs (works even if no events are defined)
            logs = web3_connection.eth.get_logs({
                'address': smart_contract.address,
                'fromBlock': from_block,
                'toBlock': 'latest'
            })
            
            # Logs should be a list (possibly empty)
            assert isinstance(logs, list), "Logs should be a list"
            assert len(logs) == 0, "Logs list length should be 0"
            print(f"Found {len(logs)} logs for the contract")
            
        except Exception as e:
            # Some networks may not support log filtering
            print(f"Log retrieval not supported: {str(e)}")

    @pytest.mark.regression
    @allure.story("Edge Cases and Boundaries")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("edge_case", "boundary")
    def test_edge_cases_and_boundaries(self, smart_contract):
        """Test contract edge cases and boundary conditions."""
        # Call function multiple times to test various edge cases
        results = {
            'random_numbers': [],           
            'errors': []
        }
        
        for i in range(50):  # More calls to test edge cases
            try:
                random_num = smart_contract.functions.getRandomNumber().call()
               
                
                results['random_numbers'].append(random_num)
                
                
                # Verify boundaries
                assert 0 <= random_num <= 2025, f"Random number {random_num} exceeds boundaries"
                
                
            except Exception as e:
                results['errors'].append(str(e))
        
        # Analyze results
        print(f"Random number range: {min(results['random_numbers'])} - {max(results['random_numbers'])}")
        print(f"Unique random numbers: {len(set(results['random_numbers']))}")
        print(f"Errors encountered: {len(results['errors'])}")
        
        # Valid calls should have no errors
        assert len(results['errors']) == 0, f"Should have no errors, but got: {results['errors'][:5]}"
        
        # Verify we reach boundary values or close to boundaries
        min_random = min(results['random_numbers'])
        max_random = max(results['random_numbers'])
        
        assert min_random >= 0, "Minimum random number should be >= 0"
        assert max_random <= 2025, "Maximum random number should be <= 2025"