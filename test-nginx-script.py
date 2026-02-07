import requests
import sys
import urllib3


def test_servers():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # since the name in the docker compose is nginx-server we can use that as the hostname
    base_url = "https://nginx-server" 
    
    tests = [
        {"port": 8080, "expected_status": 200, "expected_content": "Hello from Port 8080!"},
        {"port": 9090, "expected_status": 403, "expected_content": "Access Denied"}
    ]

    for test in tests:
        url = f"{base_url}:{test['port']}"
        print(f"Testing {url}...")
        try:
            # verify=False is used to ignore SSL certificate warnings since we are using self-signed certs
            response = requests.get(url, timeout=5, verify=False)
            
            # Check Status Code
            if response.status_code != test['expected_status']:
                print("FAILED: Expected {test['expected_status']}, got {response.status_code}")
                sys.exit(1)
            
            # Check Content
            if test['expected_content'] not in response.text:
                print("FAILED: Expected content not found in response")
                sys.exit(1)
                
            print(f"SUCCESS: {url} passed.")
            
        except requests.exceptions.RequestException as e:
            print(f"CONNECTION ERROR: {e}")
            sys.exit(1)

    print("All tests passed successfully!")


if __name__ == "__main__":
    test_servers()
    sys.exit(0)