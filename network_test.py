#!/usr/bin/env python3
"""
Network connectivity test script for Jenkins environment
"""
import requests
import socket
import sys
import time
from urllib.parse import urlparse


def test_internet_connectivity():
    """Test basic internet connectivity"""
    print("Testing internet connectivity...")
    try:
        # Test DNS resolution
        socket.gethostbyname('google.com')
        print("✓ DNS resolution works")
        
        # Test HTTP connectivity
        response = requests.get('http://httpbin.org/status/200', timeout=10)
        if response.status_code == 200:
            print("✓ HTTP connectivity works")
            return True
    except Exception as e:
        print(f"✗ Internet connectivity failed: {e}")
        return False


def test_cronos_connectivity():
    """Test Cronos testnet connectivity"""
    print("\nTesting Cronos testnet connectivity...")
    cronos_url = "https://evm-t3.cronos.org"
    
    try:
        # Parse URL
        parsed = urlparse(cronos_url)
        host = parsed.hostname
        port = parsed.port or 443
        
        # Test DNS resolution for Cronos
        ip = socket.gethostbyname(host)
        print(f"✓ DNS resolution for {host}: {ip}")
        
        # Test TCP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            print(f"✓ TCP connection to {host}:{port} successful")
        else:
            print(f"✗ TCP connection to {host}:{port} failed")
            return False
            
        # Test HTTP/HTTPS request
        response = requests.get(cronos_url, timeout=30)
        print(f"✓ HTTP request successful: {response.status_code}")
        
        # Test JSON-RPC endpoint
        rpc_data = {
            "jsonrpc": "2.0",
            "method": "eth_blockNumber", 
            "params": [],
            "id": 1
        }
        
        rpc_response = requests.post(
            cronos_url,
            json=rpc_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if rpc_response.status_code == 200:
            result = rpc_response.json()
            if 'result' in result:
                print(f"✓ JSON-RPC call successful: block number {result['result']}")
                return True
            else:
                print(f"✗ JSON-RPC call failed: {result}")
                return False
        else:
            print(f"✗ JSON-RPC request failed: {rpc_response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Cronos connectivity failed: {e}")
        return False


def test_proxy_settings():
    """Check for proxy settings that might affect connectivity"""
    print("\nChecking proxy settings...")
    import os
    
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']
    proxy_found = False
    
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            print(f"Proxy setting found: {var}={value}")
            proxy_found = True
    
    if not proxy_found:
        print("No proxy settings detected")


def main():
    """Main test function"""
    print("=== Network Connectivity Diagnostic Tool ===")
    print(f"Running tests at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run tests
    internet_ok = test_internet_connectivity()
    cronos_ok = test_cronos_connectivity() 
    test_proxy_settings()
    
    print("\n=== Summary ===")
    if internet_ok and cronos_ok:
        print("✓ All network tests passed")
        sys.exit(0)
    elif internet_ok:
        print("⚠ Internet works but Cronos testnet is unreachable")
        print("This may be due to firewall rules or proxy settings")
        sys.exit(1)
    else:
        print("✗ No internet connectivity detected")
        print("Check network settings, firewall, and proxy configuration")
        sys.exit(2)


if __name__ == "__main__":
    main()