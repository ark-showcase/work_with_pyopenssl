from OpenSSL import SSL
import socket

def get_response(host, path):
    context = SSL.Context(SSL.TLSv1_2_METHOD)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = SSL.Connection(context, sock)
    connection.connect((host, 443))

    html_response = ''
    try:
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        connection.sendall(request.encode())

        while True:
            response = connection.recv(4096)
            if not response:
                break
            html_response_in_line = response.decode()
            html_response = html_response + html_response_in_line

    except SSL.ZeroReturnError:
        pass
    finally:
        connection.close()

        return html_response

    return None