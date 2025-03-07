# SHULK

# Overview
This project is an enhanced version of the HULK (HTTP Unbearable Load King) tool, which performs high-intensity, automated flooding attacks on web servers. This version integrates Proxy Rotation and CAPTCHA Bypass, making the tool more efficient in bypassing anti-bot mechanisms, and preventing IP bans through the use of different proxy servers for each request.

# Key Features:
* HTTP Flooding: Overwhelm the target web server with HTTP requests.
* WebSocket Flooding: Attack WebSocket servers with high traffic.
* Proxy Rotation: Rotate between a list of proxies for each request to avoid detection and IP bans.
* CAPTCHA Bypass: Use headless browsers (via Selenium) to solve CAPTCHA challenges and extract session cookies.
