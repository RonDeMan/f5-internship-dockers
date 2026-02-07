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

    # Rate Limiting Test
    print("\nTesting Rate Limiting (5r/s)...")
    url_8080 = f"{base_url}:8080"
    rate_limit_triggered = False
    
    # Fire 20 requests quickly to exhaust the burst of 5 and the rate of 5r/s
    for i in range(20):
        try:
            response = requests.get(url_8080, verify=False)
            if response.status_code == 429:
                print(f"Request {i+1}: Rate limit hit (429) as expected.")
                rate_limit_triggered = True
                break
        except requests.exceptions.RequestException:
            continue

    if rate_limit_triggered:
        print("SUCCESS: Rate limiting is active.")
    else:
        print("FAILED: Did not hit rate limit (429).")
        sys.exit(1)

    print("All tests passed successfully!")


if __name__ == "__main__":
    test_servers()
    sys.exit(0)