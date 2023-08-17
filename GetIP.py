import socket


def get_ip_address():
    try:
        # Get the hostname
        host_name = socket.gethostname()
        # Get the IP address corresponding to the hostname
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except socket.error as e:
        print("Error:", e)
        return None

'''def sendServerIP():
    try:
        host


if __name__ == "__main__":
    ip_address = get_ip_address()
    if ip_address:
        print("IP Address:", ip_address)
    else:
        print("Failed to retrieve IP address.")
'''