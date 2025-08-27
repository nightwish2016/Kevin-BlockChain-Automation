# Blockchain Queries Test Cases Documentation

## Overview

This document provides detailed explanations for all test cases in `test_blockchain_queries.py`. These tests validate the `eth_getBalance` method across various scenarios on the Cronos testnet, ensuring comprehensive coverage of normal operations, error conditions, and edge cases.

## Test Scope

- **Primary Function**: `eth_getBalance` method testing
- **Network**: Cronos Testnet (Chain ID: 338)
- **RPC Endpoint**: https://evm-t3.cronos.org
- **Focus Areas**: Balance retrieval, block parameters, error handling, edge cases

---

## Test Case Details

### 1. test_get_balance_valid_addresses
**Purpose**: Validates balance retrieval for legitimate Ethereum addresses  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Allure Classification**: Epic: Blockchain QA Testing, Feature: Balance Queries, Story: Valid Address Balance Retrieval  
**Severity**: CRITICAL  

**What it tests**:
- Balance retrieval for multiple valid Ethereum addresses
- Return type validation (should be integer in wei)
- Non-negative balance validation
- Error handling for unexpected exceptions

**Test Process**:
1. Iterates through a list of valid addresses from the fixture
2. Calls `get_balance()` for each address
3. Validates return type is integer (wei format)
4. Ensures balance is non-negative
5. Captures any unexpected errors for analysis

**Expected Results**:
- All valid addresses should return integer balance values
- Balances should be >= 0
- No unexpected exceptions should occur

---

### 2. test_get_balance_latest_block
**Purpose**: Tests balance retrieval using the 'latest' block parameter  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Allure Classification**: Story: Block Parameter Testing  
**Severity**: NORMAL  

**What it tests**:
- Balance retrieval with explicit 'latest' block parameter
- Consistency between 'latest' and default block parameters
- Proper handling of the 'latest' block identifier

**Test Steps**:
1. Get balance using 'latest' block parameter
2. Get balance using default parameter (no block specified)
3. Compare both results for consistency
4. Validate both return integer values >= 0

**Expected Results**:
- 'latest' block balance should equal default balance
- Both calls should return non-negative integers

---

### 3. test_get_balance_specific_block_number
**Purpose**: Validates balance retrieval from specific block numbers  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Balance retrieval using current block number
- Balance retrieval from historical blocks (current - 100)
- Proper handling of integer block identifiers

**Test Logic**:
1. Get current block number from the network
2. Retrieve balance using current block number
3. If current block > 100, test with an earlier block (current - 100)
4. Validate all returned balances are non-negative integers

**Expected Results**:
- Current block balance should be retrievable
- Historical block balance should be accessible (if block exists)
- All balances should be non-negative integers

---

### 4. test_get_balance_pending_block
**Purpose**: Tests balance retrieval using the 'pending' block parameter  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Balance retrieval from the pending block
- Proper handling of the 'pending' block identifier
- Network support for pending block queries

**Test Approach**:
1. Call `get_balance()` with 'pending' block parameter
2. Validate return type and value constraints
3. Ensure no exceptions occur during the call

**Expected Results**:
- Pending block balance should be retrievable
- Result should be a non-negative integer

---

### 5. test_get_balance_earliest_block
**Purpose**: Tests balance retrieval using the 'earliest' block parameter  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Balance retrieval from the earliest available block
- Network support for historical block access
- Proper handling of the 'earliest' block identifier

**Test Process**:
1. Call `get_balance()` with 'earliest' block parameter
2. Validate return format and constraints
3. Handle potential network limitations gracefully

**Expected Results**:
- Earliest block balance should be accessible
- Result should be a non-negative integer

---

### 6. test_get_balance_invalid_addresses
**Purpose**: Validates error handling for invalid address formats  
**Markers**: `@pytest.mark.regression`  
**Severity**: CRITICAL  

**What it tests**:
- Error responses for various invalid address formats
- Proper exception types for different error conditions
- Robustness of address validation

**Invalid Address Types Tested**:
- `None` values (should raise Web3TypeError)
- Invalid formats, lengths, characters
- Missing 0x prefix
- Invalid checksums

**Error Handling**:
- None addresses: Expects Web3TypeError
- Invalid formats: Expects InvalidAddress or ValueError
- All exceptions should contain relevant error messages

**Expected Results**:
- Each invalid address should raise appropriate exceptions
- Exception messages should be descriptive and relevant

---

### 7. test_get_balance_invalid_block_number
**Purpose**: Tests error handling for invalid block number parameters  
**Markers**: `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Response to negative block numbers
- Response to future/non-existent block numbers
- Proper exception handling for invalid block parameters

**Invalid Block Scenarios**:
1. Negative block number (-1)
2. Future block number (current + 1,000,000)

**Expected Results**:
- Negative blocks should raise ValueError, BlockNotFound, or Web3RPCError
- Future blocks should raise BlockNotFound or Web3RPCError
- All exceptions should be properly categorized

---

### 8. test_get_balance_invalid_block_string
**Purpose**: Validates error handling for invalid block string parameters  
**Markers**: `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Error responses for malformed block string identifiers
- Validation of hex string format requirements
- Robustness of block parameter parsing

**Invalid Block Strings Tested**:
- "invalid" - non-hex string
- "123abc" - invalid hex without prefix
- "0xg123" - invalid hex characters
- "" - empty string

**Expected Results**:
- All invalid strings should raise ValueError or Web3RPCError
- Error messages should indicate format/validation issues

---

### 9. test_get_balance_zero_address
**Purpose**: Tests balance retrieval for the zero address (boundary case)  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Balance retrieval for the zero address (0x0000...0000)
- Proper handling of this special address case
- Validation that it's treated as a valid address

**Test Details**:
- Uses the zero address: "0x0000000000000000000000000000000000000000"
- Validates return type and non-negative constraint
- Ensures no exceptions occur

**Expected Results**:
- Zero address should be treated as valid
- Should return non-negative integer balance

---

### 10. test_get_balance_return_format
**Purpose**: Validates the format and type of returned balance values  
**Markers**: `@pytest.mark.smoke`, `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Balance return type (should be integer, not hex string)
- Conversion to ether format for additional validation
- Proper handling of wei to ether conversion

**Format Validation**:
1. Confirms balance is returned as integer (wei)
2. Converts balance to ether using `from_wei()`
3. Validates ether conversion returns proper numeric type
4. Ensures converted ether value is positive

**Expected Results**:
- Balance should be integer type (wei)
- Ether conversion should produce positive numeric value
- Conversion result should be float or Decimal type

---

### 11. test_get_balance_multiple_calls_consistency
**Purpose**: Tests consistency across multiple balance queries  
**Markers**: `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Consistency of balance values across multiple calls
- Reliability of the balance retrieval mechanism
- Network stability and caching behavior

**Consistency Testing**:
1. Makes 3 consecutive calls to `get_balance()` for the same address
2. Compares all results to ensure they match
3. Validates that results remain consistent

**Expected Results**:
- All 3 calls should return identical balance values
- No variation should occur between rapid consecutive calls

---

### 12. test_get_balance_connection_error_handling
**Purpose**: Validates behavior during network connectivity issues  
**Markers**: `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Proper error handling when network issues occur
- Classification of connection-related exceptions
- Graceful degradation of service

**Error Classification**:
- Tests for connection-related error types
- Validates that errors are network-specific
- Ensures error messages are informative

**Expected Results**:
- Connection errors should be properly categorized
- Error types should indicate network/connectivity issues

---

### 13. test_get_balance_edge_case_block_parameters
**Purpose**: Tests edge cases for block parameter handling  
**Markers**: `@pytest.mark.regression`  
**Severity**: NORMAL  

**What it tests**:
- Balance retrieval from genesis block (block 0)
- Hexadecimal vs integer block number consistency
- Boundary conditions for block parameters

**Edge Case Scenarios**:
1. **Genesis Block**: Attempts balance retrieval from block 0
2. **Hex vs Int**: Compares balance using hex and integer block numbers

**Special Handling**:
- Genesis block test handles BlockNotFound exceptions gracefully
- Hex/integer comparison ensures format consistency

**Expected Results**:
- Genesis block access should work or fail gracefully
- Hex and integer block formats should return identical results

---

## Test Configuration

### Pytest Markers Used:
- `smoke`: Essential functionality tests
- `regression`: Comprehensive test coverage including edge cases
- `blockchain`: Blockchain query specific tests
- `network`: Tests requiring network connectivity

### Allure Integration:
- **Epic**: Blockchain QA Testing
- **Feature**: Balance Queries
- **Stories**: Organized by test categories (Valid Address Balance Retrieval, Block Parameter Testing, Error Handling, Edge Cases, etc.)
- **Severity Levels**: CRITICAL, NORMAL
- **Tags**: positive, negative, edge_case, validation, etc.

### Test Data Dependencies:
- `valid_addresses`: Fixture providing valid Ethereum addresses for testing
- `invalid_addresses`: Fixture providing various invalid address formats
- `web3_connection`: Web3 instance connected to Cronos testnet

### Network Requirements:
- Stable internet connection
- Access to Cronos testnet RPC endpoint
- Sufficient network stability for consistent results

## Error Handling Strategy

### Exception Categories:
1. **Address Validation Errors**:
   - `InvalidAddress`: Malformed address formats
   - `ValueError`: General validation failures
   - `Web3TypeError`: Type mismatch errors

2. **Block Parameter Errors**:
   - `BlockNotFound`: Non-existent or inaccessible blocks
   - `Web3RPCError`: RPC-level communication errors
   - `ValueError`: Invalid parameter formats

3. **Network Errors**:
   - Connection-related exceptions
   - Timeout errors
   - RPC endpoint unavailability

### Error Testing Approach:
- Uses `pytest.raises()` context managers for expected exceptions
- Validates exception types and error messages
- Provides detailed logging for debugging failed assertions

