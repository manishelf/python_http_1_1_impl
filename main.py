# goal - implement http v1.1 

#import asyncio
import socket



#async def handle(sock: socket):
def handle(sock: socket):
    # Wait for an incoming connection.

    #loop = asyncio.get_running_loop()
    #conn, addr = await loop.sock_accept(sock)

    conn, addr = sock.accept() 
    file = conn.makefile("w") # SocketIO

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages
    file.write("HTTP/1.1 200")
    file.write("\n")
    file.write("OK")
    file.write("\n")
    file.write("Content-Type: text/html; charset=UTF-8")
    file.write("\n")
    file.write("Content-Length: 2000") # temp
    file.write("\n")
    file.write("\n") # marks the end of headers
    file.write("<HTML>xxxxxxxxxxxxxxxxxxxxxxxx</HTML>")
    

def main():
    address = ('', 8000)
    """
     https://github.com/python/cpython/blob/3.14/Lib/socket.py
     the socket implementation comes from Modules/socketmodule.c
     which creates os dependent TCP sockets from c
     eg fd = WSASocketW(family, type, proto,
                        NULL, 0,
                        WSA_FLAG_OVERLAPPED | WSA_FLAG_NO_HANDLE_INHERIT);
     on Windows
     or on UNIX as fd = socket(family, type, proto);

     init - sock_initobj_impl(...)
     bind - sock_bind(...) -> <sys/socket.h> bind
     listen - sock_listen(...) -> <sys/socket.h> listen
     accept - _accept -> sock_accept_imp(....) -> <sys/socket.h> accpet
     makefile - 
        raw = SocketIO(self, rawmode)
        buffer = io.BufferedWriter(raw, buffering)
        encoding = io.text_encoding(encoding)
        file = io.TextIOWrapper(buffer, encoding, errors, newline)
        file.mode = mode
     close - _socket_socket_close_impl -> SOCKETCLOSE(fd) -> closesocket(..) windows or close(..) for unix

    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.setblocking(False)
    sock.setblocking(True)

    try:
        try:
            sock.bind(address)
        except error as err:
            msg = '%s (while attempting to bind on address %r)' % \
                    (err.strerror, address)
            raise error(err.errno, msg) from None
        sock.listen()
    except error:
        sock.close()
        raise

    #asyncio.run(handle(sock))
    while True:
        handle(sock)

    sock.close()

if __name__ == '__main__':
    main()
