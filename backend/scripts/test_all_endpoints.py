import requests
import io

def test_endpoint(url, method="GET", data=None, files=None):
    if method == "GET":
        response = requests.get(url)
    elif method == "POST":
        if files:
            response = requests.post(url, data=data, files=files)
        else:
            response = requests.post(url, data=data)
    elif method == "PUT":
        response = requests.put(url, data=data)
    elif method == "DELETE":
        response = requests.delete(url)
    else:
        print(f"Unsupported method: {method}")
        return

    print(f"Testing {method} {url}:")
    try:
        print("Response:", response.json())
    except Exception:
        print(f"Error: {response.status_code}")
        print(response.text)

def test_all_endpoints():
    base_url = "http://localhost:8000"
    # Mock file for video upload
    mock_video = io.BytesIO(b"mock video content")
    # Mock file for image detection
    mock_image = io.BytesIO(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")  # PNG header
    endpoints = [
        {"url": f"{base_url}/", "method": "GET"},
        {"url": f"{base_url}/api/status", "method": "GET"},
        {"url": f"{base_url}/api/system/info", "method": "GET"},
        {"url": f"{base_url}/api/register", "method": "POST", "data": {"username": "testuser", "password": "testpass"}},
        {"url": f"{base_url}/api/login", "method": "POST", "data": {"username": "testuser", "password": "testpass"}},
        {"url": f"{base_url}/api/users/1", "method": "GET"},
        {"url": f"{base_url}/api/users/1", "method": "PUT", "data": {"username": "updateduser"}},
        {"url": f"{base_url}/api/users/1", "method": "DELETE"},
        {"url": f"{base_url}/api/videos/upload", "method": "POST", "data": {"user_id": 1}, "files": {"file": ("mock.mp4", mock_video, "video/mp4")}},
        {"url": f"{base_url}/api/videos/1", "method": "GET"},
        {"url": f"{base_url}/api/videos/user/1", "method": "GET"},
        {"url": f"{base_url}/api/videos/1", "method": "DELETE"},
        {"url": f"{base_url}/api/detect/image", "method": "POST", "files": {"file": ("mock.png", mock_image, "image/png")}},
        {"url": f"{base_url}/api/detect/video", "method": "POST", "data": {"video_id": 1}},
        {"url": f"{base_url}/api/detection_results/1", "method": "GET"},
        {"url": f"{base_url}/api/detection_results/video/1", "method": "GET"},
        {"url": f"{base_url}/api/logs/user/1", "method": "GET"},
        {"url": f"{base_url}/api/logs", "method": "POST", "data": {"user_id": 1, "action": "test_action"}}
    ]

    for endpoint in endpoints:
        test_endpoint(endpoint["url"], endpoint["method"], endpoint.get("data"), endpoint.get("files"))

if __name__ == "__main__":
    test_all_endpoints() 