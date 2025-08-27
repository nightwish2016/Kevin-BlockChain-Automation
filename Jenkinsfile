pipeline {
    agent any
	
    parameters {
        choice(
            name: 'TEST_TYPE',
            choices: ['smoke', 'regression', 'all'],
            description: 'Select test type to run: smoke (critical tests), regression (all tests), or all (smoke + regression)'
        )
        booleanParam(
            name: 'FAIL_ON_SKIP',
            defaultValue: true,
            description: 'Fail the build if tests are skipped'
        )
        booleanParam(
            name: 'VERBOSE_OUTPUT',
            defaultValue: false,
            description: 'Enable verbose pytest output'
        )
    }
    
	tools {
        // 使用在全局工具配置中定义的 Allure Commandline 工具
        allure 'allure2.34.1'
    }
    
    environment {
        // Define workspace paths based on actual Jenkins setup
        CODE_DIR = "${WORKSPACE}"  // Jenkins checks out code directly to workspace
        VENV_DIR = "${WORKSPACE}/venv"  // Virtual environment in workspace (persistent)
        PYTHON_EXE = "${VENV_DIR}/Scripts/python.exe"
        PIP_EXE = "${VENV_DIR}/Scripts/pip.exe"
        // Proxy settings (same as local environment)
        HTTP_PROXY = "http://127.0.0.1:10809"
        HTTPS_PROXY = "http://127.0.0.1:10809"
        http_proxy = "http://127.0.0.1:10809"
        https_proxy = "http://127.0.0.1:10809"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo "Checking out code from GitHub repository..."
                
                // Backup virtual environment if it exists to prevent deletion
                script {
                    if (fileExists("${VENV_DIR}")) {
                        echo "Backing up existing virtual environment..."
                        bat "if exist \"${VENV_DIR}\" move \"${VENV_DIR}\" \"${VENV_DIR}_backup\""
                    }
                }
                
                // Checkout code from GitHub using your SSH credentials
                git branch: 'main', credentialsId: 'my ssh', url: 'git@github.com:nightwish2016/Kevin-BlockChain-Automation.git'
                
                // Restore virtual environment
                script {
                    if (fileExists("${VENV_DIR}_backup")) {
                        echo "Restoring virtual environment..."
                        bat "move \"${VENV_DIR}_backup\" \"${VENV_DIR}\""
                    }
                }
                
                echo "Code checkout completed successfully"
                
                // Verify files are present
                bat "dir"
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo "Setting up Python virtual environment..."
                echo "Workspace: ${WORKSPACE}"
                echo "Code directory: ${CODE_DIR}" 
                echo "Virtual environment: ${VENV_DIR}"
                
                // Create virtual environment if it doesn't exist
                script {
                    if (!fileExists("${VENV_DIR}/Scripts/python.exe")) {
                        echo "Creating new Python virtual environment..."
                        bat "python -m venv \"${VENV_DIR}\""
                        echo "Virtual environment created successfully"
                    } else {
                        echo "Virtual environment already exists"
                    }
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                
                script {
                    // Check if requirements.txt exists
                    if (fileExists('requirements.txt')) {
                        def requirementsChanged = true
                        
                        // Check if requirements have changed
                        if (fileExists("${VENV_DIR}/installed_requirements.txt")) {
                            def currentReq = readFile('requirements.txt').trim()
                            def cachedReq = readFile("${VENV_DIR}/installed_requirements.txt").trim()
                            
                            if (currentReq == cachedReq) {
                                requirementsChanged = false
                                echo "Requirements unchanged, checking package integrity..."
                                
                                // Quick check if packages are working
                                def checkResult = bat(script: "\"${PIP_EXE}\" check", returnStatus: true)
                                if (checkResult != 0) {
                                    echo "Package dependencies broken, need to reinstall"
                                    requirementsChanged = true
                                }
                            } else {
                                echo "Requirements have changed, will reinstall"
                            }
                        } else {
                            echo "First time installation"
                        }
                        
                        if (requirementsChanged) {
                            echo "Installing/updating Python packages..."
                            
                            // Try to upgrade pip using the correct python executable
                            bat "\"${PYTHON_EXE}\" -m pip install --upgrade pip"
                            
                            // Install requirements
                            bat "\"${PIP_EXE}\" install -r requirements.txt"
                            
                            // Cache the current requirements
                            bat "copy requirements.txt \"${VENV_DIR}\\installed_requirements.txt\""
                            echo "Dependencies installed successfully"
                        } else {
                            echo "All requirements already satisfied, skipping installation"
                        }
                    } else {
                        error "requirements.txt not found!"
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    echo "Running pytest tests with type: ${params.TEST_TYPE}"
                    
                    // Build pytest command based on parameters
                    def pytestCmd = "\"${PYTHON_EXE}\" -m pytest"
                    
                    // Add test type marker
                    switch(params.TEST_TYPE) {
                        case 'smoke':
                            pytestCmd += " -m smoke"
                            echo "Running smoke tests (critical happy paths only)"
                            break
                        case 'regression':
                            pytestCmd += " -m regression"
                            echo "Running regression tests (comprehensive test suite)"
                            break
                        case 'all':
                            pytestCmd += " -m \"smoke or regression\""
                            echo "Running all tests (smoke + regression)"
                            break
                        default:
                            pytestCmd += " -m smoke"
                            echo "Default: Running smoke tests"
                    }
                    
                    // Add verbose output if requested
                    if (params.VERBOSE_OUTPUT) {
                        pytestCmd += " -v -s"
                    }
                    
                    // Add Allure reporting
                    pytestCmd += " --alluredir=allure-results --clean-alluredir"
                    
                    // Add traceback format for better error visibility
                    pytestCmd += " --tb=short"
                    
                    echo "Executing command: ${pytestCmd}"
                    
                    // Execute pytest and capture result
                    def testResult = bat(script: pytestCmd, returnStatus: true)
                    
                    // Handle test results
                    if (testResult == 0) {
                        echo "All tests passed successfully"
                    } else if (testResult == 1) {
                        currentBuild.result = 'FAILURE'
                        error("Tests failed. Check console output and Allure report for details.")
                    } else if (testResult == 2) {
                        currentBuild.result = 'FAILURE'
                        error("Test execution was interrupted")
                    } else if (testResult == 5) {
                        if (params.FAIL_ON_SKIP) {
                            currentBuild.result = 'FAILURE'
                            error("No tests were collected/run. This may indicate test discovery issues.")
                        } else {
                            currentBuild.result = 'UNSTABLE'
                            echo "Warning: No tests were collected/run"
                        }
                    } else {
                        currentBuild.result = 'FAILURE'
                        error("Pytest failed with exit code: ${testResult}")
                    }
                    
                    // Additional check for skipped tests if FAIL_ON_SKIP is enabled
                    if (params.FAIL_ON_SKIP && testResult == 0) {
                        try {
                            def skipCheck = bat(script: "\"${PYTHON_EXE}\" -m pytest --collect-only -q ${params.TEST_TYPE == 'smoke' ? '-m smoke' : params.TEST_TYPE == 'regression' ? '-m regression' : '-m \"smoke or regression\"'}", returnStdout: true)
                            def collectOutput = bat(script: pytestCmd.replace('--alluredir=allure-results --clean-alluredir', '--collect-only'), returnStdout: true)
                            if (collectOutput.contains('0 tests ran') || collectOutput.contains('no tests collected')) {
                                currentBuild.result = 'FAILURE'
                                error("No tests collected for the specified test type: ${params.TEST_TYPE}")
                            }
                        } catch (Exception e) {
                            echo "Could not verify test collection: ${e.getMessage()}"
                        }
                    }
                }
            }
            post {
                always {
                    // Archive Allure results
                    archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
                    
                    // Clean up Python cache files
                    bat '''
                        if exist "__pycache__" rmdir /s /q "__pycache__" >nul 2>&1
                        if exist ".pytest_cache" rmdir /s /q ".pytest_cache" >nul 2>&1
                    '''
                }
            }
        }
        
        stage('Generate Allure Report') {
            steps {
                echo "Generating Allure HTML report..."
                
                script {
                    // Check if allure-results directory exists and has files
                    if (fileExists('allure-results')) {
                        def hasFiles = false
                        try {
                            def output = bat(script: 'dir /b allure-results 2>nul | find /c /v ""', returnStdout: true).trim()
                            // Extract just the number from the output (last line should be the count)
                            def lines = output.split('\n')
                            def fileCount = lines[-1].trim()
                            echo "Raw output: ${output}"
                            echo "Extracted count: ${fileCount}"
                            hasFiles = fileCount.toInteger() > 0
                            echo "Found ${fileCount} files in allure-results directory"
                        } catch (Exception e) {
                            echo "Error checking allure-results contents: ${e.getMessage()}"
                            // Fallback: try simple directory listing
                            try {
                                def simpleCheck = bat(script: 'dir allure-results', returnStatus: true)
                                hasFiles = (simpleCheck == 0)
                                echo "Fallback check result: ${hasFiles}"
                            } catch (Exception e2) {
                                hasFiles = false
                                echo "Fallback check also failed: ${e2.getMessage()}"
                            }
                        }
                        
                        if (hasFiles) {
                        echo "Allure results found, generating report..."
                        
                        // Try to generate Allure report, with fallback if allure CLI is not available
                        def allureInstalled = false
                        try {
                            bat 'allure --version'
                            allureInstalled = true
                            echo "Allure CLI found and working"
                        } catch (Exception e) {
                            echo "Allure CLI not accessible: ${e.getMessage()}"
                            echo "Checking if allure is in PATH..."
                            def pathCheck = bat(script: 'where allure', returnStatus: true) == 0
                            if (pathCheck) {
                                echo "Allure found in PATH, but version check failed"
                            } else {
                                echo "Allure not found in PATH"
                            }
                        }
                        if (allureInstalled) {
                            echo "Allure CLI found, generating HTML report..."
                            bat '''
                                if exist "allure-report" rmdir /s /q "allure-report"
                                allure generate allure-results --clean -o allure-report
                            '''
                            echo "Allure HTML report generated successfully"
                        } else {
                            echo "Allure CLI not found, will rely on Jenkins plugin for report generation"
                            echo "To install Allure CLI, run: npm install -g allure-commandline"
                        }
                        } else {
                            echo "Allure-results directory exists but is empty"
                        }
                    } else {
                        echo "Allure-results directory not found, skipping report generation"
                    }
                }
            }
            post {
                always {
                    // Archive the HTML report (if generated)
                    archiveArtifacts artifacts: 'allure-report/**', allowEmptyArchive: true
                    
                    // Publish Allure report using Jenkins plugin
                    script {
                        if (fileExists('allure-results')) {
                            try {
                                // Use publishHTML as primary method for viewing reports
                                publishHTML([
                                    allowMissing: false,
                                    alwaysLinkToLastBuild: true,
                                    keepAll: true,
                                    reportDir: 'allure-report',
                                    reportFiles: 'index.html',
                                    reportName: 'Allure HTML Report',
                                    reportTitles: 'Blockchain QA Test Report'
                                ])
                                echo "HTML report published successfully"
                            } catch (Exception htmlError) {
                                echo "HTML publisher failed: ${htmlError.getMessage()}"
                            }
                            
                            // Also try Allure Jenkins plugin as backup
                            try {
                                allure([
                                    includeProperties: false,
                                    jdk: '',
                                    properties: [],
                                    reportBuildPolicy: 'ALWAYS',
                                    results: [[path: 'allure-results']]
                                ])
                                echo "Allure plugin report published successfully"
                            } catch (Exception allureError) {
                                echo "Allure Jenkins plugin not available: ${allureError.getMessage()}"
                                echo "Install Allure plugin from Jenkins Plugin Manager"
                            }
                        } else {
                            echo "No allure-results directory found for report publishing"
                        }
                    }
                }
            }
        }
		 
    }
    
    post {
        success {
            echo "✅ Tests completed successfully!"
            echo "Test Type: ${params.TEST_TYPE}"
            echo "Check Allure report for detailed test results"
        }
        failure {
            echo "❌ Tests failed. Check the console output and Allure report for details."
            echo "Test Type: ${params.TEST_TYPE}"
            echo "Failed tests require investigation"
        }
        unstable {
            echo "⚠️ Tests completed with warnings or skips"
            echo "Test Type: ${params.TEST_TYPE}"
            echo "Some tests may have been skipped or marked as unstable"
        }
        always {
            echo "=== Test Execution Summary ==="
            echo "Test Type: ${params.TEST_TYPE}"
            echo "Fail on Skip: ${params.FAIL_ON_SKIP}"
            echo "Verbose Output: ${params.VERBOSE_OUTPUT}"
            echo "Build Result: ${currentBuild.result ?: 'SUCCESS'}"
            
            // Clean up any remaining cache files
            script {
                try {
                    bat '''
                        if exist "__pycache__" rmdir /s /q "__pycache__" >nul 2>&1
                        if exist ".pytest_cache" rmdir /s /q ".pytest_cache" >nul 2>&1
                        if exist "*.pyc" del "*.pyc" >nul 2>&1
                    '''
                } catch (Exception e) {
                    echo "Cache cleanup completed with warnings: ${e.getMessage()}"
                }
            }
        }
    }
}