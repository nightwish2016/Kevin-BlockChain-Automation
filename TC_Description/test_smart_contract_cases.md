# Smart Contract Test Cases Documentation

## Overview

This document provides detailed explanations for all test cases in `test_smart_contract.py`. These tests validate smart contract interactions on the Cronos testnet, focusing on a deployed random number generator contract.

## Contract Information

- **Contract Address**: `0x3906d433Cc3120C44F972E86A9D685803D2cd8AE`
- **Network**: Cronos Testnet (Chain ID: 338)
- **Functions**: `getRandomNumber()`, `getSeed()`
- **Purpose**: Generates random numbers in the range 0-2025

---

## Test Case Details

### 1. test_contract_connection
**Purpose**: Validates basic contract setup and connection  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Allure Classification**: Epic: Blockchain QA Testing, Feature: Smart Contract Interaction, Story: Contract Setup Validation  
**Severity**: BLOCKER  

**What it tests**:
- Verifies the contract instance is properly created
- Ensures the contract has the expected `functions` attribute
- Confirms both `getRandomNumber` and `getSeed` functions are available
- Validates basic contract accessibility

**Expected Results**:
- Contract instance should not be None
- Contract should have proper function interfaces
- Both required functions should be discoverable

---

### 2. test_get_random_number_basic
**Purpose**: Tests fundamental functionality of the random number generation  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Allure Classification**: Story: Random Number Generation  
**Severity**: CRITICAL  

**What it tests**:
- Calls the `getRandomNumber()` function successfully
- Validates the return type is an integer
- Confirms the returned value is within the valid range (0-2025)
- Ensures no unexpected exceptions occur

**Test Steps**:
1. Call `getRandomNumber()` function
2. Validate return value type (should be int)
3. Validate return value range (0 ≤ value ≤ 2025)

**Expected Results**:
- Function call executes without errors
- Returns an integer value
- Value falls within the specified range

---

### 3. test_random_number_range_boundary
**Purpose**: Validates boundary conditions and range consistency  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Severity**: CRITICAL  

**What it tests**:
- Performs multiple calls (10 iterations) to test range consistency
- Validates each individual call meets boundary requirements
- Ensures all returned values are integers
- Tests the reliability of the range validation

**Test Steps**:
1. Execute 10 sequential calls to `getRandomNumber()`
2. Validate each result individually
3. Collect all results for batch validation
4. Confirm all values are integers and within range

**Expected Results**:
- All 10 calls should succeed
- Every returned value should be 0 ≤ value ≤ 2025
- All values should be integer type

---

### 4. test_random_number_variability
**Purpose**: Tests the randomness and variability of generated numbers  
**Markers**: `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Makes 20 function calls to test for value variation
- Includes small delays between calls to allow for potential state changes
- Analyzes the uniqueness of generated values
- Validates that all values remain within the valid range

**Test Approach**:
- Uses 20 calls to increase chances of getting different values
- Implements 0.1-second delays between calls
- Logs results for manual analysis
- Focuses on range validation rather than strict randomness requirements

**Expected Results**:
- All 20 values should be within the valid range
- Results are logged for variability analysis
- No exceptions should occur during execution

---

### 5. test_contract_abi_validation
**Purpose**: Validates the structure and correctness of the contract's ABI  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Verifies ABI is properly formatted as a list
- Confirms exactly 2 functions are defined in the ABI
- Validates both required functions (`getRandomNumber`, `getSeed`) are present
- Checks function properties (type, state mutability, inputs/outputs)

**Validation Checks**:
- ABI structure is a list containing exactly 2 functions
- Both functions are of type 'function'
- Both functions have 'view' state mutability
- Functions have no input parameters
- Functions return exactly one uint256 output

**Expected Results**:
- ABI contains exactly the expected function definitions
- All function properties match the expected specification

---

### 6. test_contract_address_validity
**Purpose**: Validates contract address format and deployment status  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Severity**: BLOCKER  

**What it tests**:
- Verifies the contract address is a valid Ethereum address
- Confirms the address is in proper checksum format
- Validates that the contract is actually deployed (has bytecode)

**Validation Steps**:
1. Check address validity using Web3.is_address()
2. Verify checksum format using Web3.is_checksum_address()
3. Retrieve contract bytecode to confirm deployment
4. Ensure bytecode length > 0 (indicating deployed contract)

**Expected Results**:
- Address passes Web3 validation checks
- Contract has deployed bytecode at the specified address

---

### 7. test_network_connection_requirements
**Purpose**: Validates connection to the correct blockchain network  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Severity**: BLOCKER  

**What it tests**:
- Confirms connection to Cronos testnet (Chain ID 338)
- Validates Web3 connection is active
- Ensures the latest block information is accessible

**Network Validation**:
- Chain ID must be exactly 338 (Cronos testnet)
- Web3 connection status should be active
- Latest block number should be retrievable and positive

**Expected Results**:
- Connected to the correct network
- Active connection with block access

---

### 8. test_contract_function_call_errors
**Purpose**: Tests error handling for contract function calls  
**Markers**: `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Verifies that calling non-existent functions raises appropriate exceptions
- Confirms that valid function calls work normally
- Tests the robustness of error handling mechanisms

**Error Scenarios**:
1. Call non-existent function (should raise ABIFunctionNotFound)
2. Call valid functions (should succeed without errors)

**Expected Results**:
- Non-existent function calls raise ABIFunctionNotFound
- Valid function calls execute successfully

---

### 9. test_contract_call_with_different_block_parameters
**Purpose**: Tests contract calls using different block parameters  
**Markers**: `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Calls contract functions with 'latest' block parameter
- Calls contract functions with specific block numbers
- Validates results are consistent and within expected range

**Block Parameter Testing**:
- Uses 'latest' block identifier
- Uses current block number as specific identifier
- Compares results for consistency

**Expected Results**:
- Both call types should succeed
- Results should be valid integers within range 0-2025

---

### 10. test_gas_estimation
**Purpose**: Tests gas estimation for contract function calls  
**Markers**: `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Estimates gas usage for contract function calls
- Validates that view functions have reasonable gas estimates
- Handles cases where gas estimation may not be supported

**Gas Validation**:
- Gas estimates should be positive integers
- View functions should have relatively low gas requirements (< 100,000)
- Handles network-specific limitations gracefully

**Expected Results**:
- Gas estimates are reasonable for view functions
- No critical errors during estimation

---

### 11. test_multiple_simultaneous_calls
**Purpose**: Tests concurrent contract function calls  
**Markers**: `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Makes 5 simultaneous calls using ThreadPoolExecutor
- Validates that all concurrent calls succeed
- Ensures thread safety of contract interactions

**Concurrency Testing**:
- Uses 5 worker threads for simultaneous execution
- Collects and validates all results
- Tests contract behavior under concurrent load

**Expected Results**:
- All 5 concurrent calls should succeed
- All results should be valid integers within range

---

### 12. test_contract_event_logs
**Purpose**: Tests contract event log retrieval capabilities  
**Markers**: `@pytest.mark.regression`  
**Severity**: MINOR  

**What it tests**:
- Attempts to retrieve contract event logs from recent blocks
- Validates log retrieval mechanism functionality
- Handles cases where events may not be present or supported

**Log Testing Approach**:
- Searches the last 100 blocks for contract events
- Expects empty logs for view functions
- Validates log retrieval infrastructure

**Expected Results**:
- Log retrieval mechanism works (even if no events found)
- No critical errors during log queries

---

### 13. test_edge_cases_and_boundaries
**Purpose**: Comprehensive edge case and boundary testing  
**Markers**: `@pytest.mark.regression`  
**Severity**: CRITICAL  

**What it tests**:
- Performs 50 function calls to test various edge cases
- Analyzes result distribution and boundary adherence
- Validates consistent behavior across many calls

**Edge Case Analysis**:
- 50 calls to increase chance of hitting edge cases
- Range validation for all results
- Statistical analysis of returned values
- Error tracking and reporting

**Expected Results**:
- No errors across all 50 calls
- All values within the valid range 0-2025
- Consistent function behavior

---

## Test Configuration

### Pytest Markers Used:
- `smoke`: Critical functionality tests that must pass
- `regression`: Comprehensive tests including edge cases
- `contract`: Smart contract specific tests
- `network`: Tests requiring network connectivity

### Allure Integration:
- **Epic**: Blockchain QA Testing
- **Feature**: Smart Contract Interaction
- **Stories**: Organized by functionality areas
- **Severity Levels**: BLOCKER, CRITICAL, NORMAL, MINOR
- **Tags**: Categorize test types (positive, negative, edge_case, etc.)

### Dependencies:
- Web3.py for blockchain interactions
- Contract ABI for function definitions
- Active connection to Cronos testnet
- Deployed contract at specified address

