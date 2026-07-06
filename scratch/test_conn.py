import socket
import urllib.request

try:
    print("Testing socket resolution...")
    ip = socket.gethostbyname("generativelanguage.googleapis.com")
    print(f"Resolved to: {ip}")
    
    print("Testing HTTP request...")
    response = urllib.request.urlopen("https://generativelanguage.googleapis.com", timeout=5)
    print(f"Status code: {response.status}")
except Exception as e:
    print(f"FAILED: {e}")
