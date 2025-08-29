# Blockchain QA Testing Project

Comprehensive test cases for Ethereum blockchain interactions using pytest and Web3.py, specifically targeting the Cronos testnet. The project includes Jenkins automation integration, comprehensive Allure reporting, and PowerShell automation scripts.

## Project Overview

This project contains two main testing tasks:
1. **Basic Blockchain Query Tests**: Testing the `eth_getBalance` method with various scenarios
2. **Smart Contract Interaction Tests**: Testing deployed smart contracts with random number generation functionality

## Project Structure

```
Kevin-BlockChain-Automation/
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
├── pytest.ini                    # Pytest configuration file
├── conftest.py                   # Pytest fixtures and configuration
├── test_blockchain_queries.py    # Task 1: eth_getBalance tests
├── test_smart_contract.py        # Task 2: Smart contract tests
├── network_test.py               # Network connectivity tests
├── Jenkinsfile                   # Jenkins CI/CD pipeline configuration
├── SmokeTest.ps1                 # Local PowerShell automation script - Smoke tests
├── Regression.ps1                # Local PowerShell automation script - Regression tests
├── allure-results/               # Allure test results directory
└── allure-report/                # Generated HTML test reports
```

## Environment Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for Cronos testnet access)
- PowerShell (for running automation scripts)
- Jenkins (optional, for CI/CD)
- Allure CLI (optional, for automated report generation)

### Installation Steps

1. **Clone the project**
   ```bash
   git clone git@github.com:nightwish2016/Kevin-kong-automation-testing.git
   cd Kevin-BlockChain-Automation
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   This will install the following dependencies:
   - `pytest>=7.0.0` - Testing framework
   - `web3>=6.0.0` - Ethereum interaction library
   - `allure-pytest>=2.15.0` - Allure reporting support
   
3. **Install Allure CLI (optional)**
   ```bash
   # Using npm
   npm install -g allure-commandline --save-dev
   ```

### Network Configuration

Tests are configured to connect to:
- **Network**: Cronos Testnet
- **RPC URL**: https://evm-t3.cronos.org
- **Chain ID**: 338

Configurations are hardcoded in test fixtures, requiring no additional network setup.

## Running Tests

### Quick Start

#### Using PowerShell Automation Scripts
```powershell
# Run smoke tests
.\SmokeTest.ps1

# Run regression tests
.\Regression.ps1
```

#### Manual Test Execution

**Run all tests**
```bash
pytest
```

**Run specific test types**
```bash
# Smoke tests
pytest -m smoke

# Regression tests
pytest -m regression

# Blockchain query tests
pytest test_blockchain_queries.py

# Smart contract tests
pytest test_smart_contract.py
```

**Verbose output options**
```bash
# Verbose output
pytest -v

# Verbose output with print statements
pytest -v -s

# Generate Allure reports
pytest --alluredir=allure-results
```

## Allure Reporting

### Generate and View Reports
```bash
# Run tests and generate Allure results
pytest --alluredir=allure-results

# Generate HTML report
allure generate allure-results --clean -o allure-report

# Start report server
allure serve allure-results

# Generate specific test suite reports
pytest -m smoke --alluredir=allure-results-smoke
pytest -m regression --alluredir=allure-results-regression
```

### Report Features
- **Test Organization**: Epic, Features, Stories classification
- **Severity Levels**: BLOCKER, CRITICAL, HIGH, NORMAL, LOW
- **Tag Classification**: positive, negative, edge_case, etc.
- **Step Details**: Detailed test execution steps
- **Attachments**: Balance values, random numbers, error messages, etc.



## Test Case Documentation

Detailed test case descriptions are available in the following documents:

- **Blockchain Query Tests**:  https://github.com/nightwish2016/Kevin-BlockChain-Automation/blob/main/TC_Description/test_blockchain_queries_cases.md - Contains detailed explanations of all 13 blockchain query test cases

- **Smart Contract Tests**: https://github.com/nightwish2016/Kevin-BlockChain-Automation/blob/main/TC_Description/test_smart_contract_cases.md  - Contains detailed explanations of all 13 smart contract test cases

  

Each document provides:

- Test purpose and objectives
- Test steps and methodology
- Expected results and validation criteria
- Error handling strategies
- Allure reporting integration details

## Test Markers

The project uses pytest markers to organize tests:

- `smoke`: Smoke tests - Quick validation of critical functionality
- `regression`: Regression tests - Complete functional tests including edge cases
- `contract`: Smart contract interaction tests
- `blockchain`: Blockchain query tests
- `slow`: Tests with longer execution times

## Dependencies

- **pytest>=7.0.0**: Main testing framework providing test discovery, fixtures, and assertion handling
- **web3>=6.0.0**: Python library for interacting with Ethereum blockchain
- **allure-pytest>=2.15.0**: Allure reporting integration and visualization
- **requests>=2.25.0**: HTTP request library for network connectivity testing

## Jenkins Integration

### **Jenkins URL:**

  https://b34880277e39.ngrok-free.app/view/BlockChain/ (**host on my local laptop,The address will be changed once I restarted my laptop**)

### Jenkins Jobs and Build Parameters

![Jenkins Jobs](https://kevinbucket2020.oss-cn-hangzhou.aliyuncs.com/jenkinsScreenShot/jobs.png)

![Build Parameters](https://kevinbucket2020.oss-cn-hangzhou.aliyuncs.com/jenkinsScreenShot/parameters.png)

### Smoke Tests

![Smoke Test 1](https://kevinbucket2020.oss-cn-hangzhou.aliyuncs.com/jenkinsScreenShot/smoke/1.png)

![Smoke Test 2](https://kevinbucket2020.oss-cn-hangzhou.aliyuncs.com/jenkinsScreenShot/smoke/2.png)

![Smoke Test 3](https://kevinbucket2020.oss-cn-hangzhou.aliyuncs.com/jenkinsScreenShot/smoke/3.png)

![Smoke Test 4](https://kevinbucket2020.oss-cn-hangzhou.aliyuncs.com/jenkinsScreenShot/smoke/4.png)

### Regression Tests

![Regression Test 1](https://kevinbucket2020.oss-cn-hangzhou.aliyuncs.com/jenkinsScreenShot/regression/1.png)

![Regression Test 2](https://kevinbucket2020.oss-cn-hangzhou.aliyuncs.com/jenkinsScreenShot/regression/2.png)

![Regression Test 3](https://kevinbucket2020.oss-cn-hangzhou.aliyuncs.com/jenkinsScreenShot/regression/3.png)



