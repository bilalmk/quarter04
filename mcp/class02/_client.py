import requests

URL = "http://localhost:8000/mcp"
PAYLOAD = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
HEADERS = {"Accept": "application/json, text/event-stream"}


response = requests.post(URL, headers=HEADERS, json=PAYLOAD)
print(response.text)

print("=" * 100)

URL = "http://localhost:8000/mcp"
PAYLOAD = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {"name": "get_weather", "arguments": {"city": "Karachi"}},
}
HEADERS = {"Accept": "application/json, text/event-stream"}


response = requests.post(URL, headers=HEADERS, json=PAYLOAD)
print(response.text)
