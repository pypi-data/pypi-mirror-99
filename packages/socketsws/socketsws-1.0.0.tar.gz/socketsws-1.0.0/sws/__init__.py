import socket

s = socket.socket()

def start_server(port, maxusers):
    s.bind(('localhost', port))
    s.listen(maxusers)

def stream_html(html):
    while 1:
        conn, addr = s.accept()
        conn.sendall(f'HTTP/1.1 200 OK\nContent-Type: text/html\n\n{html}'.encode())
        
def load_file(file):
    return open(file).read()

    
