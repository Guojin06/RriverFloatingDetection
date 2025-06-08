import requests

def test_system_info():
    url = "http://localhost:8000/api/system/info"
    response = requests.get(url)
    if response.status_code == 200:
        print("System Info Response:")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    test_system_info() 