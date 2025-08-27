# PowerShell script for running smoke tests
# Activate virtual environment
& ".myenv\Scripts\Activate.ps1"

pip install -r requirements.txt
# Remove existing allure results
if (Test-Path "allure-results") { Remove-Item "allure-results" -Recurse -Force }

# Run smoke tests with allure reporting
pytest -m regression -sv --alluredir=allure-results

# Serve allure report (requires allure CLI to be installed)
allure serve allure-results

# Alternative: Generate static HTML report
# allure generate allure-results -o allure-report --clean