from flask import Flask, request
import datetime
import socket
import platform
import os
import netifaces as ni
import psutil

app = Flask(__name__)

def get_mac_address():
    # Function to get the MAC address of the host
    for iface in ni.interfaces():
        try:
            mac = ni.ifaddresses(iface)[ni.AF_LINK][0]['addr']
            if mac:
                return mac
        except KeyError:
            continue
    return "N/A"

def get_uptime():
    # Function to get system uptime
    uptime_seconds = int((datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())).total_seconds())
    uptime_str = str(datetime.timedelta(seconds=uptime_seconds))
    return uptime_str

@app.route('/')
def user_info():
    # Get user IP
    user_ip = request.remote_addr
    
    # Get system username (from environment)
    username = request.headers.get('Username', 'Guest')
    
    # Get MAC address
    mac_address = get_mac_address()
    
    # Get hostname
    hostname = socket.gethostname()
    
    # Get operating system information
    os_info = f"{platform.system()} {platform.release()}"
    
    # Get browser and operating system from User-Agent
    user_agent = request.headers.get('User-Agent', 'N/A')
    
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get system uptime
    uptime = get_uptime()
    
    # Display all details
    return f"""
    <html>
    <body>
        <p><b>IP Address:</b> {user_ip}</p>
        <p><b>MAC Address:</b> {mac_address}</p>
        <p><b>Username:</b> {username}</p>
        <p><b>Hostname:</b> {hostname}</p>
        <p><b>Operating System:</b> {os_info}</p>
        <p><b>User Agent (Browser & OS):</b> {user_agent}</p>
        <p><b>Timestamp:</b> {timestamp}</p>
        <p><b>System Uptime:</b> {uptime}</p>
        <br>
        <h3>Assignment completed successfully!</h3>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
